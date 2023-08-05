# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['PermissionArgs', 'Permission']

@pulumi.input_type
class PermissionArgs:
    def __init__(__self__, *,
                 actions: pulumi.Input[Sequence[pulumi.Input[str]]],
                 certificate_authority_arn: pulumi.Input[str],
                 principal: pulumi.Input[str],
                 source_account: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a Permission resource.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] actions: The actions that the specified AWS service principal can use. Actions IssueCertificate, GetCertificate and ListPermissions must be provided.
        :param pulumi.Input[str] certificate_authority_arn: The Amazon Resource Name (ARN) of the Private Certificate Authority that grants the permission.
        :param pulumi.Input[str] principal: The AWS service or identity that receives the permission. At this time, the only valid principal is acm.amazonaws.com.
        :param pulumi.Input[str] source_account: The ID of the calling account.
        """
        pulumi.set(__self__, "actions", actions)
        pulumi.set(__self__, "certificate_authority_arn", certificate_authority_arn)
        pulumi.set(__self__, "principal", principal)
        if source_account is not None:
            pulumi.set(__self__, "source_account", source_account)

    @property
    @pulumi.getter
    def actions(self) -> pulumi.Input[Sequence[pulumi.Input[str]]]:
        """
        The actions that the specified AWS service principal can use. Actions IssueCertificate, GetCertificate and ListPermissions must be provided.
        """
        return pulumi.get(self, "actions")

    @actions.setter
    def actions(self, value: pulumi.Input[Sequence[pulumi.Input[str]]]):
        pulumi.set(self, "actions", value)

    @property
    @pulumi.getter(name="certificateAuthorityArn")
    def certificate_authority_arn(self) -> pulumi.Input[str]:
        """
        The Amazon Resource Name (ARN) of the Private Certificate Authority that grants the permission.
        """
        return pulumi.get(self, "certificate_authority_arn")

    @certificate_authority_arn.setter
    def certificate_authority_arn(self, value: pulumi.Input[str]):
        pulumi.set(self, "certificate_authority_arn", value)

    @property
    @pulumi.getter
    def principal(self) -> pulumi.Input[str]:
        """
        The AWS service or identity that receives the permission. At this time, the only valid principal is acm.amazonaws.com.
        """
        return pulumi.get(self, "principal")

    @principal.setter
    def principal(self, value: pulumi.Input[str]):
        pulumi.set(self, "principal", value)

    @property
    @pulumi.getter(name="sourceAccount")
    def source_account(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the calling account.
        """
        return pulumi.get(self, "source_account")

    @source_account.setter
    def source_account(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "source_account", value)


class Permission(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 actions: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 certificate_authority_arn: Optional[pulumi.Input[str]] = None,
                 principal: Optional[pulumi.Input[str]] = None,
                 source_account: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Permission set on private certificate authority

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] actions: The actions that the specified AWS service principal can use. Actions IssueCertificate, GetCertificate and ListPermissions must be provided.
        :param pulumi.Input[str] certificate_authority_arn: The Amazon Resource Name (ARN) of the Private Certificate Authority that grants the permission.
        :param pulumi.Input[str] principal: The AWS service or identity that receives the permission. At this time, the only valid principal is acm.amazonaws.com.
        :param pulumi.Input[str] source_account: The ID of the calling account.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: PermissionArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Permission set on private certificate authority

        :param str resource_name: The name of the resource.
        :param PermissionArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(PermissionArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 actions: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 certificate_authority_arn: Optional[pulumi.Input[str]] = None,
                 principal: Optional[pulumi.Input[str]] = None,
                 source_account: Optional[pulumi.Input[str]] = None,
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
            __props__ = PermissionArgs.__new__(PermissionArgs)

            if actions is None and not opts.urn:
                raise TypeError("Missing required property 'actions'")
            __props__.__dict__["actions"] = actions
            if certificate_authority_arn is None and not opts.urn:
                raise TypeError("Missing required property 'certificate_authority_arn'")
            __props__.__dict__["certificate_authority_arn"] = certificate_authority_arn
            if principal is None and not opts.urn:
                raise TypeError("Missing required property 'principal'")
            __props__.__dict__["principal"] = principal
            __props__.__dict__["source_account"] = source_account
        super(Permission, __self__).__init__(
            'aws-native:acmpca:Permission',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Permission':
        """
        Get an existing Permission resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = PermissionArgs.__new__(PermissionArgs)

        __props__.__dict__["actions"] = None
        __props__.__dict__["certificate_authority_arn"] = None
        __props__.__dict__["principal"] = None
        __props__.__dict__["source_account"] = None
        return Permission(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def actions(self) -> pulumi.Output[Sequence[str]]:
        """
        The actions that the specified AWS service principal can use. Actions IssueCertificate, GetCertificate and ListPermissions must be provided.
        """
        return pulumi.get(self, "actions")

    @property
    @pulumi.getter(name="certificateAuthorityArn")
    def certificate_authority_arn(self) -> pulumi.Output[str]:
        """
        The Amazon Resource Name (ARN) of the Private Certificate Authority that grants the permission.
        """
        return pulumi.get(self, "certificate_authority_arn")

    @property
    @pulumi.getter
    def principal(self) -> pulumi.Output[str]:
        """
        The AWS service or identity that receives the permission. At this time, the only valid principal is acm.amazonaws.com.
        """
        return pulumi.get(self, "principal")

    @property
    @pulumi.getter(name="sourceAccount")
    def source_account(self) -> pulumi.Output[Optional[str]]:
        """
        The ID of the calling account.
        """
        return pulumi.get(self, "source_account")

