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
    'GetRulesResult',
    'AwaitableGetRulesResult',
    'get_rules',
    'get_rules_output',
]

@pulumi.output_type
class GetRulesResult:
    """
    A collection of values returned by getRules.
    """
    def __init__(__self__, category=None, content_category=None, custom_type=None, enable_details=None, id=None, ids=None, name=None, name_regex=None, names=None, output_file=None, product_id=None, risk_level_id=None, rule_type=None, rules=None, status=None, warn_level=None):
        if category and not isinstance(category, int):
            raise TypeError("Expected argument 'category' to be a int")
        pulumi.set(__self__, "category", category)
        if content_category and not isinstance(content_category, str):
            raise TypeError("Expected argument 'content_category' to be a str")
        pulumi.set(__self__, "content_category", content_category)
        if custom_type and not isinstance(custom_type, int):
            raise TypeError("Expected argument 'custom_type' to be a int")
        pulumi.set(__self__, "custom_type", custom_type)
        if enable_details and not isinstance(enable_details, bool):
            raise TypeError("Expected argument 'enable_details' to be a bool")
        pulumi.set(__self__, "enable_details", enable_details)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if ids and not isinstance(ids, list):
            raise TypeError("Expected argument 'ids' to be a list")
        pulumi.set(__self__, "ids", ids)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if name_regex and not isinstance(name_regex, str):
            raise TypeError("Expected argument 'name_regex' to be a str")
        pulumi.set(__self__, "name_regex", name_regex)
        if names and not isinstance(names, list):
            raise TypeError("Expected argument 'names' to be a list")
        pulumi.set(__self__, "names", names)
        if output_file and not isinstance(output_file, str):
            raise TypeError("Expected argument 'output_file' to be a str")
        pulumi.set(__self__, "output_file", output_file)
        if product_id and not isinstance(product_id, str):
            raise TypeError("Expected argument 'product_id' to be a str")
        pulumi.set(__self__, "product_id", product_id)
        if risk_level_id and not isinstance(risk_level_id, str):
            raise TypeError("Expected argument 'risk_level_id' to be a str")
        pulumi.set(__self__, "risk_level_id", risk_level_id)
        if rule_type and not isinstance(rule_type, int):
            raise TypeError("Expected argument 'rule_type' to be a int")
        pulumi.set(__self__, "rule_type", rule_type)
        if rules and not isinstance(rules, list):
            raise TypeError("Expected argument 'rules' to be a list")
        pulumi.set(__self__, "rules", rules)
        if status and not isinstance(status, str):
            raise TypeError("Expected argument 'status' to be a str")
        pulumi.set(__self__, "status", status)
        if warn_level and not isinstance(warn_level, int):
            raise TypeError("Expected argument 'warn_level' to be a int")
        pulumi.set(__self__, "warn_level", warn_level)

    @property
    @pulumi.getter
    def category(self) -> Optional[int]:
        return pulumi.get(self, "category")

    @property
    @pulumi.getter(name="contentCategory")
    def content_category(self) -> Optional[str]:
        return pulumi.get(self, "content_category")

    @property
    @pulumi.getter(name="customType")
    def custom_type(self) -> Optional[int]:
        return pulumi.get(self, "custom_type")

    @property
    @pulumi.getter(name="enableDetails")
    def enable_details(self) -> Optional[bool]:
        return pulumi.get(self, "enable_details")

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
    @pulumi.getter
    def name(self) -> Optional[str]:
        return pulumi.get(self, "name")

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

    @property
    @pulumi.getter(name="productId")
    def product_id(self) -> Optional[str]:
        return pulumi.get(self, "product_id")

    @property
    @pulumi.getter(name="riskLevelId")
    def risk_level_id(self) -> Optional[str]:
        return pulumi.get(self, "risk_level_id")

    @property
    @pulumi.getter(name="ruleType")
    def rule_type(self) -> Optional[int]:
        return pulumi.get(self, "rule_type")

    @property
    @pulumi.getter
    def rules(self) -> Sequence['outputs.GetRulesRuleResult']:
        return pulumi.get(self, "rules")

    @property
    @pulumi.getter
    def status(self) -> Optional[str]:
        return pulumi.get(self, "status")

    @property
    @pulumi.getter(name="warnLevel")
    def warn_level(self) -> Optional[int]:
        return pulumi.get(self, "warn_level")


