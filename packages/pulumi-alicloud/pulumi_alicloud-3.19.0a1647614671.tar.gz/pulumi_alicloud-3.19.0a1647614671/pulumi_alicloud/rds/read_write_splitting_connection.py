# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['ReadWriteSplittingConnectionArgs', 'ReadWriteSplittingConnection']

@pulumi.input_type
class ReadWriteSplittingConnectionArgs:
    def __init__(__self__, *,
                 distribution_type: pulumi.Input[str],
                 instance_id: pulumi.Input[str],
                 connection_prefix: Optional[pulumi.Input[str]] = None,
                 max_delay_time: Optional[pulumi.Input[int]] = None,
                 port: Optional[pulumi.Input[int]] = None,
                 weight: Optional[pulumi.Input[Mapping[str, Any]]] = None):
        """
        The set of arguments for constructing a ReadWriteSplittingConnection resource.
        :param pulumi.Input[str] distribution_type: Read weight distribution mode. Values are as follows: `Standard` indicates automatic weight distribution based on types, `Custom` indicates custom weight distribution.
        :param pulumi.Input[str] instance_id: The Id of instance that can run database.
        :param pulumi.Input[str] connection_prefix: Prefix of an Internet connection string. It must be checked for uniqueness. It may consist of lowercase letters, numbers, and underlines, and must start with a letter and have no more than 30 characters. Default to <instance_id> + 'rw'.
        :param pulumi.Input[int] max_delay_time: Delay threshold, in seconds. The value range is 0 to 7200. Default to 30. Read requests are not routed to the read-only instances with a delay greater than the threshold.
        :param pulumi.Input[int] port: Intranet connection port. Valid value: [3001-3999]. Default to 3306.
        :param pulumi.Input[Mapping[str, Any]] weight: Read weight distribution. Read weights increase at a step of 100 up to 10,000. Enter weights in the following format: {"Instanceid":"Weight","Instanceid":"Weight"}. This parameter must be set when distribution_type is set to Custom.
        """
        pulumi.set(__self__, "distribution_type", distribution_type)
        pulumi.set(__self__, "instance_id", instance_id)
        if connection_prefix is not None:
            pulumi.set(__self__, "connection_prefix", connection_prefix)
        if max_delay_time is not None:
            pulumi.set(__self__, "max_delay_time", max_delay_time)
        if port is not None:
            pulumi.set(__self__, "port", port)
        if weight is not None:
            pulumi.set(__self__, "weight", weight)

    @property
    @pulumi.getter(name="distributionType")
    def distribution_type(self) -> pulumi.Input[str]:
        """
        Read weight distribution mode. Values are as follows: `Standard` indicates automatic weight distribution based on types, `Custom` indicates custom weight distribution.
        """
        return pulumi.get(self, "distribution_type")

    @distribution_type.setter
    def distribution_type(self, value: pulumi.Input[str]):
        pulumi.set(self, "distribution_type", value)

    @property
    @pulumi.getter(name="instanceId")
    def instance_id(self) -> pulumi.Input[str]:
        """
        The Id of instance that can run database.
        """
        return pulumi.get(self, "instance_id")

    @instance_id.setter
    def instance_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "instance_id", value)

    @property
    @pulumi.getter(name="connectionPrefix")
    def connection_prefix(self) -> Optional[pulumi.Input[str]]:
        """
        Prefix of an Internet connection string. It must be checked for uniqueness. It may consist of lowercase letters, numbers, and underlines, and must start with a letter and have no more than 30 characters. Default to <instance_id> + 'rw'.
        """
        return pulumi.get(self, "connection_prefix")

    @connection_prefix.setter
    def connection_prefix(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "connection_prefix", value)

    @property
    @pulumi.getter(name="maxDelayTime")
    def max_delay_time(self) -> Optional[pulumi.Input[int]]:
        """
        Delay threshold, in seconds. The value range is 0 to 7200. Default to 30. Read requests are not routed to the read-only instances with a delay greater than the threshold.
        """
        return pulumi.get(self, "max_delay_time")

    @max_delay_time.setter
    def max_delay_time(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "max_delay_time", value)

    @property
    @pulumi.getter
    def port(self) -> Optional[pulumi.Input[int]]:
        """
        Intranet connection port. Valid value: [3001-3999]. Default to 3306.
        """
        return pulumi.get(self, "port")

    @port.setter
    def port(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "port", value)

    @property
    @pulumi.getter
    def weight(self) -> Optional[pulumi.Input[Mapping[str, Any]]]:
        """
        Read weight distribution. Read weights increase at a step of 100 up to 10,000. Enter weights in the following format: {"Instanceid":"Weight","Instanceid":"Weight"}. This parameter must be set when distribution_type is set to Custom.
        """
        return pulumi.get(self, "weight")

    @weight.setter
    def weight(self, value: Optional[pulumi.Input[Mapping[str, Any]]]):
        pulumi.set(self, "weight", value)


