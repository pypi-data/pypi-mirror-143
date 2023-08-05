# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities

__all__ = ['AppSecReputationProfileAnalysisArgs', 'AppSecReputationProfileAnalysis']

@pulumi.input_type
class AppSecReputationProfileAnalysisArgs:
    def __init__(__self__, *,
                 config_id: pulumi.Input[int],
                 forward_shared_ip_to_http_header_siem: pulumi.Input[bool],
                 forward_to_http_header: pulumi.Input[bool],
                 security_policy_id: pulumi.Input[str]):
        """
        The set of arguments for constructing a AppSecReputationProfileAnalysis resource.
        :param pulumi.Input[int] config_id: . Unique identifier of the security configuration associated with the reputation profile analysis settings being modified.
        :param pulumi.Input[bool] forward_shared_ip_to_http_header_siem: . Set to **true** to add a value indicating that shared IPs are included in HTTP header and SIEM integration; set to **false** to omit this value.
        :param pulumi.Input[bool] forward_to_http_header: . Set to **true** to add client reputation details to requests forwarded to the origin server in an HTTP header; set to `false` to leave reputation details out of these requests.
        :param pulumi.Input[str] security_policy_id: . Unique identifier of the security policy associated with the reputation profile analysis settings being modified.
        """
        pulumi.set(__self__, "config_id", config_id)
        pulumi.set(__self__, "forward_shared_ip_to_http_header_siem", forward_shared_ip_to_http_header_siem)
        pulumi.set(__self__, "forward_to_http_header", forward_to_http_header)
        pulumi.set(__self__, "security_policy_id", security_policy_id)

    @property
    @pulumi.getter(name="configId")
    def config_id(self) -> pulumi.Input[int]:
        """
        . Unique identifier of the security configuration associated with the reputation profile analysis settings being modified.
        """
        return pulumi.get(self, "config_id")

    @config_id.setter
    def config_id(self, value: pulumi.Input[int]):
        pulumi.set(self, "config_id", value)

    @property
    @pulumi.getter(name="forwardSharedIpToHttpHeaderSiem")
    def forward_shared_ip_to_http_header_siem(self) -> pulumi.Input[bool]:
        """
        . Set to **true** to add a value indicating that shared IPs are included in HTTP header and SIEM integration; set to **false** to omit this value.
        """
        return pulumi.get(self, "forward_shared_ip_to_http_header_siem")

    @forward_shared_ip_to_http_header_siem.setter
    def forward_shared_ip_to_http_header_siem(self, value: pulumi.Input[bool]):
        pulumi.set(self, "forward_shared_ip_to_http_header_siem", value)

    @property
    @pulumi.getter(name="forwardToHttpHeader")
    def forward_to_http_header(self) -> pulumi.Input[bool]:
        """
        . Set to **true** to add client reputation details to requests forwarded to the origin server in an HTTP header; set to `false` to leave reputation details out of these requests.
        """
        return pulumi.get(self, "forward_to_http_header")

    @forward_to_http_header.setter
    def forward_to_http_header(self, value: pulumi.Input[bool]):
        pulumi.set(self, "forward_to_http_header", value)

    @property
    @pulumi.getter(name="securityPolicyId")
    def security_policy_id(self) -> pulumi.Input[str]:
        """
        . Unique identifier of the security policy associated with the reputation profile analysis settings being modified.
        """
        return pulumi.get(self, "security_policy_id")

    @security_policy_id.setter
    def security_policy_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "security_policy_id", value)


