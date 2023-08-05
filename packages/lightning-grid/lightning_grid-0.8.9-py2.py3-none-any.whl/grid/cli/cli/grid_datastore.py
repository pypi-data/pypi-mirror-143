import os
import shutil
from datetime import datetime
from pathlib import Path
from functools import partial
from typing import Optional, List

import click
from rich.console import Console
from rich.prompt import Confirm
from yaspin import yaspin

from grid.cli import rich_click
from grid.cli.observables import BaseObservable
from grid.cli.rich_click import deprecate_option
from grid.sdk import env
from grid.sdk.client import create_swagger_client
from grid.sdk.datastores import Datastore, list_datastores
from grid.sdk.rest import GridRestClient
from grid.sdk.utils.datastore_uploads import (
    resume_datastore_upload,
    find_incomplete_datastore_upload,
    load_datastore_work_state,
    remove_datastore_work_state,
)

WARNING_STR = click.style('WARNING', fg='yellow')


@click.group(invoke_without_command=True)
@click.pass_context
@click.option(
    '--global',
    'is_global',
    type=bool,
    is_flag=True,
    default=False,
    show_default=True,
    help='Fetch sessions from everyone in the team when flag is passed'
)
@click.option(
    '--cluster',
    'cluster_id',
    type=str,
    required=False,
    default=env.CONTEXT,
    show_default=True,
    help='The cluster id to list datastores for.',
)
@click.option(
    '--show-incomplete',
    'show_incomplete',
    type=bool,
    is_flag=True,
    default=False,
    show_default=True,
    help=(
        'Show any datastore uploads which were started, but killed or errored before '
        'they finished uploading all data and became "viewable" on the grid datastore '
        'user interface.'
    )
)
def datastore(ctx, cluster_id: str, is_global: bool, show_incomplete: bool) -> None:
    """Manages Datastore workflows."""
    if ctx.invoked_subcommand is None:

        table_rows, table_cols = [], []
        if show_incomplete is True:
            # TODO: Why are we using yaspin when Rich already contains a spinner console instance?
            #       This is literally an additional dependency for no reason...
            spinner = yaspin(text=f"Loading Incomplete Datastores on Local Machine...", color="yellow")
            spinner.start()

            table_cols = ["Name", "Cluster ID", "Started At", "Source Path"]
            try:
                incomplete_id = find_incomplete_datastore_upload(grid_dir=Path(env.GRID_DIR))
                if incomplete_id is not None:
                    ds = load_datastore_work_state(grid_dir=Path(env.GRID_DIR), datastore_id=incomplete_id)
                    created_at = f"{datetime.fromtimestamp(ds.creation_timestamp):%Y-%m-%d %H:%M}"
                    table_rows.append([ds.datastore_name, ds.cluster_id, created_at, ds.source])
            except Exception as e:
                spinner.fail("✘")
                raise click.ClickException(e)
        else:
            spinner = yaspin(text=f"Loading Datastores in {env.CONTEXT}...", color="yellow")
            spinner.start()

            table_cols = ["Name", "Cluster ID", "Version", "Size", "Created At", "Status"]
            try:
                datastores: List[Datastore] = list_datastores(cluster_id=cluster_id, is_global=is_global)
            except Exception as e:
                spinner.fail("✘")
                raise click.ClickException(e)

            for ds in sorted(datastores, key=lambda k: (k.name, k.version)):
                created_at = f'{ds.created_at:%Y-%m-%d %H:%M}'
                size = ds.size
                status = ds.snapshot_status
                table_rows.append([ds.name, ds.cluster_id, str(ds.version), size, created_at, status])

        table = BaseObservable.create_table(columns=table_cols)
        for row in table_rows:
            table.add_row(*row)

        spinner.ok("✔")
        console = Console()
        console.print(table)

    elif is_global:
        click.echo(f"{WARNING_STR}: --global flag doesn't have any effect when invoked with a subcommand")


@datastore.command()
@click.pass_context
def resume(ctx):
    """Resume uploading an incomplete datastore upload session."""
    _resume()


