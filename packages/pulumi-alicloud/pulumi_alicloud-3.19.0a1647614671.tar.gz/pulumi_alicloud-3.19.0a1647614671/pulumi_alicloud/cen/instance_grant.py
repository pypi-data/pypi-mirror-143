# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['InstanceGrantArgs', 'InstanceGrant']

@pulumi.input_type
class InstanceGrantArgs:
    def __init__(__self__, *,
                 cen_id: pulumi.Input[str],
                 cen_owner_id: pulumi.Input[str],
                 child_instance_id: pulumi.Input[str]):
        """
        The set of arguments for constructing a InstanceGrant resource.
        :param pulumi.Input[str] cen_id: The ID of the CEN.
        :param pulumi.Input[str] cen_owner_id: The owner UID of the  CEN which the child instance granted to.
        :param pulumi.Input[str] child_instance_id: The ID of the child instance to grant.
        """
        pulumi.set(__self__, "cen_id", cen_id)
        pulumi.set(__self__, "cen_owner_id", cen_owner_id)
        pulumi.set(__self__, "child_instance_id", child_instance_id)

    @property
    @pulumi.getter(name="cenId")
    def cen_id(self) -> pulumi.Input[str]:
        """
        The ID of the CEN.
        """
        return pulumi.get(self, "cen_id")

    @cen_id.setter
    def cen_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "cen_id", value)

    @property
    @pulumi.getter(name="cenOwnerId")
    def cen_owner_id(self) -> pulumi.Input[str]:
        """
        The owner UID of the  CEN which the child instance granted to.
        """
        return pulumi.get(self, "cen_owner_id")

    @cen_owner_id.setter
    def cen_owner_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "cen_owner_id", value)

    @property
    @pulumi.getter(name="childInstanceId")
    def child_instance_id(self) -> pulumi.Input[str]:
        """
        The ID of the child instance to grant.
        """
        return pulumi.get(self, "child_instance_id")

    @child_instance_id.setter
    def child_instance_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "child_instance_id", value)


