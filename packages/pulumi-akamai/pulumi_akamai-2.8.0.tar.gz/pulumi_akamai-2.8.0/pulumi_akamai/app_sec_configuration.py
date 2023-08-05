# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities

__all__ = ['AppSecConfigurationArgs', 'AppSecConfiguration']

@pulumi.input_type
class AppSecConfigurationArgs:
    def __init__(__self__, *,
                 contract_id: pulumi.Input[str],
                 description: pulumi.Input[str],
                 group_id: pulumi.Input[int],
                 host_names: pulumi.Input[Sequence[pulumi.Input[str]]],
                 create_from_config_id: Optional[pulumi.Input[int]] = None,
                 create_from_version: Optional[pulumi.Input[int]] = None,
                 name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a AppSecConfiguration resource.
        :param pulumi.Input[str] contract_id: . Unique identifier of the Akamai contract t associated with the new configuration.
        :param pulumi.Input[str] description: . Brief description of the new configuration.
        :param pulumi.Input[int] group_id: . Unique identifier of the contract group associated with the new configuration.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] host_names: . JSON array containing the hostnames to be protected by the new configuration. You must specify at least one hostname in order to create a new configuration.
        :param pulumi.Input[int] create_from_config_id: . Unique identifier of the existing configuration being cloned in order to create the new configuration.
        :param pulumi.Input[int] create_from_version: . Version number of the security configuration being cloned.
        :param pulumi.Input[str] name: . Name of the new configuration.
        """
        pulumi.set(__self__, "contract_id", contract_id)
        pulumi.set(__self__, "description", description)
        pulumi.set(__self__, "group_id", group_id)
        pulumi.set(__self__, "host_names", host_names)
        if create_from_config_id is not None:
            pulumi.set(__self__, "create_from_config_id", create_from_config_id)
        if create_from_version is not None:
            pulumi.set(__self__, "create_from_version", create_from_version)
        if name is not None:
            pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter(name="contractId")
    def contract_id(self) -> pulumi.Input[str]:
        """
        . Unique identifier of the Akamai contract t associated with the new configuration.
        """
        return pulumi.get(self, "contract_id")

    @contract_id.setter
    def contract_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "contract_id", value)

    @property
    @pulumi.getter
    def description(self) -> pulumi.Input[str]:
        """
        . Brief description of the new configuration.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: pulumi.Input[str]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="groupId")
    def group_id(self) -> pulumi.Input[int]:
        """
        . Unique identifier of the contract group associated with the new configuration.
        """
        return pulumi.get(self, "group_id")

    @group_id.setter
    def group_id(self, value: pulumi.Input[int]):
        pulumi.set(self, "group_id", value)

    @property
    @pulumi.getter(name="hostNames")
    def host_names(self) -> pulumi.Input[Sequence[pulumi.Input[str]]]:
        """
        . JSON array containing the hostnames to be protected by the new configuration. You must specify at least one hostname in order to create a new configuration.
        """
        return pulumi.get(self, "host_names")

    @host_names.setter
    def host_names(self, value: pulumi.Input[Sequence[pulumi.Input[str]]]):
        pulumi.set(self, "host_names", value)

    @property
    @pulumi.getter(name="createFromConfigId")
    def create_from_config_id(self) -> Optional[pulumi.Input[int]]:
        """
        . Unique identifier of the existing configuration being cloned in order to create the new configuration.
        """
        return pulumi.get(self, "create_from_config_id")

    @create_from_config_id.setter
    def create_from_config_id(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "create_from_config_id", value)

    @property
    @pulumi.getter(name="createFromVersion")
    def create_from_version(self) -> Optional[pulumi.Input[int]]:
        """
        . Version number of the security configuration being cloned.
        """
        return pulumi.get(self, "create_from_version")

    @create_from_version.setter
    def create_from_version(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "create_from_version", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        . Name of the new configuration.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)


