# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities

__all__ = ['CloudletsPolicyActivationArgs', 'CloudletsPolicyActivation']

@pulumi.input_type
class CloudletsPolicyActivationArgs:
    def __init__(__self__, *,
                 associated_properties: pulumi.Input[Sequence[pulumi.Input[str]]],
                 network: pulumi.Input[str],
                 policy_id: pulumi.Input[int],
                 version: pulumi.Input[int]):
        """
        The set of arguments for constructing a CloudletsPolicyActivation resource.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] associated_properties: A set of property identifiers related to this Cloudlet policy. You can't activate a Cloudlet policy if it doesn't have any properties associated with it.
        :param pulumi.Input[str] network: The network you want to activate the policy version on. For the Staging network, specify either `staging`, `stag`, or `s`. For the Production network, specify either `production`, `prod`, or `p`. All values are case insensitive.
        :param pulumi.Input[int] policy_id: An identifier for the Cloudlet policy you want to activate.
        :param pulumi.Input[int] version: The Cloudlet policy version you want to activate.
        """
        pulumi.set(__self__, "associated_properties", associated_properties)
        pulumi.set(__self__, "network", network)
        pulumi.set(__self__, "policy_id", policy_id)
        pulumi.set(__self__, "version", version)

    @property
    @pulumi.getter(name="associatedProperties")
    def associated_properties(self) -> pulumi.Input[Sequence[pulumi.Input[str]]]:
        """
        A set of property identifiers related to this Cloudlet policy. You can't activate a Cloudlet policy if it doesn't have any properties associated with it.
        """
        return pulumi.get(self, "associated_properties")

    @associated_properties.setter
    def associated_properties(self, value: pulumi.Input[Sequence[pulumi.Input[str]]]):
        pulumi.set(self, "associated_properties", value)

    @property
    @pulumi.getter
    def network(self) -> pulumi.Input[str]:
        """
        The network you want to activate the policy version on. For the Staging network, specify either `staging`, `stag`, or `s`. For the Production network, specify either `production`, `prod`, or `p`. All values are case insensitive.
        """
        return pulumi.get(self, "network")

    @network.setter
    def network(self, value: pulumi.Input[str]):
        pulumi.set(self, "network", value)

    @property
    @pulumi.getter(name="policyId")
    def policy_id(self) -> pulumi.Input[int]:
        """
        An identifier for the Cloudlet policy you want to activate.
        """
        return pulumi.get(self, "policy_id")

    @policy_id.setter
    def policy_id(self, value: pulumi.Input[int]):
        pulumi.set(self, "policy_id", value)

    @property
    @pulumi.getter
    def version(self) -> pulumi.Input[int]:
        """
        The Cloudlet policy version you want to activate.
        """
        return pulumi.get(self, "version")

    @version.setter
    def version(self, value: pulumi.Input[int]):
        pulumi.set(self, "version", value)


