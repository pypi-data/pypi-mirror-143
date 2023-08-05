# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs
from ._inputs import *

__all__ = ['GtmResourceArgs', 'GtmResource']

@pulumi.input_type
class GtmResourceArgs:
    def __init__(__self__, *,
                 aggregation_type: pulumi.Input[str],
                 domain: pulumi.Input[str],
                 type: pulumi.Input[str],
                 constrained_property: Optional[pulumi.Input[str]] = None,
                 decay_rate: Optional[pulumi.Input[float]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 host_header: Optional[pulumi.Input[str]] = None,
                 leader_string: Optional[pulumi.Input[str]] = None,
                 least_squares_decay: Optional[pulumi.Input[float]] = None,
                 load_imbalance_percentage: Optional[pulumi.Input[float]] = None,
                 max_u_multiplicative_increment: Optional[pulumi.Input[float]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 resource_instances: Optional[pulumi.Input[Sequence[pulumi.Input['GtmResourceResourceInstanceArgs']]]] = None,
                 upper_bound: Optional[pulumi.Input[int]] = None,
                 wait_on_complete: Optional[pulumi.Input[bool]] = None):
        """
        The set of arguments for constructing a GtmResource resource.
        """
        pulumi.set(__self__, "aggregation_type", aggregation_type)
        pulumi.set(__self__, "domain", domain)
        pulumi.set(__self__, "type", type)
        if constrained_property is not None:
            pulumi.set(__self__, "constrained_property", constrained_property)
        if decay_rate is not None:
            pulumi.set(__self__, "decay_rate", decay_rate)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if host_header is not None:
            pulumi.set(__self__, "host_header", host_header)
        if leader_string is not None:
            pulumi.set(__self__, "leader_string", leader_string)
        if least_squares_decay is not None:
            pulumi.set(__self__, "least_squares_decay", least_squares_decay)
        if load_imbalance_percentage is not None:
            pulumi.set(__self__, "load_imbalance_percentage", load_imbalance_percentage)
        if max_u_multiplicative_increment is not None:
            pulumi.set(__self__, "max_u_multiplicative_increment", max_u_multiplicative_increment)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if resource_instances is not None:
            pulumi.set(__self__, "resource_instances", resource_instances)
        if upper_bound is not None:
            pulumi.set(__self__, "upper_bound", upper_bound)
        if wait_on_complete is not None:
            pulumi.set(__self__, "wait_on_complete", wait_on_complete)

    @property
    @pulumi.getter(name="aggregationType")
    def aggregation_type(self) -> pulumi.Input[str]:
        return pulumi.get(self, "aggregation_type")

    @aggregation_type.setter
    def aggregation_type(self, value: pulumi.Input[str]):
        pulumi.set(self, "aggregation_type", value)

    @property
    @pulumi.getter
    def domain(self) -> pulumi.Input[str]:
        return pulumi.get(self, "domain")

    @domain.setter
    def domain(self, value: pulumi.Input[str]):
        pulumi.set(self, "domain", value)

    @property
    @pulumi.getter
    def type(self) -> pulumi.Input[str]:
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: pulumi.Input[str]):
        pulumi.set(self, "type", value)

    @property
    @pulumi.getter(name="constrainedProperty")
    def constrained_property(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "constrained_property")

    @constrained_property.setter
    def constrained_property(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "constrained_property", value)

    @property
    @pulumi.getter(name="decayRate")
    def decay_rate(self) -> Optional[pulumi.Input[float]]:
        return pulumi.get(self, "decay_rate")

    @decay_rate.setter
    def decay_rate(self, value: Optional[pulumi.Input[float]]):
        pulumi.set(self, "decay_rate", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="hostHeader")
    def host_header(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "host_header")

    @host_header.setter
    def host_header(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "host_header", value)

    @property
    @pulumi.getter(name="leaderString")
    def leader_string(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "leader_string")

    @leader_string.setter
    def leader_string(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "leader_string", value)

    @property
    @pulumi.getter(name="leastSquaresDecay")
    def least_squares_decay(self) -> Optional[pulumi.Input[float]]:
        return pulumi.get(self, "least_squares_decay")

    @least_squares_decay.setter
    def least_squares_decay(self, value: Optional[pulumi.Input[float]]):
        pulumi.set(self, "least_squares_decay", value)

    @property
    @pulumi.getter(name="loadImbalancePercentage")
    def load_imbalance_percentage(self) -> Optional[pulumi.Input[float]]:
        return pulumi.get(self, "load_imbalance_percentage")

    @load_imbalance_percentage.setter
    def load_imbalance_percentage(self, value: Optional[pulumi.Input[float]]):
        pulumi.set(self, "load_imbalance_percentage", value)

    @property
    @pulumi.getter(name="maxUMultiplicativeIncrement")
    def max_u_multiplicative_increment(self) -> Optional[pulumi.Input[float]]:
        return pulumi.get(self, "max_u_multiplicative_increment")

    @max_u_multiplicative_increment.setter
    def max_u_multiplicative_increment(self, value: Optional[pulumi.Input[float]]):
        pulumi.set(self, "max_u_multiplicative_increment", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="resourceInstances")
    def resource_instances(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['GtmResourceResourceInstanceArgs']]]]:
        return pulumi.get(self, "resource_instances")

    @resource_instances.setter
    def resource_instances(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['GtmResourceResourceInstanceArgs']]]]):
        pulumi.set(self, "resource_instances", value)

    @property
    @pulumi.getter(name="upperBound")
    def upper_bound(self) -> Optional[pulumi.Input[int]]:
        return pulumi.get(self, "upper_bound")

    @upper_bound.setter
    def upper_bound(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "upper_bound", value)

    @property
    @pulumi.getter(name="waitOnComplete")
    def wait_on_complete(self) -> Optional[pulumi.Input[bool]]:
        return pulumi.get(self, "wait_on_complete")

    @wait_on_complete.setter
    def wait_on_complete(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "wait_on_complete", value)


