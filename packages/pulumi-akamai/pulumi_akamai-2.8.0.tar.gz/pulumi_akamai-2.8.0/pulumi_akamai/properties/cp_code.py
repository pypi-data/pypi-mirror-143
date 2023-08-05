# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['CpCodeArgs', 'CpCode']

@pulumi.input_type
class CpCodeArgs:
    def __init__(__self__, *,
                 contract: Optional[pulumi.Input[str]] = None,
                 contract_id: Optional[pulumi.Input[str]] = None,
                 group: Optional[pulumi.Input[str]] = None,
                 group_id: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 product: Optional[pulumi.Input[str]] = None,
                 product_id: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a CpCode resource.
        """
        if contract is not None:
            warnings.warn("""The setting \"contract\" has been deprecated.""", DeprecationWarning)
            pulumi.log.warn("""contract is deprecated: The setting \"contract\" has been deprecated.""")
        if contract is not None:
            pulumi.set(__self__, "contract", contract)
        if contract_id is not None:
            pulumi.set(__self__, "contract_id", contract_id)
        if group is not None:
            warnings.warn("""The setting \"group\" has been deprecated.""", DeprecationWarning)
            pulumi.log.warn("""group is deprecated: The setting \"group\" has been deprecated.""")
        if group is not None:
            pulumi.set(__self__, "group", group)
        if group_id is not None:
            pulumi.set(__self__, "group_id", group_id)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if product is not None:
            warnings.warn("""The setting \"product\" has been deprecated.""", DeprecationWarning)
            pulumi.log.warn("""product is deprecated: The setting \"product\" has been deprecated.""")
        if product is not None:
            pulumi.set(__self__, "product", product)
        if product_id is not None:
            pulumi.set(__self__, "product_id", product_id)

    @property
    @pulumi.getter
    def contract(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "contract")

    @contract.setter
    def contract(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "contract", value)

    @property
    @pulumi.getter(name="contractId")
    def contract_id(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "contract_id")

    @contract_id.setter
    def contract_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "contract_id", value)

    @property
    @pulumi.getter
    def group(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "group")

    @group.setter
    def group(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "group", value)

    @property
    @pulumi.getter(name="groupId")
    def group_id(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "group_id")

    @group_id.setter
    def group_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "group_id", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def product(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "product")

    @product.setter
    def product(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "product", value)

    @property
    @pulumi.getter(name="productId")
    def product_id(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "product_id")

    @product_id.setter
    def product_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "product_id", value)


@pulumi.input_type
class _CpCodeState:
    def __init__(__self__, *,
                 contract: Optional[pulumi.Input[str]] = None,
                 contract_id: Optional[pulumi.Input[str]] = None,
                 group: Optional[pulumi.Input[str]] = None,
                 group_id: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 product: Optional[pulumi.Input[str]] = None,
                 product_id: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering CpCode resources.
        """
        if contract is not None:
            warnings.warn("""The setting \"contract\" has been deprecated.""", DeprecationWarning)
            pulumi.log.warn("""contract is deprecated: The setting \"contract\" has been deprecated.""")
        if contract is not None:
            pulumi.set(__self__, "contract", contract)
        if contract_id is not None:
            pulumi.set(__self__, "contract_id", contract_id)
        if group is not None:
            warnings.warn("""The setting \"group\" has been deprecated.""", DeprecationWarning)
            pulumi.log.warn("""group is deprecated: The setting \"group\" has been deprecated.""")
        if group is not None:
            pulumi.set(__self__, "group", group)
        if group_id is not None:
            pulumi.set(__self__, "group_id", group_id)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if product is not None:
            warnings.warn("""The setting \"product\" has been deprecated.""", DeprecationWarning)
            pulumi.log.warn("""product is deprecated: The setting \"product\" has been deprecated.""")
        if product is not None:
            pulumi.set(__self__, "product", product)
        if product_id is not None:
            pulumi.set(__self__, "product_id", product_id)

    @property
    @pulumi.getter
    def contract(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "contract")

    @contract.setter
    def contract(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "contract", value)

    @property
    @pulumi.getter(name="contractId")
    def contract_id(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "contract_id")

    @contract_id.setter
    def contract_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "contract_id", value)

    @property
    @pulumi.getter
    def group(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "group")

    @group.setter
    def group(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "group", value)

    @property
    @pulumi.getter(name="groupId")
    def group_id(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "group_id")

    @group_id.setter
    def group_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "group_id", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def product(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "product")

    @product.setter
    def product(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "product", value)

    @property
    @pulumi.getter(name="productId")
    def product_id(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "product_id")

    @product_id.setter
    def product_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "product_id", value)


