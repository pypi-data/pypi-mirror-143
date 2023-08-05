# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities
from . import outputs
from ._inputs import *

__all__ = [
    'GetCloudletsEdgeRedirectorMatchRuleResult',
    'AwaitableGetCloudletsEdgeRedirectorMatchRuleResult',
    'get_cloudlets_edge_redirector_match_rule',
    'get_cloudlets_edge_redirector_match_rule_output',
]

@pulumi.output_type
class GetCloudletsEdgeRedirectorMatchRuleResult:
    """
    A collection of values returned by getCloudletsEdgeRedirectorMatchRule.
    """
    def __init__(__self__, id=None, json=None, match_rules=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if json and not isinstance(json, str):
            raise TypeError("Expected argument 'json' to be a str")
        pulumi.set(__self__, "json", json)
        if match_rules and not isinstance(match_rules, list):
            raise TypeError("Expected argument 'match_rules' to be a list")
        pulumi.set(__self__, "match_rules", match_rules)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def json(self) -> str:
        return pulumi.get(self, "json")

    @property
    @pulumi.getter(name="matchRules")
    def match_rules(self) -> Optional[Sequence['outputs.GetCloudletsEdgeRedirectorMatchRuleMatchRuleResult']]:
        return pulumi.get(self, "match_rules")


class AwaitableGetCloudletsEdgeRedirectorMatchRuleResult(GetCloudletsEdgeRedirectorMatchRuleResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetCloudletsEdgeRedirectorMatchRuleResult(
            id=self.id,
            json=self.json,
            match_rules=self.match_rules)


def get_cloudlets_edge_redirector_match_rule(match_rules: Optional[Sequence[pulumi.InputType['GetCloudletsEdgeRedirectorMatchRuleMatchRuleArgs']]] = None,
                                             opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetCloudletsEdgeRedirectorMatchRuleResult:
    """
    Every policy version specifies the match rules that govern how the Cloudlet is used. Matches specify conditions that need to be met in the incoming request.

    Use the `get_cloudlets_edge_redirector_match_rule` data source to build a match rule JSON object for the Edge Redirector Cloudlet.

    ## Basic usage

    This example returns the JSON-encoded rules for the Edge Redirector Cloudlet:

    ```python
    import pulumi
    import pulumi_akamai as akamai

    example = akamai.get_cloudlets_edge_redirector_match_rule(match_rules=[akamai.GetCloudletsEdgeRedirectorMatchRuleMatchRuleArgs(
        end=1645037845,
        match_url="example.com",
        matches=[akamai.GetCloudletsEdgeRedirectorMatchRuleMatchRuleMatchArgs(
            case_sensitive=False,
            match_operator="equals",
            match_type="method",
            negate=False,
            object_match_value=[{
                "type": "simple",
                "value": ["GET"],
            }],
        )],
        name="rule",
        redirect_url="https://www.example.com",
        start=1644865045,
        status_code=301,
        use_incoming_query_string=False,
        use_relative_url="none",
    )])
    ```

    ## Attributes reference

    This data source returns these attributes:

    * `type` - The type of Cloudlet the rule is for.
    * `json` - A `match_rules` JSON structure generated from the API schema that defines the rules for this policy.


    :param Sequence[pulumi.InputType['GetCloudletsEdgeRedirectorMatchRuleMatchRuleArgs']] match_rules: - (Optional) A list of Cloudlet-specific match rules for a policy.
    """
    __args__ = dict()
    __args__['matchRules'] = match_rules
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('akamai:index/getCloudletsEdgeRedirectorMatchRule:getCloudletsEdgeRedirectorMatchRule', __args__, opts=opts, typ=GetCloudletsEdgeRedirectorMatchRuleResult).value

    return AwaitableGetCloudletsEdgeRedirectorMatchRuleResult(
        id=__ret__.id,
        json=__ret__.json,
        match_rules=__ret__.match_rules)


@_utilities.lift_output_func(get_cloudlets_edge_redirector_match_rule)
def get_cloudlets_edge_redirector_match_rule_output(match_rules: Optional[pulumi.Input[Optional[Sequence[pulumi.InputType['GetCloudletsEdgeRedirectorMatchRuleMatchRuleArgs']]]]] = None,
                                                    opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetCloudletsEdgeRedirectorMatchRuleResult]:
    """
    Every policy version specifies the match rules that govern how the Cloudlet is used. Matches specify conditions that need to be met in the incoming request.

    Use the `get_cloudlets_edge_redirector_match_rule` data source to build a match rule JSON object for the Edge Redirector Cloudlet.

    ## Basic usage

    This example returns the JSON-encoded rules for the Edge Redirector Cloudlet:

    ```python
    import pulumi
    import pulumi_akamai as akamai

    example = akamai.get_cloudlets_edge_redirector_match_rule(match_rules=[akamai.GetCloudletsEdgeRedirectorMatchRuleMatchRuleArgs(
        end=1645037845,
        match_url="example.com",
        matches=[akamai.GetCloudletsEdgeRedirectorMatchRuleMatchRuleMatchArgs(
            case_sensitive=False,
            match_operator="equals",
            match_type="method",
            negate=False,
            object_match_value=[{
                "type": "simple",
                "value": ["GET"],
            }],
        )],
        name="rule",
        redirect_url="https://www.example.com",
        start=1644865045,
        status_code=301,
        use_incoming_query_string=False,
        use_relative_url="none",
    )])
    ```

    ## Attributes reference

    This data source returns these attributes:

    * `type` - The type of Cloudlet the rule is for.
    * `json` - A `match_rules` JSON structure generated from the API schema that defines the rules for this policy.


    :param Sequence[pulumi.InputType['GetCloudletsEdgeRedirectorMatchRuleMatchRuleArgs']] match_rules: - (Optional) A list of Cloudlet-specific match rules for a policy.
    """
    ...
