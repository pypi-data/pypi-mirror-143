# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['NetworkArgs', 'Network']

@pulumi.input_type
class NetworkArgs:
    def __init__(__self__, *,
                 cidr_block: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 dry_run: Optional[pulumi.Input[bool]] = None,
                 enable_ipv6: Optional[pulumi.Input[bool]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 resource_group_id: Optional[pulumi.Input[str]] = None,
                 secondary_cidr_blocks: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, Any]]] = None,
                 user_cidrs: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 vpc_name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a Network resource.
        :param pulumi.Input[str] cidr_block: The CIDR block for the VPC. The `cidr_block` is Optional and default value is `172.16.0.0/12` after v1.119.0+.
        :param pulumi.Input[str] description: The VPC description. Defaults to null.
        :param pulumi.Input[bool] dry_run: Specifies whether to precheck this request only. Valid values: `true` and `false`.
        :param pulumi.Input[bool] enable_ipv6: Specifies whether to enable the IPv6 CIDR block. Valid values: `false` (Default): disables IPv6 CIDR blocks. `true`: enables IPv6 CIDR blocks. If the `enable_ipv6` is `true`, the system will automatically create a free version of an IPv6 gateway for your private network and assign an IPv6 network segment assigned as /56.
        :param pulumi.Input[str] name: Field `name` has been deprecated from provider version 1.119.0. New field `vpc_name` instead.
        :param pulumi.Input[str] resource_group_id: The Id of resource group which the VPC belongs.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] secondary_cidr_blocks: The secondary CIDR blocks for the VPC.
        :param pulumi.Input[Mapping[str, Any]] tags: A mapping of tags to assign to the resource.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] user_cidrs: The user cidrs of the VPC.
        :param pulumi.Input[str] vpc_name: The name of the VPC. Defaults to null.
        """
        if cidr_block is not None:
            pulumi.set(__self__, "cidr_block", cidr_block)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if dry_run is not None:
            pulumi.set(__self__, "dry_run", dry_run)
        if enable_ipv6 is not None:
            pulumi.set(__self__, "enable_ipv6", enable_ipv6)
        if name is not None:
            warnings.warn("""Field 'name' has been deprecated from provider version 1.119.0. New field 'vpc_name' instead.""", DeprecationWarning)
            pulumi.log.warn("""name is deprecated: Field 'name' has been deprecated from provider version 1.119.0. New field 'vpc_name' instead.""")
        if name is not None:
            pulumi.set(__self__, "name", name)
        if resource_group_id is not None:
            pulumi.set(__self__, "resource_group_id", resource_group_id)
        if secondary_cidr_blocks is not None:
            pulumi.set(__self__, "secondary_cidr_blocks", secondary_cidr_blocks)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if user_cidrs is not None:
            pulumi.set(__self__, "user_cidrs", user_cidrs)
        if vpc_name is not None:
            pulumi.set(__self__, "vpc_name", vpc_name)

    @property
    @pulumi.getter(name="cidrBlock")
    def cidr_block(self) -> Optional[pulumi.Input[str]]:
        """
        The CIDR block for the VPC. The `cidr_block` is Optional and default value is `172.16.0.0/12` after v1.119.0+.
        """
        return pulumi.get(self, "cidr_block")

    @cidr_block.setter
    def cidr_block(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "cidr_block", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        The VPC description. Defaults to null.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="dryRun")
    def dry_run(self) -> Optional[pulumi.Input[bool]]:
        """
        Specifies whether to precheck this request only. Valid values: `true` and `false`.
        """
        return pulumi.get(self, "dry_run")

    @dry_run.setter
    def dry_run(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "dry_run", value)

    @property
    @pulumi.getter(name="enableIpv6")
    def enable_ipv6(self) -> Optional[pulumi.Input[bool]]:
        """
        Specifies whether to enable the IPv6 CIDR block. Valid values: `false` (Default): disables IPv6 CIDR blocks. `true`: enables IPv6 CIDR blocks. If the `enable_ipv6` is `true`, the system will automatically create a free version of an IPv6 gateway for your private network and assign an IPv6 network segment assigned as /56.
        """
        return pulumi.get(self, "enable_ipv6")

    @enable_ipv6.setter
    def enable_ipv6(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "enable_ipv6", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Field `name` has been deprecated from provider version 1.119.0. New field `vpc_name` instead.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="resourceGroupId")
    def resource_group_id(self) -> Optional[pulumi.Input[str]]:
        """
        The Id of resource group which the VPC belongs.
        """
        return pulumi.get(self, "resource_group_id")

    @resource_group_id.setter
    def resource_group_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "resource_group_id", value)

    @property
    @pulumi.getter(name="secondaryCidrBlocks")
    def secondary_cidr_blocks(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The secondary CIDR blocks for the VPC.
        """
        return pulumi.get(self, "secondary_cidr_blocks")

    @secondary_cidr_blocks.setter
    def secondary_cidr_blocks(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "secondary_cidr_blocks", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, Any]]]:
        """
        A mapping of tags to assign to the resource.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, Any]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter(name="userCidrs")
    def user_cidrs(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The user cidrs of the VPC.
        """
        return pulumi.get(self, "user_cidrs")

    @user_cidrs.setter
    def user_cidrs(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "user_cidrs", value)

    @property
    @pulumi.getter(name="vpcName")
    def vpc_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the VPC. Defaults to null.
        """
        return pulumi.get(self, "vpc_name")

    @vpc_name.setter
    def vpc_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "vpc_name", value)


@pulumi.input_type
class _NetworkState:
    def __init__(__self__, *,
                 cidr_block: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 dry_run: Optional[pulumi.Input[bool]] = None,
                 enable_ipv6: Optional[pulumi.Input[bool]] = None,
                 ipv6_cidr_block: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 resource_group_id: Optional[pulumi.Input[str]] = None,
                 route_table_id: Optional[pulumi.Input[str]] = None,
                 router_id: Optional[pulumi.Input[str]] = None,
                 router_table_id: Optional[pulumi.Input[str]] = None,
                 secondary_cidr_blocks: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 status: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, Any]]] = None,
                 user_cidrs: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 vpc_name: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering Network resources.
        :param pulumi.Input[str] cidr_block: The CIDR block for the VPC. The `cidr_block` is Optional and default value is `172.16.0.0/12` after v1.119.0+.
        :param pulumi.Input[str] description: The VPC description. Defaults to null.
        :param pulumi.Input[bool] dry_run: Specifies whether to precheck this request only. Valid values: `true` and `false`.
        :param pulumi.Input[bool] enable_ipv6: Specifies whether to enable the IPv6 CIDR block. Valid values: `false` (Default): disables IPv6 CIDR blocks. `true`: enables IPv6 CIDR blocks. If the `enable_ipv6` is `true`, the system will automatically create a free version of an IPv6 gateway for your private network and assign an IPv6 network segment assigned as /56.
        :param pulumi.Input[str] ipv6_cidr_block: (Available in v1.119.0+) ) The ipv6 cidr block of VPC.
        :param pulumi.Input[str] name: Field `name` has been deprecated from provider version 1.119.0. New field `vpc_name` instead.
        :param pulumi.Input[str] resource_group_id: The Id of resource group which the VPC belongs.
        :param pulumi.Input[str] route_table_id: The route table ID of the router created by default on VPC creation.
        :param pulumi.Input[str] router_id: The ID of the router created by default on VPC creation.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] secondary_cidr_blocks: The secondary CIDR blocks for the VPC.
        :param pulumi.Input[Mapping[str, Any]] tags: A mapping of tags to assign to the resource.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] user_cidrs: The user cidrs of the VPC.
        :param pulumi.Input[str] vpc_name: The name of the VPC. Defaults to null.
        """
        if cidr_block is not None:
            pulumi.set(__self__, "cidr_block", cidr_block)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if dry_run is not None:
            pulumi.set(__self__, "dry_run", dry_run)
        if enable_ipv6 is not None:
            pulumi.set(__self__, "enable_ipv6", enable_ipv6)
        if ipv6_cidr_block is not None:
            pulumi.set(__self__, "ipv6_cidr_block", ipv6_cidr_block)
        if name is not None:
            warnings.warn("""Field 'name' has been deprecated from provider version 1.119.0. New field 'vpc_name' instead.""", DeprecationWarning)
            pulumi.log.warn("""name is deprecated: Field 'name' has been deprecated from provider version 1.119.0. New field 'vpc_name' instead.""")
        if name is not None:
            pulumi.set(__self__, "name", name)
        if resource_group_id is not None:
            pulumi.set(__self__, "resource_group_id", resource_group_id)
        if route_table_id is not None:
            pulumi.set(__self__, "route_table_id", route_table_id)
        if router_id is not None:
            pulumi.set(__self__, "router_id", router_id)
        if router_table_id is not None:
            warnings.warn("""Attribute router_table_id has been deprecated and replaced with route_table_id.""", DeprecationWarning)
            pulumi.log.warn("""router_table_id is deprecated: Attribute router_table_id has been deprecated and replaced with route_table_id.""")
        if router_table_id is not None:
            pulumi.set(__self__, "router_table_id", router_table_id)
        if secondary_cidr_blocks is not None:
            pulumi.set(__self__, "secondary_cidr_blocks", secondary_cidr_blocks)
        if status is not None:
            pulumi.set(__self__, "status", status)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if user_cidrs is not None:
            pulumi.set(__self__, "user_cidrs", user_cidrs)
        if vpc_name is not None:
            pulumi.set(__self__, "vpc_name", vpc_name)

    @property
    @pulumi.getter(name="cidrBlock")
    def cidr_block(self) -> Optional[pulumi.Input[str]]:
        """
        The CIDR block for the VPC. The `cidr_block` is Optional and default value is `172.16.0.0/12` after v1.119.0+.
        """
        return pulumi.get(self, "cidr_block")

    @cidr_block.setter
    def cidr_block(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "cidr_block", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        The VPC description. Defaults to null.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="dryRun")
    def dry_run(self) -> Optional[pulumi.Input[bool]]:
        """
        Specifies whether to precheck this request only. Valid values: `true` and `false`.
        """
        return pulumi.get(self, "dry_run")

    @dry_run.setter
    def dry_run(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "dry_run", value)

    @property
    @pulumi.getter(name="enableIpv6")
    def enable_ipv6(self) -> Optional[pulumi.Input[bool]]:
        """
        Specifies whether to enable the IPv6 CIDR block. Valid values: `false` (Default): disables IPv6 CIDR blocks. `true`: enables IPv6 CIDR blocks. If the `enable_ipv6` is `true`, the system will automatically create a free version of an IPv6 gateway for your private network and assign an IPv6 network segment assigned as /56.
        """
        return pulumi.get(self, "enable_ipv6")

    @enable_ipv6.setter
    def enable_ipv6(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "enable_ipv6", value)

    @property
    @pulumi.getter(name="ipv6CidrBlock")
    def ipv6_cidr_block(self) -> Optional[pulumi.Input[str]]:
        """
        (Available in v1.119.0+) ) The ipv6 cidr block of VPC.
        """
        return pulumi.get(self, "ipv6_cidr_block")

    @ipv6_cidr_block.setter
    def ipv6_cidr_block(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "ipv6_cidr_block", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Field `name` has been deprecated from provider version 1.119.0. New field `vpc_name` instead.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="resourceGroupId")
    def resource_group_id(self) -> Optional[pulumi.Input[str]]:
        """
        The Id of resource group which the VPC belongs.
        """
        return pulumi.get(self, "resource_group_id")

    @resource_group_id.setter
    def resource_group_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "resource_group_id", value)

    @property
    @pulumi.getter(name="routeTableId")
    def route_table_id(self) -> Optional[pulumi.Input[str]]:
        """
        The route table ID of the router created by default on VPC creation.
        """
        return pulumi.get(self, "route_table_id")

    @route_table_id.setter
    def route_table_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "route_table_id", value)

    @property
    @pulumi.getter(name="routerId")
    def router_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the router created by default on VPC creation.
        """
        return pulumi.get(self, "router_id")

    @router_id.setter
    def router_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "router_id", value)

    @property
    @pulumi.getter(name="routerTableId")
    def router_table_id(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "router_table_id")

    @router_table_id.setter
    def router_table_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "router_table_id", value)

    @property
    @pulumi.getter(name="secondaryCidrBlocks")
    def secondary_cidr_blocks(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The secondary CIDR blocks for the VPC.
        """
        return pulumi.get(self, "secondary_cidr_blocks")

    @secondary_cidr_blocks.setter
    def secondary_cidr_blocks(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "secondary_cidr_blocks", value)

    @property
    @pulumi.getter
    def status(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "status")

    @status.setter
    def status(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "status", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, Any]]]:
        """
        A mapping of tags to assign to the resource.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, Any]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter(name="userCidrs")
    def user_cidrs(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The user cidrs of the VPC.
        """
        return pulumi.get(self, "user_cidrs")

    @user_cidrs.setter
    def user_cidrs(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "user_cidrs", value)

    @property
    @pulumi.getter(name="vpcName")
    def vpc_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the VPC. Defaults to null.
        """
        return pulumi.get(self, "vpc_name")

    @vpc_name.setter
    def vpc_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "vpc_name", value)


class Network(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 cidr_block: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 dry_run: Optional[pulumi.Input[bool]] = None,
                 enable_ipv6: Optional[pulumi.Input[bool]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 resource_group_id: Optional[pulumi.Input[str]] = None,
                 secondary_cidr_blocks: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, Any]]] = None,
                 user_cidrs: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 vpc_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        ## Import

        VPC can be imported using the id, e.g.

        ```sh
         $ pulumi import alicloud:vpc/network:Network example vpc-abc123456
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] cidr_block: The CIDR block for the VPC. The `cidr_block` is Optional and default value is `172.16.0.0/12` after v1.119.0+.
        :param pulumi.Input[str] description: The VPC description. Defaults to null.
        :param pulumi.Input[bool] dry_run: Specifies whether to precheck this request only. Valid values: `true` and `false`.
        :param pulumi.Input[bool] enable_ipv6: Specifies whether to enable the IPv6 CIDR block. Valid values: `false` (Default): disables IPv6 CIDR blocks. `true`: enables IPv6 CIDR blocks. If the `enable_ipv6` is `true`, the system will automatically create a free version of an IPv6 gateway for your private network and assign an IPv6 network segment assigned as /56.
        :param pulumi.Input[str] name: Field `name` has been deprecated from provider version 1.119.0. New field `vpc_name` instead.
        :param pulumi.Input[str] resource_group_id: The Id of resource group which the VPC belongs.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] secondary_cidr_blocks: The secondary CIDR blocks for the VPC.
        :param pulumi.Input[Mapping[str, Any]] tags: A mapping of tags to assign to the resource.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] user_cidrs: The user cidrs of the VPC.
        :param pulumi.Input[str] vpc_name: The name of the VPC. Defaults to null.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: Optional[NetworkArgs] = None,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        ## Import

        VPC can be imported using the id, e.g.

        ```sh
         $ pulumi import alicloud:vpc/network:Network example vpc-abc123456
        ```

        :param str resource_name: The name of the resource.
        :param NetworkArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(NetworkArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 cidr_block: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 dry_run: Optional[pulumi.Input[bool]] = None,
                 enable_ipv6: Optional[pulumi.Input[bool]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 resource_group_id: Optional[pulumi.Input[str]] = None,
                 secondary_cidr_blocks: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, Any]]] = None,
                 user_cidrs: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 vpc_name: Optional[pulumi.Input[str]] = None,
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
            __props__ = NetworkArgs.__new__(NetworkArgs)

            __props__.__dict__["cidr_block"] = cidr_block
            __props__.__dict__["description"] = description
            __props__.__dict__["dry_run"] = dry_run
            __props__.__dict__["enable_ipv6"] = enable_ipv6
            if name is not None and not opts.urn:
                warnings.warn("""Field 'name' has been deprecated from provider version 1.119.0. New field 'vpc_name' instead.""", DeprecationWarning)
                pulumi.log.warn("""name is deprecated: Field 'name' has been deprecated from provider version 1.119.0. New field 'vpc_name' instead.""")
            __props__.__dict__["name"] = name
            __props__.__dict__["resource_group_id"] = resource_group_id
            __props__.__dict__["secondary_cidr_blocks"] = secondary_cidr_blocks
            __props__.__dict__["tags"] = tags
            __props__.__dict__["user_cidrs"] = user_cidrs
            __props__.__dict__["vpc_name"] = vpc_name
            __props__.__dict__["ipv6_cidr_block"] = None
            __props__.__dict__["route_table_id"] = None
            __props__.__dict__["router_id"] = None
            __props__.__dict__["router_table_id"] = None
            __props__.__dict__["status"] = None
        super(Network, __self__).__init__(
            'alicloud:vpc/network:Network',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            cidr_block: Optional[pulumi.Input[str]] = None,
            description: Optional[pulumi.Input[str]] = None,
            dry_run: Optional[pulumi.Input[bool]] = None,
            enable_ipv6: Optional[pulumi.Input[bool]] = None,
            ipv6_cidr_block: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            resource_group_id: Optional[pulumi.Input[str]] = None,
            route_table_id: Optional[pulumi.Input[str]] = None,
            router_id: Optional[pulumi.Input[str]] = None,
            router_table_id: Optional[pulumi.Input[str]] = None,
            secondary_cidr_blocks: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            status: Optional[pulumi.Input[str]] = None,
            tags: Optional[pulumi.Input[Mapping[str, Any]]] = None,
            user_cidrs: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            vpc_name: Optional[pulumi.Input[str]] = None) -> 'Network':
        """
        Get an existing Network resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] cidr_block: The CIDR block for the VPC. The `cidr_block` is Optional and default value is `172.16.0.0/12` after v1.119.0+.
        :param pulumi.Input[str] description: The VPC description. Defaults to null.
        :param pulumi.Input[bool] dry_run: Specifies whether to precheck this request only. Valid values: `true` and `false`.
        :param pulumi.Input[bool] enable_ipv6: Specifies whether to enable the IPv6 CIDR block. Valid values: `false` (Default): disables IPv6 CIDR blocks. `true`: enables IPv6 CIDR blocks. If the `enable_ipv6` is `true`, the system will automatically create a free version of an IPv6 gateway for your private network and assign an IPv6 network segment assigned as /56.
        :param pulumi.Input[str] ipv6_cidr_block: (Available in v1.119.0+) ) The ipv6 cidr block of VPC.
        :param pulumi.Input[str] name: Field `name` has been deprecated from provider version 1.119.0. New field `vpc_name` instead.
        :param pulumi.Input[str] resource_group_id: The Id of resource group which the VPC belongs.
        :param pulumi.Input[str] route_table_id: The route table ID of the router created by default on VPC creation.
        :param pulumi.Input[str] router_id: The ID of the router created by default on VPC creation.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] secondary_cidr_blocks: The secondary CIDR blocks for the VPC.
        :param pulumi.Input[Mapping[str, Any]] tags: A mapping of tags to assign to the resource.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] user_cidrs: The user cidrs of the VPC.
        :param pulumi.Input[str] vpc_name: The name of the VPC. Defaults to null.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _NetworkState.__new__(_NetworkState)

        __props__.__dict__["cidr_block"] = cidr_block
        __props__.__dict__["description"] = description
        __props__.__dict__["dry_run"] = dry_run
        __props__.__dict__["enable_ipv6"] = enable_ipv6
        __props__.__dict__["ipv6_cidr_block"] = ipv6_cidr_block
        __props__.__dict__["name"] = name
        __props__.__dict__["resource_group_id"] = resource_group_id
        __props__.__dict__["route_table_id"] = route_table_id
        __props__.__dict__["router_id"] = router_id
        __props__.__dict__["router_table_id"] = router_table_id
        __props__.__dict__["secondary_cidr_blocks"] = secondary_cidr_blocks
        __props__.__dict__["status"] = status
        __props__.__dict__["tags"] = tags
        __props__.__dict__["user_cidrs"] = user_cidrs
        __props__.__dict__["vpc_name"] = vpc_name
        return Network(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="cidrBlock")
    def cidr_block(self) -> pulumi.Output[Optional[str]]:
        """
        The CIDR block for the VPC. The `cidr_block` is Optional and default value is `172.16.0.0/12` after v1.119.0+.
        """
        return pulumi.get(self, "cidr_block")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        The VPC description. Defaults to null.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="dryRun")
    def dry_run(self) -> pulumi.Output[Optional[bool]]:
        """
        Specifies whether to precheck this request only. Valid values: `true` and `false`.
        """
        return pulumi.get(self, "dry_run")

    @property
    @pulumi.getter(name="enableIpv6")
    def enable_ipv6(self) -> pulumi.Output[Optional[bool]]:
        """
        Specifies whether to enable the IPv6 CIDR block. Valid values: `false` (Default): disables IPv6 CIDR blocks. `true`: enables IPv6 CIDR blocks. If the `enable_ipv6` is `true`, the system will automatically create a free version of an IPv6 gateway for your private network and assign an IPv6 network segment assigned as /56.
        """
        return pulumi.get(self, "enable_ipv6")

    @property
    @pulumi.getter(name="ipv6CidrBlock")
    def ipv6_cidr_block(self) -> pulumi.Output[str]:
        """
        (Available in v1.119.0+) ) The ipv6 cidr block of VPC.
        """
        return pulumi.get(self, "ipv6_cidr_block")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Field `name` has been deprecated from provider version 1.119.0. New field `vpc_name` instead.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="resourceGroupId")
    def resource_group_id(self) -> pulumi.Output[str]:
        """
        The Id of resource group which the VPC belongs.
        """
        return pulumi.get(self, "resource_group_id")

    @property
    @pulumi.getter(name="routeTableId")
    def route_table_id(self) -> pulumi.Output[str]:
        """
        The route table ID of the router created by default on VPC creation.
        """
        return pulumi.get(self, "route_table_id")

    @property
    @pulumi.getter(name="routerId")
    def router_id(self) -> pulumi.Output[str]:
        """
        The ID of the router created by default on VPC creation.
        """
        return pulumi.get(self, "router_id")

    @property
    @pulumi.getter(name="routerTableId")
    def router_table_id(self) -> pulumi.Output[str]:
        return pulumi.get(self, "router_table_id")

    @property
    @pulumi.getter(name="secondaryCidrBlocks")
    def secondary_cidr_blocks(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        The secondary CIDR blocks for the VPC.
        """
        return pulumi.get(self, "secondary_cidr_blocks")

    @property
    @pulumi.getter
    def status(self) -> pulumi.Output[str]:
        return pulumi.get(self, "status")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, Any]]]:
        """
        A mapping of tags to assign to the resource.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="userCidrs")
    def user_cidrs(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        The user cidrs of the VPC.
        """
        return pulumi.get(self, "user_cidrs")

    @property
    @pulumi.getter(name="vpcName")
    def vpc_name(self) -> pulumi.Output[str]:
        """
        The name of the VPC. Defaults to null.
        """
        return pulumi.get(self, "vpc_name")

