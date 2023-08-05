# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities

__all__ = [
    'GetAppSecSiemDefinitionsResult',
    'AwaitableGetAppSecSiemDefinitionsResult',
    'get_app_sec_siem_definitions',
    'get_app_sec_siem_definitions_output',
]

@pulumi.output_type
class GetAppSecSiemDefinitionsResult:
    """
    A collection of values returned by getAppSecSiemDefinitions.
    """
    def __init__(__self__, id=None, json=None, output_text=None, siem_definition_name=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if json and not isinstance(json, str):
            raise TypeError("Expected argument 'json' to be a str")
        pulumi.set(__self__, "json", json)
        if output_text and not isinstance(output_text, str):
            raise TypeError("Expected argument 'output_text' to be a str")
        pulumi.set(__self__, "output_text", output_text)
        if siem_definition_name and not isinstance(siem_definition_name, str):
            raise TypeError("Expected argument 'siem_definition_name' to be a str")
        pulumi.set(__self__, "siem_definition_name", siem_definition_name)

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
    @pulumi.getter(name="outputText")
    def output_text(self) -> str:
        return pulumi.get(self, "output_text")

    @property
    @pulumi.getter(name="siemDefinitionName")
    def siem_definition_name(self) -> Optional[str]:
        return pulumi.get(self, "siem_definition_name")


class AwaitableGetAppSecSiemDefinitionsResult(GetAppSecSiemDefinitionsResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetAppSecSiemDefinitionsResult(
            id=self.id,
            json=self.json,
            output_text=self.output_text,
            siem_definition_name=self.siem_definition_name)


def get_app_sec_siem_definitions(siem_definition_name: Optional[str] = None,
                                 opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetAppSecSiemDefinitionsResult:
    """
    **Scopes**: SIEM definition

    Returns information about your SIEM (Security Information and Event Management) versions. The returned information is described in the [Get SIEM versions](https://developer.akamai.com/api/cloud_security/application_security/v1.html#getsiemversions) section of the Application Security API.

    **Related API Endpoint**: [/appsec/v1/siem-definitions](https://developer.akamai.com/api/cloud_security/application_security/v1.html#getsiemversions)

    ## Example Usage

    Basic usage:

    ```python
    import pulumi
    import pulumi_akamai as akamai

    siem_definitions = akamai.get_app_sec_siem_definitions()
    pulumi.export("siemDefinitionsJson", siem_definitions.json)
    pulumi.export("siemDefinitionsOutput", siem_definitions.output_text)
    siem_definition = akamai.get_app_sec_siem_definitions(siem_definition_name="SIEM Version 01")
    pulumi.export("siemDefinitionId", siem_definition.id)
    ```
    ## Output Options

    The following options can be used to determine the information returned, and how that returned information is formatted:

    - `json`. JSON-formatted list of the SIEM version information.
    - `output_text`. Tabular report showing the ID and name of each SIEM version.


    :param str siem_definition_name: . Name of the SIEM definition you want to return information for. If not included, information is returned for all your SIEM definitions.
    """
    __args__ = dict()
    __args__['siemDefinitionName'] = siem_definition_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('akamai:index/getAppSecSiemDefinitions:getAppSecSiemDefinitions', __args__, opts=opts, typ=GetAppSecSiemDefinitionsResult).value

    return AwaitableGetAppSecSiemDefinitionsResult(
        id=__ret__.id,
        json=__ret__.json,
        output_text=__ret__.output_text,
        siem_definition_name=__ret__.siem_definition_name)


@_utilities.lift_output_func(get_app_sec_siem_definitions)
def get_app_sec_siem_definitions_output(siem_definition_name: Optional[pulumi.Input[Optional[str]]] = None,
                                        opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetAppSecSiemDefinitionsResult]:
    """
    **Scopes**: SIEM definition

    Returns information about your SIEM (Security Information and Event Management) versions. The returned information is described in the [Get SIEM versions](https://developer.akamai.com/api/cloud_security/application_security/v1.html#getsiemversions) section of the Application Security API.

    **Related API Endpoint**: [/appsec/v1/siem-definitions](https://developer.akamai.com/api/cloud_security/application_security/v1.html#getsiemversions)

    ## Example Usage

    Basic usage:

    ```python
    import pulumi
    import pulumi_akamai as akamai

    siem_definitions = akamai.get_app_sec_siem_definitions()
    pulumi.export("siemDefinitionsJson", siem_definitions.json)
    pulumi.export("siemDefinitionsOutput", siem_definitions.output_text)
    siem_definition = akamai.get_app_sec_siem_definitions(siem_definition_name="SIEM Version 01")
    pulumi.export("siemDefinitionId", siem_definition.id)
    ```
    ## Output Options

    The following options can be used to determine the information returned, and how that returned information is formatted:

    - `json`. JSON-formatted list of the SIEM version information.
    - `output_text`. Tabular report showing the ID and name of each SIEM version.


    :param str siem_definition_name: . Name of the SIEM definition you want to return information for. If not included, information is returned for all your SIEM definitions.
    """
    ...