def _resume():
    """Implementation of the resume_command function not requiring the context to be passed.
    """
    Console()  # THIS IS IMPORTANT! (otherwise console text overwrites eachother)
    with Console().status("[bold yellow]Indexing incomplete datastore uploads....", spinner_style="yellow") as status:
        incomplete_id = find_incomplete_datastore_upload(grid_dir=Path(env.GRID_DIR))
        if incomplete_id is not None:
            try:
                ds_work = load_datastore_work_state(grid_dir=Path(env.GRID_DIR), datastore_id=incomplete_id)
                status.update("[bold yellow]Checking for modified files on disk...")
                modified_files = ds_work.check_for_modified_files()
                status.stop()
                if len(modified_files) > 0:
                    files_changed_dialogue = '\n'.join([f"- {f.absolute_path}" for f in modified_files])
                    should_resume = Confirm.ask(
                        "Files have been modified on disk since the last datastore upload began:\n\n"
                        f"{files_changed_dialogue} \n\n"
                        "[b]Are you sure that you would like to continue uploading the original files which remain?[/b] \n"
                        "[i]NOTE: Any files which have already been uploaded will not be updated with new content[/i]",
                        default=False,
                    )
                    if not should_resume:
                        click.echo("Exiting!")
                        return
                c = GridRestClient(create_swagger_client())
                click.echo(f"creating datastore from {ds_work.source}")
                resume_datastore_upload(client=c, grid_dir=Path(env.GRID_DIR), work=ds_work)
            except Exception as e:
                raise click.ClickException(e)
        else:
            raise click.ClickException(f"no incomplete datastore upload sessions exist")


@datastore.command()
@rich_click.argument(
    'source',
    type=str,
    default=None,
    required=False,
    help=(
        "Source to create datastore from. This could either be a local "
        "directory (e.g: /opt/local_folder) a remote http URL pointing "
        "to a TAR or ZIP file (e.g. http://some_domain/data.tar.gz), or "
        "an s3 bucket to copy data from (e.g. s3://ryft-public-sample-data/esRedditJson/)"
    )
)
@click.option(
    '--source',
    'source_',
    type=str,
    show_default=False,
    default=None,
    required=False,
    hidden=True,
    callback=partial(deprecate_option, "the argument form (grid datastore create SOURCE) of this command"),
)
@click.option('--name', type=str, required=False, help='Name of the datastore')
@click.option(
    '--cluster',
    type=str,
    default=env.CONTEXT,
    show_default=True,
    required=False,
    help='cluster id to create the datastore on. (Bring Your Own Cloud Customers Only).'
)
@click.pass_context
def create(ctx, source: str, source_: str, cluster: str, name: Optional[str] = None) -> None:
    """Creates a datastore from SOURCE.

    The upload session is referenced by the name. this name
    must be used to resume the upload if it is interupted.
    """
    if source_ is not None:
        source = source_
    try:
        Console()  # THIS IS IMPORTANT! (otherwise console text overwrites eachother)
        incomplete_id = find_incomplete_datastore_upload(Path(env.GRID_DIR))
        if incomplete_id is not None:
            should_resume = Confirm.ask(
                "[b]A previous datastore upload was interrupted before it was able to complete.[/b]\n\n"
                "Do you wish to resume this upload [bold green](yes/y)[reset]? If not [bold red](no/n)[reset], \n"
                "then the [i]progress on the interrupted upload will be deleted[/i], \n"
                "and you will have to upload the dataset in full.\n",
                default=True,
            )
            if should_resume is True:
                _resume()
            else:
                remove_datastore_work_state(grid_dir=Path(env.GRID_DIR), datastore_id=incomplete_id)
                dstore = Datastore(name=name, source=source, cluster_id=cluster)
                click.echo(f"creating datastore from {source}")
                dstore.upload()
        else:
            with Console().status("[bold yellow]Indexing datastore uploads....", spinner_style="yellow") as status:
                dstore = Datastore(name=name, source=source, cluster_id=cluster)
                click.echo(f"creating datastoree from {source}")
                status.stop()
                dstore.upload()
    except Exception as e:
        raise click.ClickException(e)


@datastore.command()
@click.pass_context
def clearcache(ctx) -> None:
    """Clears datastore cache which is saved on the local machine when uploading a datastore to grid.

    This removes all the cached files from the local machine, meaning that resuming an incomplete
    upload is not possible after running this command.
    """
    for f in Path(env.GRID_DIR).joinpath("datastores").iterdir():
        if f.is_file():
            os.remove(str(f.absolute()))
        if f.is_dir():
            shutil.rmtree(str(f.absolute()))
    click.echo("Datastore cache cleared")


@datastore.command(cls=rich_click.deprecate_grid_options())
@click.option('--name', type=str, required=True, help='Name of the datastore')
@click.option('--version', type=int, required=True, help='Version of the datastore')
@click.option(
    '--cluster',
    type=str,
    required=False,
    default=env.CONTEXT,
    show_default=True,
    help='cluster id to delete the datastore from. (Bring Your Own Cloud Customers Only).'
)
@click.pass_context
def delete(ctx, name: str, version: int, cluster: str) -> None:
    """Deletes a datastore with the given name and version tag.

    For bring-your-own-cloud customers, the cluster id of the associated
    resource is required as well.
    """
    try:
        dstore = Datastore(name=name, version=version, cluster_id=cluster)
        dstore.delete()
    except Exception as e:
        raise click.ClickException(str(e))
    click.echo("Done!")
