# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = [
    'DomainConfigFunctionArgArgs',
    'DomainSourceArgs',
    'IpaDomainSourceArgs',
]

@pulumi.input_type
class DomainConfigFunctionArgArgs:
    def __init__(__self__, *,
                 arg_name: pulumi.Input[str],
                 arg_value: pulumi.Input[str]):
        """
        :param pulumi.Input[str] arg_name: The name of arg.
        :param pulumi.Input[str] arg_value: The value of arg.
        """
        pulumi.set(__self__, "arg_name", arg_name)
        pulumi.set(__self__, "arg_value", arg_value)

    @property
    @pulumi.getter(name="argName")
    def arg_name(self) -> pulumi.Input[str]:
        """
        The name of arg.
        """
        return pulumi.get(self, "arg_name")

    @arg_name.setter
    def arg_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "arg_name", value)

    @property
    @pulumi.getter(name="argValue")
    def arg_value(self) -> pulumi.Input[str]:
        """
        The value of arg.
        """
        return pulumi.get(self, "arg_value")

    @arg_value.setter
    def arg_value(self, value: pulumi.Input[str]):
        pulumi.set(self, "arg_value", value)


@pulumi.input_type
class DomainSourceArgs:
    def __init__(__self__, *,
                 content: pulumi.Input[str],
                 type: pulumi.Input[str],
                 port: Optional[pulumi.Input[int]] = None,
                 priority: Optional[pulumi.Input[str]] = None,
                 weight: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] content: The origin address.
        :param pulumi.Input[str] type: The type of the origin. Valid values:
               `ipaddr`: The origin is configured using an IP address.
               `domain`: The origin is configured using a domain name.
               `oss`: The origin is configured using the Internet domain name of an Alibaba Cloud Object Storage Service (OSS) bucket.
        :param pulumi.Input[int] port: The port number. Valid values: `443` and `80`. Default to `80`.
        :param pulumi.Input[str] priority: The priority of the origin if multiple origins are specified. Default to `20`.
        :param pulumi.Input[str] weight: The weight of the origin if multiple origins are specified. Default to `10`.
        """
        pulumi.set(__self__, "content", content)
        pulumi.set(__self__, "type", type)
        if port is not None:
            pulumi.set(__self__, "port", port)
        if priority is not None:
            pulumi.set(__self__, "priority", priority)
        if weight is not None:
            pulumi.set(__self__, "weight", weight)

    @property
    @pulumi.getter
    def content(self) -> pulumi.Input[str]:
        """
        The origin address.
        """
        return pulumi.get(self, "content")

    @content.setter
    def content(self, value: pulumi.Input[str]):
        pulumi.set(self, "content", value)

    @property
    @pulumi.getter
    def type(self) -> pulumi.Input[str]:
        """
        The type of the origin. Valid values:
        `ipaddr`: The origin is configured using an IP address.
        `domain`: The origin is configured using a domain name.
        `oss`: The origin is configured using the Internet domain name of an Alibaba Cloud Object Storage Service (OSS) bucket.
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: pulumi.Input[str]):
        pulumi.set(self, "type", value)

    @property
    @pulumi.getter
    def port(self) -> Optional[pulumi.Input[int]]:
        """
        The port number. Valid values: `443` and `80`. Default to `80`.
        """
        return pulumi.get(self, "port")

    @port.setter
    def port(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "port", value)

    @property
    @pulumi.getter
    def priority(self) -> Optional[pulumi.Input[str]]:
        """
        The priority of the origin if multiple origins are specified. Default to `20`.
        """
        return pulumi.get(self, "priority")

    @priority.setter
    def priority(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "priority", value)

    @property
    @pulumi.getter
    def weight(self) -> Optional[pulumi.Input[str]]:
        """
        The weight of the origin if multiple origins are specified. Default to `10`.
        """
        return pulumi.get(self, "weight")

    @weight.setter
    def weight(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "weight", value)


@pulumi.input_type
class IpaDomainSourceArgs:
    def __init__(__self__, *,
                 content: pulumi.Input[str],
                 port: pulumi.Input[int],
                 priority: pulumi.Input[str],
                 type: pulumi.Input[str],
                 weight: pulumi.Input[int]):
        """
        :param pulumi.Input[str] content: The address of the origin server. You can specify an IP address or a domain name.
        :param pulumi.Input[int] port: The custom port number. Valid values: `0` to `65535`.
        :param pulumi.Input[str] priority: The priority of the origin server. Valid values: `20` and `30`. Default value: `20`. A value of 20 specifies that the origin is a primary origin. A value of 30 specifies that the origin is a secondary origin.
        :param pulumi.Input[str] type: The type of the origin server. Valid values: `ipaddr`, `domain`, `oss`.
        :param pulumi.Input[int] weight: The weight of the origin server. You must specify a value that is less than `100`. Default value: `10`.
        """
        pulumi.set(__self__, "content", content)
        pulumi.set(__self__, "port", port)
        pulumi.set(__self__, "priority", priority)
        pulumi.set(__self__, "type", type)
        pulumi.set(__self__, "weight", weight)

    @property
    @pulumi.getter
    def content(self) -> pulumi.Input[str]:
        """
        The address of the origin server. You can specify an IP address or a domain name.
        """
        return pulumi.get(self, "content")

    @content.setter
    def content(self, value: pulumi.Input[str]):
        pulumi.set(self, "content", value)

    @property
    @pulumi.getter
    def port(self) -> pulumi.Input[int]:
        """
        The custom port number. Valid values: `0` to `65535`.
        """
        return pulumi.get(self, "port")

    @port.setter
    def port(self, value: pulumi.Input[int]):
        pulumi.set(self, "port", value)

    @property
    @pulumi.getter
    def priority(self) -> pulumi.Input[str]:
        """
        The priority of the origin server. Valid values: `20` and `30`. Default value: `20`. A value of 20 specifies that the origin is a primary origin. A value of 30 specifies that the origin is a secondary origin.
        """
        return pulumi.get(self, "priority")

    @priority.setter
    def priority(self, value: pulumi.Input[str]):
        pulumi.set(self, "priority", value)

    @property
    @pulumi.getter
    def type(self) -> pulumi.Input[str]:
        """
        The type of the origin server. Valid values: `ipaddr`, `domain`, `oss`.
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: pulumi.Input[str]):
        pulumi.set(self, "type", value)

    @property
    @pulumi.getter
    def weight(self) -> pulumi.Input[int]:
        """
        The weight of the origin server. You must specify a value that is less than `100`. Default value: `10`.
        """
        return pulumi.get(self, "weight")

    @weight.setter
    def weight(self, value: pulumi.Input[int]):
        pulumi.set(self, "weight", value)


