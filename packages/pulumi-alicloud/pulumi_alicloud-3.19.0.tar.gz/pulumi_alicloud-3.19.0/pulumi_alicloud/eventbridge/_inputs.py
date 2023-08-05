# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = [
    'RuleTargetArgs',
    'RuleTargetParamListArgs',
]

@pulumi.input_type
class RuleTargetArgs:
    def __init__(__self__, *,
                 endpoint: pulumi.Input[str],
                 param_lists: pulumi.Input[Sequence[pulumi.Input['RuleTargetParamListArgs']]],
                 target_id: pulumi.Input[str],
                 type: pulumi.Input[str]):
        """
        :param pulumi.Input[str] endpoint: The endpoint of target.
        :param pulumi.Input[Sequence[pulumi.Input['RuleTargetParamListArgs']]] param_lists: A list of param.
        :param pulumi.Input[str] target_id: The ID of target.
        :param pulumi.Input[str] type: The type of target. Valid values: `acs.fc.function`, `acs.mns.topic`, `acs.mns.queue`,`http`,`acs.sms`,`acs.mail`,`acs.dingtalk`,`https`, `acs.eventbridge`,`acs.rabbitmq` and `acs.rocketmq`.
        """
        pulumi.set(__self__, "endpoint", endpoint)
        pulumi.set(__self__, "param_lists", param_lists)
        pulumi.set(__self__, "target_id", target_id)
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def endpoint(self) -> pulumi.Input[str]:
        """
        The endpoint of target.
        """
        return pulumi.get(self, "endpoint")

    @endpoint.setter
    def endpoint(self, value: pulumi.Input[str]):
        pulumi.set(self, "endpoint", value)

    @property
    @pulumi.getter(name="paramLists")
    def param_lists(self) -> pulumi.Input[Sequence[pulumi.Input['RuleTargetParamListArgs']]]:
        """
        A list of param.
        """
        return pulumi.get(self, "param_lists")

    @param_lists.setter
    def param_lists(self, value: pulumi.Input[Sequence[pulumi.Input['RuleTargetParamListArgs']]]):
        pulumi.set(self, "param_lists", value)

    @property
    @pulumi.getter(name="targetId")
    def target_id(self) -> pulumi.Input[str]:
        """
        The ID of target.
        """
        return pulumi.get(self, "target_id")

    @target_id.setter
    def target_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "target_id", value)

    @property
    @pulumi.getter
    def type(self) -> pulumi.Input[str]:
        """
        The type of target. Valid values: `acs.fc.function`, `acs.mns.topic`, `acs.mns.queue`,`http`,`acs.sms`,`acs.mail`,`acs.dingtalk`,`https`, `acs.eventbridge`,`acs.rabbitmq` and `acs.rocketmq`.
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: pulumi.Input[str]):
        pulumi.set(self, "type", value)


@pulumi.input_type
class RuleTargetParamListArgs:
    def __init__(__self__, *,
                 form: pulumi.Input[str],
                 resource_key: pulumi.Input[str],
                 template: Optional[pulumi.Input[str]] = None,
                 value: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] form: The format of param.  Valid values: `ORIGINAL`, `TEMPLATE`, `JSONPATH`, `CONSTANT`.
        :param pulumi.Input[str] resource_key: The resource key of param.  For more information, see [Event target parameters](https://help.aliyun.com/document_detail/185887.htm)
        :param pulumi.Input[str] template: The template of param.
        :param pulumi.Input[str] value: The value of param.
        """
        pulumi.set(__self__, "form", form)
        pulumi.set(__self__, "resource_key", resource_key)
        if template is not None:
            pulumi.set(__self__, "template", template)
        if value is not None:
            pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def form(self) -> pulumi.Input[str]:
        """
        The format of param.  Valid values: `ORIGINAL`, `TEMPLATE`, `JSONPATH`, `CONSTANT`.
        """
        return pulumi.get(self, "form")

    @form.setter
    def form(self, value: pulumi.Input[str]):
        pulumi.set(self, "form", value)

    @property
    @pulumi.getter(name="resourceKey")
    def resource_key(self) -> pulumi.Input[str]:
        """
        The resource key of param.  For more information, see [Event target parameters](https://help.aliyun.com/document_detail/185887.htm)
        """
        return pulumi.get(self, "resource_key")

    @resource_key.setter
    def resource_key(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_key", value)

    @property
    @pulumi.getter
    def template(self) -> Optional[pulumi.Input[str]]:
        """
        The template of param.
        """
        return pulumi.get(self, "template")

    @template.setter
    def template(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "template", value)

    @property
    @pulumi.getter
    def value(self) -> Optional[pulumi.Input[str]]:
        """
        The value of param.
        """
        return pulumi.get(self, "value")

    @value.setter
    def value(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "value", value)


