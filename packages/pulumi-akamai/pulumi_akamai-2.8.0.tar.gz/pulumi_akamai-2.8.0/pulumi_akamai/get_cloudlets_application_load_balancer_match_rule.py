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
    'GetCloudletsApplicationLoadBalancerMatchRuleResult',
    'AwaitableGetCloudletsApplicationLoadBalancerMatchRuleResult',
    'get_cloudlets_application_load_balancer_match_rule',
    'get_cloudlets_application_load_balancer_match_rule_output',
]

@pulumi.output_type
class GetCloudletsApplicationLoadBalancerMatchRuleResult:
    """
    A collection of values returned by getCloudletsApplicationLoadBalancerMatchRule.
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
    def match_rules(self) -> Optional[Sequence['outputs.GetCloudletsApplicationLoadBalancerMatchRuleMatchRuleResult']]:
        return pulumi.get(self, "match_rules")


class AwaitableGetCloudletsApplicationLoadBalancerMatchRuleResult(GetCloudletsApplicationLoadBalancerMatchRuleResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetCloudletsApplicationLoadBalancerMatchRuleResult(
            id=self.id,
            json=self.json,
            match_rules=self.match_rules)


def get_cloudlets_application_load_balancer_match_rule(match_rules: Optional[Sequence[pulumi.InputType['GetCloudletsApplicationLoadBalancerMatchRuleMatchRuleArgs']]] = None,
                                                       opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetCloudletsApplicationLoadBalancerMatchRuleResult:
    """
    Every policy version specifies the match rules that govern how the Cloudlet is used. Matches specify conditions that need to be met in the incoming request.

    Use the `get_cloudlets_application_load_balancer_match_rule` data source to build a match rule JSON object for the Application Load Balancer Cloudlet.

    ## Basic usage

    This example returns the JSON-encoded rules for the Application Load Balancer Cloudlet:

    ```python
    import pulumi
    import pulumi_akamai as akamai

    example = akamai.get_cloudlets_application_load_balancer_match_rule(match_rules=[akamai.GetCloudletsApplicationLoadBalancerMatchRuleMatchRuleArgs(
        end=1645037845,
        forward_settings=[akamai.GetCloudletsApplicationLoadBalancerMatchRuleMatchRuleForwardSettingArgs(
            origin_id="alb_test_1",
        )],
        match_url="example.com",
        matches=[akamai.GetCloudletsApplicationLoadBalancerMatchRuleMatchRuleMatchArgs(
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
        start=1644865045,
    )])
    ```

    ## Attributes reference

    This data source returns these attributes:

    * `type` - The type of Cloudlet the rule is for.
    * `json` - A `match_rules` JSON structure generated from the API schema that defines the rules for this policy.


    :param Sequence[pulumi.InputType['GetCloudletsApplicationLoadBalancerMatchRuleMatchRuleArgs']] match_rules: - (Optional) A list of Cloudlet-specific match rules for a policy.
    """
    __args__ = dict()
    __args__['matchRules'] = match_rules
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('akamai:index/getCloudletsApplicationLoadBalancerMatchRule:getCloudletsApplicationLoadBalancerMatchRule', __args__, opts=opts, typ=GetCloudletsApplicationLoadBalancerMatchRuleResult).value

    return AwaitableGetCloudletsApplicationLoadBalancerMatchRuleResult(
        id=__ret__.id,
        json=__ret__.json,
        match_rules=__ret__.match_rules)


@_utilities.lift_output_func(get_cloudlets_application_load_balancer_match_rule)
def get_cloudlets_application_load_balancer_match_rule_output(match_rules: Optional[pulumi.Input[Optional[Sequence[pulumi.InputType['GetCloudletsApplicationLoadBalancerMatchRuleMatchRuleArgs']]]]] = None,
                                                              opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetCloudletsApplicationLoadBalancerMatchRuleResult]:
    """
    Every policy version specifies the match rules that govern how the Cloudlet is used. Matches specify conditions that need to be met in the incoming request.

    Use the `get_cloudlets_application_load_balancer_match_rule` data source to build a match rule JSON object for the Application Load Balancer Cloudlet.

    ## Basic usage

    This example returns the JSON-encoded rules for the Application Load Balancer Cloudlet:

    ```python
    import pulumi
    import pulumi_akamai as akamai

    example = akamai.get_cloudlets_application_load_balancer_match_rule(match_rules=[akamai.GetCloudletsApplicationLoadBalancerMatchRuleMatchRuleArgs(
        end=1645037845,
        forward_settings=[akamai.GetCloudletsApplicationLoadBalancerMatchRuleMatchRuleForwardSettingArgs(
            origin_id="alb_test_1",
        )],
        match_url="example.com",
        matches=[akamai.GetCloudletsApplicationLoadBalancerMatchRuleMatchRuleMatchArgs(
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
        start=1644865045,
    )])
    ```

    ## Attributes reference

    This data source returns these attributes:

    * `type` - The type of Cloudlet the rule is for.
    * `json` - A `match_rules` JSON structure generated from the API schema that defines the rules for this policy.


    :param Sequence[pulumi.InputType['GetCloudletsApplicationLoadBalancerMatchRuleMatchRuleArgs']] match_rules: - (Optional) A list of Cloudlet-specific match rules for a policy.
    """
    ...
