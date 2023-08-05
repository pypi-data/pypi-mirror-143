# coding: utf-8

"""
    external/v1/external_session_service.proto

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: version not set
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git

    NOTE
    ----
    standard swagger-codegen-cli for this python client has been modified
    by custom templates. The purpose of these templates is to include
    typing information in the API and Model code. Please refer to the
    main grid repository for more info
"""


import pprint
import re  # noqa: F401
from typing import TYPE_CHECKING

import six

from grid.openapi.configuration import Configuration

if TYPE_CHECKING:
    from datetime import datetime
    from grid.openapi.models import *

class V1TensorboardSpec(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'cluster_id': 'str',
        'desired_state': 'V1TensorboardState',
        'experiments': 'list[V1TensorboardExperimentConfig]',
        'user_id': 'str'
    }

    attribute_map = {
        'cluster_id': 'clusterId',
        'desired_state': 'desiredState',
        'experiments': 'experiments',
        'user_id': 'userId'
    }

    def __init__(self, cluster_id: 'str' = None, desired_state: 'V1TensorboardState' = None, experiments: 'list[V1TensorboardExperimentConfig]' = None, user_id: 'str' = None, _configuration=None):  # noqa: E501
        """V1TensorboardSpec - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._cluster_id = None
        self._desired_state = None
        self._experiments = None
        self._user_id = None
        self.discriminator = None

        if cluster_id is not None:
            self.cluster_id = cluster_id
        if desired_state is not None:
            self.desired_state = desired_state
        if experiments is not None:
            self.experiments = experiments
        if user_id is not None:
            self.user_id = user_id

    @property
    def cluster_id(self) -> 'str':
        """Gets the cluster_id of this V1TensorboardSpec.  # noqa: E501


        :return: The cluster_id of this V1TensorboardSpec.  # noqa: E501
        :rtype: str
        """
        return self._cluster_id

    @cluster_id.setter
    def cluster_id(self, cluster_id: 'str'):
        """Sets the cluster_id of this V1TensorboardSpec.


        :param cluster_id: The cluster_id of this V1TensorboardSpec.  # noqa: E501
        :type: str
        """

        self._cluster_id = cluster_id

    @property
    def desired_state(self) -> 'V1TensorboardState':
        """Gets the desired_state of this V1TensorboardSpec.  # noqa: E501


        :return: The desired_state of this V1TensorboardSpec.  # noqa: E501
        :rtype: V1TensorboardState
        """
        return self._desired_state

    @desired_state.setter
    def desired_state(self, desired_state: 'V1TensorboardState'):
        """Sets the desired_state of this V1TensorboardSpec.


        :param desired_state: The desired_state of this V1TensorboardSpec.  # noqa: E501
        :type: V1TensorboardState
        """

        self._desired_state = desired_state

    @property
    def experiments(self) -> 'list[V1TensorboardExperimentConfig]':
        """Gets the experiments of this V1TensorboardSpec.  # noqa: E501


        :return: The experiments of this V1TensorboardSpec.  # noqa: E501
        :rtype: list[V1TensorboardExperimentConfig]
        """
        return self._experiments

    @experiments.setter
    def experiments(self, experiments: 'list[V1TensorboardExperimentConfig]'):
        """Sets the experiments of this V1TensorboardSpec.


        :param experiments: The experiments of this V1TensorboardSpec.  # noqa: E501
        :type: list[V1TensorboardExperimentConfig]
        """

        self._experiments = experiments

    @property
    def user_id(self) -> 'str':
        """Gets the user_id of this V1TensorboardSpec.  # noqa: E501


        :return: The user_id of this V1TensorboardSpec.  # noqa: E501
        :rtype: str
        """
        return self._user_id

    @user_id.setter
    def user_id(self, user_id: 'str'):
        """Sets the user_id of this V1TensorboardSpec.


        :param user_id: The user_id of this V1TensorboardSpec.  # noqa: E501
        :type: str
        """

        self._user_id = user_id

    def to_dict(self) -> dict:
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value
        if issubclass(V1TensorboardSpec, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self) -> str:
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self) -> str:
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other: 'V1TensorboardSpec') -> bool:
        """Returns true if both objects are equal"""
        if not isinstance(other, V1TensorboardSpec):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other: 'V1TensorboardSpec') -> bool:
        """Returns true if both objects are not equal"""
        if not isinstance(other, V1TensorboardSpec):
            return True

        return self.to_dict() != other.to_dict()
