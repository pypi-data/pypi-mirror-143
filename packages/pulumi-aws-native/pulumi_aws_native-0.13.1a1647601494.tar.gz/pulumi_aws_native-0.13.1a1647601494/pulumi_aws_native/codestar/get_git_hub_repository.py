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
    'GetGitHubRepositoryResult',
    'AwaitableGetGitHubRepositoryResult',
    'get_git_hub_repository',
    'get_git_hub_repository_output',
]

@pulumi.output_type
class GetGitHubRepositoryResult:
    def __init__(__self__, code=None, connection_arn=None, enable_issues=None, id=None, is_private=None, repository_access_token=None, repository_description=None, repository_name=None, repository_owner=None):
        if code and not isinstance(code, dict):
            raise TypeError("Expected argument 'code' to be a dict")
        pulumi.set(__self__, "code", code)
        if connection_arn and not isinstance(connection_arn, str):
            raise TypeError("Expected argument 'connection_arn' to be a str")
        pulumi.set(__self__, "connection_arn", connection_arn)
        if enable_issues and not isinstance(enable_issues, bool):
            raise TypeError("Expected argument 'enable_issues' to be a bool")
        pulumi.set(__self__, "enable_issues", enable_issues)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if is_private and not isinstance(is_private, bool):
            raise TypeError("Expected argument 'is_private' to be a bool")
        pulumi.set(__self__, "is_private", is_private)
        if repository_access_token and not isinstance(repository_access_token, str):
            raise TypeError("Expected argument 'repository_access_token' to be a str")
        pulumi.set(__self__, "repository_access_token", repository_access_token)
        if repository_description and not isinstance(repository_description, str):
            raise TypeError("Expected argument 'repository_description' to be a str")
        pulumi.set(__self__, "repository_description", repository_description)
        if repository_name and not isinstance(repository_name, str):
            raise TypeError("Expected argument 'repository_name' to be a str")
        pulumi.set(__self__, "repository_name", repository_name)
        if repository_owner and not isinstance(repository_owner, str):
            raise TypeError("Expected argument 'repository_owner' to be a str")
        pulumi.set(__self__, "repository_owner", repository_owner)

    @property
    @pulumi.getter
    def code(self) -> Optional['outputs.GitHubRepositoryCode']:
        return pulumi.get(self, "code")

    @property
    @pulumi.getter(name="connectionArn")
    def connection_arn(self) -> Optional[str]:
        return pulumi.get(self, "connection_arn")

    @property
    @pulumi.getter(name="enableIssues")
    def enable_issues(self) -> Optional[bool]:
        return pulumi.get(self, "enable_issues")

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="isPrivate")
    def is_private(self) -> Optional[bool]:
        return pulumi.get(self, "is_private")

    @property
    @pulumi.getter(name="repositoryAccessToken")
    def repository_access_token(self) -> Optional[str]:
        return pulumi.get(self, "repository_access_token")

    @property
    @pulumi.getter(name="repositoryDescription")
    def repository_description(self) -> Optional[str]:
        return pulumi.get(self, "repository_description")

    @property
    @pulumi.getter(name="repositoryName")
    def repository_name(self) -> Optional[str]:
        return pulumi.get(self, "repository_name")

    @property
    @pulumi.getter(name="repositoryOwner")
    def repository_owner(self) -> Optional[str]:
        return pulumi.get(self, "repository_owner")


class AwaitableGetGitHubRepositoryResult(GetGitHubRepositoryResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetGitHubRepositoryResult(
            code=self.code,
            connection_arn=self.connection_arn,
            enable_issues=self.enable_issues,
            id=self.id,
            is_private=self.is_private,
            repository_access_token=self.repository_access_token,
            repository_description=self.repository_description,
            repository_name=self.repository_name,
            repository_owner=self.repository_owner)


def get_git_hub_repository(id: Optional[str] = None,
                           opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetGitHubRepositoryResult:
    """
    Resource Type definition for AWS::CodeStar::GitHubRepository
    """
    __args__ = dict()
    __args__['id'] = id
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('aws-native:codestar:getGitHubRepository', __args__, opts=opts, typ=GetGitHubRepositoryResult).value

    return AwaitableGetGitHubRepositoryResult(
        code=__ret__.code,
        connection_arn=__ret__.connection_arn,
        enable_issues=__ret__.enable_issues,
        id=__ret__.id,
        is_private=__ret__.is_private,
        repository_access_token=__ret__.repository_access_token,
        repository_description=__ret__.repository_description,
        repository_name=__ret__.repository_name,
        repository_owner=__ret__.repository_owner)


@_utilities.lift_output_func(get_git_hub_repository)
def get_git_hub_repository_output(id: Optional[pulumi.Input[str]] = None,
                                  opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetGitHubRepositoryResult]:
    """
    Resource Type definition for AWS::CodeStar::GitHubRepository
    """
    ...