@pulumi.input_type
class _ReadWriteSplittingConnectionState:
    def __init__(__self__, *,
                 connection_prefix: Optional[pulumi.Input[str]] = None,
                 connection_string: Optional[pulumi.Input[str]] = None,
                 distribution_type: Optional[pulumi.Input[str]] = None,
                 instance_id: Optional[pulumi.Input[str]] = None,
                 max_delay_time: Optional[pulumi.Input[int]] = None,
                 port: Optional[pulumi.Input[int]] = None,
                 weight: Optional[pulumi.Input[Mapping[str, Any]]] = None):
        """
        Input properties used for looking up and filtering ReadWriteSplittingConnection resources.
        :param pulumi.Input[str] connection_prefix: Prefix of an Internet connection string. It must be checked for uniqueness. It may consist of lowercase letters, numbers, and underlines, and must start with a letter and have no more than 30 characters. Default to <instance_id> + 'rw'.
        :param pulumi.Input[str] connection_string: Connection instance string.
        :param pulumi.Input[str] distribution_type: Read weight distribution mode. Values are as follows: `Standard` indicates automatic weight distribution based on types, `Custom` indicates custom weight distribution.
        :param pulumi.Input[str] instance_id: The Id of instance that can run database.
        :param pulumi.Input[int] max_delay_time: Delay threshold, in seconds. The value range is 0 to 7200. Default to 30. Read requests are not routed to the read-only instances with a delay greater than the threshold.
        :param pulumi.Input[int] port: Intranet connection port. Valid value: [3001-3999]. Default to 3306.
        :param pulumi.Input[Mapping[str, Any]] weight: Read weight distribution. Read weights increase at a step of 100 up to 10,000. Enter weights in the following format: {"Instanceid":"Weight","Instanceid":"Weight"}. This parameter must be set when distribution_type is set to Custom.
        """
        if connection_prefix is not None:
            pulumi.set(__self__, "connection_prefix", connection_prefix)
        if connection_string is not None:
            pulumi.set(__self__, "connection_string", connection_string)
        if distribution_type is not None:
            pulumi.set(__self__, "distribution_type", distribution_type)
        if instance_id is not None:
            pulumi.set(__self__, "instance_id", instance_id)
        if max_delay_time is not None:
            pulumi.set(__self__, "max_delay_time", max_delay_time)
        if port is not None:
            pulumi.set(__self__, "port", port)
        if weight is not None:
            pulumi.set(__self__, "weight", weight)

    @property
    @pulumi.getter(name="connectionPrefix")
    def connection_prefix(self) -> Optional[pulumi.Input[str]]:
        """
        Prefix of an Internet connection string. It must be checked for uniqueness. It may consist of lowercase letters, numbers, and underlines, and must start with a letter and have no more than 30 characters. Default to <instance_id> + 'rw'.
        """
        return pulumi.get(self, "connection_prefix")

    @connection_prefix.setter
    def connection_prefix(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "connection_prefix", value)

    @property
    @pulumi.getter(name="connectionString")
    def connection_string(self) -> Optional[pulumi.Input[str]]:
        """
        Connection instance string.
        """
        return pulumi.get(self, "connection_string")

    @connection_string.setter
    def connection_string(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "connection_string", value)

    @property
    @pulumi.getter(name="distributionType")
    def distribution_type(self) -> Optional[pulumi.Input[str]]:
        """
        Read weight distribution mode. Values are as follows: `Standard` indicates automatic weight distribution based on types, `Custom` indicates custom weight distribution.
        """
        return pulumi.get(self, "distribution_type")

    @distribution_type.setter
    def distribution_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "distribution_type", value)

    @property
    @pulumi.getter(name="instanceId")
    def instance_id(self) -> Optional[pulumi.Input[str]]:
        """
        The Id of instance that can run database.
        """
        return pulumi.get(self, "instance_id")

    @instance_id.setter
    def instance_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "instance_id", value)

    @property
    @pulumi.getter(name="maxDelayTime")
    def max_delay_time(self) -> Optional[pulumi.Input[int]]:
        """
        Delay threshold, in seconds. The value range is 0 to 7200. Default to 30. Read requests are not routed to the read-only instances with a delay greater than the threshold.
        """
        return pulumi.get(self, "max_delay_time")

    @max_delay_time.setter
    def max_delay_time(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "max_delay_time", value)

    @property
    @pulumi.getter
    def port(self) -> Optional[pulumi.Input[int]]:
        """
        Intranet connection port. Valid value: [3001-3999]. Default to 3306.
        """
        return pulumi.get(self, "port")

    @port.setter
    def port(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "port", value)

    @property
    @pulumi.getter
    def weight(self) -> Optional[pulumi.Input[Mapping[str, Any]]]:
        """
        Read weight distribution. Read weights increase at a step of 100 up to 10,000. Enter weights in the following format: {"Instanceid":"Weight","Instanceid":"Weight"}. This parameter must be set when distribution_type is set to Custom.
        """
        return pulumi.get(self, "weight")

    @weight.setter
    def weight(self, value: Optional[pulumi.Input[Mapping[str, Any]]]):
        pulumi.set(self, "weight", value)


