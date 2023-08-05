# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs

__all__ = [
    'GetBgpNetworksResult',
    'AwaitableGetBgpNetworksResult',
    'get_bgp_networks',
    'get_bgp_networks_output',
]

@pulumi.output_type
class GetBgpNetworksResult:
    """
    A collection of values returned by getBgpNetworks.
    """
    def __init__(__self__, id=None, ids=None, networks=None, output_file=None, router_id=None, status=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if ids and not isinstance(ids, list):
            raise TypeError("Expected argument 'ids' to be a list")
        pulumi.set(__self__, "ids", ids)
        if networks and not isinstance(networks, list):
            raise TypeError("Expected argument 'networks' to be a list")
        pulumi.set(__self__, "networks", networks)
        if output_file and not isinstance(output_file, str):
            raise TypeError("Expected argument 'output_file' to be a str")
        pulumi.set(__self__, "output_file", output_file)
        if router_id and not isinstance(router_id, str):
            raise TypeError("Expected argument 'router_id' to be a str")
        pulumi.set(__self__, "router_id", router_id)
        if status and not isinstance(status, str):
            raise TypeError("Expected argument 'status' to be a str")
        pulumi.set(__self__, "status", status)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def ids(self) -> Sequence[str]:
        return pulumi.get(self, "ids")

    @property
    @pulumi.getter
    def networks(self) -> Sequence['outputs.GetBgpNetworksNetworkResult']:
        return pulumi.get(self, "networks")

    @property
    @pulumi.getter(name="outputFile")
    def output_file(self) -> Optional[str]:
        return pulumi.get(self, "output_file")

    @property
    @pulumi.getter(name="routerId")
    def router_id(self) -> Optional[str]:
        return pulumi.get(self, "router_id")

    @property
    @pulumi.getter
    def status(self) -> Optional[str]:
        return pulumi.get(self, "status")


class AwaitableGetBgpNetworksResult(GetBgpNetworksResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetBgpNetworksResult(
            id=self.id,
            ids=self.ids,
            networks=self.networks,
            output_file=self.output_file,
            router_id=self.router_id,
            status=self.status)


def get_bgp_networks(ids: Optional[Sequence[str]] = None,
                     output_file: Optional[str] = None,
                     router_id: Optional[str] = None,
                     status: Optional[str] = None,
                     opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetBgpNetworksResult:
    """
    This data source provides the Vpc Bgp Networks of the current Alibaba Cloud user.

    > **NOTE:** Available in v1.153.0+.

    ## Example Usage

    Basic Usage

    ```python
    import pulumi
    import pulumi_alicloud as alicloud

    ids = alicloud.vpc.get_bgp_networks(ids=["example_value"])
    pulumi.export("vpcBgpNetworkId1", ids.networks[0].id)
    router_id = alicloud.vpc.get_bgp_networks(router_id="example_value")
    pulumi.export("vpcBgpNetworkId2", router_id.networks[0].id)
    status = alicloud.vpc.get_bgp_networks(status="Available")
    pulumi.export("vpcBgpNetworkId3", status.networks[0].id)
    ```


    :param Sequence[str] ids: A list of Bgp Network IDs.
    :param str router_id: The ID of the vRouter.
    :param str status: The state of the advertised BGP network.
    """
    __args__ = dict()
    __args__['ids'] = ids
    __args__['outputFile'] = output_file
    __args__['routerId'] = router_id
    __args__['status'] = status
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('alicloud:vpc/getBgpNetworks:getBgpNetworks', __args__, opts=opts, typ=GetBgpNetworksResult).value

    return AwaitableGetBgpNetworksResult(
        id=__ret__.id,
        ids=__ret__.ids,
        networks=__ret__.networks,
        output_file=__ret__.output_file,
        router_id=__ret__.router_id,
        status=__ret__.status)


@_utilities.lift_output_func(get_bgp_networks)
def get_bgp_networks_output(ids: Optional[pulumi.Input[Optional[Sequence[str]]]] = None,
                            output_file: Optional[pulumi.Input[Optional[str]]] = None,
                            router_id: Optional[pulumi.Input[Optional[str]]] = None,
                            status: Optional[pulumi.Input[Optional[str]]] = None,
                            opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetBgpNetworksResult]:
    """
    This data source provides the Vpc Bgp Networks of the current Alibaba Cloud user.

    > **NOTE:** Available in v1.153.0+.

    ## Example Usage

    Basic Usage

    ```python
    import pulumi
    import pulumi_alicloud as alicloud

    ids = alicloud.vpc.get_bgp_networks(ids=["example_value"])
    pulumi.export("vpcBgpNetworkId1", ids.networks[0].id)
    router_id = alicloud.vpc.get_bgp_networks(router_id="example_value")
    pulumi.export("vpcBgpNetworkId2", router_id.networks[0].id)
    status = alicloud.vpc.get_bgp_networks(status="Available")
    pulumi.export("vpcBgpNetworkId3", status.networks[0].id)
    ```


    :param Sequence[str] ids: A list of Bgp Network IDs.
    :param str router_id: The ID of the vRouter.
    :param str status: The state of the advertised BGP network.
    """
    ...
