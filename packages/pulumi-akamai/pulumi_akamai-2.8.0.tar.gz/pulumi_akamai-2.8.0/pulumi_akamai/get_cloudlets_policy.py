# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities
from . import outputs

__all__ = [
    'GetCloudletsPolicyResult',
    'AwaitableGetCloudletsPolicyResult',
    'get_cloudlets_policy',
    'get_cloudlets_policy_output',
]

@pulumi.output_type
class GetCloudletsPolicyResult:
    """
    A collection of values returned by getCloudletsPolicy.
    """
    def __init__(__self__, activations=None, api_version=None, cloudlet_code=None, cloudlet_id=None, description=None, group_id=None, id=None, match_rule_format=None, match_rules=None, name=None, policy_id=None, revision_id=None, rules_locked=None, version=None, version_description=None, warnings=None):
        if activations and not isinstance(activations, list):
            raise TypeError("Expected argument 'activations' to be a list")
        pulumi.set(__self__, "activations", activations)
        if api_version and not isinstance(api_version, str):
            raise TypeError("Expected argument 'api_version' to be a str")
        pulumi.set(__self__, "api_version", api_version)
        if cloudlet_code and not isinstance(cloudlet_code, str):
            raise TypeError("Expected argument 'cloudlet_code' to be a str")
        pulumi.set(__self__, "cloudlet_code", cloudlet_code)
        if cloudlet_id and not isinstance(cloudlet_id, int):
            raise TypeError("Expected argument 'cloudlet_id' to be a int")
        pulumi.set(__self__, "cloudlet_id", cloudlet_id)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if group_id and not isinstance(group_id, int):
            raise TypeError("Expected argument 'group_id' to be a int")
        pulumi.set(__self__, "group_id", group_id)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if match_rule_format and not isinstance(match_rule_format, str):
            raise TypeError("Expected argument 'match_rule_format' to be a str")
        pulumi.set(__self__, "match_rule_format", match_rule_format)
        if match_rules and not isinstance(match_rules, str):
            raise TypeError("Expected argument 'match_rules' to be a str")
        pulumi.set(__self__, "match_rules", match_rules)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if policy_id and not isinstance(policy_id, int):
            raise TypeError("Expected argument 'policy_id' to be a int")
        pulumi.set(__self__, "policy_id", policy_id)
        if revision_id and not isinstance(revision_id, int):
            raise TypeError("Expected argument 'revision_id' to be a int")
        pulumi.set(__self__, "revision_id", revision_id)
        if rules_locked and not isinstance(rules_locked, bool):
            raise TypeError("Expected argument 'rules_locked' to be a bool")
        pulumi.set(__self__, "rules_locked", rules_locked)
        if version and not isinstance(version, int):
            raise TypeError("Expected argument 'version' to be a int")
        pulumi.set(__self__, "version", version)
        if version_description and not isinstance(version_description, str):
            raise TypeError("Expected argument 'version_description' to be a str")
        pulumi.set(__self__, "version_description", version_description)
        if warnings and not isinstance(warnings, str):
            raise TypeError("Expected argument 'warnings' to be a str")
        pulumi.set(__self__, "warnings", warnings)

    @property
    @pulumi.getter
    def activations(self) -> Sequence['outputs.GetCloudletsPolicyActivationResult']:
        return pulumi.get(self, "activations")

    @property
    @pulumi.getter(name="apiVersion")
    def api_version(self) -> str:
        return pulumi.get(self, "api_version")

    @property
    @pulumi.getter(name="cloudletCode")
    def cloudlet_code(self) -> str:
        return pulumi.get(self, "cloudlet_code")

    @property
    @pulumi.getter(name="cloudletId")
    def cloudlet_id(self) -> int:
        return pulumi.get(self, "cloudlet_id")

    @property
    @pulumi.getter
    def description(self) -> str:
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="groupId")
    def group_id(self) -> int:
        return pulumi.get(self, "group_id")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="matchRuleFormat")
    def match_rule_format(self) -> str:
        return pulumi.get(self, "match_rule_format")

    @property
    @pulumi.getter(name="matchRules")
    def match_rules(self) -> str:
        return pulumi.get(self, "match_rules")

    @property
    @pulumi.getter
    def name(self) -> str:
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="policyId")
    def policy_id(self) -> int:
        return pulumi.get(self, "policy_id")

    @property
    @pulumi.getter(name="revisionId")
    def revision_id(self) -> int:
        return pulumi.get(self, "revision_id")

    @property
    @pulumi.getter(name="rulesLocked")
    def rules_locked(self) -> bool:
        return pulumi.get(self, "rules_locked")

    @property
    @pulumi.getter
    def version(self) -> Optional[int]:
        return pulumi.get(self, "version")

    @property
    @pulumi.getter(name="versionDescription")
    def version_description(self) -> str:
        return pulumi.get(self, "version_description")

    @property
    @pulumi.getter
    def warnings(self) -> str:
        return pulumi.get(self, "warnings")