@pulumi.input_type
class _GtmResourceState:
    def __init__(__self__, *,
                 aggregation_type: Optional[pulumi.Input[str]] = None,
                 constrained_property: Optional[pulumi.Input[str]] = None,
                 decay_rate: Optional[pulumi.Input[float]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 domain: Optional[pulumi.Input[str]] = None,
                 host_header: Optional[pulumi.Input[str]] = None,
                 leader_string: Optional[pulumi.Input[str]] = None,
                 least_squares_decay: Optional[pulumi.Input[float]] = None,
                 load_imbalance_percentage: Optional[pulumi.Input[float]] = None,
                 max_u_multiplicative_increment: Optional[pulumi.Input[float]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 resource_instances: Optional[pulumi.Input[Sequence[pulumi.Input['GtmResourceResourceInstanceArgs']]]] = None,
                 type: Optional[pulumi.Input[str]] = None,
                 upper_bound: Optional[pulumi.Input[int]] = None,
                 wait_on_complete: Optional[pulumi.Input[bool]] = None):
        """
        Input properties used for looking up and filtering GtmResource resources.
        """
        if aggregation_type is not None:
            pulumi.set(__self__, "aggregation_type", aggregation_type)
        if constrained_property is not None:
            pulumi.set(__self__, "constrained_property", constrained_property)
        if decay_rate is not None:
            pulumi.set(__self__, "decay_rate", decay_rate)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if domain is not None:
            pulumi.set(__self__, "domain", domain)
        if host_header is not None:
            pulumi.set(__self__, "host_header", host_header)
        if leader_string is not None:
            pulumi.set(__self__, "leader_string", leader_string)
        if least_squares_decay is not None:
            pulumi.set(__self__, "least_squares_decay", least_squares_decay)
        if load_imbalance_percentage is not None:
            pulumi.set(__self__, "load_imbalance_percentage", load_imbalance_percentage)
        if max_u_multiplicative_increment is not None:
            pulumi.set(__self__, "max_u_multiplicative_increment", max_u_multiplicative_increment)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if resource_instances is not None:
            pulumi.set(__self__, "resource_instances", resource_instances)
        if type is not None:
            pulumi.set(__self__, "type", type)
        if upper_bound is not None:
            pulumi.set(__self__, "upper_bound", upper_bound)
        if wait_on_complete is not None:
            pulumi.set(__self__, "wait_on_complete", wait_on_complete)

    @property
    @pulumi.getter(name="aggregationType")
    def aggregation_type(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "aggregation_type")

    @aggregation_type.setter
    def aggregation_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "aggregation_type", value)

    @property
    @pulumi.getter(name="constrainedProperty")
    def constrained_property(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "constrained_property")

    @constrained_property.setter
    def constrained_property(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "constrained_property", value)

    @property
    @pulumi.getter(name="decayRate")
    def decay_rate(self) -> Optional[pulumi.Input[float]]:
        return pulumi.get(self, "decay_rate")

    @decay_rate.setter
    def decay_rate(self, value: Optional[pulumi.Input[float]]):
        pulumi.set(self, "decay_rate", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def domain(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "domain")

    @domain.setter
    def domain(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "domain", value)

    @property
    @pulumi.getter(name="hostHeader")
    def host_header(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "host_header")

    @host_header.setter
    def host_header(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "host_header", value)

    @property
    @pulumi.getter(name="leaderString")
    def leader_string(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "leader_string")

    @leader_string.setter
    def leader_string(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "leader_string", value)

    @property
    @pulumi.getter(name="leastSquaresDecay")
    def least_squares_decay(self) -> Optional[pulumi.Input[float]]:
        return pulumi.get(self, "least_squares_decay")

    @least_squares_decay.setter
    def least_squares_decay(self, value: Optional[pulumi.Input[float]]):
        pulumi.set(self, "least_squares_decay", value)

    @property
    @pulumi.getter(name="loadImbalancePercentage")
    def load_imbalance_percentage(self) -> Optional[pulumi.Input[float]]:
        return pulumi.get(self, "load_imbalance_percentage")

    @load_imbalance_percentage.setter
    def load_imbalance_percentage(self, value: Optional[pulumi.Input[float]]):
        pulumi.set(self, "load_imbalance_percentage", value)

    @property
    @pulumi.getter(name="maxUMultiplicativeIncrement")
    def max_u_multiplicative_increment(self) -> Optional[pulumi.Input[float]]:
        return pulumi.get(self, "max_u_multiplicative_increment")

    @max_u_multiplicative_increment.setter
    def max_u_multiplicative_increment(self, value: Optional[pulumi.Input[float]]):
        pulumi.set(self, "max_u_multiplicative_increment", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="resourceInstances")
    def resource_instances(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['GtmResourceResourceInstanceArgs']]]]:
        return pulumi.get(self, "resource_instances")

    @resource_instances.setter
    def resource_instances(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['GtmResourceResourceInstanceArgs']]]]):
        pulumi.set(self, "resource_instances", value)

    @property
    @pulumi.getter
    def type(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "type", value)

    @property
    @pulumi.getter(name="upperBound")
    def upper_bound(self) -> Optional[pulumi.Input[int]]:
        return pulumi.get(self, "upper_bound")

    @upper_bound.setter
    def upper_bound(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "upper_bound", value)

    @property
    @pulumi.getter(name="waitOnComplete")
    def wait_on_complete(self) -> Optional[pulumi.Input[bool]]:
        return pulumi.get(self, "wait_on_complete")

    @wait_on_complete.setter
    def wait_on_complete(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "wait_on_complete", value)


