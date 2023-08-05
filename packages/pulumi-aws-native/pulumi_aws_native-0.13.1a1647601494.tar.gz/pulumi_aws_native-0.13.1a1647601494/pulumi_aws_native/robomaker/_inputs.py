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
    'FleetTagsArgs',
    'RobotApplicationRobotSoftwareSuiteArgs',
    'RobotApplicationSourceConfigArgs',
    'RobotApplicationTagsArgs',
    'RobotTagsArgs',
    'SimulationApplicationRenderingEngineArgs',
    'SimulationApplicationRobotSoftwareSuiteArgs',
    'SimulationApplicationSimulationSoftwareSuiteArgs',
    'SimulationApplicationSourceConfigArgs',
    'SimulationApplicationTagsArgs',
]

@pulumi.input_type
class FleetTagsArgs:
    def __init__(__self__):
        """
        A key-value pair to associate with a resource.
        """
        pass


@pulumi.input_type
class RobotApplicationRobotSoftwareSuiteArgs:
    def __init__(__self__, *,
                 name: pulumi.Input['RobotApplicationRobotSoftwareSuiteName'],
                 version: Optional[pulumi.Input['RobotApplicationRobotSoftwareSuiteVersion']] = None):
        """
        The robot software suite used by the robot application.
        :param pulumi.Input['RobotApplicationRobotSoftwareSuiteName'] name: The name of robot software suite.
        :param pulumi.Input['RobotApplicationRobotSoftwareSuiteVersion'] version: The version of robot software suite.
        """
        pulumi.set(__self__, "name", name)
        if version is not None:
            pulumi.set(__self__, "version", version)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input['RobotApplicationRobotSoftwareSuiteName']:
        """
        The name of robot software suite.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: pulumi.Input['RobotApplicationRobotSoftwareSuiteName']):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def version(self) -> Optional[pulumi.Input['RobotApplicationRobotSoftwareSuiteVersion']]:
        """
        The version of robot software suite.
        """
        return pulumi.get(self, "version")

    @version.setter
    def version(self, value: Optional[pulumi.Input['RobotApplicationRobotSoftwareSuiteVersion']]):
        pulumi.set(self, "version", value)


@pulumi.input_type
class RobotApplicationSourceConfigArgs:
    def __init__(__self__, *,
                 architecture: pulumi.Input['RobotApplicationSourceConfigArchitecture'],
                 s3_bucket: pulumi.Input[str],
                 s3_key: pulumi.Input[str]):
        """
        :param pulumi.Input['RobotApplicationSourceConfigArchitecture'] architecture: The architecture of robot application.
        :param pulumi.Input[str] s3_bucket: The Arn of the S3Bucket that stores the robot application source.
        :param pulumi.Input[str] s3_key: The s3 key of robot application source.
        """
        pulumi.set(__self__, "architecture", architecture)
        pulumi.set(__self__, "s3_bucket", s3_bucket)
        pulumi.set(__self__, "s3_key", s3_key)

    @property
    @pulumi.getter
    def architecture(self) -> pulumi.Input['RobotApplicationSourceConfigArchitecture']:
        """
        The architecture of robot application.
        """
        return pulumi.get(self, "architecture")

    @architecture.setter
    def architecture(self, value: pulumi.Input['RobotApplicationSourceConfigArchitecture']):
        pulumi.set(self, "architecture", value)

    @property
    @pulumi.getter(name="s3Bucket")
    def s3_bucket(self) -> pulumi.Input[str]:
        """
        The Arn of the S3Bucket that stores the robot application source.
        """
        return pulumi.get(self, "s3_bucket")

    @s3_bucket.setter
    def s3_bucket(self, value: pulumi.Input[str]):
        pulumi.set(self, "s3_bucket", value)

    @property
    @pulumi.getter(name="s3Key")
    def s3_key(self) -> pulumi.Input[str]:
        """
        The s3 key of robot application source.
        """
        return pulumi.get(self, "s3_key")

    @s3_key.setter
    def s3_key(self, value: pulumi.Input[str]):
        pulumi.set(self, "s3_key", value)


@pulumi.input_type
class RobotApplicationTagsArgs:
    def __init__(__self__):
        """
        A key-value pair to associate with a resource.
        """
        pass


@pulumi.input_type
class RobotTagsArgs:
    def __init__(__self__):
        """
        A key-value pair to associate with a resource.
        """
        pass


@pulumi.input_type
class SimulationApplicationRenderingEngineArgs:
    def __init__(__self__, *,
                 name: pulumi.Input['SimulationApplicationRenderingEngineName'],
                 version: pulumi.Input[str]):
        """
        Information about a rendering engine.
        :param pulumi.Input['SimulationApplicationRenderingEngineName'] name: The name of the rendering engine.
        :param pulumi.Input[str] version: The version of the rendering engine.
        """
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "version", version)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input['SimulationApplicationRenderingEngineName']:
        """
        The name of the rendering engine.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: pulumi.Input['SimulationApplicationRenderingEngineName']):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def version(self) -> pulumi.Input[str]:
        """
        The version of the rendering engine.
        """
        return pulumi.get(self, "version")

    @version.setter
    def version(self, value: pulumi.Input[str]):
        pulumi.set(self, "version", value)


