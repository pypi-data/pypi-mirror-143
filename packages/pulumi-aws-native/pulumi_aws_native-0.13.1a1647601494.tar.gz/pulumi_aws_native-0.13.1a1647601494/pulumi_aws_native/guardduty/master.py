# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['MasterArgs', 'Master']

@pulumi.input_type
class MasterArgs:
    def __init__(__self__, *,
                 detector_id: pulumi.Input[str],
                 invitation_id: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a Master resource.
        """
        pulumi.set(__self__, "detector_id", detector_id)
        if invitation_id is not None:
            pulumi.set(__self__, "invitation_id", invitation_id)

    @property
    @pulumi.getter(name="detectorId")
    def detector_id(self) -> pulumi.Input[str]:
        return pulumi.get(self, "detector_id")

    @detector_id.setter
    def detector_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "detector_id", value)

    @property
    @pulumi.getter(name="invitationId")
    def invitation_id(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "invitation_id")

    @invitation_id.setter
    def invitation_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "invitation_id", value)


warnings.warn("""Master is not yet supported by AWS Native, so its creation will currently fail. Please use the classic AWS provider, if possible.""", DeprecationWarning)


class Master(pulumi.CustomResource):
    warnings.warn("""Master is not yet supported by AWS Native, so its creation will currently fail. Please use the classic AWS provider, if possible.""", DeprecationWarning)

    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 detector_id: Optional[pulumi.Input[str]] = None,
                 invitation_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Resource Type definition for AWS::GuardDuty::Master

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: MasterArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Resource Type definition for AWS::GuardDuty::Master

        :param str resource_name: The name of the resource.
        :param MasterArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(MasterArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 detector_id: Optional[pulumi.Input[str]] = None,
                 invitation_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        pulumi.log.warn("""Master is deprecated: Master is not yet supported by AWS Native, so its creation will currently fail. Please use the classic AWS provider, if possible.""")
        if opts is None:
            opts = pulumi.ResourceOptions()
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.version is None:
            opts.version = _utilities.get_version()
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = MasterArgs.__new__(MasterArgs)

            if detector_id is None and not opts.urn:
                raise TypeError("Missing required property 'detector_id'")
            __props__.__dict__["detector_id"] = detector_id
            __props__.__dict__["invitation_id"] = invitation_id
            __props__.__dict__["master_id"] = None
        super(Master, __self__).__init__(
            'aws-native:guardduty:Master',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Master':
        """
        Get an existing Master resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = MasterArgs.__new__(MasterArgs)

        __props__.__dict__["detector_id"] = None
        __props__.__dict__["invitation_id"] = None
        __props__.__dict__["master_id"] = None
        return Master(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="detectorId")
    def detector_id(self) -> pulumi.Output[str]:
        return pulumi.get(self, "detector_id")

    @property
    @pulumi.getter(name="invitationId")
    def invitation_id(self) -> pulumi.Output[Optional[str]]:
        return pulumi.get(self, "invitation_id")

    @property
    @pulumi.getter(name="masterId")
    def master_id(self) -> pulumi.Output[str]:
        return pulumi.get(self, "master_id")