warnings.warn("""akamai.properties.CpCode has been deprecated in favor of akamai.CpCode""", DeprecationWarning)


class CpCode(pulumi.CustomResource):
    warnings.warn("""akamai.properties.CpCode has been deprecated in favor of akamai.CpCode""", DeprecationWarning)

    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 contract: Optional[pulumi.Input[str]] = None,
                 contract_id: Optional[pulumi.Input[str]] = None,
                 group: Optional[pulumi.Input[str]] = None,
                 group_id: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 product: Optional[pulumi.Input[str]] = None,
                 product_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Create a CpCode resource with the given unique name, props, and options.
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: Optional[CpCodeArgs] = None,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Create a CpCode resource with the given unique name, props, and options.
        :param str resource_name: The name of the resource.
        :param CpCodeArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(CpCodeArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 contract: Optional[pulumi.Input[str]] = None,
                 contract_id: Optional[pulumi.Input[str]] = None,
                 group: Optional[pulumi.Input[str]] = None,
                 group_id: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 product: Optional[pulumi.Input[str]] = None,
                 product_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        pulumi.log.warn("""CpCode is deprecated: akamai.properties.CpCode has been deprecated in favor of akamai.CpCode""")
        if opts is None:
            opts = pulumi.ResourceOptions()
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.version is None:
            opts.version = _utilities.get_version()
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = CpCodeArgs.__new__(CpCodeArgs)

            if contract is not None and not opts.urn:
                warnings.warn("""The setting \"contract\" has been deprecated.""", DeprecationWarning)
                pulumi.log.warn("""contract is deprecated: The setting \"contract\" has been deprecated.""")
            __props__.__dict__["contract"] = contract
            __props__.__dict__["contract_id"] = contract_id
            if group is not None and not opts.urn:
                warnings.warn("""The setting \"group\" has been deprecated.""", DeprecationWarning)
                pulumi.log.warn("""group is deprecated: The setting \"group\" has been deprecated.""")
            __props__.__dict__["group"] = group
            __props__.__dict__["group_id"] = group_id
            __props__.__dict__["name"] = name
            if product is not None and not opts.urn:
                warnings.warn("""The setting \"product\" has been deprecated.""", DeprecationWarning)
                pulumi.log.warn("""product is deprecated: The setting \"product\" has been deprecated.""")
            __props__.__dict__["product"] = product
            __props__.__dict__["product_id"] = product_id
        super(CpCode, __self__).__init__(
            'akamai:properties/cpCode:CpCode',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            contract: Optional[pulumi.Input[str]] = None,
            contract_id: Optional[pulumi.Input[str]] = None,
            group: Optional[pulumi.Input[str]] = None,
            group_id: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            product: Optional[pulumi.Input[str]] = None,
            product_id: Optional[pulumi.Input[str]] = None) -> 'CpCode':
        """
        Get an existing CpCode resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _CpCodeState.__new__(_CpCodeState)

        __props__.__dict__["contract"] = contract
        __props__.__dict__["contract_id"] = contract_id
        __props__.__dict__["group"] = group
        __props__.__dict__["group_id"] = group_id
        __props__.__dict__["name"] = name
        __props__.__dict__["product"] = product
        __props__.__dict__["product_id"] = product_id
        return CpCode(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def contract(self) -> pulumi.Output[str]:
        return pulumi.get(self, "contract")

    @property
    @pulumi.getter(name="contractId")
    def contract_id(self) -> pulumi.Output[str]:
        return pulumi.get(self, "contract_id")

    @property
    @pulumi.getter
    def group(self) -> pulumi.Output[str]:
        return pulumi.get(self, "group")

    @property
    @pulumi.getter(name="groupId")
    def group_id(self) -> pulumi.Output[str]:
        return pulumi.get(self, "group_id")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def product(self) -> pulumi.Output[str]:
        return pulumi.get(self, "product")

    @property
    @pulumi.getter(name="productId")
    def product_id(self) -> pulumi.Output[str]:
        return pulumi.get(self, "product_id")