class ReadWriteSplittingConnection(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 connection_prefix: Optional[pulumi.Input[str]] = None,
                 distribution_type: Optional[pulumi.Input[str]] = None,
                 instance_id: Optional[pulumi.Input[str]] = None,
                 max_delay_time: Optional[pulumi.Input[int]] = None,
                 port: Optional[pulumi.Input[int]] = None,
                 weight: Optional[pulumi.Input[Mapping[str, Any]]] = None,
                 __props__=None):
        """
        Provides an RDS read write splitting connection resource to allocate an Intranet connection string for RDS instance.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_alicloud as alicloud

        config = pulumi.Config()
        creation = config.get("creation")
        if creation is None:
            creation = "Rds"
        name = config.get("name")
        if name is None:
            name = "dbInstancevpc"
        default_zones = alicloud.get_zones(available_resource_creation=creation)
        default_network = alicloud.vpc.Network("defaultNetwork",
            vpc_name=name,
            cidr_block="172.16.0.0/16")
        default_switch = alicloud.vpc.Switch("defaultSwitch",
            vpc_id=default_network.id,
            cidr_block="172.16.0.0/24",
            zone_id=default_zones.zones[0].id,
            vswitch_name=name)
        default_instance = alicloud.rds.Instance("defaultInstance",
            engine="MySQL",
            engine_version="5.6",
            instance_type="rds.mysql.t1.small",
            instance_storage=20,
            instance_charge_type="Postpaid",
            instance_name=name,
            vswitch_id=default_switch.id,
            security_ips=[
                "10.168.1.12",
                "100.69.7.112",
            ])
        default_read_only_instance = alicloud.rds.ReadOnlyInstance("defaultReadOnlyInstance",
            master_db_instance_id=default_instance.id,
            zone_id=default_instance.zone_id,
            engine_version=default_instance.engine_version,
            instance_type=default_instance.instance_type,
            instance_storage=30,
            instance_name=f"{name}ro",
            vswitch_id=default_switch.id)
        default_read_write_splitting_connection = alicloud.rds.ReadWriteSplittingConnection("defaultReadWriteSplittingConnection",
            instance_id=default_instance.id,
            connection_prefix="t-con-123",
            distribution_type="Standard",
            opts=pulumi.ResourceOptions(depends_on=[default_read_only_instance]))
        ```

        > **NOTE:** Resource `rds.ReadWriteSplittingConnection` should be created after `rds.ReadOnlyInstance`, so the `depends_on` statement is necessary.

        ## Import

        RDS read write splitting connection can be imported using the id, e.g.

        ```sh
         $ pulumi import alicloud:rds/readWriteSplittingConnection:ReadWriteSplittingConnection example abc12345678
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] connection_prefix: Prefix of an Internet connection string. It must be checked for uniqueness. It may consist of lowercase letters, numbers, and underlines, and must start with a letter and have no more than 30 characters. Default to <instance_id> + 'rw'.
        :param pulumi.Input[str] distribution_type: Read weight distribution mode. Values are as follows: `Standard` indicates automatic weight distribution based on types, `Custom` indicates custom weight distribution.
        :param pulumi.Input[str] instance_id: The Id of instance that can run database.
        :param pulumi.Input[int] max_delay_time: Delay threshold, in seconds. The value range is 0 to 7200. Default to 30. Read requests are not routed to the read-only instances with a delay greater than the threshold.
        :param pulumi.Input[int] port: Intranet connection port. Valid value: [3001-3999]. Default to 3306.
        :param pulumi.Input[Mapping[str, Any]] weight: Read weight distribution. Read weights increase at a step of 100 up to 10,000. Enter weights in the following format: {"Instanceid":"Weight","Instanceid":"Weight"}. This parameter must be set when distribution_type is set to Custom.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ReadWriteSplittingConnectionArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides an RDS read write splitting connection resource to allocate an Intranet connection string for RDS instance.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_alicloud as alicloud

        config = pulumi.Config()
        creation = config.get("creation")
        if creation is None:
            creation = "Rds"
        name = config.get("name")
        if name is None:
            name = "dbInstancevpc"
        default_zones = alicloud.get_zones(available_resource_creation=creation)
        default_network = alicloud.vpc.Network("defaultNetwork",
            vpc_name=name,
            cidr_block="172.16.0.0/16")
        default_switch = alicloud.vpc.Switch("defaultSwitch",
            vpc_id=default_network.id,
            cidr_block="172.16.0.0/24",
            zone_id=default_zones.zones[0].id,
            vswitch_name=name)
        default_instance = alicloud.rds.Instance("defaultInstance",
            engine="MySQL",
            engine_version="5.6",
            instance_type="rds.mysql.t1.small",
            instance_storage=20,
            instance_charge_type="Postpaid",
            instance_name=name,
            vswitch_id=default_switch.id,
            security_ips=[
                "10.168.1.12",
                "100.69.7.112",
            ])
        default_read_only_instance = alicloud.rds.ReadOnlyInstance("defaultReadOnlyInstance",
            master_db_instance_id=default_instance.id,
            zone_id=default_instance.zone_id,
            engine_version=default_instance.engine_version,
            instance_type=default_instance.instance_type,
            instance_storage=30,
            instance_name=f"{name}ro",
            vswitch_id=default_switch.id)
        default_read_write_splitting_connection = alicloud.rds.ReadWriteSplittingConnection("defaultReadWriteSplittingConnection",
            instance_id=default_instance.id,
            connection_prefix="t-con-123",
            distribution_type="Standard",
            opts=pulumi.ResourceOptions(depends_on=[default_read_only_instance]))
        ```

        > **NOTE:** Resource `rds.ReadWriteSplittingConnection` should be created after `rds.ReadOnlyInstance`, so the `depends_on` statement is necessary.

        ## Import

        RDS read write splitting connection can be imported using the id, e.g.

        ```sh
         $ pulumi import alicloud:rds/readWriteSplittingConnection:ReadWriteSplittingConnection example abc12345678
        ```

        :param str resource_name: The name of the resource.
        :param ReadWriteSplittingConnectionArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ReadWriteSplittingConnectionArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 connection_prefix: Optional[pulumi.Input[str]] = None,
                 distribution_type: Optional[pulumi.Input[str]] = None,
                 instance_id: Optional[pulumi.Input[str]] = None,
                 max_delay_time: Optional[pulumi.Input[int]] = None,
                 port: Optional[pulumi.Input[int]] = None,
                 weight: Optional[pulumi.Input[Mapping[str, Any]]] = None,
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
            __props__ = ReadWriteSplittingConnectionArgs.__new__(ReadWriteSplittingConnectionArgs)

            __props__.__dict__["connection_prefix"] = connection_prefix
            if distribution_type is None and not opts.urn:
                raise TypeError("Missing required property 'distribution_type'")
            __props__.__dict__["distribution_type"] = distribution_type
            if instance_id is None and not opts.urn:
                raise TypeError("Missing required property 'instance_id'")
            __props__.__dict__["instance_id"] = instance_id
            __props__.__dict__["max_delay_time"] = max_delay_time
            __props__.__dict__["port"] = port
            __props__.__dict__["weight"] = weight
            __props__.__dict__["connection_string"] = None
        super(ReadWriteSplittingConnection, __self__).__init__(
            'alicloud:rds/readWriteSplittingConnection:ReadWriteSplittingConnection',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            connection_prefix: Optional[pulumi.Input[str]] = None,
            connection_string: Optional[pulumi.Input[str]] = None,
            distribution_type: Optional[pulumi.Input[str]] = None,
            instance_id: Optional[pulumi.Input[str]] = None,
            max_delay_time: Optional[pulumi.Input[int]] = None,
            port: Optional[pulumi.Input[int]] = None,
            weight: Optional[pulumi.Input[Mapping[str, Any]]] = None) -> 'ReadWriteSplittingConnection':
        """
        Get an existing ReadWriteSplittingConnection resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] connection_prefix: Prefix of an Internet connection string. It must be checked for uniqueness. It may consist of lowercase letters, numbers, and underlines, and must start with a letter and have no more than 30 characters. Default to <instance_id> + 'rw'.
        :param pulumi.Input[str] connection_string: Connection instance string.
        :param pulumi.Input[str] distribution_type: Read weight distribution mode. Values are as follows: `Standard` indicates automatic weight distribution based on types, `Custom` indicates custom weight distribution.
        :param pulumi.Input[str] instance_id: The Id of instance that can run database.
        :param pulumi.Input[int] max_delay_time: Delay threshold, in seconds. The value range is 0 to 7200. Default to 30. Read requests are not routed to the read-only instances with a delay greater than the threshold.
        :param pulumi.Input[int] port: Intranet connection port. Valid value: [3001-3999]. Default to 3306.
        :param pulumi.Input[Mapping[str, Any]] weight: Read weight distribution. Read weights increase at a step of 100 up to 10,000. Enter weights in the following format: {"Instanceid":"Weight","Instanceid":"Weight"}. This parameter must be set when distribution_type is set to Custom.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _ReadWriteSplittingConnectionState.__new__(_ReadWriteSplittingConnectionState)

        __props__.__dict__["connection_prefix"] = connection_prefix
        __props__.__dict__["connection_string"] = connection_string
        __props__.__dict__["distribution_type"] = distribution_type
        __props__.__dict__["instance_id"] = instance_id
        __props__.__dict__["max_delay_time"] = max_delay_time
        __props__.__dict__["port"] = port
        __props__.__dict__["weight"] = weight
        return ReadWriteSplittingConnection(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="connectionPrefix")
    def connection_prefix(self) -> pulumi.Output[Optional[str]]:
        """
        Prefix of an Internet connection string. It must be checked for uniqueness. It may consist of lowercase letters, numbers, and underlines, and must start with a letter and have no more than 30 characters. Default to <instance_id> + 'rw'.
        """
        return pulumi.get(self, "connection_prefix")

    @property
    @pulumi.getter(name="connectionString")
    def connection_string(self) -> pulumi.Output[str]:
        """
        Connection instance string.
        """
        return pulumi.get(self, "connection_string")

    @property
    @pulumi.getter(name="distributionType")
    def distribution_type(self) -> pulumi.Output[str]:
        """
        Read weight distribution mode. Values are as follows: `Standard` indicates automatic weight distribution based on types, `Custom` indicates custom weight distribution.
        """
        return pulumi.get(self, "distribution_type")

    @property
    @pulumi.getter(name="instanceId")
    def instance_id(self) -> pulumi.Output[str]:
        """
        The Id of instance that can run database.
        """
        return pulumi.get(self, "instance_id")

    @property
    @pulumi.getter(name="maxDelayTime")
    def max_delay_time(self) -> pulumi.Output[int]:
        """
        Delay threshold, in seconds. The value range is 0 to 7200. Default to 30. Read requests are not routed to the read-only instances with a delay greater than the threshold.
        """
        return pulumi.get(self, "max_delay_time")

    @property
    @pulumi.getter
    def port(self) -> pulumi.Output[int]:
        """
        Intranet connection port. Valid value: [3001-3999]. Default to 3306.
        """
        return pulumi.get(self, "port")

    @property
    @pulumi.getter
    def weight(self) -> pulumi.Output[Optional[Mapping[str, Any]]]:
        """
        Read weight distribution. Read weights increase at a step of 100 up to 10,000. Enter weights in the following format: {"Instanceid":"Weight","Instanceid":"Weight"}. This parameter must be set when distribution_type is set to Custom.
        """
        return pulumi.get(self, "weight")