@pulumi.input_type
class _InstanceGrantState:
    def __init__(__self__, *,
                 cen_id: Optional[pulumi.Input[str]] = None,
                 cen_owner_id: Optional[pulumi.Input[str]] = None,
                 child_instance_id: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering InstanceGrant resources.
        :param pulumi.Input[str] cen_id: The ID of the CEN.
        :param pulumi.Input[str] cen_owner_id: The owner UID of the  CEN which the child instance granted to.
        :param pulumi.Input[str] child_instance_id: The ID of the child instance to grant.
        """
        if cen_id is not None:
            pulumi.set(__self__, "cen_id", cen_id)
        if cen_owner_id is not None:
            pulumi.set(__self__, "cen_owner_id", cen_owner_id)
        if child_instance_id is not None:
            pulumi.set(__self__, "child_instance_id", child_instance_id)

    @property
    @pulumi.getter(name="cenId")
    def cen_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the CEN.
        """
        return pulumi.get(self, "cen_id")

    @cen_id.setter
    def cen_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "cen_id", value)

    @property
    @pulumi.getter(name="cenOwnerId")
    def cen_owner_id(self) -> Optional[pulumi.Input[str]]:
        """
        The owner UID of the  CEN which the child instance granted to.
        """
        return pulumi.get(self, "cen_owner_id")

    @cen_owner_id.setter
    def cen_owner_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "cen_owner_id", value)

    @property
    @pulumi.getter(name="childInstanceId")
    def child_instance_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the child instance to grant.
        """
        return pulumi.get(self, "child_instance_id")

    @child_instance_id.setter
    def child_instance_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "child_instance_id", value)


class InstanceGrant(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 cen_id: Optional[pulumi.Input[str]] = None,
                 cen_owner_id: Optional[pulumi.Input[str]] = None,
                 child_instance_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Provides a CEN child instance grant resource, which allow you to authorize a VPC or VBR to a CEN of a different account.

        For more information about how to use it, see [Attach a network in a different account](https://www.alibabacloud.com/help/doc-detail/73645.htm).

        ## Example Usage

        Basic Usage

        ```python
        import pulumi
        import pulumi_alicloud as alicloud
        import pulumi_pulumi as pulumi

        # Create a new instance-grant and use it to grant one child instance of account1 to a new CEN of account 2.
        account1 = pulumi.providers.Alicloud("account1",
            access_key="access123",
            secret_key="secret123")
        account2 = pulumi.providers.Alicloud("account2",
            access_key="access456",
            secret_key="secret456")
        config = pulumi.Config()
        name = config.get("name")
        if name is None:
            name = "tf-testAccCenInstanceGrantBasic"
        cen = alicloud.cen.Instance("cen", opts=pulumi.ResourceOptions(provider=alicloud["account2"]))
        vpc = alicloud.vpc.Network("vpc", cidr_block="192.168.0.0/16",
        opts=pulumi.ResourceOptions(provider=alicloud["account1"]))
        foo_instance_grant = alicloud.cen.InstanceGrant("fooInstanceGrant",
            cen_id=cen.id,
            child_instance_id=vpc.id,
            cen_owner_id="uid2",
            opts=pulumi.ResourceOptions(provider=alicloud["account1"]))
        foo_instance_attachment = alicloud.cen.InstanceAttachment("fooInstanceAttachment",
            instance_id=cen.id,
            child_instance_id=vpc.id,
            child_instance_type="VPC",
            child_instance_region_id="cn-qingdao",
            child_instance_owner_id="uid1",
            opts=pulumi.ResourceOptions(provider=alicloud["account2"],
                depends_on=[foo_instance_grant]))
        ```

        ## Import

        CEN instance can be imported using the id, e.g.

        ```sh
         $ pulumi import alicloud:cen/instanceGrant:InstanceGrant example cen-abc123456:vpc-abc123456:uid123456
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] cen_id: The ID of the CEN.
        :param pulumi.Input[str] cen_owner_id: The owner UID of the  CEN which the child instance granted to.
        :param pulumi.Input[str] child_instance_id: The ID of the child instance to grant.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: InstanceGrantArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a CEN child instance grant resource, which allow you to authorize a VPC or VBR to a CEN of a different account.

        For more information about how to use it, see [Attach a network in a different account](https://www.alibabacloud.com/help/doc-detail/73645.htm).

        ## Example Usage

        Basic Usage

        ```python
        import pulumi
        import pulumi_alicloud as alicloud
        import pulumi_pulumi as pulumi

        # Create a new instance-grant and use it to grant one child instance of account1 to a new CEN of account 2.
        account1 = pulumi.providers.Alicloud("account1",
            access_key="access123",
            secret_key="secret123")
        account2 = pulumi.providers.Alicloud("account2",
            access_key="access456",
            secret_key="secret456")
        config = pulumi.Config()
        name = config.get("name")
        if name is None:
            name = "tf-testAccCenInstanceGrantBasic"
        cen = alicloud.cen.Instance("cen", opts=pulumi.ResourceOptions(provider=alicloud["account2"]))
        vpc = alicloud.vpc.Network("vpc", cidr_block="192.168.0.0/16",
        opts=pulumi.ResourceOptions(provider=alicloud["account1"]))
        foo_instance_grant = alicloud.cen.InstanceGrant("fooInstanceGrant",
            cen_id=cen.id,
            child_instance_id=vpc.id,
            cen_owner_id="uid2",
            opts=pulumi.ResourceOptions(provider=alicloud["account1"]))
        foo_instance_attachment = alicloud.cen.InstanceAttachment("fooInstanceAttachment",
            instance_id=cen.id,
            child_instance_id=vpc.id,
            child_instance_type="VPC",
            child_instance_region_id="cn-qingdao",
            child_instance_owner_id="uid1",
            opts=pulumi.ResourceOptions(provider=alicloud["account2"],
                depends_on=[foo_instance_grant]))
        ```

        ## Import

        CEN instance can be imported using the id, e.g.

        ```sh
         $ pulumi import alicloud:cen/instanceGrant:InstanceGrant example cen-abc123456:vpc-abc123456:uid123456
        ```

        :param str resource_name: The name of the resource.
        :param InstanceGrantArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(InstanceGrantArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 cen_id: Optional[pulumi.Input[str]] = None,
                 cen_owner_id: Optional[pulumi.Input[str]] = None,
                 child_instance_id: Optional[pulumi.Input[str]] = None,
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
            __props__ = InstanceGrantArgs.__new__(InstanceGrantArgs)

            if cen_id is None and not opts.urn:
                raise TypeError("Missing required property 'cen_id'")
            __props__.__dict__["cen_id"] = cen_id
            if cen_owner_id is None and not opts.urn:
                raise TypeError("Missing required property 'cen_owner_id'")
            __props__.__dict__["cen_owner_id"] = cen_owner_id
            if child_instance_id is None and not opts.urn:
                raise TypeError("Missing required property 'child_instance_id'")
            __props__.__dict__["child_instance_id"] = child_instance_id
        super(InstanceGrant, __self__).__init__(
            'alicloud:cen/instanceGrant:InstanceGrant',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            cen_id: Optional[pulumi.Input[str]] = None,
            cen_owner_id: Optional[pulumi.Input[str]] = None,
            child_instance_id: Optional[pulumi.Input[str]] = None) -> 'InstanceGrant':
        """
        Get an existing InstanceGrant resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] cen_id: The ID of the CEN.
        :param pulumi.Input[str] cen_owner_id: The owner UID of the  CEN which the child instance granted to.
        :param pulumi.Input[str] child_instance_id: The ID of the child instance to grant.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _InstanceGrantState.__new__(_InstanceGrantState)

        __props__.__dict__["cen_id"] = cen_id
        __props__.__dict__["cen_owner_id"] = cen_owner_id
        __props__.__dict__["child_instance_id"] = child_instance_id
        return InstanceGrant(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="cenId")
    def cen_id(self) -> pulumi.Output[str]:
        """
        The ID of the CEN.
        """
        return pulumi.get(self, "cen_id")

    @property
    @pulumi.getter(name="cenOwnerId")
    def cen_owner_id(self) -> pulumi.Output[str]:
        """
        The owner UID of the  CEN which the child instance granted to.
        """
        return pulumi.get(self, "cen_owner_id")

    @property
    @pulumi.getter(name="childInstanceId")
    def child_instance_id(self) -> pulumi.Output[str]:
        """
        The ID of the child instance to grant.
        """
        return pulumi.get(self, "child_instance_id")