@pulumi.input_type
class SimulationApplicationRobotSoftwareSuiteArgs:
    def __init__(__self__, *,
                 name: pulumi.Input['SimulationApplicationRobotSoftwareSuiteName'],
                 version: Optional[pulumi.Input['SimulationApplicationRobotSoftwareSuiteVersion']] = None):
        """
        Information about a robot software suite.
        :param pulumi.Input['SimulationApplicationRobotSoftwareSuiteName'] name: The name of the robot software suite.
        :param pulumi.Input['SimulationApplicationRobotSoftwareSuiteVersion'] version: The version of the robot software suite.
        """
        pulumi.set(__self__, "name", name)
        if version is not None:
            pulumi.set(__self__, "version", version)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input['SimulationApplicationRobotSoftwareSuiteName']:
        """
        The name of the robot software suite.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: pulumi.Input['SimulationApplicationRobotSoftwareSuiteName']):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def version(self) -> Optional[pulumi.Input['SimulationApplicationRobotSoftwareSuiteVersion']]:
        """
        The version of the robot software suite.
        """
        return pulumi.get(self, "version")

    @version.setter
    def version(self, value: Optional[pulumi.Input['SimulationApplicationRobotSoftwareSuiteVersion']]):
        pulumi.set(self, "version", value)


@pulumi.input_type
class SimulationApplicationSimulationSoftwareSuiteArgs:
    def __init__(__self__, *,
                 name: pulumi.Input['SimulationApplicationSimulationSoftwareSuiteName'],
                 version: Optional[pulumi.Input['SimulationApplicationSimulationSoftwareSuiteVersion']] = None):
        """
        Information about a simulation software suite.
        :param pulumi.Input['SimulationApplicationSimulationSoftwareSuiteName'] name: The name of the simulation software suite.
        :param pulumi.Input['SimulationApplicationSimulationSoftwareSuiteVersion'] version: The version of the simulation software suite.
        """
        pulumi.set(__self__, "name", name)
        if version is not None:
            pulumi.set(__self__, "version", version)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input['SimulationApplicationSimulationSoftwareSuiteName']:
        """
        The name of the simulation software suite.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: pulumi.Input['SimulationApplicationSimulationSoftwareSuiteName']):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def version(self) -> Optional[pulumi.Input['SimulationApplicationSimulationSoftwareSuiteVersion']]:
        """
        The version of the simulation software suite.
        """
        return pulumi.get(self, "version")

    @version.setter
    def version(self, value: Optional[pulumi.Input['SimulationApplicationSimulationSoftwareSuiteVersion']]):
        pulumi.set(self, "version", value)


@pulumi.input_type
class SimulationApplicationSourceConfigArgs:
    def __init__(__self__, *,
                 architecture: pulumi.Input['SimulationApplicationSourceConfigArchitecture'],
                 s3_bucket: pulumi.Input[str],
                 s3_key: pulumi.Input[str]):
        """
        Information about a source configuration.
        :param pulumi.Input['SimulationApplicationSourceConfigArchitecture'] architecture: The target processor architecture for the application.
        :param pulumi.Input[str] s3_bucket: The Amazon S3 bucket name.
        :param pulumi.Input[str] s3_key: The s3 object key.
        """
        pulumi.set(__self__, "architecture", architecture)
        pulumi.set(__self__, "s3_bucket", s3_bucket)
        pulumi.set(__self__, "s3_key", s3_key)

    @property
    @pulumi.getter
    def architecture(self) -> pulumi.Input['SimulationApplicationSourceConfigArchitecture']:
        """
        The target processor architecture for the application.
        """
        return pulumi.get(self, "architecture")

    @architecture.setter
    def architecture(self, value: pulumi.Input['SimulationApplicationSourceConfigArchitecture']):
        pulumi.set(self, "architecture", value)

    @property
    @pulumi.getter(name="s3Bucket")
    def s3_bucket(self) -> pulumi.Input[str]:
        """
        The Amazon S3 bucket name.
        """
        return pulumi.get(self, "s3_bucket")

    @s3_bucket.setter
    def s3_bucket(self, value: pulumi.Input[str]):
        pulumi.set(self, "s3_bucket", value)

    @property
    @pulumi.getter(name="s3Key")
    def s3_key(self) -> pulumi.Input[str]:
        """
        The s3 object key.
        """
        return pulumi.get(self, "s3_key")

    @s3_key.setter
    def s3_key(self, value: pulumi.Input[str]):
        pulumi.set(self, "s3_key", value)


@pulumi.input_type
class SimulationApplicationTagsArgs:
    def __init__(__self__):
        """
        A key-value pair to associate with a resource.
        """
        pass


