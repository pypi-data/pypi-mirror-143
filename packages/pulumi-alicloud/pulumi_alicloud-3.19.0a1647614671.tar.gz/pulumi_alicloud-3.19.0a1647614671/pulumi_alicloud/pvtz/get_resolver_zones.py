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
    'GetResolverZonesResult',
    'AwaitableGetResolverZonesResult',
    'get_resolver_zones',
    'get_resolver_zones_output',
]

@pulumi.output_type
class GetResolverZonesResult:
    """
    A collection of values returned by getResolverZones.
    """
    def __init__(__self__, id=None, output_file=None, status=None, zones=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if output_file and not isinstance(output_file, str):
            raise TypeError("Expected argument 'output_file' to be a str")
        pulumi.set(__self__, "output_file", output_file)
        if status and not isinstance(status, str):
            raise TypeError("Expected argument 'status' to be a str")
        pulumi.set(__self__, "status", status)
        if zones and not isinstance(zones, list):
            raise TypeError("Expected argument 'zones' to be a list")
        pulumi.set(__self__, "zones", zones)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="outputFile")
    def output_file(self) -> Optional[str]:
        return pulumi.get(self, "output_file")

    @property
    @pulumi.getter
    def status(self) -> Optional[str]:
        return pulumi.get(self, "status")

    @property
    @pulumi.getter
    def zones(self) -> Sequence['outputs.GetResolverZonesZoneResult']:
        return pulumi.get(self, "zones")


class AwaitableGetResolverZonesResult(GetResolverZonesResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetResolverZonesResult(
            id=self.id,
            output_file=self.output_file,
            status=self.status,
            zones=self.zones)


def get_resolver_zones(output_file: Optional[str] = None,
                       status: Optional[str] = None,
                       opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetResolverZonesResult:
    """
    This data source provides the available zones with the Private Zone Resolver of the current Alibaba Cloud user.

    > **NOTE:** Available in v1.143.0+.

    ## Example Usage

    Basic Usage

    ```python
    import pulumi
    import pulumi_alicloud as alicloud

    default = alicloud.pvtz.get_resolver_zones(status="NORMAL")
    pulumi.export("firstZonesId", default.zones[0].zone_id)
    ```


    :param str status: The status of the Zone.
    """
    __args__ = dict()
    __args__['outputFile'] = output_file
    __args__['status'] = status
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('alicloud:pvtz/getResolverZones:getResolverZones', __args__, opts=opts, typ=GetResolverZonesResult).value

    return AwaitableGetResolverZonesResult(
        id=__ret__.id,
        output_file=__ret__.output_file,
        status=__ret__.status,
        zones=__ret__.zones)


@_utilities.lift_output_func(get_resolver_zones)
def get_resolver_zones_output(output_file: Optional[pulumi.Input[Optional[str]]] = None,
                              status: Optional[pulumi.Input[Optional[str]]] = None,
                              opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetResolverZonesResult]:
    """
    This data source provides the available zones with the Private Zone Resolver of the current Alibaba Cloud user.

    > **NOTE:** Available in v1.143.0+.

    ## Example Usage

    Basic Usage

    ```python
    import pulumi
    import pulumi_alicloud as alicloud

    default = alicloud.pvtz.get_resolver_zones(status="NORMAL")
    pulumi.export("firstZonesId", default.zones[0].zone_id)
    ```


    :param str status: The status of the Zone.
    """
    ...