class AwaitableGetCloudletsPolicyResult(GetCloudletsPolicyResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetCloudletsPolicyResult(
            activations=self.activations,
            api_version=self.api_version,
            cloudlet_code=self.cloudlet_code,
            cloudlet_id=self.cloudlet_id,
            description=self.description,
            group_id=self.group_id,
            id=self.id,
            match_rule_format=self.match_rule_format,
            match_rules=self.match_rules,
            name=self.name,
            policy_id=self.policy_id,
            revision_id=self.revision_id,
            rules_locked=self.rules_locked,
            version=self.version,
            version_description=self.version_description,
            warnings=self.warnings)


def get_cloudlets_policy(policy_id: Optional[int] = None,
                         version: Optional[int] = None,
                         opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetCloudletsPolicyResult:
    """
    Use the `CloudletsPolicy` data source to list details about a policy with and its specified version, or latest if not specified.

    ## Basic usage

    This example returns the policy details based on the policy ID and optionally, a version:

    ```python
    import pulumi
    import pulumi_akamai as akamai

    example = akamai.get_cloudlets_policy(policy_id=1234,
        version=1)
    ```

    ## Attributes reference

    This data source returns these attributes:

    * `group_id` - Defines the group association for the policy. You must have edit privileges for the group.
    * `name` - The unique name of the policy.
    * `api_version` - The specific version of the Cloudlets API.
    * `cloudlet_id` - A unique identifier that corresponds to a Cloudlets policy type. Enter `0` for Edge Redirector, `1` for Visitor Prioritization, `3` for Forward Rewrite, `5` for API Prioritization, `7` for Phased Release, or `9` for Application Load Balancer.
    * `cloudlet_code` - The two- or three- character code for the type of Cloudlet, `ALB` for Application Load Balancer, `AP` for API Prioritization, `CD` for Phased Release, `ER` for Edge Redirector, `FR` for Forward Rewrite, and `VP` for Visitor Prioritization.
    * `revision_id` - A unique identifier given to every policy version update.
    * `description` - The description of this specific policy.
    * `version_description` - The description of this specific policy version.
    * `rules_locked` - Whether editing `match_rules` for the Cloudlet policy version is blocked.
    * `match_rules`- A JSON structure that defines the rules for this policy.
    * `match_rule_format` - The format of the Cloudlet-specific `match_rules`.
    * `warnings` - A JSON encoded list of warnings.
    * `activations` - A list of of current policy activation information, including:
      * `api_version` - The specific version of the Cloudlets API.
      * `network` - The network, either `staging` or `prod` on which a property or a Cloudlets policy has been activated.
      * `policy_info` - A list of Cloudlet policy information, including:
          * `policy_id` - An integer identifier that is associated with all versions of a policy.
          * `name` - The name of the policy.
          * `version` - The version number of the policy.
          * `status` - The activation status for the policy. Values include the following: `inactive` where the policy version has not been activated. No active property versions reference this policy. `active` where the policy version is currently active (published) and its associated property version is also active. `deactivated` where the policy version was previously activated but it has been superseded by a more recent activation of another policy version. `pending` where the policy version is proceeding through the activation workflow. `failed` where the policy version activation workflow has failed.
          * `status_detail` - Information about the status of an activation operation. This field is not returned when it has no value.
          * `activated_by` - The name of the user who activated the policy.
          * `activation_date` - The date on which the policy was activated in milliseconds since epoch.
      * `property_info` A list of Cloudlet property information, including:
          * `name` - The name of the property.
          * `version` - The version number of the activated property.
          * `group_id` - Defines the group association for the policy or property. If returns `0`, the policy is not tied to a group and in effect appears in all groups for the account. You must have edit privileges for the group.
          * `status` - The activation status for the property. Values include the following: `inactive` where the policy version has not been activated. No active property versions reference this policy. `active` where the policy version is currently active (published) and its associated property version is also active. `deactivated` where the policy version was previously activated but it has been superseded by a more recent activation of another policy version. `pending` where the policy version is proceeding through the activation workflow. `failed` where the policy version activation workflow has failed.
          * `activated_by` - The name of the user who activated the property.
          * `activation_date` - The date on which the property was activated in milliseconds since epoch.


    :param int policy_id: - (Required) An integer identifier that is associated with all versions of a policy.
    :param int version: - (Optional) The version number of a policy.
    """
    __args__ = dict()
    __args__['policyId'] = policy_id
    __args__['version'] = version
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('akamai:index/getCloudletsPolicy:getCloudletsPolicy', __args__, opts=opts, typ=GetCloudletsPolicyResult).value

    return AwaitableGetCloudletsPolicyResult(
        activations=__ret__.activations,
        api_version=__ret__.api_version,
        cloudlet_code=__ret__.cloudlet_code,
        cloudlet_id=__ret__.cloudlet_id,
        description=__ret__.description,
        group_id=__ret__.group_id,
        id=__ret__.id,
        match_rule_format=__ret__.match_rule_format,
        match_rules=__ret__.match_rules,
        name=__ret__.name,
        policy_id=__ret__.policy_id,
        revision_id=__ret__.revision_id,
        rules_locked=__ret__.rules_locked,
        version=__ret__.version,
        version_description=__ret__.version_description,
        warnings=__ret__.warnings)


@_utilities.lift_output_func(get_cloudlets_policy)
def get_cloudlets_policy_output(policy_id: Optional[pulumi.Input[int]] = None,
                                version: Optional[pulumi.Input[Optional[int]]] = None,
                                opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetCloudletsPolicyResult]:
    """
    Use the `CloudletsPolicy` data source to list details about a policy with and its specified version, or latest if not specified.

    ## Basic usage

    This example returns the policy details based on the policy ID and optionally, a version:

    ```python
    import pulumi
    import pulumi_akamai as akamai

    example = akamai.get_cloudlets_policy(policy_id=1234,
        version=1)
    ```

    ## Attributes reference

    This data source returns these attributes:

    * `group_id` - Defines the group association for the policy. You must have edit privileges for the group.
    * `name` - The unique name of the policy.
    * `api_version` - The specific version of the Cloudlets API.
    * `cloudlet_id` - A unique identifier that corresponds to a Cloudlets policy type. Enter `0` for Edge Redirector, `1` for Visitor Prioritization, `3` for Forward Rewrite, `5` for API Prioritization, `7` for Phased Release, or `9` for Application Load Balancer.
    * `cloudlet_code` - The two- or three- character code for the type of Cloudlet, `ALB` for Application Load Balancer, `AP` for API Prioritization, `CD` for Phased Release, `ER` for Edge Redirector, `FR` for Forward Rewrite, and `VP` for Visitor Prioritization.
    * `revision_id` - A unique identifier given to every policy version update.
    * `description` - The description of this specific policy.
    * `version_description` - The description of this specific policy version.
    * `rules_locked` - Whether editing `match_rules` for the Cloudlet policy version is blocked.
    * `match_rules`- A JSON structure that defines the rules for this policy.
    * `match_rule_format` - The format of the Cloudlet-specific `match_rules`.
    * `warnings` - A JSON encoded list of warnings.
    * `activations` - A list of of current policy activation information, including:
      * `api_version` - The specific version of the Cloudlets API.
      * `network` - The network, either `staging` or `prod` on which a property or a Cloudlets policy has been activated.
      * `policy_info` - A list of Cloudlet policy information, including:
          * `policy_id` - An integer identifier that is associated with all versions of a policy.
          * `name` - The name of the policy.
          * `version` - The version number of the policy.
          * `status` - The activation status for the policy. Values include the following: `inactive` where the policy version has not been activated. No active property versions reference this policy. `active` where the policy version is currently active (published) and its associated property version is also active. `deactivated` where the policy version was previously activated but it has been superseded by a more recent activation of another policy version. `pending` where the policy version is proceeding through the activation workflow. `failed` where the policy version activation workflow has failed.
          * `status_detail` - Information about the status of an activation operation. This field is not returned when it has no value.
          * `activated_by` - The name of the user who activated the policy.
          * `activation_date` - The date on which the policy was activated in milliseconds since epoch.
      * `property_info` A list of Cloudlet property information, including:
          * `name` - The name of the property.
          * `version` - The version number of the activated property.
          * `group_id` - Defines the group association for the policy or property. If returns `0`, the policy is not tied to a group and in effect appears in all groups for the account. You must have edit privileges for the group.
          * `status` - The activation status for the property. Values include the following: `inactive` where the policy version has not been activated. No active property versions reference this policy. `active` where the policy version is currently active (published) and its associated property version is also active. `deactivated` where the policy version was previously activated but it has been superseded by a more recent activation of another policy version. `pending` where the policy version is proceeding through the activation workflow. `failed` where the policy version activation workflow has failed.
          * `activated_by` - The name of the user who activated the property.
          * `activation_date` - The date on which the property was activated in milliseconds since epoch.


    :param int policy_id: - (Required) An integer identifier that is associated with all versions of a policy.
    :param int version: - (Optional) The version number of a policy.
    """
    ...
