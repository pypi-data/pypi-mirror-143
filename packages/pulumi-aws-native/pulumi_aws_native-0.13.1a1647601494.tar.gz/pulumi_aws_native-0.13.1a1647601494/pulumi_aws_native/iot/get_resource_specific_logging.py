# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from ._enums import *

__all__ = [
    'GetResourceSpecificLoggingResult',
    'AwaitableGetResourceSpecificLoggingResult',
    'get_resource_specific_logging',
    'get_resource_specific_logging_output',
]

@pulumi.output_type
class GetResourceSpecificLoggingResult:
    def __init__(__self__, log_level=None, target_id=None):
        if log_level and not isinstance(log_level, str):
            raise TypeError("Expected argument 'log_level' to be a str")
        pulumi.set(__self__, "log_level", log_level)
        if target_id and not isinstance(target_id, str):
            raise TypeError("Expected argument 'target_id' to be a str")
        pulumi.set(__self__, "target_id", target_id)

    @property
    @pulumi.getter(name="logLevel")
    def log_level(self) -> Optional['ResourceSpecificLoggingLogLevel']:
        """
        The log level for a specific target. Valid values are: ERROR, WARN, INFO, DEBUG, or DISABLED.
        """
        return pulumi.get(self, "log_level")

    @property
    @pulumi.getter(name="targetId")
    def target_id(self) -> Optional[str]:
        """
        Unique Id for a Target (TargetType:TargetName), this will be internally built to serve as primary identifier for a log target.
        """
        return pulumi.get(self, "target_id")


class AwaitableGetResourceSpecificLoggingResult(GetResourceSpecificLoggingResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetResourceSpecificLoggingResult(
            log_level=self.log_level,
            target_id=self.target_id)


def get_resource_specific_logging(target_id: Optional[str] = None,
                                  opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetResourceSpecificLoggingResult:
    """
    Resource-specific logging allows you to specify a logging level for a specific thing group.


    :param str target_id: Unique Id for a Target (TargetType:TargetName), this will be internally built to serve as primary identifier for a log target.
    """
    __args__ = dict()
    __args__['targetId'] = target_id
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('aws-native:iot:getResourceSpecificLogging', __args__, opts=opts, typ=GetResourceSpecificLoggingResult).value

    return AwaitableGetResourceSpecificLoggingResult(
        log_level=__ret__.log_level,
        target_id=__ret__.target_id)


@_utilities.lift_output_func(get_resource_specific_logging)
def get_resource_specific_logging_output(target_id: Optional[pulumi.Input[str]] = None,
                                         opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetResourceSpecificLoggingResult]:
    """
    Resource-specific logging allows you to specify a logging level for a specific thing group.


    :param str target_id: Unique Id for a Target (TargetType:TargetName), this will be internally built to serve as primary identifier for a log target.
    """
    ...
