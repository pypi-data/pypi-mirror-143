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
    'GetInstancesResult',
    'AwaitableGetInstancesResult',
    'get_instances',
    'get_instances_output',
]

@pulumi.output_type
class GetInstancesResult:
    """
    A collection of values returned by getInstances.
    """
    def __init__(__self__, availability_zone=None, id=None, ids=None, image_id=None, instances=None, name_regex=None, names=None, output_file=None, page_number=None, page_size=None, ram_role_name=None, resource_group_id=None, status=None, tags=None, total_count=None, vpc_id=None, vswitch_id=None):
        if availability_zone and not isinstance(availability_zone, str):
            raise TypeError("Expected argument 'availability_zone' to be a str")
        pulumi.set(__self__, "availability_zone", availability_zone)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if ids and not isinstance(ids, list):
            raise TypeError("Expected argument 'ids' to be a list")
        pulumi.set(__self__, "ids", ids)
        if image_id and not isinstance(image_id, str):
            raise TypeError("Expected argument 'image_id' to be a str")
        pulumi.set(__self__, "image_id", image_id)
        if instances and not isinstance(instances, list):
            raise TypeError("Expected argument 'instances' to be a list")
        pulumi.set(__self__, "instances", instances)
        if name_regex and not isinstance(name_regex, str):
            raise TypeError("Expected argument 'name_regex' to be a str")
        pulumi.set(__self__, "name_regex", name_regex)
        if names and not isinstance(names, list):
            raise TypeError("Expected argument 'names' to be a list")
        pulumi.set(__self__, "names", names)
        if output_file and not isinstance(output_file, str):
            raise TypeError("Expected argument 'output_file' to be a str")
        pulumi.set(__self__, "output_file", output_file)
        if page_number and not isinstance(page_number, int):
            raise TypeError("Expected argument 'page_number' to be a int")
        pulumi.set(__self__, "page_number", page_number)
        if page_size and not isinstance(page_size, int):
            raise TypeError("Expected argument 'page_size' to be a int")
        pulumi.set(__self__, "page_size", page_size)
        if ram_role_name and not isinstance(ram_role_name, str):
            raise TypeError("Expected argument 'ram_role_name' to be a str")
        pulumi.set(__self__, "ram_role_name", ram_role_name)
        if resource_group_id and not isinstance(resource_group_id, str):
            raise TypeError("Expected argument 'resource_group_id' to be a str")
        pulumi.set(__self__, "resource_group_id", resource_group_id)
        if status and not isinstance(status, str):
            raise TypeError("Expected argument 'status' to be a str")
        pulumi.set(__self__, "status", status)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if total_count and not isinstance(total_count, int):
            raise TypeError("Expected argument 'total_count' to be a int")
        pulumi.set(__self__, "total_count", total_count)
        if vpc_id and not isinstance(vpc_id, str):
            raise TypeError("Expected argument 'vpc_id' to be a str")
        pulumi.set(__self__, "vpc_id", vpc_id)
        if vswitch_id and not isinstance(vswitch_id, str):
            raise TypeError("Expected argument 'vswitch_id' to be a str")
        pulumi.set(__self__, "vswitch_id", vswitch_id)

    @property
    @pulumi.getter(name="availabilityZone")
    def availability_zone(self) -> Optional[str]:
        """
        Availability zone the instance belongs to.
        """
        return pulumi.get(self, "availability_zone")

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
        """
        A list of ECS instance IDs.
        """
        return pulumi.get(self, "ids")

    @property
    @pulumi.getter(name="imageId")
    def image_id(self) -> Optional[str]:
        """
        Image ID the instance is using.
        """
        return pulumi.get(self, "image_id")

    @property
    @pulumi.getter
    def instances(self) -> Sequence['outputs.GetInstancesInstanceResult']:
        """
        A list of instances. Each element contains the following attributes:
        """
        return pulumi.get(self, "instances")

    @property
    @pulumi.getter(name="nameRegex")
    def name_regex(self) -> Optional[str]:
        return pulumi.get(self, "name_regex")

    @property
    @pulumi.getter
    def names(self) -> Sequence[str]:
        """
        A list of instances names.
        """
        return pulumi.get(self, "names")

    @property
    @pulumi.getter(name="outputFile")
    def output_file(self) -> Optional[str]:
        return pulumi.get(self, "output_file")

    @property
    @pulumi.getter(name="pageNumber")
    def page_number(self) -> Optional[int]:
        return pulumi.get(self, "page_number")

    @property
    @pulumi.getter(name="pageSize")
    def page_size(self) -> Optional[int]:
        return pulumi.get(self, "page_size")

    @property
    @pulumi.getter(name="ramRoleName")
    def ram_role_name(self) -> Optional[str]:
        """
        The Ram role name.
        """
        return pulumi.get(self, "ram_role_name")

    @property
    @pulumi.getter(name="resourceGroupId")
    def resource_group_id(self) -> Optional[str]:
        """
        The Id of resource group.
        """
        return pulumi.get(self, "resource_group_id")

    @property
    @pulumi.getter
    def status(self) -> Optional[str]:
        """
        Instance current status.
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Mapping[str, Any]]:
        """
        A map of tags assigned to the ECS instance.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="totalCount")
    def total_count(self) -> int:
        return pulumi.get(self, "total_count")

    @property
    @pulumi.getter(name="vpcId")
    def vpc_id(self) -> Optional[str]:
        """
        ID of the VPC the instance belongs to.
        """
        return pulumi.get(self, "vpc_id")

    @property
    @pulumi.getter(name="vswitchId")
    def vswitch_id(self) -> Optional[str]:
        """
        ID of the VSwitch the instance belongs to.
        """
        return pulumi.get(self, "vswitch_id")


