# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs

__all__ = [
    'GetListenerResult',
    'AwaitableGetListenerResult',
    'get_listener',
    'get_listener_output',
]

@pulumi.output_type
class GetListenerResult:
    def __init__(__self__, alpn_policy=None, certificates=None, default_actions=None, listener_arn=None, port=None, protocol=None, ssl_policy=None):
        if alpn_policy and not isinstance(alpn_policy, list):
            raise TypeError("Expected argument 'alpn_policy' to be a list")
        pulumi.set(__self__, "alpn_policy", alpn_policy)
        if certificates and not isinstance(certificates, list):
            raise TypeError("Expected argument 'certificates' to be a list")
        pulumi.set(__self__, "certificates", certificates)
        if default_actions and not isinstance(default_actions, list):
            raise TypeError("Expected argument 'default_actions' to be a list")
        pulumi.set(__self__, "default_actions", default_actions)
        if listener_arn and not isinstance(listener_arn, str):
            raise TypeError("Expected argument 'listener_arn' to be a str")
        pulumi.set(__self__, "listener_arn", listener_arn)
        if port and not isinstance(port, int):
            raise TypeError("Expected argument 'port' to be a int")
        pulumi.set(__self__, "port", port)
        if protocol and not isinstance(protocol, str):
            raise TypeError("Expected argument 'protocol' to be a str")
        pulumi.set(__self__, "protocol", protocol)
        if ssl_policy and not isinstance(ssl_policy, str):
            raise TypeError("Expected argument 'ssl_policy' to be a str")
        pulumi.set(__self__, "ssl_policy", ssl_policy)

    @property
    @pulumi.getter(name="alpnPolicy")
    def alpn_policy(self) -> Optional[Sequence[str]]:
        return pulumi.get(self, "alpn_policy")

    @property
    @pulumi.getter
    def certificates(self) -> Optional[Sequence['outputs.ListenerCertificate']]:
        return pulumi.get(self, "certificates")

    @property
    @pulumi.getter(name="defaultActions")
    def default_actions(self) -> Optional[Sequence['outputs.ListenerAction']]:
        return pulumi.get(self, "default_actions")

    @property
    @pulumi.getter(name="listenerArn")
    def listener_arn(self) -> Optional[str]:
        return pulumi.get(self, "listener_arn")

    @property
    @pulumi.getter
    def port(self) -> Optional[int]:
        return pulumi.get(self, "port")

    @property
    @pulumi.getter
    def protocol(self) -> Optional[str]:
        return pulumi.get(self, "protocol")

    @property
    @pulumi.getter(name="sslPolicy")
    def ssl_policy(self) -> Optional[str]:
        return pulumi.get(self, "ssl_policy")


class AwaitableGetListenerResult(GetListenerResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetListenerResult(
            alpn_policy=self.alpn_policy,
            certificates=self.certificates,
            default_actions=self.default_actions,
            listener_arn=self.listener_arn,
            port=self.port,
            protocol=self.protocol,
            ssl_policy=self.ssl_policy)


def get_listener(listener_arn: Optional[str] = None,
                 opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetListenerResult:
    """
    Resource Type definition for AWS::ElasticLoadBalancingV2::Listener
    """
    __args__ = dict()
    __args__['listenerArn'] = listener_arn
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('aws-native:elasticloadbalancingv2:getListener', __args__, opts=opts, typ=GetListenerResult).value

    return AwaitableGetListenerResult(
        alpn_policy=__ret__.alpn_policy,
        certificates=__ret__.certificates,
        default_actions=__ret__.default_actions,
        listener_arn=__ret__.listener_arn,
        port=__ret__.port,
        protocol=__ret__.protocol,
        ssl_policy=__ret__.ssl_policy)


@_utilities.lift_output_func(get_listener)
def get_listener_output(listener_arn: Optional[pulumi.Input[str]] = None,
                        opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetListenerResult]:
    """
    Resource Type definition for AWS::ElasticLoadBalancingV2::Listener
    """
    ...
