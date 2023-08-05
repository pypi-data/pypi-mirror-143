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
    'GetSystemGroupsResult',
    'AwaitableGetSystemGroupsResult',
    'get_system_groups',
    'get_system_groups_output',
]

@pulumi.output_type
class GetSystemGroupsResult:
    """
    A collection of values returned by getSystemGroups.
    """
    def __init__(__self__, groups=None, id=None, ids=None, in_protocol=None, name=None, name_regex=None, names=None, output_file=None, status=None):
        if groups and not isinstance(groups, list):
            raise TypeError("Expected argument 'groups' to be a list")
        pulumi.set(__self__, "groups", groups)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if ids and not isinstance(ids, list):
            raise TypeError("Expected argument 'ids' to be a list")
        pulumi.set(__self__, "ids", ids)
        if in_protocol and not isinstance(in_protocol, str):
            raise TypeError("Expected argument 'in_protocol' to be a str")
        pulumi.set(__self__, "in_protocol", in_protocol)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if name_regex and not isinstance(name_regex, str):
            raise TypeError("Expected argument 'name_regex' to be a str")
        pulumi.set(__self__, "name_regex", name_regex)
        if names and not isinstance(names, list):
            raise TypeError("Expected argument 'names' to be a list")
        pulumi.set(__self__, "names", names)
        if output_file and not isinstance(output_file, str):
            raise TypeError("Expected argument 'output_file' to be a str")
        pulumi.set(__self__, "output_file", output_file)
        if status and not isinstance(status, str):
            raise TypeError("Expected argument 'status' to be a str")
        pulumi.set(__self__, "status", status)

    @property
    @pulumi.getter
    def groups(self) -> Sequence['outputs.GetSystemGroupsGroupResult']:
        return pulumi.get(self, "groups")

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
    @pulumi.getter(name="inProtocol")
    def in_protocol(self) -> Optional[str]:
        return pulumi.get(self, "in_protocol")

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="nameRegex")
    def name_regex(self) -> Optional[str]:
        return pulumi.get(self, "name_regex")

    @property
    @pulumi.getter
    def names(self) -> Sequence[str]:
        return pulumi.get(self, "names")

    @property
    @pulumi.getter(name="outputFile")
    def output_file(self) -> Optional[str]:
        return pulumi.get(self, "output_file")

    @property
    @pulumi.getter
    def status(self) -> Optional[str]:
        return pulumi.get(self, "status")


class AwaitableGetSystemGroupsResult(GetSystemGroupsResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetSystemGroupsResult(
            groups=self.groups,
            id=self.id,
            ids=self.ids,
            in_protocol=self.in_protocol,
            name=self.name,
            name_regex=self.name_regex,
            names=self.names,
            output_file=self.output_file,
            status=self.status)


def get_system_groups(ids: Optional[Sequence[str]] = None,
                      in_protocol: Optional[str] = None,
                      name: Optional[str] = None,
                      name_regex: Optional[str] = None,
                      output_file: Optional[str] = None,
                      status: Optional[str] = None,
                      opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetSystemGroupsResult:
    """
    This data source provides the Video Surveillance System Groups of the current Alibaba Cloud user.

    > **NOTE:** Available in v1.135.0+.

    ## Example Usage

    Basic Usage

    ```python
    import pulumi
    import pulumi_alicloud as alicloud

    default_system_group = alicloud.videosurveillance.SystemGroup("defaultSystemGroup",
        group_name="groupname",
        in_protocol="rtmp",
        out_protocol="flv",
        play_domain="your_plan_domain",
        push_domain="your_push_domain")
    default_system_groups = alicloud.videosurveillance.get_system_groups_output(ids=[default_system_group.id])
    pulumi.export("vsGroup", default_system_groups.ids[0])
    ```


    :param Sequence[str] ids: A list of Group IDs.
    :param str in_protocol: The use of the access protocol support `gb28181`,`rtmp`(Real Time Messaging Protocol).
    :param str name: The name.
    :param str name_regex: A regex string to filter results by Group name.
    :param str status: The status. Valid values: `on`,`off`.
    """
    __args__ = dict()
    __args__['ids'] = ids
    __args__['inProtocol'] = in_protocol
    __args__['name'] = name
    __args__['nameRegex'] = name_regex
    __args__['outputFile'] = output_file
    __args__['status'] = status
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('alicloud:videosurveillance/getSystemGroups:getSystemGroups', __args__, opts=opts, typ=GetSystemGroupsResult).value

    return AwaitableGetSystemGroupsResult(
        groups=__ret__.groups,
        id=__ret__.id,
        ids=__ret__.ids,
        in_protocol=__ret__.in_protocol,
        name=__ret__.name,
        name_regex=__ret__.name_regex,
        names=__ret__.names,
        output_file=__ret__.output_file,
        status=__ret__.status)


@_utilities.lift_output_func(get_system_groups)
def get_system_groups_output(ids: Optional[pulumi.Input[Optional[Sequence[str]]]] = None,
                             in_protocol: Optional[pulumi.Input[Optional[str]]] = None,
                             name: Optional[pulumi.Input[Optional[str]]] = None,
                             name_regex: Optional[pulumi.Input[Optional[str]]] = None,
                             output_file: Optional[pulumi.Input[Optional[str]]] = None,
                             status: Optional[pulumi.Input[Optional[str]]] = None,
                             opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetSystemGroupsResult]:
    """
    This data source provides the Video Surveillance System Groups of the current Alibaba Cloud user.

    > **NOTE:** Available in v1.135.0+.

    ## Example Usage

    Basic Usage

    ```python
    import pulumi
    import pulumi_alicloud as alicloud

    default_system_group = alicloud.videosurveillance.SystemGroup("defaultSystemGroup",
        group_name="groupname",
        in_protocol="rtmp",
        out_protocol="flv",
        play_domain="your_plan_domain",
        push_domain="your_push_domain")
    default_system_groups = alicloud.videosurveillance.get_system_groups_output(ids=[default_system_group.id])
    pulumi.export("vsGroup", default_system_groups.ids[0])
    ```


    :param Sequence[str] ids: A list of Group IDs.
    :param str in_protocol: The use of the access protocol support `gb28181`,`rtmp`(Real Time Messaging Protocol).
    :param str name: The name.
    :param str name_regex: A regex string to filter results by Group name.
    :param str status: The status. Valid values: `on`,`off`.
    """
    ...
