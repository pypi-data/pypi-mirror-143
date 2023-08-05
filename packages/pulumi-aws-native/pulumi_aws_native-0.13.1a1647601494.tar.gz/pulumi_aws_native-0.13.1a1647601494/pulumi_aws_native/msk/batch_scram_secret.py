# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['BatchScramSecretArgs', 'BatchScramSecret']

@pulumi.input_type
class BatchScramSecretArgs:
    def __init__(__self__, *,
                 cluster_arn: pulumi.Input[str],
                 secret_arn_list: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a BatchScramSecret resource.
        """
        pulumi.set(__self__, "cluster_arn", cluster_arn)
        if secret_arn_list is not None:
            pulumi.set(__self__, "secret_arn_list", secret_arn_list)

    @property
    @pulumi.getter(name="clusterArn")
    def cluster_arn(self) -> pulumi.Input[str]:
        return pulumi.get(self, "cluster_arn")

    @cluster_arn.setter
    def cluster_arn(self, value: pulumi.Input[str]):
        pulumi.set(self, "cluster_arn", value)

    @property
    @pulumi.getter(name="secretArnList")
    def secret_arn_list(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        return pulumi.get(self, "secret_arn_list")

    @secret_arn_list.setter
    def secret_arn_list(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "secret_arn_list", value)


class BatchScramSecret(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 cluster_arn: Optional[pulumi.Input[str]] = None,
                 secret_arn_list: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        Resource Type definition for AWS::MSK::BatchScramSecret

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: BatchScramSecretArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Resource Type definition for AWS::MSK::BatchScramSecret

        :param str resource_name: The name of the resource.
        :param BatchScramSecretArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(BatchScramSecretArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 cluster_arn: Optional[pulumi.Input[str]] = None,
                 secret_arn_list: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 __props__=None):
        if opts is None:
            opts = pulumi.ResourceOptions()
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.version is None:
            opts.version = _utilities.get_version()
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = BatchScramSecretArgs.__new__(BatchScramSecretArgs)

            if cluster_arn is None and not opts.urn:
                raise TypeError("Missing required property 'cluster_arn'")
            __props__.__dict__["cluster_arn"] = cluster_arn
            __props__.__dict__["secret_arn_list"] = secret_arn_list
        super(BatchScramSecret, __self__).__init__(
            'aws-native:msk:BatchScramSecret',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'BatchScramSecret':
        """
        Get an existing BatchScramSecret resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = BatchScramSecretArgs.__new__(BatchScramSecretArgs)

        __props__.__dict__["cluster_arn"] = None
        __props__.__dict__["secret_arn_list"] = None
        return BatchScramSecret(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="clusterArn")
    def cluster_arn(self) -> pulumi.Output[str]:
        return pulumi.get(self, "cluster_arn")

    @property
    @pulumi.getter(name="secretArnList")
    def secret_arn_list(self) -> pulumi.Output[Optional[Sequence[str]]]:
        return pulumi.get(self, "secret_arn_list")

