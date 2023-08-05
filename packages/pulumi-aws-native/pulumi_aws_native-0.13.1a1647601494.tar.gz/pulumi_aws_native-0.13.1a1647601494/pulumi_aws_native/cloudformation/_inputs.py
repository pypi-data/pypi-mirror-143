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
    'HookVersionLoggingConfigArgs',
    'ManagedExecutionPropertiesArgs',
    'ResourceVersionLoggingConfigArgs',
    'StackSetAutoDeploymentArgs',
    'StackSetDeploymentTargetsArgs',
    'StackSetOperationPreferencesArgs',
    'StackSetParameterArgs',
    'StackSetStackInstancesArgs',
    'StackSetTagArgs',
    'StackTagArgs',
    'TypeActivationLoggingConfigArgs',
]

@pulumi.input_type
class HookVersionLoggingConfigArgs:
    def __init__(__self__, *,
                 log_group_name: Optional[pulumi.Input[str]] = None,
                 log_role_arn: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] log_group_name: The Amazon CloudWatch log group to which CloudFormation sends error logging information when invoking the type's handlers.
        :param pulumi.Input[str] log_role_arn: The ARN of the role that CloudFormation should assume when sending log entries to CloudWatch logs.
        """
        if log_group_name is not None:
            pulumi.set(__self__, "log_group_name", log_group_name)
        if log_role_arn is not None:
            pulumi.set(__self__, "log_role_arn", log_role_arn)

    @property
    @pulumi.getter(name="logGroupName")
    def log_group_name(self) -> Optional[pulumi.Input[str]]:
        """
        The Amazon CloudWatch log group to which CloudFormation sends error logging information when invoking the type's handlers.
        """
        return pulumi.get(self, "log_group_name")

    @log_group_name.setter
    def log_group_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "log_group_name", value)

    @property
    @pulumi.getter(name="logRoleArn")
    def log_role_arn(self) -> Optional[pulumi.Input[str]]:
        """
        The ARN of the role that CloudFormation should assume when sending log entries to CloudWatch logs.
        """
        return pulumi.get(self, "log_role_arn")

    @log_role_arn.setter
    def log_role_arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "log_role_arn", value)


@pulumi.input_type
class ManagedExecutionPropertiesArgs:
    def __init__(__self__, *,
                 active: Optional[pulumi.Input[bool]] = None):
        """
        Describes whether StackSets performs non-conflicting operations concurrently and queues conflicting operations.
        """
        if active is not None:
            pulumi.set(__self__, "active", active)

    @property
    @pulumi.getter
    def active(self) -> Optional[pulumi.Input[bool]]:
        return pulumi.get(self, "active")

    @active.setter
    def active(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "active", value)


@pulumi.input_type
class ResourceVersionLoggingConfigArgs:
    def __init__(__self__, *,
                 log_group_name: Optional[pulumi.Input[str]] = None,
                 log_role_arn: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] log_group_name: The Amazon CloudWatch log group to which CloudFormation sends error logging information when invoking the type's handlers.
        :param pulumi.Input[str] log_role_arn: The ARN of the role that CloudFormation should assume when sending log entries to CloudWatch logs.
        """
        if log_group_name is not None:
            pulumi.set(__self__, "log_group_name", log_group_name)
        if log_role_arn is not None:
            pulumi.set(__self__, "log_role_arn", log_role_arn)

    @property
    @pulumi.getter(name="logGroupName")
    def log_group_name(self) -> Optional[pulumi.Input[str]]:
        """
        The Amazon CloudWatch log group to which CloudFormation sends error logging information when invoking the type's handlers.
        """
        return pulumi.get(self, "log_group_name")

    @log_group_name.setter
    def log_group_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "log_group_name", value)

    @property
    @pulumi.getter(name="logRoleArn")
    def log_role_arn(self) -> Optional[pulumi.Input[str]]:
        """
        The ARN of the role that CloudFormation should assume when sending log entries to CloudWatch logs.
        """
        return pulumi.get(self, "log_role_arn")

    @log_role_arn.setter
    def log_role_arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "log_role_arn", value)


