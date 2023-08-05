# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities

__all__ = [
    'GetNetworkListsResult',
    'AwaitableGetNetworkListsResult',
    'get_network_lists',
    'get_network_lists_output',
]

@pulumi.output_type
class GetNetworkListsResult:
    """
    A collection of values returned by getNetworkLists.
    """
    def __init__(__self__, contract_id=None, group_id=None, id=None, json=None, lists=None, name=None, network_list_id=None, output_text=None, type=None):
        if contract_id and not isinstance(contract_id, str):
            raise TypeError("Expected argument 'contract_id' to be a str")
        pulumi.set(__self__, "contract_id", contract_id)
        if group_id and not isinstance(group_id, int):
            raise TypeError("Expected argument 'group_id' to be a int")
        pulumi.set(__self__, "group_id", group_id)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if json and not isinstance(json, str):
            raise TypeError("Expected argument 'json' to be a str")
        pulumi.set(__self__, "json", json)
        if lists and not isinstance(lists, list):
            raise TypeError("Expected argument 'lists' to be a list")
        pulumi.set(__self__, "lists", lists)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if network_list_id and not isinstance(network_list_id, str):
            raise TypeError("Expected argument 'network_list_id' to be a str")
        pulumi.set(__self__, "network_list_id", network_list_id)
        if output_text and not isinstance(output_text, str):
            raise TypeError("Expected argument 'output_text' to be a str")
        pulumi.set(__self__, "output_text", output_text)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="contractId")
    def contract_id(self) -> str:
        return pulumi.get(self, "contract_id")

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
    @pulumi.getter
    def json(self) -> str:
        """
        A JSON-formatted list of information about the specified network list(s).
        """
        return pulumi.get(self, "json")

    @property
    @pulumi.getter
    def lists(self) -> Sequence[str]:
        """
        A list containing the IDs of the specified network lists(s).
        """
        return pulumi.get(self, "lists")

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="networkListId")
    def network_list_id(self) -> str:
        return pulumi.get(self, "network_list_id")

    @property
    @pulumi.getter(name="outputText")
    def output_text(self) -> str:
        """
        A tabular display showing the network list information.
        """
        return pulumi.get(self, "output_text")

    @property
    @pulumi.getter
    def type(self) -> Optional[str]:
        return pulumi.get(self, "type")


class AwaitableGetNetworkListsResult(GetNetworkListsResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetNetworkListsResult(
            contract_id=self.contract_id,
            group_id=self.group_id,
            id=self.id,
            json=self.json,
            lists=self.lists,
            name=self.name,
            network_list_id=self.network_list_id,
            output_text=self.output_text,
            type=self.type)


def get_network_lists(name: Optional[str] = None,
                      network_list_id: Optional[str] = None,
                      type: Optional[str] = None,
                      opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetNetworkListsResult:
    """
    Use the `get_network_lists` data source to retrieve information about the available network lists,
    optionally filtered by list type or based on a search string. The information available is described
    [here](https://developer.akamai.com/api/cloud_security/network_lists/v2.html#getlists).

    ## Example Usage

    Basic usage:

    ```python
    import pulumi
    import pulumi_akamai as akamai

    network_lists = akamai.get_network_lists()
    pulumi.export("networkListsText", network_lists.output_text)
    pulumi.export("networkListsJson", network_lists.json)
    pulumi.export("networkListsList", network_lists.lists)
    network_lists_filter = akamai.get_network_lists(name="Test Whitelist",
        type="IP")
    pulumi.export("networkListsFilterText", network_lists_filter.output_text)
    pulumi.export("networkListsFilterJson", network_lists_filter.json)
    pulumi.export("networkListsFilterList", network_lists_filter.lists)
    ```


    :param str name: The name of a specific network list to retrieve. If not supplied, information about all network
           lists will be returned.
    :param str network_list_id: The ID of a specific network list to retrieve.
           If not supplied, information about all network lists will be returned.
    :param str type: The type of network lists to be retrieved; must be either "IP" or "GEO". If not supplied,
           information about both types will be returned.
    """
    __args__ = dict()
    __args__['name'] = name
    __args__['networkListId'] = network_list_id
    __args__['type'] = type
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('akamai:index/getNetworkLists:getNetworkLists', __args__, opts=opts, typ=GetNetworkListsResult).value

    return AwaitableGetNetworkListsResult(
        contract_id=__ret__.contract_id,
        group_id=__ret__.group_id,
        id=__ret__.id,
        json=__ret__.json,
        lists=__ret__.lists,
        name=__ret__.name,
        network_list_id=__ret__.network_list_id,
        output_text=__ret__.output_text,
        type=__ret__.type)


@_utilities.lift_output_func(get_network_lists)
def get_network_lists_output(name: Optional[pulumi.Input[Optional[str]]] = None,
                             network_list_id: Optional[pulumi.Input[Optional[str]]] = None,
                             type: Optional[pulumi.Input[Optional[str]]] = None,
                             opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetNetworkListsResult]:
    """
    Use the `get_network_lists` data source to retrieve information about the available network lists,
    optionally filtered by list type or based on a search string. The information available is described
    [here](https://developer.akamai.com/api/cloud_security/network_lists/v2.html#getlists).

    ## Example Usage

    Basic usage:

    ```python
    import pulumi
    import pulumi_akamai as akamai

    network_lists = akamai.get_network_lists()
    pulumi.export("networkListsText", network_lists.output_text)
    pulumi.export("networkListsJson", network_lists.json)
    pulumi.export("networkListsList", network_lists.lists)
    network_lists_filter = akamai.get_network_lists(name="Test Whitelist",
        type="IP")
    pulumi.export("networkListsFilterText", network_lists_filter.output_text)
    pulumi.export("networkListsFilterJson", network_lists_filter.json)
    pulumi.export("networkListsFilterList", network_lists_filter.lists)
    ```


    :param str name: The name of a specific network list to retrieve. If not supplied, information about all network
           lists will be returned.
    :param str network_list_id: The ID of a specific network list to retrieve.
           If not supplied, information about all network lists will be returned.
    :param str type: The type of network lists to be retrieved; must be either "IP" or "GEO". If not supplied,
           information about both types will be returned.
    """
    ...
