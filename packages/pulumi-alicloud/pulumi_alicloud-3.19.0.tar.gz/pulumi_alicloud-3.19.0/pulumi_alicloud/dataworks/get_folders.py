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
    'GetFoldersResult',
    'AwaitableGetFoldersResult',
    'get_folders',
    'get_folders_output',
]

@pulumi.output_type
class GetFoldersResult:
    """
    A collection of values returned by getFolders.
    """
    def __init__(__self__, folders=None, id=None, ids=None, output_file=None, parent_folder_path=None, project_id=None):
        if folders and not isinstance(folders, list):
            raise TypeError("Expected argument 'folders' to be a list")
        pulumi.set(__self__, "folders", folders)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if ids and not isinstance(ids, list):
            raise TypeError("Expected argument 'ids' to be a list")
        pulumi.set(__self__, "ids", ids)
        if output_file and not isinstance(output_file, str):
            raise TypeError("Expected argument 'output_file' to be a str")
        pulumi.set(__self__, "output_file", output_file)
        if parent_folder_path and not isinstance(parent_folder_path, str):
            raise TypeError("Expected argument 'parent_folder_path' to be a str")
        pulumi.set(__self__, "parent_folder_path", parent_folder_path)
        if project_id and not isinstance(project_id, str):
            raise TypeError("Expected argument 'project_id' to be a str")
        pulumi.set(__self__, "project_id", project_id)

    @property
    @pulumi.getter
    def folders(self) -> Sequence['outputs.GetFoldersFolderResult']:
        return pulumi.get(self, "folders")

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
    @pulumi.getter(name="parentFolderPath")
    def parent_folder_path(self) -> str:
        return pulumi.get(self, "parent_folder_path")

    @property
    @pulumi.getter(name="projectId")
    def project_id(self) -> str:
        return pulumi.get(self, "project_id")


class AwaitableGetFoldersResult(GetFoldersResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetFoldersResult(
            folders=self.folders,
            id=self.id,
            ids=self.ids,
            output_file=self.output_file,
            parent_folder_path=self.parent_folder_path,
            project_id=self.project_id)


def get_folders(ids: Optional[Sequence[str]] = None,
                output_file: Optional[str] = None,
                parent_folder_path: Optional[str] = None,
                project_id: Optional[str] = None,
                opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetFoldersResult:
    """
    This data source provides the Data Works Folders of the current Alibaba Cloud user.

    > **NOTE:** Available in v1.131.0+.

    ## Example Usage

    Basic Usage

    ```python
    import pulumi
    import pulumi_alicloud as alicloud

    default = alicloud.dataworks.Folder("default",
        project_id="xxxx",
        folder_path="Business Flow/tfTestAcc/folderDi")
    ids = pulumi.Output.all(default.folder_id, default.project_id).apply(lambda folder_id, project_id: alicloud.dataworks.get_folders_output(ids=[folder_id],
        project_id=project_id,
        parent_folder_path="Business Flow/tfTestAcc/folderDi"))
    pulumi.export("dataWorksFolderId1", ids.folders[0].id)
    ```


    :param Sequence[str] ids: A list of Folder IDs.
    :param str parent_folder_path: The parent folder path.
    :param str project_id: The ID of the project.
    """
    __args__ = dict()
    __args__['ids'] = ids
    __args__['outputFile'] = output_file
    __args__['parentFolderPath'] = parent_folder_path
    __args__['projectId'] = project_id
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('alicloud:dataworks/getFolders:getFolders', __args__, opts=opts, typ=GetFoldersResult).value

    return AwaitableGetFoldersResult(
        folders=__ret__.folders,
        id=__ret__.id,
        ids=__ret__.ids,
        output_file=__ret__.output_file,
        parent_folder_path=__ret__.parent_folder_path,
        project_id=__ret__.project_id)


@_utilities.lift_output_func(get_folders)
def get_folders_output(ids: Optional[pulumi.Input[Optional[Sequence[str]]]] = None,
                       output_file: Optional[pulumi.Input[Optional[str]]] = None,
                       parent_folder_path: Optional[pulumi.Input[str]] = None,
                       project_id: Optional[pulumi.Input[str]] = None,
                       opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetFoldersResult]:
    """
    This data source provides the Data Works Folders of the current Alibaba Cloud user.

    > **NOTE:** Available in v1.131.0+.

    ## Example Usage

    Basic Usage

    ```python
    import pulumi
    import pulumi_alicloud as alicloud

    default = alicloud.dataworks.Folder("default",
        project_id="xxxx",
        folder_path="Business Flow/tfTestAcc/folderDi")
    ids = pulumi.Output.all(default.folder_id, default.project_id).apply(lambda folder_id, project_id: alicloud.dataworks.get_folders_output(ids=[folder_id],
        project_id=project_id,
        parent_folder_path="Business Flow/tfTestAcc/folderDi"))
    pulumi.export("dataWorksFolderId1", ids.folders[0].id)
    ```


    :param Sequence[str] ids: A list of Folder IDs.
    :param str parent_folder_path: The parent folder path.
    :param str project_id: The ID of the project.
    """
    ...
