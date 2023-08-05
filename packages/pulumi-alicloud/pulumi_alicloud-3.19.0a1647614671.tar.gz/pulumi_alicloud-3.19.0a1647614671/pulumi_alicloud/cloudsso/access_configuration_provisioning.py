# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['AccessConfigurationProvisioningArgs', 'AccessConfigurationProvisioning']

@pulumi.input_type
class AccessConfigurationProvisioningArgs:
    def __init__(__self__, *,
                 access_configuration_id: pulumi.Input[str],
                 directory_id: pulumi.Input[str],
                 target_id: pulumi.Input[str],
                 target_type: pulumi.Input[str],
                 status: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a AccessConfigurationProvisioning resource.
        :param pulumi.Input[str] access_configuration_id: The Access configuration ID.
        :param pulumi.Input[str] directory_id: The ID of the Directory.
        :param pulumi.Input[str] target_id: The ID of the target to create the resource range.
        :param pulumi.Input[str] target_type: The type of the resource range target to be accessed. Valid values: `RD-Account`.
        :param pulumi.Input[str] status: The status of the resource. Valid values: `Provisioned`, `ReprovisionRequired` and `DeprovisionFailed`.
        """
        pulumi.set(__self__, "access_configuration_id", access_configuration_id)
        pulumi.set(__self__, "directory_id", directory_id)
        pulumi.set(__self__, "target_id", target_id)
        pulumi.set(__self__, "target_type", target_type)
        if status is not None:
            pulumi.set(__self__, "status", status)

    @property
    @pulumi.getter(name="accessConfigurationId")
    def access_configuration_id(self) -> pulumi.Input[str]:
        """
        The Access configuration ID.
        """
        return pulumi.get(self, "access_configuration_id")

    @access_configuration_id.setter
    def access_configuration_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "access_configuration_id", value)

    @property
    @pulumi.getter(name="directoryId")
    def directory_id(self) -> pulumi.Input[str]:
        """
        The ID of the Directory.
        """
        return pulumi.get(self, "directory_id")

    @directory_id.setter
    def directory_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "directory_id", value)

    @property
    @pulumi.getter(name="targetId")
    def target_id(self) -> pulumi.Input[str]:
        """
        The ID of the target to create the resource range.
        """
        return pulumi.get(self, "target_id")

    @target_id.setter
    def target_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "target_id", value)

    @property
    @pulumi.getter(name="targetType")
    def target_type(self) -> pulumi.Input[str]:
        """
        The type of the resource range target to be accessed. Valid values: `RD-Account`.
        """
        return pulumi.get(self, "target_type")

    @target_type.setter
    def target_type(self, value: pulumi.Input[str]):
        pulumi.set(self, "target_type", value)

    @property
    @pulumi.getter
    def status(self) -> Optional[pulumi.Input[str]]:
        """
        The status of the resource. Valid values: `Provisioned`, `ReprovisionRequired` and `DeprovisionFailed`.
        """
        return pulumi.get(self, "status")

    @status.setter
    def status(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "status", value)


@pulumi.input_type
class _AccessConfigurationProvisioningState:
    def __init__(__self__, *,
                 access_configuration_id: Optional[pulumi.Input[str]] = None,
                 directory_id: Optional[pulumi.Input[str]] = None,
                 status: Optional[pulumi.Input[str]] = None,
                 target_id: Optional[pulumi.Input[str]] = None,
                 target_type: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering AccessConfigurationProvisioning resources.
        :param pulumi.Input[str] access_configuration_id: The Access configuration ID.
        :param pulumi.Input[str] directory_id: The ID of the Directory.
        :param pulumi.Input[str] status: The status of the resource. Valid values: `Provisioned`, `ReprovisionRequired` and `DeprovisionFailed`.
        :param pulumi.Input[str] target_id: The ID of the target to create the resource range.
        :param pulumi.Input[str] target_type: The type of the resource range target to be accessed. Valid values: `RD-Account`.
        """
        if access_configuration_id is not None:
            pulumi.set(__self__, "access_configuration_id", access_configuration_id)
        if directory_id is not None:
            pulumi.set(__self__, "directory_id", directory_id)
        if status is not None:
            pulumi.set(__self__, "status", status)
        if target_id is not None:
            pulumi.set(__self__, "target_id", target_id)
        if target_type is not None:
            pulumi.set(__self__, "target_type", target_type)

    @property
    @pulumi.getter(name="accessConfigurationId")
    def access_configuration_id(self) -> Optional[pulumi.Input[str]]:
        """
        The Access configuration ID.
        """
        return pulumi.get(self, "access_configuration_id")

    @access_configuration_id.setter
    def access_configuration_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "access_configuration_id", value)

    @property
    @pulumi.getter(name="directoryId")
    def directory_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the Directory.
        """
        return pulumi.get(self, "directory_id")

    @directory_id.setter
    def directory_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "directory_id", value)

    @property
    @pulumi.getter
    def status(self) -> Optional[pulumi.Input[str]]:
        """
        The status of the resource. Valid values: `Provisioned`, `ReprovisionRequired` and `DeprovisionFailed`.
        """
        return pulumi.get(self, "status")

    @status.setter
    def status(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "status", value)

    @property
    @pulumi.getter(name="targetId")
    def target_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the target to create the resource range.
        """
        return pulumi.get(self, "target_id")

    @target_id.setter
    def target_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "target_id", value)

    @property
    @pulumi.getter(name="targetType")
    def target_type(self) -> Optional[pulumi.Input[str]]:
        """
        The type of the resource range target to be accessed. Valid values: `RD-Account`.
        """
        return pulumi.get(self, "target_type")

    @target_type.setter
    def target_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "target_type", value)


