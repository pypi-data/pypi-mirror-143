# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = [
    'GetRuleGroupResult',
    'AwaitableGetRuleGroupResult',
    'get_rule_group',
    'get_rule_group_output',
]

@pulumi.output_type
class GetRuleGroupResult:
    """
    A collection of values returned by getRuleGroup.
    """
    def __init__(__self__, arn=None, description=None, id=None, name=None, scope=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if scope and not isinstance(scope, str):
            raise TypeError("Expected argument 'scope' to be a str")
        pulumi.set(__self__, "scope", scope)

    @property
    @pulumi.getter
    def arn(self) -> str:
        """
        The Amazon Resource Name (ARN) of the entity.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter
    def description(self) -> str:
        """
        The description of the rule group that helps with identification.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def name(self) -> str:
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def scope(self) -> str:
        return pulumi.get(self, "scope")


class AwaitableGetRuleGroupResult(GetRuleGroupResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetRuleGroupResult(
            arn=self.arn,
            description=self.description,
            id=self.id,
            name=self.name,
            scope=self.scope)


def get_rule_group(name: Optional[str] = None,
                   scope: Optional[str] = None,
                   opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetRuleGroupResult:
    """
    Retrieves the summary of a WAFv2 Rule Group.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.wafv2.get_rule_group(name="some-rule-group",
        scope="REGIONAL")
    ```


    :param str name: The name of the WAFv2 Rule Group.
    :param str scope: Specifies whether this is for an AWS CloudFront distribution or for a regional application. Valid values are `CLOUDFRONT` or `REGIONAL`. To work with CloudFront, you must also specify the region `us-east-1` (N. Virginia) on the AWS provider.
    """
    __args__ = dict()
    __args__['name'] = name
    __args__['scope'] = scope
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('aws:wafv2/getRuleGroup:getRuleGroup', __args__, opts=opts, typ=GetRuleGroupResult).value

    return AwaitableGetRuleGroupResult(
        arn=__ret__.arn,
        description=__ret__.description,
        id=__ret__.id,
        name=__ret__.name,
        scope=__ret__.scope)


@_utilities.lift_output_func(get_rule_group)
def get_rule_group_output(name: Optional[pulumi.Input[str]] = None,
                          scope: Optional[pulumi.Input[str]] = None,
                          opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetRuleGroupResult]:
    """
    Retrieves the summary of a WAFv2 Rule Group.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.wafv2.get_rule_group(name="some-rule-group",
        scope="REGIONAL")
    ```


    :param str name: The name of the WAFv2 Rule Group.
    :param str scope: Specifies whether this is for an AWS CloudFront distribution or for a regional application. Valid values are `CLOUDFRONT` or `REGIONAL`. To work with CloudFront, you must also specify the region `us-east-1` (N. Virginia) on the AWS provider.
    """
    ...
