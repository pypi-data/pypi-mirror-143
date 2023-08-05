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
    'GetCloudletsAudienceSegmentationMatchRuleResult',
    'AwaitableGetCloudletsAudienceSegmentationMatchRuleResult',
    'get_cloudlets_audience_segmentation_match_rule',
    'get_cloudlets_audience_segmentation_match_rule_output',
]

@pulumi.output_type
class GetCloudletsAudienceSegmentationMatchRuleResult:
    """
    A collection of values returned by getCloudletsAudienceSegmentationMatchRule.
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
    def match_rules(self) -> Optional[Sequence['outputs.GetCloudletsAudienceSegmentationMatchRuleMatchRuleResult']]:
        return pulumi.get(self, "match_rules")


class AwaitableGetCloudletsAudienceSegmentationMatchRuleResult(GetCloudletsAudienceSegmentationMatchRuleResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetCloudletsAudienceSegmentationMatchRuleResult(
            id=self.id,
            json=self.json,
            match_rules=self.match_rules)


def get_cloudlets_audience_segmentation_match_rule(match_rules: Optional[Sequence[pulumi.InputType['GetCloudletsAudienceSegmentationMatchRuleMatchRuleArgs']]] = None,
                                                   opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetCloudletsAudienceSegmentationMatchRuleResult:
    """
    Every policy version specifies the match rules that govern how the Cloudlet is used. Matches specify conditions that need to be met in the incoming request.

    Use the `get_cloudlets_audience_segmentation_match_rule` data source to build a match rule JSON object for the Audience Segmentation Cloudlet.

    ## Basic usage

    This example returns the JSON-encoded rules for the Audience Segmentation Cloudlet:

    ```python
    import pulumi
    import pulumi_akamai as akamai

    example = akamai.get_cloudlets_audience_segmentation_match_rule(match_rules=[akamai.GetCloudletsAudienceSegmentationMatchRuleMatchRuleArgs(
        forward_settings=akamai.GetCloudletsAudienceSegmentationMatchRuleMatchRuleForwardSettingsArgs(
            origin_id="123",
            path_and_qs="/test",
            use_incoming_query_string=True,
        ),
        matches=[akamai.GetCloudletsAudienceSegmentationMatchRuleMatchRuleMatchArgs(
            match_operator="contains",
            match_type="header",
            object_match_value=[{
                "name": "cookie",
                "options": {
                    "value": ["abcd"],
                },
                "type": "object",
            }],
        )],
        name="rule",
    )])
    ```

    ## Attributes reference

    This data source returns these attributes:

    * `type` - The type of Cloudlet the rule is for.
    * `json` - A `match_rules` JSON structure generated from the API schema that defines the rules for this policy.


    :param Sequence[pulumi.InputType['GetCloudletsAudienceSegmentationMatchRuleMatchRuleArgs']] match_rules: - (Optional) A list of Cloudlet-specific match rules for a policy.
    """
    __args__ = dict()
    __args__['matchRules'] = match_rules
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('akamai:index/getCloudletsAudienceSegmentationMatchRule:getCloudletsAudienceSegmentationMatchRule', __args__, opts=opts, typ=GetCloudletsAudienceSegmentationMatchRuleResult).value

    return AwaitableGetCloudletsAudienceSegmentationMatchRuleResult(
        id=__ret__.id,
        json=__ret__.json,
        match_rules=__ret__.match_rules)


@_utilities.lift_output_func(get_cloudlets_audience_segmentation_match_rule)
def get_cloudlets_audience_segmentation_match_rule_output(match_rules: Optional[pulumi.Input[Optional[Sequence[pulumi.InputType['GetCloudletsAudienceSegmentationMatchRuleMatchRuleArgs']]]]] = None,
                                                          opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetCloudletsAudienceSegmentationMatchRuleResult]:
    """
    Every policy version specifies the match rules that govern how the Cloudlet is used. Matches specify conditions that need to be met in the incoming request.

    Use the `get_cloudlets_audience_segmentation_match_rule` data source to build a match rule JSON object for the Audience Segmentation Cloudlet.

    ## Basic usage

    This example returns the JSON-encoded rules for the Audience Segmentation Cloudlet:

    ```python
    import pulumi
    import pulumi_akamai as akamai

    example = akamai.get_cloudlets_audience_segmentation_match_rule(match_rules=[akamai.GetCloudletsAudienceSegmentationMatchRuleMatchRuleArgs(
        forward_settings=akamai.GetCloudletsAudienceSegmentationMatchRuleMatchRuleForwardSettingsArgs(
            origin_id="123",
            path_and_qs="/test",
            use_incoming_query_string=True,
        ),
        matches=[akamai.GetCloudletsAudienceSegmentationMatchRuleMatchRuleMatchArgs(
            match_operator="contains",
            match_type="header",
            object_match_value=[{
                "name": "cookie",
                "options": {
                    "value": ["abcd"],
                },
                "type": "object",
            }],
        )],
        name="rule",
    )])
    ```

    ## Attributes reference

    This data source returns these attributes:

    * `type` - The type of Cloudlet the rule is for.
    * `json` - A `match_rules` JSON structure generated from the API schema that defines the rules for this policy.


    :param Sequence[pulumi.InputType['GetCloudletsAudienceSegmentationMatchRuleMatchRuleArgs']] match_rules: - (Optional) A list of Cloudlet-specific match rules for a policy.
    """
    ...
