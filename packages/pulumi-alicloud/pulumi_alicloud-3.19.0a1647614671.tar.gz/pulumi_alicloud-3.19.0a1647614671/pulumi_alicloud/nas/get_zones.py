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
    'GetZonesResult',
    'AwaitableGetZonesResult',
    'get_zones',
    'get_zones_output',
]

@pulumi.output_type
class GetZonesResult:
    """
    A collection of values returned by getZones.
    """
    def __init__(__self__, file_system_type=None, id=None, output_file=None, zones=None):
        if file_system_type and not isinstance(file_system_type, str):
            raise TypeError("Expected argument 'file_system_type' to be a str")
        pulumi.set(__self__, "file_system_type", file_system_type)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if output_file and not isinstance(output_file, str):
            raise TypeError("Expected argument 'output_file' to be a str")
        pulumi.set(__self__, "output_file", output_file)
        if zones and not isinstance(zones, list):
            raise TypeError("Expected argument 'zones' to be a list")
        pulumi.set(__self__, "zones", zones)

    @property
    @pulumi.getter(name="fileSystemType")
    def file_system_type(self) -> Optional[str]:
        return pulumi.get(self, "file_system_type")

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
    def zones(self) -> Sequence['outputs.GetZonesZoneResult']:
        """
        A list of availability zone information collection.
        """
        return pulumi.get(self, "zones")


class AwaitableGetZonesResult(GetZonesResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetZonesResult(
            file_system_type=self.file_system_type,
            id=self.id,
            output_file=self.output_file,
            zones=self.zones)


def get_zones(file_system_type: Optional[str] = None,
              output_file: Optional[str] = None,
              opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetZonesResult:
    """
    Provide  a data source to retrieve the type of zone used to create NAS file system.

    > **NOTE:** Available in v1.140.0+.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_alicloud as alicloud

    default = alicloud.nas.get_zones()
    pulumi.export("alicloudNasZonesId", default.zones[0].zone_id)
    ```


    :param str file_system_type: The type of the file system.  Valid values: `standard`, `extreme`, `cpfs`.
    """
    __args__ = dict()
    __args__['fileSystemType'] = file_system_type
    __args__['outputFile'] = output_file
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('alicloud:nas/getZones:getZones', __args__, opts=opts, typ=GetZonesResult).value

    return AwaitableGetZonesResult(
        file_system_type=__ret__.file_system_type,
        id=__ret__.id,
        output_file=__ret__.output_file,
        zones=__ret__.zones)


@_utilities.lift_output_func(get_zones)
def get_zones_output(file_system_type: Optional[pulumi.Input[Optional[str]]] = None,
                     output_file: Optional[pulumi.Input[Optional[str]]] = None,
                     opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetZonesResult]:
    """
    Provide  a data source to retrieve the type of zone used to create NAS file system.

    > **NOTE:** Available in v1.140.0+.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_alicloud as alicloud

    default = alicloud.nas.get_zones()
    pulumi.export("alicloudNasZonesId", default.zones[0].zone_id)
    ```


    :param str file_system_type: The type of the file system.  Valid values: `standard`, `extreme`, `cpfs`.
    """
    ...
