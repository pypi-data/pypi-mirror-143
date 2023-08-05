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
    'GetVirtualHostsResult',
    'AwaitableGetVirtualHostsResult',
    'get_virtual_hosts',
    'get_virtual_hosts_output',
]

@pulumi.output_type
class GetVirtualHostsResult:
    """
    A collection of values returned by getVirtualHosts.
    """
    def __init__(__self__, hosts=None, id=None, ids=None, instance_id=None, name_regex=None, names=None, output_file=None):
        if hosts and not isinstance(hosts, list):
            raise TypeError("Expected argument 'hosts' to be a list")
        pulumi.set(__self__, "hosts", hosts)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if ids and not isinstance(ids, list):
            raise TypeError("Expected argument 'ids' to be a list")
        pulumi.set(__self__, "ids", ids)
        if instance_id and not isinstance(instance_id, str):
            raise TypeError("Expected argument 'instance_id' to be a str")
        pulumi.set(__self__, "instance_id", instance_id)
        if name_regex and not isinstance(name_regex, str):
            raise TypeError("Expected argument 'name_regex' to be a str")
        pulumi.set(__self__, "name_regex", name_regex)
        if names and not isinstance(names, list):
            raise TypeError("Expected argument 'names' to be a list")
        pulumi.set(__self__, "names", names)
        if output_file and not isinstance(output_file, str):
            raise TypeError("Expected argument 'output_file' to be a str")
        pulumi.set(__self__, "output_file", output_file)

    @property
    @pulumi.getter
    def hosts(self) -> Sequence['outputs.GetVirtualHostsHostResult']:
        return pulumi.get(self, "hosts")

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
    @pulumi.getter(name="instanceId")
    def instance_id(self) -> str:
        return pulumi.get(self, "instance_id")

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


class AwaitableGetVirtualHostsResult(GetVirtualHostsResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetVirtualHostsResult(
            hosts=self.hosts,
            id=self.id,
            ids=self.ids,
            instance_id=self.instance_id,
            name_regex=self.name_regex,
            names=self.names,
            output_file=self.output_file)


def get_virtual_hosts(ids: Optional[Sequence[str]] = None,
                      instance_id: Optional[str] = None,
                      name_regex: Optional[str] = None,
                      output_file: Optional[str] = None,
                      opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetVirtualHostsResult:
    """
    This data source provides the Amqp Virtual Hosts of the current Alibaba Cloud user.

    > **NOTE:** Available in v1.126.0+.

    ## Example Usage

    Basic Usage

    ```python
    import pulumi
    import pulumi_alicloud as alicloud

    ids = alicloud.amqp.get_virtual_hosts(instance_id="amqp-abc12345",
        ids=[
            "my-VirtualHost-1",
            "my-VirtualHost-2",
        ])
    pulumi.export("amqpVirtualHostId1", ids.hosts[0].id)
    name_regex = alicloud.amqp.get_virtual_hosts(instance_id="amqp-abc12345",
        name_regex="^my-VirtualHost")
    pulumi.export("amqpVirtualHostId2", name_regex.hosts[0].id)
    ```


    :param Sequence[str] ids: A list of Virtual Host IDs. Its element value is same as Virtual Host Name.
    :param str instance_id: InstanceId.
    :param str name_regex: A regex string to filter results by Virtual Host name.
    """
    __args__ = dict()
    __args__['ids'] = ids
    __args__['instanceId'] = instance_id
    __args__['nameRegex'] = name_regex
    __args__['outputFile'] = output_file
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('alicloud:amqp/getVirtualHosts:getVirtualHosts', __args__, opts=opts, typ=GetVirtualHostsResult).value

    return AwaitableGetVirtualHostsResult(
        hosts=__ret__.hosts,
        id=__ret__.id,
        ids=__ret__.ids,
        instance_id=__ret__.instance_id,
        name_regex=__ret__.name_regex,
        names=__ret__.names,
        output_file=__ret__.output_file)


@_utilities.lift_output_func(get_virtual_hosts)
def get_virtual_hosts_output(ids: Optional[pulumi.Input[Optional[Sequence[str]]]] = None,
                             instance_id: Optional[pulumi.Input[str]] = None,
                             name_regex: Optional[pulumi.Input[Optional[str]]] = None,
                             output_file: Optional[pulumi.Input[Optional[str]]] = None,
                             opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetVirtualHostsResult]:
    """
    This data source provides the Amqp Virtual Hosts of the current Alibaba Cloud user.

    > **NOTE:** Available in v1.126.0+.

    ## Example Usage

    Basic Usage

    ```python
    import pulumi
    import pulumi_alicloud as alicloud

    ids = alicloud.amqp.get_virtual_hosts(instance_id="amqp-abc12345",
        ids=[
            "my-VirtualHost-1",
            "my-VirtualHost-2",
        ])
    pulumi.export("amqpVirtualHostId1", ids.hosts[0].id)
    name_regex = alicloud.amqp.get_virtual_hosts(instance_id="amqp-abc12345",
        name_regex="^my-VirtualHost")
    pulumi.export("amqpVirtualHostId2", name_regex.hosts[0].id)
    ```


    :param Sequence[str] ids: A list of Virtual Host IDs. Its element value is same as Virtual Host Name.
    :param str instance_id: InstanceId.
    :param str name_regex: A regex string to filter results by Virtual Host name.
    """
    ...
