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
    'GetSharedTargetsResult',
    'AwaitableGetSharedTargetsResult',
    'get_shared_targets',
    'get_shared_targets_output',
]

@pulumi.output_type
class GetSharedTargetsResult:
    """
    A collection of values returned by getSharedTargets.
    """
    def __init__(__self__, id=None, ids=None, output_file=None, resource_share_id=None, status=None, targets=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if ids and not isinstance(ids, list):
            raise TypeError("Expected argument 'ids' to be a list")
        pulumi.set(__self__, "ids", ids)
        if output_file and not isinstance(output_file, str):
            raise TypeError("Expected argument 'output_file' to be a str")
        pulumi.set(__self__, "output_file", output_file)
        if resource_share_id and not isinstance(resource_share_id, str):
            raise TypeError("Expected argument 'resource_share_id' to be a str")
        pulumi.set(__self__, "resource_share_id", resource_share_id)
        if status and not isinstance(status, str):
            raise TypeError("Expected argument 'status' to be a str")
        pulumi.set(__self__, "status", status)
        if targets and not isinstance(targets, list):
            raise TypeError("Expected argument 'targets' to be a list")
        pulumi.set(__self__, "targets", targets)

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
    @pulumi.getter(name="outputFile")
    def output_file(self) -> Optional[str]:
        return pulumi.get(self, "output_file")

    @property
    @pulumi.getter(name="resourceShareId")
    def resource_share_id(self) -> Optional[str]:
        return pulumi.get(self, "resource_share_id")

    @property
    @pulumi.getter
    def status(self) -> Optional[str]:
        return pulumi.get(self, "status")

    @property
    @pulumi.getter
    def targets(self) -> Sequence['outputs.GetSharedTargetsTargetResult']:
        return pulumi.get(self, "targets")


class AwaitableGetSharedTargetsResult(GetSharedTargetsResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetSharedTargetsResult(
            id=self.id,
            ids=self.ids,
            output_file=self.output_file,
            resource_share_id=self.resource_share_id,
            status=self.status,
            targets=self.targets)


def get_shared_targets(ids: Optional[Sequence[str]] = None,
                       output_file: Optional[str] = None,
                       resource_share_id: Optional[str] = None,
                       status: Optional[str] = None,
                       opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetSharedTargetsResult:
    """
    This data source provides the Resource Manager Shared Targets of the current Alibaba Cloud user.

    > **NOTE:** Available in v1.111.0+.

    ## Example Usage

    Basic Usage

    ```python
    import pulumi
    import pulumi_alicloud as alicloud

    example = alicloud.resourcemanager.get_shared_targets(ids=["15681091********"])
    pulumi.export("firstResourceManagerSharedTargetId", example.targets[0].id)
    ```


    :param Sequence[str] ids: A list of Shared Target IDs.
    :param str resource_share_id: The resource shared ID of resource manager.
    :param str status: The status of shared target.
    """
    __args__ = dict()
    __args__['ids'] = ids
    __args__['outputFile'] = output_file
    __args__['resourceShareId'] = resource_share_id
    __args__['status'] = status
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('alicloud:resourcemanager/getSharedTargets:getSharedTargets', __args__, opts=opts, typ=GetSharedTargetsResult).value

    return AwaitableGetSharedTargetsResult(
        id=__ret__.id,
        ids=__ret__.ids,
        output_file=__ret__.output_file,
        resource_share_id=__ret__.resource_share_id,
        status=__ret__.status,
        targets=__ret__.targets)


@_utilities.lift_output_func(get_shared_targets)
def get_shared_targets_output(ids: Optional[pulumi.Input[Optional[Sequence[str]]]] = None,
                              output_file: Optional[pulumi.Input[Optional[str]]] = None,
                              resource_share_id: Optional[pulumi.Input[Optional[str]]] = None,
                              status: Optional[pulumi.Input[Optional[str]]] = None,
                              opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetSharedTargetsResult]:
    """
    This data source provides the Resource Manager Shared Targets of the current Alibaba Cloud user.

    > **NOTE:** Available in v1.111.0+.

    ## Example Usage

    Basic Usage

    ```python
    import pulumi
    import pulumi_alicloud as alicloud

    example = alicloud.resourcemanager.get_shared_targets(ids=["15681091********"])
    pulumi.export("firstResourceManagerSharedTargetId", example.targets[0].id)
    ```


    :param Sequence[str] ids: A list of Shared Target IDs.
    :param str resource_share_id: The resource shared ID of resource manager.
    :param str status: The status of shared target.
    """
    ...