class AwaitableGetInstancesResult(GetInstancesResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetInstancesResult(
            availability_zone=self.availability_zone,
            id=self.id,
            ids=self.ids,
            image_id=self.image_id,
            instances=self.instances,
            name_regex=self.name_regex,
            names=self.names,
            output_file=self.output_file,
            page_number=self.page_number,
            page_size=self.page_size,
            ram_role_name=self.ram_role_name,
            resource_group_id=self.resource_group_id,
            status=self.status,
            tags=self.tags,
            total_count=self.total_count,
            vpc_id=self.vpc_id,
            vswitch_id=self.vswitch_id)


def get_instances(availability_zone: Optional[str] = None,
                  ids: Optional[Sequence[str]] = None,
                  image_id: Optional[str] = None,
                  name_regex: Optional[str] = None,
                  output_file: Optional[str] = None,
                  page_number: Optional[int] = None,
                  page_size: Optional[int] = None,
                  ram_role_name: Optional[str] = None,
                  resource_group_id: Optional[str] = None,
                  status: Optional[str] = None,
                  tags: Optional[Mapping[str, Any]] = None,
                  vpc_id: Optional[str] = None,
                  vswitch_id: Optional[str] = None,
                  opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetInstancesResult:
    """
    The Instances data source list ECS instance resources according to their ID, name regex, image id, status and other fields.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_alicloud as alicloud

    instances_ds = alicloud.ecs.get_instances(name_regex="web_server",
        status="Running")
    pulumi.export("firstInstanceId", instances_ds.instances[0].id)
    pulumi.export("instanceIds", instances_ds.ids)
    ```


    :param str availability_zone: Availability zone where instances are located.
    :param Sequence[str] ids: A list of ECS instance IDs.
    :param str image_id: The image ID of some ECS instance used.
    :param str name_regex: A regex string to filter results by instance name.
    :param str ram_role_name: The RAM role name which the instance attaches.
    :param str resource_group_id: The Id of resource group which the instance belongs.
    :param str status: Instance status. Valid values: "Creating", "Starting", "Running", "Stopping" and "Stopped". If undefined, all statuses are considered.
    :param Mapping[str, Any] tags: A map of tags assigned to the ECS instances. It must be in the format:
           ```python
           import pulumi
           import pulumi_alicloud as alicloud
           
           tagged_instances = alicloud.ecs.get_instances(tags={
               "tagKey1": "tagValue1",
               "tagKey2": "tagValue2",
           })
           ```
    :param str vpc_id: ID of the VPC linked to the instances.
    :param str vswitch_id: ID of the VSwitch linked to the instances.
    """
    __args__ = dict()
    __args__['availabilityZone'] = availability_zone
    __args__['ids'] = ids
    __args__['imageId'] = image_id
    __args__['nameRegex'] = name_regex
    __args__['outputFile'] = output_file
    __args__['pageNumber'] = page_number
    __args__['pageSize'] = page_size
    __args__['ramRoleName'] = ram_role_name
    __args__['resourceGroupId'] = resource_group_id
    __args__['status'] = status
    __args__['tags'] = tags
    __args__['vpcId'] = vpc_id
    __args__['vswitchId'] = vswitch_id
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('alicloud:ecs/getInstances:getInstances', __args__, opts=opts, typ=GetInstancesResult).value

    return AwaitableGetInstancesResult(
        availability_zone=__ret__.availability_zone,
        id=__ret__.id,
        ids=__ret__.ids,
        image_id=__ret__.image_id,
        instances=__ret__.instances,
        name_regex=__ret__.name_regex,
        names=__ret__.names,
        output_file=__ret__.output_file,
        page_number=__ret__.page_number,
        page_size=__ret__.page_size,
        ram_role_name=__ret__.ram_role_name,
        resource_group_id=__ret__.resource_group_id,
        status=__ret__.status,
        tags=__ret__.tags,
        total_count=__ret__.total_count,
        vpc_id=__ret__.vpc_id,
        vswitch_id=__ret__.vswitch_id)


@_utilities.lift_output_func(get_instances)
def get_instances_output(availability_zone: Optional[pulumi.Input[Optional[str]]] = None,
                         ids: Optional[pulumi.Input[Optional[Sequence[str]]]] = None,
                         image_id: Optional[pulumi.Input[Optional[str]]] = None,
                         name_regex: Optional[pulumi.Input[Optional[str]]] = None,
                         output_file: Optional[pulumi.Input[Optional[str]]] = None,
                         page_number: Optional[pulumi.Input[Optional[int]]] = None,
                         page_size: Optional[pulumi.Input[Optional[int]]] = None,
                         ram_role_name: Optional[pulumi.Input[Optional[str]]] = None,
                         resource_group_id: Optional[pulumi.Input[Optional[str]]] = None,
                         status: Optional[pulumi.Input[Optional[str]]] = None,
                         tags: Optional[pulumi.Input[Optional[Mapping[str, Any]]]] = None,
                         vpc_id: Optional[pulumi.Input[Optional[str]]] = None,
                         vswitch_id: Optional[pulumi.Input[Optional[str]]] = None,
                         opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetInstancesResult]:
    """
    The Instances data source list ECS instance resources according to their ID, name regex, image id, status and other fields.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_alicloud as alicloud

    instances_ds = alicloud.ecs.get_instances(name_regex="web_server",
        status="Running")
    pulumi.export("firstInstanceId", instances_ds.instances[0].id)
    pulumi.export("instanceIds", instances_ds.ids)
    ```


    :param str availability_zone: Availability zone where instances are located.
    :param Sequence[str] ids: A list of ECS instance IDs.
    :param str image_id: The image ID of some ECS instance used.
    :param str name_regex: A regex string to filter results by instance name.
    :param str ram_role_name: The RAM role name which the instance attaches.
    :param str resource_group_id: The Id of resource group which the instance belongs.
    :param str status: Instance status. Valid values: "Creating", "Starting", "Running", "Stopping" and "Stopped". If undefined, all statuses are considered.
    :param Mapping[str, Any] tags: A map of tags assigned to the ECS instances. It must be in the format:
           ```python
           import pulumi
           import pulumi_alicloud as alicloud
           
           tagged_instances = alicloud.ecs.get_instances(tags={
               "tagKey1": "tagValue1",
               "tagKey2": "tagValue2",
           })
           ```
    :param str vpc_id: ID of the VPC linked to the instances.
    :param str vswitch_id: ID of the VSwitch linked to the instances.
    """
    ...