class AwaitableGetRulesResult(GetRulesResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetRulesResult(
            category=self.category,
            content_category=self.content_category,
            custom_type=self.custom_type,
            enable_details=self.enable_details,
            id=self.id,
            ids=self.ids,
            name=self.name,
            name_regex=self.name_regex,
            names=self.names,
            output_file=self.output_file,
            product_id=self.product_id,
            risk_level_id=self.risk_level_id,
            rule_type=self.rule_type,
            rules=self.rules,
            status=self.status,
            warn_level=self.warn_level)


def get_rules(category: Optional[int] = None,
              content_category: Optional[str] = None,
              custom_type: Optional[int] = None,
              enable_details: Optional[bool] = None,
              ids: Optional[Sequence[str]] = None,
              name: Optional[str] = None,
              name_regex: Optional[str] = None,
              output_file: Optional[str] = None,
              product_id: Optional[str] = None,
              risk_level_id: Optional[str] = None,
              rule_type: Optional[int] = None,
              status: Optional[str] = None,
              warn_level: Optional[int] = None,
              opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetRulesResult:
    """
    This data source provides the Sddp Rules of the current Alibaba Cloud user.

    > **NOTE:** Available in v1.132.0+.

    ## Example Usage

    Basic Usage

    ```python
    import pulumi
    import pulumi_alicloud as alicloud

    default_rule = alicloud.sddp.Rule("defaultRule",
        category=0,
        content="content",
        rule_name="rule_name",
        risk_level_id="4",
        product_code="ODPS")
    default_rules = alicloud.sddp.get_rules_output(ids=[default_rule.id])
    pulumi.export("sddpRuleId", default_rules.id)
    ```


    :param int category: Sensitive Data Identification Rules for the Type of.
    :param str content_category: The Content Classification.
    :param int custom_type: Sensitive Data Identification Rules of Type. 0: the Built-in 1: The User-Defined.
    :param Sequence[str] ids: A list of Rule IDs.
    :param str name: The name of rule.
    :param str name_regex: A regex string to filter results by Rule name.
    :param str product_id: Product ID.
    :param str risk_level_id: Sensitive Data Identification Rules of Risk Level ID. Valid values:1:S1, Weak Risk Level. 2:S2, Medium Risk Level. 3:S3 High Risk Level. 4:S4, the Highest Risk Level.
    :param int rule_type: Rule Type.
    :param str status: Sensitive Data Identification Rules Detection State of.
    :param int warn_level: The Level of Risk.
    """
    __args__ = dict()
    __args__['category'] = category
    __args__['contentCategory'] = content_category
    __args__['customType'] = custom_type
    __args__['enableDetails'] = enable_details
    __args__['ids'] = ids
    __args__['name'] = name
    __args__['nameRegex'] = name_regex
    __args__['outputFile'] = output_file
    __args__['productId'] = product_id
    __args__['riskLevelId'] = risk_level_id
    __args__['ruleType'] = rule_type
    __args__['status'] = status
    __args__['warnLevel'] = warn_level
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('alicloud:sddp/getRules:getRules', __args__, opts=opts, typ=GetRulesResult).value

    return AwaitableGetRulesResult(
        category=__ret__.category,
        content_category=__ret__.content_category,
        custom_type=__ret__.custom_type,
        enable_details=__ret__.enable_details,
        id=__ret__.id,
        ids=__ret__.ids,
        name=__ret__.name,
        name_regex=__ret__.name_regex,
        names=__ret__.names,
        output_file=__ret__.output_file,
        product_id=__ret__.product_id,
        risk_level_id=__ret__.risk_level_id,
        rule_type=__ret__.rule_type,
        rules=__ret__.rules,
        status=__ret__.status,
        warn_level=__ret__.warn_level)


@_utilities.lift_output_func(get_rules)
def get_rules_output(category: Optional[pulumi.Input[Optional[int]]] = None,
                     content_category: Optional[pulumi.Input[Optional[str]]] = None,
                     custom_type: Optional[pulumi.Input[Optional[int]]] = None,
                     enable_details: Optional[pulumi.Input[Optional[bool]]] = None,
                     ids: Optional[pulumi.Input[Optional[Sequence[str]]]] = None,
                     name: Optional[pulumi.Input[Optional[str]]] = None,
                     name_regex: Optional[pulumi.Input[Optional[str]]] = None,
                     output_file: Optional[pulumi.Input[Optional[str]]] = None,
                     product_id: Optional[pulumi.Input[Optional[str]]] = None,
                     risk_level_id: Optional[pulumi.Input[Optional[str]]] = None,
                     rule_type: Optional[pulumi.Input[Optional[int]]] = None,
                     status: Optional[pulumi.Input[Optional[str]]] = None,
                     warn_level: Optional[pulumi.Input[Optional[int]]] = None,
                     opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetRulesResult]:
    """
    This data source provides the Sddp Rules of the current Alibaba Cloud user.

    > **NOTE:** Available in v1.132.0+.

    ## Example Usage

    Basic Usage

    ```python
    import pulumi
    import pulumi_alicloud as alicloud

    default_rule = alicloud.sddp.Rule("defaultRule",
        category=0,
        content="content",
        rule_name="rule_name",
        risk_level_id="4",
        product_code="ODPS")
    default_rules = alicloud.sddp.get_rules_output(ids=[default_rule.id])
    pulumi.export("sddpRuleId", default_rules.id)
    ```


    :param int category: Sensitive Data Identification Rules for the Type of.
    :param str content_category: The Content Classification.
    :param int custom_type: Sensitive Data Identification Rules of Type. 0: the Built-in 1: The User-Defined.
    :param Sequence[str] ids: A list of Rule IDs.
    :param str name: The name of rule.
    :param str name_regex: A regex string to filter results by Rule name.
    :param str product_id: Product ID.
    :param str risk_level_id: Sensitive Data Identification Rules of Risk Level ID. Valid values:1:S1, Weak Risk Level. 2:S2, Medium Risk Level. 3:S3 High Risk Level. 4:S4, the Highest Risk Level.
    :param int rule_type: Rule Type.
    :param str status: Sensitive Data Identification Rules Detection State of.
    :param int warn_level: The Level of Risk.
    """
    ...