@pulumi.input_type
class StackSetAutoDeploymentArgs:
    def __init__(__self__, *,
                 enabled: Optional[pulumi.Input[bool]] = None,
                 retain_stacks_on_account_removal: Optional[pulumi.Input[bool]] = None):
        """
        :param pulumi.Input[bool] enabled: If set to true, StackSets automatically deploys additional stack instances to AWS Organizations accounts that are added to a target organization or organizational unit (OU) in the specified Regions. If an account is removed from a target organization or OU, StackSets deletes stack instances from the account in the specified Regions.
        :param pulumi.Input[bool] retain_stacks_on_account_removal: If set to true, stack resources are retained when an account is removed from a target organization or OU. If set to false, stack resources are deleted. Specify only if Enabled is set to True.
        """
        if enabled is not None:
            pulumi.set(__self__, "enabled", enabled)
        if retain_stacks_on_account_removal is not None:
            pulumi.set(__self__, "retain_stacks_on_account_removal", retain_stacks_on_account_removal)

    @property
    @pulumi.getter
    def enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        If set to true, StackSets automatically deploys additional stack instances to AWS Organizations accounts that are added to a target organization or organizational unit (OU) in the specified Regions. If an account is removed from a target organization or OU, StackSets deletes stack instances from the account in the specified Regions.
        """
        return pulumi.get(self, "enabled")

    @enabled.setter
    def enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "enabled", value)

    @property
    @pulumi.getter(name="retainStacksOnAccountRemoval")
    def retain_stacks_on_account_removal(self) -> Optional[pulumi.Input[bool]]:
        """
        If set to true, stack resources are retained when an account is removed from a target organization or OU. If set to false, stack resources are deleted. Specify only if Enabled is set to True.
        """
        return pulumi.get(self, "retain_stacks_on_account_removal")

    @retain_stacks_on_account_removal.setter
    def retain_stacks_on_account_removal(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "retain_stacks_on_account_removal", value)


@pulumi.input_type
class StackSetDeploymentTargetsArgs:
    def __init__(__self__, *,
                 accounts: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 organizational_unit_ids: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        """
         The AWS OrganizationalUnitIds or Accounts for which to create stack instances in the specified Regions.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] accounts: AWS accounts that you want to create stack instances in the specified Region(s) for.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] organizational_unit_ids: The organization root ID or organizational unit (OU) IDs to which StackSets deploys.
        """
        if accounts is not None:
            pulumi.set(__self__, "accounts", accounts)
        if organizational_unit_ids is not None:
            pulumi.set(__self__, "organizational_unit_ids", organizational_unit_ids)

    @property
    @pulumi.getter
    def accounts(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        AWS accounts that you want to create stack instances in the specified Region(s) for.
        """
        return pulumi.get(self, "accounts")

    @accounts.setter
    def accounts(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "accounts", value)

    @property
    @pulumi.getter(name="organizationalUnitIds")
    def organizational_unit_ids(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The organization root ID or organizational unit (OU) IDs to which StackSets deploys.
        """
        return pulumi.get(self, "organizational_unit_ids")

    @organizational_unit_ids.setter
    def organizational_unit_ids(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "organizational_unit_ids", value)


@pulumi.input_type
class StackSetOperationPreferencesArgs:
    def __init__(__self__, *,
                 failure_tolerance_count: Optional[pulumi.Input[int]] = None,
                 failure_tolerance_percentage: Optional[pulumi.Input[int]] = None,
                 max_concurrent_count: Optional[pulumi.Input[int]] = None,
                 max_concurrent_percentage: Optional[pulumi.Input[int]] = None,
                 region_concurrency_type: Optional[pulumi.Input['StackSetRegionConcurrencyType']] = None,
                 region_order: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        """
        The user-specified preferences for how AWS CloudFormation performs a stack set operation.
        """
        if failure_tolerance_count is not None:
            pulumi.set(__self__, "failure_tolerance_count", failure_tolerance_count)
        if failure_tolerance_percentage is not None:
            pulumi.set(__self__, "failure_tolerance_percentage", failure_tolerance_percentage)
        if max_concurrent_count is not None:
            pulumi.set(__self__, "max_concurrent_count", max_concurrent_count)
        if max_concurrent_percentage is not None:
            pulumi.set(__self__, "max_concurrent_percentage", max_concurrent_percentage)
        if region_concurrency_type is not None:
            pulumi.set(__self__, "region_concurrency_type", region_concurrency_type)
        if region_order is not None:
            pulumi.set(__self__, "region_order", region_order)

    @property
    @pulumi.getter(name="failureToleranceCount")
    def failure_tolerance_count(self) -> Optional[pulumi.Input[int]]:
        return pulumi.get(self, "failure_tolerance_count")

    @failure_tolerance_count.setter
    def failure_tolerance_count(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "failure_tolerance_count", value)

    @property
    @pulumi.getter(name="failureTolerancePercentage")
    def failure_tolerance_percentage(self) -> Optional[pulumi.Input[int]]:
        return pulumi.get(self, "failure_tolerance_percentage")

    @failure_tolerance_percentage.setter
    def failure_tolerance_percentage(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "failure_tolerance_percentage", value)

    @property
    @pulumi.getter(name="maxConcurrentCount")
    def max_concurrent_count(self) -> Optional[pulumi.Input[int]]:
        return pulumi.get(self, "max_concurrent_count")

    @max_concurrent_count.setter
    def max_concurrent_count(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "max_concurrent_count", value)

    @property
    @pulumi.getter(name="maxConcurrentPercentage")
    def max_concurrent_percentage(self) -> Optional[pulumi.Input[int]]:
        return pulumi.get(self, "max_concurrent_percentage")

    @max_concurrent_percentage.setter
    def max_concurrent_percentage(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "max_concurrent_percentage", value)

    @property
    @pulumi.getter(name="regionConcurrencyType")
    def region_concurrency_type(self) -> Optional[pulumi.Input['StackSetRegionConcurrencyType']]:
        return pulumi.get(self, "region_concurrency_type")

    @region_concurrency_type.setter
    def region_concurrency_type(self, value: Optional[pulumi.Input['StackSetRegionConcurrencyType']]):
        pulumi.set(self, "region_concurrency_type", value)

    @property
    @pulumi.getter(name="regionOrder")
    def region_order(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        return pulumi.get(self, "region_order")

    @region_order.setter
    def region_order(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "region_order", value)


@pulumi.input_type
class StackSetParameterArgs:
    def __init__(__self__, *,
                 parameter_key: pulumi.Input[str],
                 parameter_value: pulumi.Input[str]):
        """
        :param pulumi.Input[str] parameter_key: The key associated with the parameter. If you don't specify a key and value for a particular parameter, AWS CloudFormation uses the default value that is specified in your template.
        :param pulumi.Input[str] parameter_value: The input value associated with the parameter.
        """
        pulumi.set(__self__, "parameter_key", parameter_key)
        pulumi.set(__self__, "parameter_value", parameter_value)

    @property
    @pulumi.getter(name="parameterKey")
    def parameter_key(self) -> pulumi.Input[str]:
        """
        The key associated with the parameter. If you don't specify a key and value for a particular parameter, AWS CloudFormation uses the default value that is specified in your template.
        """
        return pulumi.get(self, "parameter_key")

    @parameter_key.setter
    def parameter_key(self, value: pulumi.Input[str]):
        pulumi.set(self, "parameter_key", value)

    @property
    @pulumi.getter(name="parameterValue")
    def parameter_value(self) -> pulumi.Input[str]:
        """
        The input value associated with the parameter.
        """
        return pulumi.get(self, "parameter_value")

    @parameter_value.setter
    def parameter_value(self, value: pulumi.Input[str]):
        pulumi.set(self, "parameter_value", value)


@pulumi.input_type
class StackSetStackInstancesArgs:
    def __init__(__self__, *,
                 deployment_targets: pulumi.Input['StackSetDeploymentTargetsArgs'],
                 regions: pulumi.Input[Sequence[pulumi.Input[str]]],
                 parameter_overrides: Optional[pulumi.Input[Sequence[pulumi.Input['StackSetParameterArgs']]]] = None):
        """
        Stack instances in some specific accounts and Regions.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] regions: The names of one or more Regions where you want to create stack instances using the specified AWS account(s).
        :param pulumi.Input[Sequence[pulumi.Input['StackSetParameterArgs']]] parameter_overrides: A list of stack set parameters whose values you want to override in the selected stack instances.
        """
        pulumi.set(__self__, "deployment_targets", deployment_targets)
        pulumi.set(__self__, "regions", regions)
        if parameter_overrides is not None:
            pulumi.set(__self__, "parameter_overrides", parameter_overrides)

    @property
    @pulumi.getter(name="deploymentTargets")
    def deployment_targets(self) -> pulumi.Input['StackSetDeploymentTargetsArgs']:
        return pulumi.get(self, "deployment_targets")

    @deployment_targets.setter
    def deployment_targets(self, value: pulumi.Input['StackSetDeploymentTargetsArgs']):
        pulumi.set(self, "deployment_targets", value)

    @property
    @pulumi.getter
    def regions(self) -> pulumi.Input[Sequence[pulumi.Input[str]]]:
        """
        The names of one or more Regions where you want to create stack instances using the specified AWS account(s).
        """
        return pulumi.get(self, "regions")

    @regions.setter
    def regions(self, value: pulumi.Input[Sequence[pulumi.Input[str]]]):
        pulumi.set(self, "regions", value)

    @property
    @pulumi.getter(name="parameterOverrides")
    def parameter_overrides(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['StackSetParameterArgs']]]]:
        """
        A list of stack set parameters whose values you want to override in the selected stack instances.
        """
        return pulumi.get(self, "parameter_overrides")

    @parameter_overrides.setter
    def parameter_overrides(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['StackSetParameterArgs']]]]):
        pulumi.set(self, "parameter_overrides", value)


@pulumi.input_type
class StackSetTagArgs:
    def __init__(__self__, *,
                 key: pulumi.Input[str],
                 value: pulumi.Input[str]):
        """
        Tag type enables you to specify a key-value pair that can be used to store information about an AWS CloudFormation StackSet.
        :param pulumi.Input[str] key: A string used to identify this tag. You can specify a maximum of 127 characters for a tag key.
        :param pulumi.Input[str] value: A string containing the value for this tag. You can specify a maximum of 256 characters for a tag value.
        """
        pulumi.set(__self__, "key", key)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def key(self) -> pulumi.Input[str]:
        """
        A string used to identify this tag. You can specify a maximum of 127 characters for a tag key.
        """
        return pulumi.get(self, "key")

    @key.setter
    def key(self, value: pulumi.Input[str]):
        pulumi.set(self, "key", value)

    @property
    @pulumi.getter
    def value(self) -> pulumi.Input[str]:
        """
        A string containing the value for this tag. You can specify a maximum of 256 characters for a tag value.
        """
        return pulumi.get(self, "value")

    @value.setter
    def value(self, value: pulumi.Input[str]):
        pulumi.set(self, "value", value)


@pulumi.input_type
class StackTagArgs:
    def __init__(__self__, *,
                 key: pulumi.Input[str],
                 value: pulumi.Input[str]):
        pulumi.set(__self__, "key", key)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def key(self) -> pulumi.Input[str]:
        return pulumi.get(self, "key")

    @key.setter
    def key(self, value: pulumi.Input[str]):
        pulumi.set(self, "key", value)

    @property
    @pulumi.getter
    def value(self) -> pulumi.Input[str]:
        return pulumi.get(self, "value")

    @value.setter
    def value(self, value: pulumi.Input[str]):
        pulumi.set(self, "value", value)


@pulumi.input_type
class TypeActivationLoggingConfigArgs:
    def __init__(__self__, *,
                 log_group_name: Optional[pulumi.Input[str]] = None,
                 log_role_arn: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] log_group_name: The Amazon CloudWatch log group to which CloudFormation sends error logging information when invoking the type's handlers.
        :param pulumi.Input[str] log_role_arn: The ARN of the role that CloudFormation should assume when sending log entries to CloudWatch logs.
        """
        if log_group_name is not None:
            pulumi.set(__self__, "log_group_name", log_group_name)
        if log_role_arn is not None:
            pulumi.set(__self__, "log_role_arn", log_role_arn)

    @property
    @pulumi.getter(name="logGroupName")
    def log_group_name(self) -> Optional[pulumi.Input[str]]:
        """
        The Amazon CloudWatch log group to which CloudFormation sends error logging information when invoking the type's handlers.
        """
        return pulumi.get(self, "log_group_name")

    @log_group_name.setter
    def log_group_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "log_group_name", value)

    @property
    @pulumi.getter(name="logRoleArn")
    def log_role_arn(self) -> Optional[pulumi.Input[str]]:
        """
        The ARN of the role that CloudFormation should assume when sending log entries to CloudWatch logs.
        """
        return pulumi.get(self, "log_role_arn")

    @log_role_arn.setter
    def log_role_arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "log_role_arn", value)