@pulumi.input_type
class _CloudletsPolicyActivationState:
    def __init__(__self__, *,
                 associated_properties: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 network: Optional[pulumi.Input[str]] = None,
                 policy_id: Optional[pulumi.Input[int]] = None,
                 status: Optional[pulumi.Input[str]] = None,
                 version: Optional[pulumi.Input[int]] = None):
        """
        Input properties used for looking up and filtering CloudletsPolicyActivation resources.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] associated_properties: A set of property identifiers related to this Cloudlet policy. You can't activate a Cloudlet policy if it doesn't have any properties associated with it.
        :param pulumi.Input[str] network: The network you want to activate the policy version on. For the Staging network, specify either `staging`, `stag`, or `s`. For the Production network, specify either `production`, `prod`, or `p`. All values are case insensitive.
        :param pulumi.Input[int] policy_id: An identifier for the Cloudlet policy you want to activate.
        :param pulumi.Input[str] status: The activation status for this Cloudlet policy.
        :param pulumi.Input[int] version: The Cloudlet policy version you want to activate.
        """
        if associated_properties is not None:
            pulumi.set(__self__, "associated_properties", associated_properties)
        if network is not None:
            pulumi.set(__self__, "network", network)
        if policy_id is not None:
            pulumi.set(__self__, "policy_id", policy_id)
        if status is not None:
            pulumi.set(__self__, "status", status)
        if version is not None:
            pulumi.set(__self__, "version", version)

    @property
    @pulumi.getter(name="associatedProperties")
    def associated_properties(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        A set of property identifiers related to this Cloudlet policy. You can't activate a Cloudlet policy if it doesn't have any properties associated with it.
        """
        return pulumi.get(self, "associated_properties")

    @associated_properties.setter
    def associated_properties(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "associated_properties", value)

    @property
    @pulumi.getter
    def network(self) -> Optional[pulumi.Input[str]]:
        """
        The network you want to activate the policy version on. For the Staging network, specify either `staging`, `stag`, or `s`. For the Production network, specify either `production`, `prod`, or `p`. All values are case insensitive.
        """
        return pulumi.get(self, "network")

    @network.setter
    def network(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "network", value)

    @property
    @pulumi.getter(name="policyId")
    def policy_id(self) -> Optional[pulumi.Input[int]]:
        """
        An identifier for the Cloudlet policy you want to activate.
        """
        return pulumi.get(self, "policy_id")

    @policy_id.setter
    def policy_id(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "policy_id", value)

    @property
    @pulumi.getter
    def status(self) -> Optional[pulumi.Input[str]]:
        """
        The activation status for this Cloudlet policy.
        """
        return pulumi.get(self, "status")

    @status.setter
    def status(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "status", value)

    @property
    @pulumi.getter
    def version(self) -> Optional[pulumi.Input[int]]:
        """
        The Cloudlet policy version you want to activate.
        """
        return pulumi.get(self, "version")

    @version.setter
    def version(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "version", value)


class CloudletsPolicyActivation(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 associated_properties: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 network: Optional[pulumi.Input[str]] = None,
                 policy_id: Optional[pulumi.Input[int]] = None,
                 version: Optional[pulumi.Input[int]] = None,
                 __props__=None):
        """
        Use the `CloudletsPolicyActivation` resource to activate a specific version of a Cloudlet policy. An activation deploys the version to either the Akamai staging or production network. You can activate a specific version multiple times if you need to.

        Before activating on production, activate on staging first. This way you can detect any problems in staging before your changes progress to production.

        ## Example Usage

        Basic usage:

        ```python
        import pulumi
        import pulumi_akamai as akamai

        example = akamai.CloudletsPolicyActivation("example",
            associated_properties=[
                "Property_1",
                "Property_2",
                "Property_3",
            ],
            network="staging",
            policy_id=1234,
            version=1)
        ```
        If you're handling two `CloudletsPolicyActivation` resources in the same configuration file with the same `policy_id`, but different `network` arguments (for example, `production` and `staging`), you need to add `depends_on` to the production resource. See the example:

        ```python
        import pulumi
        import pulumi_akamai as akamai

        stag = akamai.CloudletsPolicyActivation("stag",
            policy_id=1234567,
            network="staging",
            version=1,
            associated_properties=[
                "Property_1",
                "Property_2",
            ])
        prod = akamai.CloudletsPolicyActivation("prod",
            policy_id=1234567,
            network="production",
            version=1,
            associated_properties=[
                "Property_1",
                "Property_2",
            ],
            opts=pulumi.ResourceOptions(depends_on=[stag]))
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] associated_properties: A set of property identifiers related to this Cloudlet policy. You can't activate a Cloudlet policy if it doesn't have any properties associated with it.
        :param pulumi.Input[str] network: The network you want to activate the policy version on. For the Staging network, specify either `staging`, `stag`, or `s`. For the Production network, specify either `production`, `prod`, or `p`. All values are case insensitive.
        :param pulumi.Input[int] policy_id: An identifier for the Cloudlet policy you want to activate.
        :param pulumi.Input[int] version: The Cloudlet policy version you want to activate.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: CloudletsPolicyActivationArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Use the `CloudletsPolicyActivation` resource to activate a specific version of a Cloudlet policy. An activation deploys the version to either the Akamai staging or production network. You can activate a specific version multiple times if you need to.

        Before activating on production, activate on staging first. This way you can detect any problems in staging before your changes progress to production.

        ## Example Usage

        Basic usage:

        ```python
        import pulumi
        import pulumi_akamai as akamai

        example = akamai.CloudletsPolicyActivation("example",
            associated_properties=[
                "Property_1",
                "Property_2",
                "Property_3",
            ],
            network="staging",
            policy_id=1234,
            version=1)
        ```
        If you're handling two `CloudletsPolicyActivation` resources in the same configuration file with the same `policy_id`, but different `network` arguments (for example, `production` and `staging`), you need to add `depends_on` to the production resource. See the example:

        ```python
        import pulumi
        import pulumi_akamai as akamai

        stag = akamai.CloudletsPolicyActivation("stag",
            policy_id=1234567,
            network="staging",
            version=1,
            associated_properties=[
                "Property_1",
                "Property_2",
            ])
        prod = akamai.CloudletsPolicyActivation("prod",
            policy_id=1234567,
            network="production",
            version=1,
            associated_properties=[
                "Property_1",
                "Property_2",
            ],
            opts=pulumi.ResourceOptions(depends_on=[stag]))
        ```

        :param str resource_name: The name of the resource.
        :param CloudletsPolicyActivationArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(CloudletsPolicyActivationArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 associated_properties: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 network: Optional[pulumi.Input[str]] = None,
                 policy_id: Optional[pulumi.Input[int]] = None,
                 version: Optional[pulumi.Input[int]] = None,
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
            __props__ = CloudletsPolicyActivationArgs.__new__(CloudletsPolicyActivationArgs)

            if associated_properties is None and not opts.urn:
                raise TypeError("Missing required property 'associated_properties'")
            __props__.__dict__["associated_properties"] = associated_properties
            if network is None and not opts.urn:
                raise TypeError("Missing required property 'network'")
            __props__.__dict__["network"] = network
            if policy_id is None and not opts.urn:
                raise TypeError("Missing required property 'policy_id'")
            __props__.__dict__["policy_id"] = policy_id
            if version is None and not opts.urn:
                raise TypeError("Missing required property 'version'")
            __props__.__dict__["version"] = version
            __props__.__dict__["status"] = None
        super(CloudletsPolicyActivation, __self__).__init__(
            'akamai:index/cloudletsPolicyActivation:CloudletsPolicyActivation',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            associated_properties: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            network: Optional[pulumi.Input[str]] = None,
            policy_id: Optional[pulumi.Input[int]] = None,
            status: Optional[pulumi.Input[str]] = None,
            version: Optional[pulumi.Input[int]] = None) -> 'CloudletsPolicyActivation':
        """
        Get an existing CloudletsPolicyActivation resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] associated_properties: A set of property identifiers related to this Cloudlet policy. You can't activate a Cloudlet policy if it doesn't have any properties associated with it.
        :param pulumi.Input[str] network: The network you want to activate the policy version on. For the Staging network, specify either `staging`, `stag`, or `s`. For the Production network, specify either `production`, `prod`, or `p`. All values are case insensitive.
        :param pulumi.Input[int] policy_id: An identifier for the Cloudlet policy you want to activate.
        :param pulumi.Input[str] status: The activation status for this Cloudlet policy.
        :param pulumi.Input[int] version: The Cloudlet policy version you want to activate.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _CloudletsPolicyActivationState.__new__(_CloudletsPolicyActivationState)

        __props__.__dict__["associated_properties"] = associated_properties
        __props__.__dict__["network"] = network
        __props__.__dict__["policy_id"] = policy_id
        __props__.__dict__["status"] = status
        __props__.__dict__["version"] = version
        return CloudletsPolicyActivation(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="associatedProperties")
    def associated_properties(self) -> pulumi.Output[Sequence[str]]:
        """
        A set of property identifiers related to this Cloudlet policy. You can't activate a Cloudlet policy if it doesn't have any properties associated with it.
        """
        return pulumi.get(self, "associated_properties")

    @property
    @pulumi.getter
    def network(self) -> pulumi.Output[str]:
        """
        The network you want to activate the policy version on. For the Staging network, specify either `staging`, `stag`, or `s`. For the Production network, specify either `production`, `prod`, or `p`. All values are case insensitive.
        """
        return pulumi.get(self, "network")

    @property
    @pulumi.getter(name="policyId")
    def policy_id(self) -> pulumi.Output[int]:
        """
        An identifier for the Cloudlet policy you want to activate.
        """
        return pulumi.get(self, "policy_id")

    @property
    @pulumi.getter
    def status(self) -> pulumi.Output[str]:
        """
        The activation status for this Cloudlet policy.
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter
    def version(self) -> pulumi.Output[int]:
        """
        The Cloudlet policy version you want to activate.
        """
        return pulumi.get(self, "version")

