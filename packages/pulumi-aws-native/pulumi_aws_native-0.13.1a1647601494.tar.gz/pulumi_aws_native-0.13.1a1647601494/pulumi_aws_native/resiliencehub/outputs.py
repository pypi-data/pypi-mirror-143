# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs
from ._enums import *

__all__ = [
    'AppPhysicalResourceId',
    'AppResourceMapping',
    'AppTagMap',
    'ResiliencyPolicyPolicyMap',
    'ResiliencyPolicyTagMap',
]

@pulumi.output_type
class AppPhysicalResourceId(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "awsAccountId":
            suggest = "aws_account_id"
        elif key == "awsRegion":
            suggest = "aws_region"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in AppPhysicalResourceId. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        AppPhysicalResourceId.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        AppPhysicalResourceId.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 identifier: str,
                 type: str,
                 aws_account_id: Optional[str] = None,
                 aws_region: Optional[str] = None):
        pulumi.set(__self__, "identifier", identifier)
        pulumi.set(__self__, "type", type)
        if aws_account_id is not None:
            pulumi.set(__self__, "aws_account_id", aws_account_id)
        if aws_region is not None:
            pulumi.set(__self__, "aws_region", aws_region)

    @property
    @pulumi.getter
    def identifier(self) -> str:
        return pulumi.get(self, "identifier")

    @property
    @pulumi.getter
    def type(self) -> str:
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="awsAccountId")
    def aws_account_id(self) -> Optional[str]:
        return pulumi.get(self, "aws_account_id")

    @property
    @pulumi.getter(name="awsRegion")
    def aws_region(self) -> Optional[str]:
        return pulumi.get(self, "aws_region")


@pulumi.output_type
class AppResourceMapping(dict):
    """
    Resource mapping is used to map logical resources from template to physical resource
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "mappingType":
            suggest = "mapping_type"
        elif key == "physicalResourceId":
            suggest = "physical_resource_id"
        elif key == "logicalStackName":
            suggest = "logical_stack_name"
        elif key == "resourceName":
            suggest = "resource_name"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in AppResourceMapping. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        AppResourceMapping.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        AppResourceMapping.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 mapping_type: str,
                 physical_resource_id: 'outputs.AppPhysicalResourceId',
                 logical_stack_name: Optional[str] = None,
                 resource_name: Optional[str] = None):
        """
        Resource mapping is used to map logical resources from template to physical resource
        """
        pulumi.set(__self__, "mapping_type", mapping_type)
        pulumi.set(__self__, "physical_resource_id", physical_resource_id)
        if logical_stack_name is not None:
            pulumi.set(__self__, "logical_stack_name", logical_stack_name)
        if resource_name is not None:
            pulumi.set(__self__, "resource_name", resource_name)

    @property
    @pulumi.getter(name="mappingType")
    def mapping_type(self) -> str:
        return pulumi.get(self, "mapping_type")

    @property
    @pulumi.getter(name="physicalResourceId")
    def physical_resource_id(self) -> 'outputs.AppPhysicalResourceId':
        return pulumi.get(self, "physical_resource_id")

    @property
    @pulumi.getter(name="logicalStackName")
    def logical_stack_name(self) -> Optional[str]:
        return pulumi.get(self, "logical_stack_name")

    @property
    @pulumi.getter(name="resourceName")
    def resource_name(self) -> Optional[str]:
        return pulumi.get(self, "resource_name")


@pulumi.output_type
class AppTagMap(dict):
    def __init__(__self__):
        pass


@pulumi.output_type
class ResiliencyPolicyPolicyMap(dict):
    def __init__(__self__):
        pass


@pulumi.output_type
class ResiliencyPolicyTagMap(dict):
    def __init__(__self__):
        pass