class AccessConfigurationProvisioning(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 access_configuration_id: Optional[pulumi.Input[str]] = None,
                 directory_id: Optional[pulumi.Input[str]] = None,
                 status: Optional[pulumi.Input[str]] = None,
                 target_id: Optional[pulumi.Input[str]] = None,
                 target_type: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Provides a Cloud SSO Access Configuration Provisioning resource.

        For information about Cloud SSO Access Configuration Provisioning and how to use it, see [What is Access Configuration Provisioning](https://www.alibabacloud.com/help/en/doc-detail/266737.html).

        > **NOTE:** Available in v1.148.0+.

        ## Import

        Cloud SSO Access Configuration Provisioning can be imported using the id, e.g.

        ```sh
         $ pulumi import alicloud:cloudsso/accessConfigurationProvisioning:AccessConfigurationProvisioning example <directory_id>:<access_configuration_id>:<target_type>:<target_id>
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] access_configuration_id: The Access configuration ID.
        :param pulumi.Input[str] directory_id: The ID of the Directory.
        :param pulumi.Input[str] status: The status of the resource. Valid values: `Provisioned`, `ReprovisionRequired` and `DeprovisionFailed`.
        :param pulumi.Input[str] target_id: The ID of the target to create the resource range.
        :param pulumi.Input[str] target_type: The type of the resource range target to be accessed. Valid values: `RD-Account`.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: AccessConfigurationProvisioningArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a Cloud SSO Access Configuration Provisioning resource.

        For information about Cloud SSO Access Configuration Provisioning and how to use it, see [What is Access Configuration Provisioning](https://www.alibabacloud.com/help/en/doc-detail/266737.html).

        > **NOTE:** Available in v1.148.0+.

        ## Import

        Cloud SSO Access Configuration Provisioning can be imported using the id, e.g.

        ```sh
         $ pulumi import alicloud:cloudsso/accessConfigurationProvisioning:AccessConfigurationProvisioning example <directory_id>:<access_configuration_id>:<target_type>:<target_id>
        ```

        :param str resource_name: The name of the resource.
        :param AccessConfigurationProvisioningArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(AccessConfigurationProvisioningArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 access_configuration_id: Optional[pulumi.Input[str]] = None,
                 directory_id: Optional[pulumi.Input[str]] = None,
                 status: Optional[pulumi.Input[str]] = None,
                 target_id: Optional[pulumi.Input[str]] = None,
                 target_type: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        if opts is None:
            opts = pulumi.ResourceOptions()
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.version is None:
            opts.version = _utilities.get_version()
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = AccessConfigurationProvisioningArgs.__new__(AccessConfigurationProvisioningArgs)

            if access_configuration_id is None and not opts.urn:
                raise TypeError("Missing required property 'access_configuration_id'")
            __props__.__dict__["access_configuration_id"] = access_configuration_id
            if directory_id is None and not opts.urn:
                raise TypeError("Missing required property 'directory_id'")
            __props__.__dict__["directory_id"] = directory_id
            __props__.__dict__["status"] = status
            if target_id is None and not opts.urn:
                raise TypeError("Missing required property 'target_id'")
            __props__.__dict__["target_id"] = target_id
            if target_type is None and not opts.urn:
                raise TypeError("Missing required property 'target_type'")
            __props__.__dict__["target_type"] = target_type
        super(AccessConfigurationProvisioning, __self__).__init__(
            'alicloud:cloudsso/accessConfigurationProvisioning:AccessConfigurationProvisioning',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            access_configuration_id: Optional[pulumi.Input[str]] = None,
            directory_id: Optional[pulumi.Input[str]] = None,
            status: Optional[pulumi.Input[str]] = None,
            target_id: Optional[pulumi.Input[str]] = None,
            target_type: Optional[pulumi.Input[str]] = None) -> 'AccessConfigurationProvisioning':
        """
        Get an existing AccessConfigurationProvisioning resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] access_configuration_id: The Access configuration ID.
        :param pulumi.Input[str] directory_id: The ID of the Directory.
        :param pulumi.Input[str] status: The status of the resource. Valid values: `Provisioned`, `ReprovisionRequired` and `DeprovisionFailed`.
        :param pulumi.Input[str] target_id: The ID of the target to create the resource range.
        :param pulumi.Input[str] target_type: The type of the resource range target to be accessed. Valid values: `RD-Account`.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _AccessConfigurationProvisioningState.__new__(_AccessConfigurationProvisioningState)

        __props__.__dict__["access_configuration_id"] = access_configuration_id
        __props__.__dict__["directory_id"] = directory_id
        __props__.__dict__["status"] = status
        __props__.__dict__["target_id"] = target_id
        __props__.__dict__["target_type"] = target_type
        return AccessConfigurationProvisioning(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="accessConfigurationId")
    def access_configuration_id(self) -> pulumi.Output[str]:
        """
        The Access configuration ID.
        """
        return pulumi.get(self, "access_configuration_id")

    @property
    @pulumi.getter(name="directoryId")
    def directory_id(self) -> pulumi.Output[str]:
        """
        The ID of the Directory.
        """
        return pulumi.get(self, "directory_id")

    @property
    @pulumi.getter
    def status(self) -> pulumi.Output[str]:
        """
        The status of the resource. Valid values: `Provisioned`, `ReprovisionRequired` and `DeprovisionFailed`.
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter(name="targetId")
    def target_id(self) -> pulumi.Output[str]:
        """
        The ID of the target to create the resource range.
        """
        return pulumi.get(self, "target_id")

    @property
    @pulumi.getter(name="targetType")
    def target_type(self) -> pulumi.Output[str]:
        """
        The type of the resource range target to be accessed. Valid values: `RD-Account`.
        """
        return pulumi.get(self, "target_type")