@pulumi.input_type
class _AppSecConfigurationState:
    def __init__(__self__, *,
                 config_id: Optional[pulumi.Input[int]] = None,
                 contract_id: Optional[pulumi.Input[str]] = None,
                 create_from_config_id: Optional[pulumi.Input[int]] = None,
                 create_from_version: Optional[pulumi.Input[int]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 group_id: Optional[pulumi.Input[int]] = None,
                 host_names: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 name: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering AppSecConfiguration resources.
        :param pulumi.Input[str] contract_id: . Unique identifier of the Akamai contract t associated with the new configuration.
        :param pulumi.Input[int] create_from_config_id: . Unique identifier of the existing configuration being cloned in order to create the new configuration.
        :param pulumi.Input[int] create_from_version: . Version number of the security configuration being cloned.
        :param pulumi.Input[str] description: . Brief description of the new configuration.
        :param pulumi.Input[int] group_id: . Unique identifier of the contract group associated with the new configuration.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] host_names: . JSON array containing the hostnames to be protected by the new configuration. You must specify at least one hostname in order to create a new configuration.
        :param pulumi.Input[str] name: . Name of the new configuration.
        """
        if config_id is not None:
            pulumi.set(__self__, "config_id", config_id)
        if contract_id is not None:
            pulumi.set(__self__, "contract_id", contract_id)
        if create_from_config_id is not None:
            pulumi.set(__self__, "create_from_config_id", create_from_config_id)
        if create_from_version is not None:
            pulumi.set(__self__, "create_from_version", create_from_version)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if group_id is not None:
            pulumi.set(__self__, "group_id", group_id)
        if host_names is not None:
            pulumi.set(__self__, "host_names", host_names)
        if name is not None:
            pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter(name="configId")
    def config_id(self) -> Optional[pulumi.Input[int]]:
        return pulumi.get(self, "config_id")

    @config_id.setter
    def config_id(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "config_id", value)

    @property
    @pulumi.getter(name="contractId")
    def contract_id(self) -> Optional[pulumi.Input[str]]:
        """
        . Unique identifier of the Akamai contract t associated with the new configuration.
        """
        return pulumi.get(self, "contract_id")

    @contract_id.setter
    def contract_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "contract_id", value)

    @property
    @pulumi.getter(name="createFromConfigId")
    def create_from_config_id(self) -> Optional[pulumi.Input[int]]:
        """
        . Unique identifier of the existing configuration being cloned in order to create the new configuration.
        """
        return pulumi.get(self, "create_from_config_id")

    @create_from_config_id.setter
    def create_from_config_id(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "create_from_config_id", value)

    @property
    @pulumi.getter(name="createFromVersion")
    def create_from_version(self) -> Optional[pulumi.Input[int]]:
        """
        . Version number of the security configuration being cloned.
        """
        return pulumi.get(self, "create_from_version")

    @create_from_version.setter
    def create_from_version(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "create_from_version", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        . Brief description of the new configuration.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="groupId")
    def group_id(self) -> Optional[pulumi.Input[int]]:
        """
        . Unique identifier of the contract group associated with the new configuration.
        """
        return pulumi.get(self, "group_id")

    @group_id.setter
    def group_id(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "group_id", value)

    @property
    @pulumi.getter(name="hostNames")
    def host_names(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        . JSON array containing the hostnames to be protected by the new configuration. You must specify at least one hostname in order to create a new configuration.
        """
        return pulumi.get(self, "host_names")

    @host_names.setter
    def host_names(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "host_names", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        . Name of the new configuration.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)


class AppSecConfiguration(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 contract_id: Optional[pulumi.Input[str]] = None,
                 create_from_config_id: Optional[pulumi.Input[int]] = None,
                 create_from_version: Optional[pulumi.Input[int]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 group_id: Optional[pulumi.Input[int]] = None,
                 host_names: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        **Scopes**: Contract and group

        Creates a new WAP (Web Application Protector) or KSD (Kona Site Defender) security configuration. KSD security configurations start out empty (i.e., unconfigured), while WAP configurations are created using preset values. The contract referenced in the request body determines the type of configuration you can create.

        In addition to manually creating a new configuration, you can use the `create_from_config_id` argument to clone an existing configuration.

        **Related API Endpoint**: [/appsec/v1/configs](https://developer.akamai.com/api/cloud_security/application_security/v1.html#postconfigurations)

        ## Example Usage

        Basic usage:

        ```python
        import pulumi
        import pulumi_akamai as akamai

        selectable_hostnames = akamai.get_app_sec_selectable_hostnames(config_id="Documentation")
        create_config = akamai.AppSecConfiguration("createConfig",
            description="This configuration is used as a testing environment for the documentation team.",
            contract_id="5-2WA382",
            group_id=12198,
            host_names=[
                "documentation.akamai.com",
                "training.akamai.com",
            ])
        pulumi.export("createConfigId", create_config.config_id)
        clone_config = akamai.AppSecConfiguration("cloneConfig",
            description="This configuration is used as a testing environment for the documentation team.",
            create_from_config_id=data["akamai_appsec_configuration"]["configuration"]["config_id"],
            create_from_version=data["akamai_appsec_configuration"]["configuration"]["latest_version"],
            contract_id="5-2WA382",
            group_id=12198,
            host_names=selectable_hostnames.hostnames)
        pulumi.export("cloneConfigId", clone_config.config_id)
        ```
        ## Output Options

        The following options can be used to determine the information returned, and how that returned information is formatted:

        - `config_id`. ID of the new security configuration.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] contract_id: . Unique identifier of the Akamai contract t associated with the new configuration.
        :param pulumi.Input[int] create_from_config_id: . Unique identifier of the existing configuration being cloned in order to create the new configuration.
        :param pulumi.Input[int] create_from_version: . Version number of the security configuration being cloned.
        :param pulumi.Input[str] description: . Brief description of the new configuration.
        :param pulumi.Input[int] group_id: . Unique identifier of the contract group associated with the new configuration.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] host_names: . JSON array containing the hostnames to be protected by the new configuration. You must specify at least one hostname in order to create a new configuration.
        :param pulumi.Input[str] name: . Name of the new configuration.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: AppSecConfigurationArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        **Scopes**: Contract and group

        Creates a new WAP (Web Application Protector) or KSD (Kona Site Defender) security configuration. KSD security configurations start out empty (i.e., unconfigured), while WAP configurations are created using preset values. The contract referenced in the request body determines the type of configuration you can create.

        In addition to manually creating a new configuration, you can use the `create_from_config_id` argument to clone an existing configuration.

        **Related API Endpoint**: [/appsec/v1/configs](https://developer.akamai.com/api/cloud_security/application_security/v1.html#postconfigurations)

        ## Example Usage

        Basic usage:

        ```python
        import pulumi
        import pulumi_akamai as akamai

        selectable_hostnames = akamai.get_app_sec_selectable_hostnames(config_id="Documentation")
        create_config = akamai.AppSecConfiguration("createConfig",
            description="This configuration is used as a testing environment for the documentation team.",
            contract_id="5-2WA382",
            group_id=12198,
            host_names=[
                "documentation.akamai.com",
                "training.akamai.com",
            ])
        pulumi.export("createConfigId", create_config.config_id)
        clone_config = akamai.AppSecConfiguration("cloneConfig",
            description="This configuration is used as a testing environment for the documentation team.",
            create_from_config_id=data["akamai_appsec_configuration"]["configuration"]["config_id"],
            create_from_version=data["akamai_appsec_configuration"]["configuration"]["latest_version"],
            contract_id="5-2WA382",
            group_id=12198,
            host_names=selectable_hostnames.hostnames)
        pulumi.export("cloneConfigId", clone_config.config_id)
        ```
        ## Output Options

        The following options can be used to determine the information returned, and how that returned information is formatted:

        - `config_id`. ID of the new security configuration.

        :param str resource_name: The name of the resource.
        :param AppSecConfigurationArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(AppSecConfigurationArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 contract_id: Optional[pulumi.Input[str]] = None,
                 create_from_config_id: Optional[pulumi.Input[int]] = None,
                 create_from_version: Optional[pulumi.Input[int]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 group_id: Optional[pulumi.Input[int]] = None,
                 host_names: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
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
            __props__ = AppSecConfigurationArgs.__new__(AppSecConfigurationArgs)

            if contract_id is None and not opts.urn:
                raise TypeError("Missing required property 'contract_id'")
            __props__.__dict__["contract_id"] = contract_id
            __props__.__dict__["create_from_config_id"] = create_from_config_id
            __props__.__dict__["create_from_version"] = create_from_version
            if description is None and not opts.urn:
                raise TypeError("Missing required property 'description'")
            __props__.__dict__["description"] = description
            if group_id is None and not opts.urn:
                raise TypeError("Missing required property 'group_id'")
            __props__.__dict__["group_id"] = group_id
            if host_names is None and not opts.urn:
                raise TypeError("Missing required property 'host_names'")
            __props__.__dict__["host_names"] = host_names
            __props__.__dict__["name"] = name
            __props__.__dict__["config_id"] = None
        super(AppSecConfiguration, __self__).__init__(
            'akamai:index/appSecConfiguration:AppSecConfiguration',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            config_id: Optional[pulumi.Input[int]] = None,
            contract_id: Optional[pulumi.Input[str]] = None,
            create_from_config_id: Optional[pulumi.Input[int]] = None,
            create_from_version: Optional[pulumi.Input[int]] = None,
            description: Optional[pulumi.Input[str]] = None,
            group_id: Optional[pulumi.Input[int]] = None,
            host_names: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            name: Optional[pulumi.Input[str]] = None) -> 'AppSecConfiguration':
        """
        Get an existing AppSecConfiguration resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] contract_id: . Unique identifier of the Akamai contract t associated with the new configuration.
        :param pulumi.Input[int] create_from_config_id: . Unique identifier of the existing configuration being cloned in order to create the new configuration.
        :param pulumi.Input[int] create_from_version: . Version number of the security configuration being cloned.
        :param pulumi.Input[str] description: . Brief description of the new configuration.
        :param pulumi.Input[int] group_id: . Unique identifier of the contract group associated with the new configuration.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] host_names: . JSON array containing the hostnames to be protected by the new configuration. You must specify at least one hostname in order to create a new configuration.
        :param pulumi.Input[str] name: . Name of the new configuration.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _AppSecConfigurationState.__new__(_AppSecConfigurationState)

        __props__.__dict__["config_id"] = config_id
        __props__.__dict__["contract_id"] = contract_id
        __props__.__dict__["create_from_config_id"] = create_from_config_id
        __props__.__dict__["create_from_version"] = create_from_version
        __props__.__dict__["description"] = description
        __props__.__dict__["group_id"] = group_id
        __props__.__dict__["host_names"] = host_names
        __props__.__dict__["name"] = name
        return AppSecConfiguration(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="configId")
    def config_id(self) -> pulumi.Output[int]:
        return pulumi.get(self, "config_id")

    @property
    @pulumi.getter(name="contractId")
    def contract_id(self) -> pulumi.Output[str]:
        """
        . Unique identifier of the Akamai contract t associated with the new configuration.
        """
        return pulumi.get(self, "contract_id")

    @property
    @pulumi.getter(name="createFromConfigId")
    def create_from_config_id(self) -> pulumi.Output[Optional[int]]:
        """
        . Unique identifier of the existing configuration being cloned in order to create the new configuration.
        """
        return pulumi.get(self, "create_from_config_id")

    @property
    @pulumi.getter(name="createFromVersion")
    def create_from_version(self) -> pulumi.Output[Optional[int]]:
        """
        . Version number of the security configuration being cloned.
        """
        return pulumi.get(self, "create_from_version")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[str]:
        """
        . Brief description of the new configuration.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="groupId")
    def group_id(self) -> pulumi.Output[int]:
        """
        . Unique identifier of the contract group associated with the new configuration.
        """
        return pulumi.get(self, "group_id")

    @property
    @pulumi.getter(name="hostNames")
    def host_names(self) -> pulumi.Output[Sequence[str]]:
        """
        . JSON array containing the hostnames to be protected by the new configuration. You must specify at least one hostname in order to create a new configuration.
        """
        return pulumi.get(self, "host_names")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        . Name of the new configuration.
        """
        return pulumi.get(self, "name")