warnings.warn("""akamai.trafficmanagement.GtmResource has been deprecated in favor of akamai.GtmResource""", DeprecationWarning)


class GtmResource(pulumi.CustomResource):
    warnings.warn("""akamai.trafficmanagement.GtmResource has been deprecated in favor of akamai.GtmResource""", DeprecationWarning)

    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 aggregation_type: Optional[pulumi.Input[str]] = None,
                 constrained_property: Optional[pulumi.Input[str]] = None,
                 decay_rate: Optional[pulumi.Input[float]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 domain: Optional[pulumi.Input[str]] = None,
                 host_header: Optional[pulumi.Input[str]] = None,
                 leader_string: Optional[pulumi.Input[str]] = None,
                 least_squares_decay: Optional[pulumi.Input[float]] = None,
                 load_imbalance_percentage: Optional[pulumi.Input[float]] = None,
                 max_u_multiplicative_increment: Optional[pulumi.Input[float]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 resource_instances: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['GtmResourceResourceInstanceArgs']]]]] = None,
                 type: Optional[pulumi.Input[str]] = None,
                 upper_bound: Optional[pulumi.Input[int]] = None,
                 wait_on_complete: Optional[pulumi.Input[bool]] = None,
                 __props__=None):
        """
        Create a GtmResource resource with the given unique name, props, and options.
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: GtmResourceArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Create a GtmResource resource with the given unique name, props, and options.
        :param str resource_name: The name of the resource.
        :param GtmResourceArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(GtmResourceArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 aggregation_type: Optional[pulumi.Input[str]] = None,
                 constrained_property: Optional[pulumi.Input[str]] = None,
                 decay_rate: Optional[pulumi.Input[float]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 domain: Optional[pulumi.Input[str]] = None,
                 host_header: Optional[pulumi.Input[str]] = None,
                 leader_string: Optional[pulumi.Input[str]] = None,
                 least_squares_decay: Optional[pulumi.Input[float]] = None,
                 load_imbalance_percentage: Optional[pulumi.Input[float]] = None,
                 max_u_multiplicative_increment: Optional[pulumi.Input[float]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 resource_instances: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['GtmResourceResourceInstanceArgs']]]]] = None,
                 type: Optional[pulumi.Input[str]] = None,
                 upper_bound: Optional[pulumi.Input[int]] = None,
                 wait_on_complete: Optional[pulumi.Input[bool]] = None,
                 __props__=None):
        pulumi.log.warn("""GtmResource is deprecated: akamai.trafficmanagement.GtmResource has been deprecated in favor of akamai.GtmResource""")
        if opts is None:
            opts = pulumi.ResourceOptions()
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.version is None:
            opts.version = _utilities.get_version()
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = GtmResourceArgs.__new__(GtmResourceArgs)

            if aggregation_type is None and not opts.urn:
                raise TypeError("Missing required property 'aggregation_type'")
            __props__.__dict__["aggregation_type"] = aggregation_type
            __props__.__dict__["constrained_property"] = constrained_property
            __props__.__dict__["decay_rate"] = decay_rate
            __props__.__dict__["description"] = description
            if domain is None and not opts.urn:
                raise TypeError("Missing required property 'domain'")
            __props__.__dict__["domain"] = domain
            __props__.__dict__["host_header"] = host_header
            __props__.__dict__["leader_string"] = leader_string
            __props__.__dict__["least_squares_decay"] = least_squares_decay
            __props__.__dict__["load_imbalance_percentage"] = load_imbalance_percentage
            __props__.__dict__["max_u_multiplicative_increment"] = max_u_multiplicative_increment
            __props__.__dict__["name"] = name
            __props__.__dict__["resource_instances"] = resource_instances
            if type is None and not opts.urn:
                raise TypeError("Missing required property 'type'")
            __props__.__dict__["type"] = type
            __props__.__dict__["upper_bound"] = upper_bound
            __props__.__dict__["wait_on_complete"] = wait_on_complete
        super(GtmResource, __self__).__init__(
            'akamai:trafficmanagement/gtmResource:GtmResource',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            aggregation_type: Optional[pulumi.Input[str]] = None,
            constrained_property: Optional[pulumi.Input[str]] = None,
            decay_rate: Optional[pulumi.Input[float]] = None,
            description: Optional[pulumi.Input[str]] = None,
            domain: Optional[pulumi.Input[str]] = None,
            host_header: Optional[pulumi.Input[str]] = None,
            leader_string: Optional[pulumi.Input[str]] = None,
            least_squares_decay: Optional[pulumi.Input[float]] = None,
            load_imbalance_percentage: Optional[pulumi.Input[float]] = None,
            max_u_multiplicative_increment: Optional[pulumi.Input[float]] = None,
            name: Optional[pulumi.Input[str]] = None,
            resource_instances: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['GtmResourceResourceInstanceArgs']]]]] = None,
            type: Optional[pulumi.Input[str]] = None,
            upper_bound: Optional[pulumi.Input[int]] = None,
            wait_on_complete: Optional[pulumi.Input[bool]] = None) -> 'GtmResource':
        """
        Get an existing GtmResource resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _GtmResourceState.__new__(_GtmResourceState)

        __props__.__dict__["aggregation_type"] = aggregation_type
        __props__.__dict__["constrained_property"] = constrained_property
        __props__.__dict__["decay_rate"] = decay_rate
        __props__.__dict__["description"] = description
        __props__.__dict__["domain"] = domain
        __props__.__dict__["host_header"] = host_header
        __props__.__dict__["leader_string"] = leader_string
        __props__.__dict__["least_squares_decay"] = least_squares_decay
        __props__.__dict__["load_imbalance_percentage"] = load_imbalance_percentage
        __props__.__dict__["max_u_multiplicative_increment"] = max_u_multiplicative_increment
        __props__.__dict__["name"] = name
        __props__.__dict__["resource_instances"] = resource_instances
        __props__.__dict__["type"] = type
        __props__.__dict__["upper_bound"] = upper_bound
        __props__.__dict__["wait_on_complete"] = wait_on_complete
        return GtmResource(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="aggregationType")
    def aggregation_type(self) -> pulumi.Output[str]:
        return pulumi.get(self, "aggregation_type")

    @property
    @pulumi.getter(name="constrainedProperty")
    def constrained_property(self) -> pulumi.Output[Optional[str]]:
        return pulumi.get(self, "constrained_property")

    @property
    @pulumi.getter(name="decayRate")
    def decay_rate(self) -> pulumi.Output[Optional[float]]:
        return pulumi.get(self, "decay_rate")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def domain(self) -> pulumi.Output[str]:
        return pulumi.get(self, "domain")

    @property
    @pulumi.getter(name="hostHeader")
    def host_header(self) -> pulumi.Output[Optional[str]]:
        return pulumi.get(self, "host_header")

    @property
    @pulumi.getter(name="leaderString")
    def leader_string(self) -> pulumi.Output[Optional[str]]:
        return pulumi.get(self, "leader_string")

    @property
    @pulumi.getter(name="leastSquaresDecay")
    def least_squares_decay(self) -> pulumi.Output[Optional[float]]:
        return pulumi.get(self, "least_squares_decay")

    @property
    @pulumi.getter(name="loadImbalancePercentage")
    def load_imbalance_percentage(self) -> pulumi.Output[Optional[float]]:
        return pulumi.get(self, "load_imbalance_percentage")

    @property
    @pulumi.getter(name="maxUMultiplicativeIncrement")
    def max_u_multiplicative_increment(self) -> pulumi.Output[Optional[float]]:
        return pulumi.get(self, "max_u_multiplicative_increment")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="resourceInstances")
    def resource_instances(self) -> pulumi.Output[Optional[Sequence['outputs.GtmResourceResourceInstance']]]:
        return pulumi.get(self, "resource_instances")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="upperBound")
    def upper_bound(self) -> pulumi.Output[Optional[int]]:
        return pulumi.get(self, "upper_bound")

    @property
    @pulumi.getter(name="waitOnComplete")
    def wait_on_complete(self) -> pulumi.Output[Optional[bool]]:
        return pulumi.get(self, "wait_on_complete")

