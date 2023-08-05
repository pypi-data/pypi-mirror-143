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
    'GetBillingGroupResult',
    'AwaitableGetBillingGroupResult',
    'get_billing_group',
    'get_billing_group_output',
]

@pulumi.output_type
class GetBillingGroupResult:
    def __init__(__self__, account_grouping=None, arn=None, computation_preference=None, creation_time=None, description=None, last_modified_time=None, name=None, size=None, status=None, status_reason=None):
        if account_grouping and not isinstance(account_grouping, dict):
            raise TypeError("Expected argument 'account_grouping' to be a dict")
        pulumi.set(__self__, "account_grouping", account_grouping)
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if computation_preference and not isinstance(computation_preference, dict):
            raise TypeError("Expected argument 'computation_preference' to be a dict")
        pulumi.set(__self__, "computation_preference", computation_preference)
        if creation_time and not isinstance(creation_time, int):
            raise TypeError("Expected argument 'creation_time' to be a int")
        pulumi.set(__self__, "creation_time", creation_time)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if last_modified_time and not isinstance(last_modified_time, int):
            raise TypeError("Expected argument 'last_modified_time' to be a int")
        pulumi.set(__self__, "last_modified_time", last_modified_time)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if size and not isinstance(size, int):
            raise TypeError("Expected argument 'size' to be a int")
        pulumi.set(__self__, "size", size)
        if status and not isinstance(status, str):
            raise TypeError("Expected argument 'status' to be a str")
        pulumi.set(__self__, "status", status)
        if status_reason and not isinstance(status_reason, str):
            raise TypeError("Expected argument 'status_reason' to be a str")
        pulumi.set(__self__, "status_reason", status_reason)

    @property
    @pulumi.getter(name="accountGrouping")
    def account_grouping(self) -> Optional['outputs.BillingGroupAccountGrouping']:
        return pulumi.get(self, "account_grouping")

    @property
    @pulumi.getter
    def arn(self) -> Optional[str]:
        """
        Billing Group ARN
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="computationPreference")
    def computation_preference(self) -> Optional['outputs.BillingGroupComputationPreference']:
        return pulumi.get(self, "computation_preference")

    @property
    @pulumi.getter(name="creationTime")
    def creation_time(self) -> Optional[int]:
        """
        Creation timestamp in UNIX epoch time format
        """
        return pulumi.get(self, "creation_time")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="lastModifiedTime")
    def last_modified_time(self) -> Optional[int]:
        """
        Latest modified timestamp in UNIX epoch time format
        """
        return pulumi.get(self, "last_modified_time")

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def size(self) -> Optional[int]:
        """
        Number of accounts in the billing group
        """
        return pulumi.get(self, "size")

    @property
    @pulumi.getter
    def status(self) -> Optional['BillingGroupStatus']:
        return pulumi.get(self, "status")

    @property
    @pulumi.getter(name="statusReason")
    def status_reason(self) -> Optional[str]:
        return pulumi.get(self, "status_reason")


class AwaitableGetBillingGroupResult(GetBillingGroupResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetBillingGroupResult(
            account_grouping=self.account_grouping,
            arn=self.arn,
            computation_preference=self.computation_preference,
            creation_time=self.creation_time,
            description=self.description,
            last_modified_time=self.last_modified_time,
            name=self.name,
            size=self.size,
            status=self.status,
            status_reason=self.status_reason)


def get_billing_group(arn: Optional[str] = None,
                      opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetBillingGroupResult:
    """
    A billing group is a set of linked account which belong to the same end customer. It can be seen as a virtual consolidated billing family.


    :param str arn: Billing Group ARN
    """
    __args__ = dict()
    __args__['arn'] = arn
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('aws-native:billingconductor:getBillingGroup', __args__, opts=opts, typ=GetBillingGroupResult).value

    return AwaitableGetBillingGroupResult(
        account_grouping=__ret__.account_grouping,
        arn=__ret__.arn,
        computation_preference=__ret__.computation_preference,
        creation_time=__ret__.creation_time,
        description=__ret__.description,
        last_modified_time=__ret__.last_modified_time,
        name=__ret__.name,
        size=__ret__.size,
        status=__ret__.status,
        status_reason=__ret__.status_reason)


@_utilities.lift_output_func(get_billing_group)
def get_billing_group_output(arn: Optional[pulumi.Input[str]] = None,
                             opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetBillingGroupResult]:
    """
    A billing group is a set of linked account which belong to the same end customer. It can be seen as a virtual consolidated billing family.


    :param str arn: Billing Group ARN
    """
    ...