@pulumi.input_type
class _AppSecReputationProfileAnalysisState:
    def __init__(__self__, *,
                 config_id: Optional[pulumi.Input[int]] = None,
                 forward_shared_ip_to_http_header_siem: Optional[pulumi.Input[bool]] = None,
                 forward_to_http_header: Optional[pulumi.Input[bool]] = None,
                 security_policy_id: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering AppSecReputationProfileAnalysis resources.
        :param pulumi.Input[int] config_id: . Unique identifier of the security configuration associated with the reputation profile analysis settings being modified.
        :param pulumi.Input[bool] forward_shared_ip_to_http_header_siem: . Set to **true** to add a value indicating that shared IPs are included in HTTP header and SIEM integration; set to **false** to omit this value.
        :param pulumi.Input[bool] forward_to_http_header: . Set to **true** to add client reputation details to requests forwarded to the origin server in an HTTP header; set to `false` to leave reputation details out of these requests.
        :param pulumi.Input[str] security_policy_id: . Unique identifier of the security policy associated with the reputation profile analysis settings being modified.
        """
        if config_id is not None:
            pulumi.set(__self__, "config_id", config_id)
        if forward_shared_ip_to_http_header_siem is not None:
            pulumi.set(__self__, "forward_shared_ip_to_http_header_siem", forward_shared_ip_to_http_header_siem)
        if forward_to_http_header is not None:
            pulumi.set(__self__, "forward_to_http_header", forward_to_http_header)
        if security_policy_id is not None:
            pulumi.set(__self__, "security_policy_id", security_policy_id)

    @property
    @pulumi.getter(name="configId")
    def config_id(self) -> Optional[pulumi.Input[int]]:
        """
        . Unique identifier of the security configuration associated with the reputation profile analysis settings being modified.
        """
        return pulumi.get(self, "config_id")

    @config_id.setter
    def config_id(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "config_id", value)

    @property
    @pulumi.getter(name="forwardSharedIpToHttpHeaderSiem")
    def forward_shared_ip_to_http_header_siem(self) -> Optional[pulumi.Input[bool]]:
        """
        . Set to **true** to add a value indicating that shared IPs are included in HTTP header and SIEM integration; set to **false** to omit this value.
        """
        return pulumi.get(self, "forward_shared_ip_to_http_header_siem")

    @forward_shared_ip_to_http_header_siem.setter
    def forward_shared_ip_to_http_header_siem(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "forward_shared_ip_to_http_header_siem", value)

    @property
    @pulumi.getter(name="forwardToHttpHeader")
    def forward_to_http_header(self) -> Optional[pulumi.Input[bool]]:
        """
        . Set to **true** to add client reputation details to requests forwarded to the origin server in an HTTP header; set to `false` to leave reputation details out of these requests.
        """
        return pulumi.get(self, "forward_to_http_header")

    @forward_to_http_header.setter
    def forward_to_http_header(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "forward_to_http_header", value)

    @property
    @pulumi.getter(name="securityPolicyId")
    def security_policy_id(self) -> Optional[pulumi.Input[str]]:
        """
        . Unique identifier of the security policy associated with the reputation profile analysis settings being modified.
        """
        return pulumi.get(self, "security_policy_id")

    @security_policy_id.setter
    def security_policy_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "security_policy_id", value)


class AppSecReputationProfileAnalysis(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 config_id: Optional[pulumi.Input[int]] = None,
                 forward_shared_ip_to_http_header_siem: Optional[pulumi.Input[bool]] = None,
                 forward_to_http_header: Optional[pulumi.Input[bool]] = None,
                 security_policy_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        **Scopes**: Security policy

        Modifies the reputation analysis settings for a security policy. These settings include the following:

        - The `forward_to_http_header` parameter, which indicates whether client reputation details are added to requests forwarded to origin in an HTTP header.
        - The `forward_shared_ip_to_http_header_siem` parameter, which specifies whether a value is added indicating that shared IPs addresses are included in HTTP headers and in SIEM integration events.

        **Related API Endpoint**: [/appsec/v1/configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/reputation-analysis](https://developer.akamai.com/api/cloud_security/application_security/v1.html#putreputationanalysis)

        ## Example Usage

        Basic usage:

        ```python
        import pulumi
        import pulumi_akamai as akamai

        configuration = akamai.get_app_sec_configuration(name="Documentation")
        reputation_analysis = akamai.get_app_sec_reputation_profile_analysis(config_id=configuration.config_id,
            security_policy_id="gms1_134637",
            forward_to_http_header=True)
        pulumi.export("reputationAnalysisText", reputation_analysis.output_text)
        pulumi.export("reputationAnalysisJson", reputation_analysis.json)
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[int] config_id: . Unique identifier of the security configuration associated with the reputation profile analysis settings being modified.
        :param pulumi.Input[bool] forward_shared_ip_to_http_header_siem: . Set to **true** to add a value indicating that shared IPs are included in HTTP header and SIEM integration; set to **false** to omit this value.
        :param pulumi.Input[bool] forward_to_http_header: . Set to **true** to add client reputation details to requests forwarded to the origin server in an HTTP header; set to `false` to leave reputation details out of these requests.
        :param pulumi.Input[str] security_policy_id: . Unique identifier of the security policy associated with the reputation profile analysis settings being modified.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: AppSecReputationProfileAnalysisArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        **Scopes**: Security policy

        Modifies the reputation analysis settings for a security policy. These settings include the following:

        - The `forward_to_http_header` parameter, which indicates whether client reputation details are added to requests forwarded to origin in an HTTP header.
        - The `forward_shared_ip_to_http_header_siem` parameter, which specifies whether a value is added indicating that shared IPs addresses are included in HTTP headers and in SIEM integration events.

        **Related API Endpoint**: [/appsec/v1/configs/{configId}/versions/{versionNumber}/security-policies/{policyId}/reputation-analysis](https://developer.akamai.com/api/cloud_security/application_security/v1.html#putreputationanalysis)

        ## Example Usage

        Basic usage:

        ```python
        import pulumi
        import pulumi_akamai as akamai

        configuration = akamai.get_app_sec_configuration(name="Documentation")
        reputation_analysis = akamai.get_app_sec_reputation_profile_analysis(config_id=configuration.config_id,
            security_policy_id="gms1_134637",
            forward_to_http_header=True)
        pulumi.export("reputationAnalysisText", reputation_analysis.output_text)
        pulumi.export("reputationAnalysisJson", reputation_analysis.json)
        ```

        :param str resource_name: The name of the resource.
        :param AppSecReputationProfileAnalysisArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(AppSecReputationProfileAnalysisArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 config_id: Optional[pulumi.Input[int]] = None,
                 forward_shared_ip_to_http_header_siem: Optional[pulumi.Input[bool]] = None,
                 forward_to_http_header: Optional[pulumi.Input[bool]] = None,
                 security_policy_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        if opts is None:
            opts = pulumi.ResourceOptions()
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.version is None:
            opts.version = _utilities.get_version()
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = AppSecReputationProfileAnalysisArgs.__new__(AppSecReputationProfileAnalysisArgs)

            if config_id is None and not opts.urn:
                raise TypeError("Missing required property 'config_id'")
            __props__.__dict__["config_id"] = config_id
            if forward_shared_ip_to_http_header_siem is None and not opts.urn:
                raise TypeError("Missing required property 'forward_shared_ip_to_http_header_siem'")
            __props__.__dict__["forward_shared_ip_to_http_header_siem"] = forward_shared_ip_to_http_header_siem
            if forward_to_http_header is None and not opts.urn:
                raise TypeError("Missing required property 'forward_to_http_header'")
            __props__.__dict__["forward_to_http_header"] = forward_to_http_header
            if security_policy_id is None and not opts.urn:
                raise TypeError("Missing required property 'security_policy_id'")
            __props__.__dict__["security_policy_id"] = security_policy_id
        super(AppSecReputationProfileAnalysis, __self__).__init__(
            'akamai:index/appSecReputationProfileAnalysis:AppSecReputationProfileAnalysis',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            config_id: Optional[pulumi.Input[int]] = None,
            forward_shared_ip_to_http_header_siem: Optional[pulumi.Input[bool]] = None,
            forward_to_http_header: Optional[pulumi.Input[bool]] = None,
            security_policy_id: Optional[pulumi.Input[str]] = None) -> 'AppSecReputationProfileAnalysis':
        """
        Get an existing AppSecReputationProfileAnalysis resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[int] config_id: . Unique identifier of the security configuration associated with the reputation profile analysis settings being modified.
        :param pulumi.Input[bool] forward_shared_ip_to_http_header_siem: . Set to **true** to add a value indicating that shared IPs are included in HTTP header and SIEM integration; set to **false** to omit this value.
        :param pulumi.Input[bool] forward_to_http_header: . Set to **true** to add client reputation details to requests forwarded to the origin server in an HTTP header; set to `false` to leave reputation details out of these requests.
        :param pulumi.Input[str] security_policy_id: . Unique identifier of the security policy associated with the reputation profile analysis settings being modified.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _AppSecReputationProfileAnalysisState.__new__(_AppSecReputationProfileAnalysisState)

        __props__.__dict__["config_id"] = config_id
        __props__.__dict__["forward_shared_ip_to_http_header_siem"] = forward_shared_ip_to_http_header_siem
        __props__.__dict__["forward_to_http_header"] = forward_to_http_header
        __props__.__dict__["security_policy_id"] = security_policy_id
        return AppSecReputationProfileAnalysis(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="configId")
    def config_id(self) -> pulumi.Output[int]:
        """
        . Unique identifier of the security configuration associated with the reputation profile analysis settings being modified.
        """
        return pulumi.get(self, "config_id")

    @property
    @pulumi.getter(name="forwardSharedIpToHttpHeaderSiem")
    def forward_shared_ip_to_http_header_siem(self) -> pulumi.Output[bool]:
        """
        . Set to **true** to add a value indicating that shared IPs are included in HTTP header and SIEM integration; set to **false** to omit this value.
        """
        return pulumi.get(self, "forward_shared_ip_to_http_header_siem")

    @property
    @pulumi.getter(name="forwardToHttpHeader")
    def forward_to_http_header(self) -> pulumi.Output[bool]:
        """
        . Set to **true** to add client reputation details to requests forwarded to the origin server in an HTTP header; set to `false` to leave reputation details out of these requests.
        """
        return pulumi.get(self, "forward_to_http_header")

    @property
    @pulumi.getter(name="securityPolicyId")
    def security_policy_id(self) -> pulumi.Output[str]:
        """
        . Unique identifier of the security policy associated with the reputation profile analysis settings being modified.
        """
        return pulumi.get(self, "security_policy_id")

