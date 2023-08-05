# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs
from ._inputs import *

__all__ = ['DBClusterArgs', 'DBCluster']

@pulumi.input_type
class DBClusterArgs:
    def __init__(__self__, *,
                 associated_roles: Optional[pulumi.Input[Sequence[pulumi.Input['DBClusterRoleArgs']]]] = None,
                 availability_zones: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 backup_retention_period: Optional[pulumi.Input[int]] = None,
                 d_b_cluster_identifier: Optional[pulumi.Input[str]] = None,
                 d_b_cluster_parameter_group_name: Optional[pulumi.Input[str]] = None,
                 d_b_subnet_group_name: Optional[pulumi.Input[str]] = None,
                 deletion_protection: Optional[pulumi.Input[bool]] = None,
                 enable_cloudwatch_logs_exports: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 engine_version: Optional[pulumi.Input[str]] = None,
                 iam_auth_enabled: Optional[pulumi.Input[bool]] = None,
                 kms_key_id: Optional[pulumi.Input[str]] = None,
                 port: Optional[pulumi.Input[int]] = None,
                 preferred_backup_window: Optional[pulumi.Input[str]] = None,
                 preferred_maintenance_window: Optional[pulumi.Input[str]] = None,
                 restore_to_time: Optional[pulumi.Input[str]] = None,
                 restore_type: Optional[pulumi.Input[str]] = None,
                 snapshot_identifier: Optional[pulumi.Input[str]] = None,
                 source_db_cluster_identifier: Optional[pulumi.Input[str]] = None,
                 storage_encrypted: Optional[pulumi.Input[bool]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input['DBClusterTagArgs']]]] = None,
                 use_latest_restorable_time: Optional[pulumi.Input[bool]] = None,
                 vpc_security_group_ids: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a DBCluster resource.
        """
        if associated_roles is not None:
            pulumi.set(__self__, "associated_roles", associated_roles)
        if availability_zones is not None:
            pulumi.set(__self__, "availability_zones", availability_zones)
        if backup_retention_period is not None:
            pulumi.set(__self__, "backup_retention_period", backup_retention_period)
        if d_b_cluster_identifier is not None:
            pulumi.set(__self__, "d_b_cluster_identifier", d_b_cluster_identifier)
        if d_b_cluster_parameter_group_name is not None:
            pulumi.set(__self__, "d_b_cluster_parameter_group_name", d_b_cluster_parameter_group_name)
        if d_b_subnet_group_name is not None:
            pulumi.set(__self__, "d_b_subnet_group_name", d_b_subnet_group_name)
        if deletion_protection is not None:
            pulumi.set(__self__, "deletion_protection", deletion_protection)
        if enable_cloudwatch_logs_exports is not None:
            pulumi.set(__self__, "enable_cloudwatch_logs_exports", enable_cloudwatch_logs_exports)
        if engine_version is not None:
            pulumi.set(__self__, "engine_version", engine_version)
        if iam_auth_enabled is not None:
            pulumi.set(__self__, "iam_auth_enabled", iam_auth_enabled)
        if kms_key_id is not None:
            pulumi.set(__self__, "kms_key_id", kms_key_id)
        if port is not None:
            pulumi.set(__self__, "port", port)
        if preferred_backup_window is not None:
            pulumi.set(__self__, "preferred_backup_window", preferred_backup_window)
        if preferred_maintenance_window is not None:
            pulumi.set(__self__, "preferred_maintenance_window", preferred_maintenance_window)
        if restore_to_time is not None:
            pulumi.set(__self__, "restore_to_time", restore_to_time)
        if restore_type is not None:
            pulumi.set(__self__, "restore_type", restore_type)
        if snapshot_identifier is not None:
            pulumi.set(__self__, "snapshot_identifier", snapshot_identifier)
        if source_db_cluster_identifier is not None:
            pulumi.set(__self__, "source_db_cluster_identifier", source_db_cluster_identifier)
        if storage_encrypted is not None:
            pulumi.set(__self__, "storage_encrypted", storage_encrypted)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if use_latest_restorable_time is not None:
            pulumi.set(__self__, "use_latest_restorable_time", use_latest_restorable_time)
        if vpc_security_group_ids is not None:
            pulumi.set(__self__, "vpc_security_group_ids", vpc_security_group_ids)

    @property
    @pulumi.getter(name="associatedRoles")
    def associated_roles(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['DBClusterRoleArgs']]]]:
        return pulumi.get(self, "associated_roles")

    @associated_roles.setter
    def associated_roles(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['DBClusterRoleArgs']]]]):
        pulumi.set(self, "associated_roles", value)

    @property
    @pulumi.getter(name="availabilityZones")
    def availability_zones(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        return pulumi.get(self, "availability_zones")

    @availability_zones.setter
    def availability_zones(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "availability_zones", value)

    @property
    @pulumi.getter(name="backupRetentionPeriod")
    def backup_retention_period(self) -> Optional[pulumi.Input[int]]:
        return pulumi.get(self, "backup_retention_period")

    @backup_retention_period.setter
    def backup_retention_period(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "backup_retention_period", value)

    @property
    @pulumi.getter(name="dBClusterIdentifier")
    def d_b_cluster_identifier(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "d_b_cluster_identifier")

    @d_b_cluster_identifier.setter
    def d_b_cluster_identifier(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "d_b_cluster_identifier", value)

    @property
    @pulumi.getter(name="dBClusterParameterGroupName")
    def d_b_cluster_parameter_group_name(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "d_b_cluster_parameter_group_name")

    @d_b_cluster_parameter_group_name.setter
    def d_b_cluster_parameter_group_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "d_b_cluster_parameter_group_name", value)

    @property
    @pulumi.getter(name="dBSubnetGroupName")
    def d_b_subnet_group_name(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "d_b_subnet_group_name")

    @d_b_subnet_group_name.setter
    def d_b_subnet_group_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "d_b_subnet_group_name", value)

    @property
    @pulumi.getter(name="deletionProtection")
    def deletion_protection(self) -> Optional[pulumi.Input[bool]]:
        return pulumi.get(self, "deletion_protection")

    @deletion_protection.setter
    def deletion_protection(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "deletion_protection", value)

    @property
    @pulumi.getter(name="enableCloudwatchLogsExports")
    def enable_cloudwatch_logs_exports(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        return pulumi.get(self, "enable_cloudwatch_logs_exports")

    @enable_cloudwatch_logs_exports.setter
    def enable_cloudwatch_logs_exports(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "enable_cloudwatch_logs_exports", value)

    @property
    @pulumi.getter(name="engineVersion")
    def engine_version(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "engine_version")

    @engine_version.setter
    def engine_version(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "engine_version", value)

    @property
    @pulumi.getter(name="iamAuthEnabled")
    def iam_auth_enabled(self) -> Optional[pulumi.Input[bool]]:
        return pulumi.get(self, "iam_auth_enabled")

    @iam_auth_enabled.setter
    def iam_auth_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "iam_auth_enabled", value)

    @property
    @pulumi.getter(name="kmsKeyId")
    def kms_key_id(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "kms_key_id")

    @kms_key_id.setter
    def kms_key_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "kms_key_id", value)

    @property
    @pulumi.getter
    def port(self) -> Optional[pulumi.Input[int]]:
        return pulumi.get(self, "port")

    @port.setter
    def port(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "port", value)

    @property
    @pulumi.getter(name="preferredBackupWindow")
    def preferred_backup_window(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "preferred_backup_window")

    @preferred_backup_window.setter
    def preferred_backup_window(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "preferred_backup_window", value)

    @property
    @pulumi.getter(name="preferredMaintenanceWindow")
    def preferred_maintenance_window(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "preferred_maintenance_window")

    @preferred_maintenance_window.setter
    def preferred_maintenance_window(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "preferred_maintenance_window", value)

    @property
    @pulumi.getter(name="restoreToTime")
    def restore_to_time(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "restore_to_time")

    @restore_to_time.setter
    def restore_to_time(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "restore_to_time", value)

    @property
    @pulumi.getter(name="restoreType")
    def restore_type(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "restore_type")

    @restore_type.setter
    def restore_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "restore_type", value)

    @property
    @pulumi.getter(name="snapshotIdentifier")
    def snapshot_identifier(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "snapshot_identifier")

    @snapshot_identifier.setter
    def snapshot_identifier(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "snapshot_identifier", value)

    @property
    @pulumi.getter(name="sourceDBClusterIdentifier")
    def source_db_cluster_identifier(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "source_db_cluster_identifier")

    @source_db_cluster_identifier.setter
    def source_db_cluster_identifier(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "source_db_cluster_identifier", value)

    @property
    @pulumi.getter(name="storageEncrypted")
    def storage_encrypted(self) -> Optional[pulumi.Input[bool]]:
        return pulumi.get(self, "storage_encrypted")

    @storage_encrypted.setter
    def storage_encrypted(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "storage_encrypted", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['DBClusterTagArgs']]]]:
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['DBClusterTagArgs']]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter(name="useLatestRestorableTime")
    def use_latest_restorable_time(self) -> Optional[pulumi.Input[bool]]:
        return pulumi.get(self, "use_latest_restorable_time")

    @use_latest_restorable_time.setter
    def use_latest_restorable_time(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "use_latest_restorable_time", value)

    @property
    @pulumi.getter(name="vpcSecurityGroupIds")
    def vpc_security_group_ids(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        return pulumi.get(self, "vpc_security_group_ids")

    @vpc_security_group_ids.setter
    def vpc_security_group_ids(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "vpc_security_group_ids", value)


warnings.warn("""DBCluster is not yet supported by AWS Native, so its creation will currently fail. Please use the classic AWS provider, if possible.""", DeprecationWarning)


class DBCluster(pulumi.CustomResource):
    warnings.warn("""DBCluster is not yet supported by AWS Native, so its creation will currently fail. Please use the classic AWS provider, if possible.""", DeprecationWarning)

    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 associated_roles: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['DBClusterRoleArgs']]]]] = None,
                 availability_zones: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 backup_retention_period: Optional[pulumi.Input[int]] = None,
                 d_b_cluster_identifier: Optional[pulumi.Input[str]] = None,
                 d_b_cluster_parameter_group_name: Optional[pulumi.Input[str]] = None,
                 d_b_subnet_group_name: Optional[pulumi.Input[str]] = None,
                 deletion_protection: Optional[pulumi.Input[bool]] = None,
                 enable_cloudwatch_logs_exports: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 engine_version: Optional[pulumi.Input[str]] = None,
                 iam_auth_enabled: Optional[pulumi.Input[bool]] = None,
                 kms_key_id: Optional[pulumi.Input[str]] = None,
                 port: Optional[pulumi.Input[int]] = None,
                 preferred_backup_window: Optional[pulumi.Input[str]] = None,
                 preferred_maintenance_window: Optional[pulumi.Input[str]] = None,
                 restore_to_time: Optional[pulumi.Input[str]] = None,
                 restore_type: Optional[pulumi.Input[str]] = None,
                 snapshot_identifier: Optional[pulumi.Input[str]] = None,
                 source_db_cluster_identifier: Optional[pulumi.Input[str]] = None,
                 storage_encrypted: Optional[pulumi.Input[bool]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['DBClusterTagArgs']]]]] = None,
                 use_latest_restorable_time: Optional[pulumi.Input[bool]] = None,
                 vpc_security_group_ids: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        Resource Type definition for AWS::Neptune::DBCluster

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: Optional[DBClusterArgs] = None,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Resource Type definition for AWS::Neptune::DBCluster

        :param str resource_name: The name of the resource.
        :param DBClusterArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(DBClusterArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 associated_roles: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['DBClusterRoleArgs']]]]] = None,
                 availability_zones: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 backup_retention_period: Optional[pulumi.Input[int]] = None,
                 d_b_cluster_identifier: Optional[pulumi.Input[str]] = None,
                 d_b_cluster_parameter_group_name: Optional[pulumi.Input[str]] = None,
                 d_b_subnet_group_name: Optional[pulumi.Input[str]] = None,
                 deletion_protection: Optional[pulumi.Input[bool]] = None,
                 enable_cloudwatch_logs_exports: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 engine_version: Optional[pulumi.Input[str]] = None,
                 iam_auth_enabled: Optional[pulumi.Input[bool]] = None,
                 kms_key_id: Optional[pulumi.Input[str]] = None,
                 port: Optional[pulumi.Input[int]] = None,
                 preferred_backup_window: Optional[pulumi.Input[str]] = None,
                 preferred_maintenance_window: Optional[pulumi.Input[str]] = None,
                 restore_to_time: Optional[pulumi.Input[str]] = None,
                 restore_type: Optional[pulumi.Input[str]] = None,
                 snapshot_identifier: Optional[pulumi.Input[str]] = None,
                 source_db_cluster_identifier: Optional[pulumi.Input[str]] = None,
                 storage_encrypted: Optional[pulumi.Input[bool]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['DBClusterTagArgs']]]]] = None,
                 use_latest_restorable_time: Optional[pulumi.Input[bool]] = None,
                 vpc_security_group_ids: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 __props__=None):
        pulumi.log.warn("""DBCluster is deprecated: DBCluster is not yet supported by AWS Native, so its creation will currently fail. Please use the classic AWS provider, if possible.""")
        if opts is None:
            opts = pulumi.ResourceOptions()
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.version is None:
            opts.version = _utilities.get_version()
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = DBClusterArgs.__new__(DBClusterArgs)

            __props__.__dict__["associated_roles"] = associated_roles
            __props__.__dict__["availability_zones"] = availability_zones
            __props__.__dict__["backup_retention_period"] = backup_retention_period
            __props__.__dict__["d_b_cluster_identifier"] = d_b_cluster_identifier
            __props__.__dict__["d_b_cluster_parameter_group_name"] = d_b_cluster_parameter_group_name
            __props__.__dict__["d_b_subnet_group_name"] = d_b_subnet_group_name
            __props__.__dict__["deletion_protection"] = deletion_protection
            __props__.__dict__["enable_cloudwatch_logs_exports"] = enable_cloudwatch_logs_exports
            __props__.__dict__["engine_version"] = engine_version
            __props__.__dict__["iam_auth_enabled"] = iam_auth_enabled
            __props__.__dict__["kms_key_id"] = kms_key_id
            __props__.__dict__["port"] = port
            __props__.__dict__["preferred_backup_window"] = preferred_backup_window
            __props__.__dict__["preferred_maintenance_window"] = preferred_maintenance_window
            __props__.__dict__["restore_to_time"] = restore_to_time
            __props__.__dict__["restore_type"] = restore_type
            __props__.__dict__["snapshot_identifier"] = snapshot_identifier
            __props__.__dict__["source_db_cluster_identifier"] = source_db_cluster_identifier
            __props__.__dict__["storage_encrypted"] = storage_encrypted
            __props__.__dict__["tags"] = tags
            __props__.__dict__["use_latest_restorable_time"] = use_latest_restorable_time
            __props__.__dict__["vpc_security_group_ids"] = vpc_security_group_ids
            __props__.__dict__["cluster_resource_id"] = None
            __props__.__dict__["endpoint"] = None
            __props__.__dict__["read_endpoint"] = None
        super(DBCluster, __self__).__init__(
            'aws-native:neptune:DBCluster',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'DBCluster':
        """
        Get an existing DBCluster resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = DBClusterArgs.__new__(DBClusterArgs)

        __props__.__dict__["associated_roles"] = None
        __props__.__dict__["availability_zones"] = None
        __props__.__dict__["backup_retention_period"] = None
        __props__.__dict__["cluster_resource_id"] = None
        __props__.__dict__["d_b_cluster_identifier"] = None
        __props__.__dict__["d_b_cluster_parameter_group_name"] = None
        __props__.__dict__["d_b_subnet_group_name"] = None
        __props__.__dict__["deletion_protection"] = None
        __props__.__dict__["enable_cloudwatch_logs_exports"] = None
        __props__.__dict__["endpoint"] = None
        __props__.__dict__["engine_version"] = None
        __props__.__dict__["iam_auth_enabled"] = None
        __props__.__dict__["kms_key_id"] = None
        __props__.__dict__["port"] = None
        __props__.__dict__["preferred_backup_window"] = None
        __props__.__dict__["preferred_maintenance_window"] = None
        __props__.__dict__["read_endpoint"] = None
        __props__.__dict__["restore_to_time"] = None
        __props__.__dict__["restore_type"] = None
        __props__.__dict__["snapshot_identifier"] = None
        __props__.__dict__["source_db_cluster_identifier"] = None
        __props__.__dict__["storage_encrypted"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["use_latest_restorable_time"] = None
        __props__.__dict__["vpc_security_group_ids"] = None
        return DBCluster(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="associatedRoles")
    def associated_roles(self) -> pulumi.Output[Optional[Sequence['outputs.DBClusterRole']]]:
        return pulumi.get(self, "associated_roles")

    @property
    @pulumi.getter(name="availabilityZones")
    def availability_zones(self) -> pulumi.Output[Optional[Sequence[str]]]:
        return pulumi.get(self, "availability_zones")

    @property
    @pulumi.getter(name="backupRetentionPeriod")
    def backup_retention_period(self) -> pulumi.Output[Optional[int]]:
        return pulumi.get(self, "backup_retention_period")

    @property
    @pulumi.getter(name="clusterResourceId")
    def cluster_resource_id(self) -> pulumi.Output[str]:
        return pulumi.get(self, "cluster_resource_id")

    @property
    @pulumi.getter(name="dBClusterIdentifier")
    def d_b_cluster_identifier(self) -> pulumi.Output[Optional[str]]:
        return pulumi.get(self, "d_b_cluster_identifier")

    @property
    @pulumi.getter(name="dBClusterParameterGroupName")
    def d_b_cluster_parameter_group_name(self) -> pulumi.Output[Optional[str]]:
        return pulumi.get(self, "d_b_cluster_parameter_group_name")

    @property
    @pulumi.getter(name="dBSubnetGroupName")
    def d_b_subnet_group_name(self) -> pulumi.Output[Optional[str]]:
        return pulumi.get(self, "d_b_subnet_group_name")

    @property
    @pulumi.getter(name="deletionProtection")
    def deletion_protection(self) -> pulumi.Output[Optional[bool]]:
        return pulumi.get(self, "deletion_protection")

    @property
    @pulumi.getter(name="enableCloudwatchLogsExports")
    def enable_cloudwatch_logs_exports(self) -> pulumi.Output[Optional[Sequence[str]]]:
        return pulumi.get(self, "enable_cloudwatch_logs_exports")

    @property
    @pulumi.getter
    def endpoint(self) -> pulumi.Output[str]:
        return pulumi.get(self, "endpoint")

    @property
    @pulumi.getter(name="engineVersion")
    def engine_version(self) -> pulumi.Output[Optional[str]]:
        return pulumi.get(self, "engine_version")

    @property
    @pulumi.getter(name="iamAuthEnabled")
    def iam_auth_enabled(self) -> pulumi.Output[Optional[bool]]:
        return pulumi.get(self, "iam_auth_enabled")

    @property
    @pulumi.getter(name="kmsKeyId")
    def kms_key_id(self) -> pulumi.Output[Optional[str]]:
        return pulumi.get(self, "kms_key_id")

    @property
    @pulumi.getter
    def port(self) -> pulumi.Output[Optional[int]]:
        return pulumi.get(self, "port")

    @property
    @pulumi.getter(name="preferredBackupWindow")
    def preferred_backup_window(self) -> pulumi.Output[Optional[str]]:
        return pulumi.get(self, "preferred_backup_window")

    @property
    @pulumi.getter(name="preferredMaintenanceWindow")
    def preferred_maintenance_window(self) -> pulumi.Output[Optional[str]]:
        return pulumi.get(self, "preferred_maintenance_window")

    @property
    @pulumi.getter(name="readEndpoint")
    def read_endpoint(self) -> pulumi.Output[str]:
        return pulumi.get(self, "read_endpoint")

    @property
    @pulumi.getter(name="restoreToTime")
    def restore_to_time(self) -> pulumi.Output[Optional[str]]:
        return pulumi.get(self, "restore_to_time")

    @property
    @pulumi.getter(name="restoreType")
    def restore_type(self) -> pulumi.Output[Optional[str]]:
        return pulumi.get(self, "restore_type")

    @property
    @pulumi.getter(name="snapshotIdentifier")
    def snapshot_identifier(self) -> pulumi.Output[Optional[str]]:
        return pulumi.get(self, "snapshot_identifier")

    @property
    @pulumi.getter(name="sourceDBClusterIdentifier")
    def source_db_cluster_identifier(self) -> pulumi.Output[Optional[str]]:
        return pulumi.get(self, "source_db_cluster_identifier")

    @property
    @pulumi.getter(name="storageEncrypted")
    def storage_encrypted(self) -> pulumi.Output[Optional[bool]]:
        return pulumi.get(self, "storage_encrypted")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Sequence['outputs.DBClusterTag']]]:
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="useLatestRestorableTime")
    def use_latest_restorable_time(self) -> pulumi.Output[Optional[bool]]:
        return pulumi.get(self, "use_latest_restorable_time")

    @property
    @pulumi.getter(name="vpcSecurityGroupIds")
    def vpc_security_group_ids(self) -> pulumi.Output[Optional[Sequence[str]]]:
        return pulumi.get(self, "vpc_security_group_ids")

