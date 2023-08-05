# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['SimpleOfficeSiteArgs', 'SimpleOfficeSite']

@pulumi.input_type
class SimpleOfficeSiteArgs:
    def __init__(__self__, *,
                 cidr_block: pulumi.Input[str],
                 bandwidth: Optional[pulumi.Input[int]] = None,
                 cen_id: Optional[pulumi.Input[str]] = None,
                 cen_owner_id: Optional[pulumi.Input[str]] = None,
                 desktop_access_type: Optional[pulumi.Input[str]] = None,
                 enable_admin_access: Optional[pulumi.Input[bool]] = None,
                 enable_cross_desktop_access: Optional[pulumi.Input[bool]] = None,
                 enable_internet_access: Optional[pulumi.Input[bool]] = None,
                 mfa_enabled: Optional[pulumi.Input[bool]] = None,
                 office_site_name: Optional[pulumi.Input[str]] = None,
                 sso_enabled: Optional[pulumi.Input[bool]] = None):
        """
        The set of arguments for constructing a SimpleOfficeSite resource.
        :param pulumi.Input[str] cidr_block: Workspace Corresponds to the Security Office Network of IPv4 Segment.
        :param pulumi.Input[int] bandwidth: The Internet Bandwidth Peak. It has been deprecated from version 1.142.0 and can be found in the new resource alicloud_ecd_network_package.
        :param pulumi.Input[str] cen_id: Cloud Enterprise Network Instance ID.
        :param pulumi.Input[str] cen_owner_id: The cen owner id.
        :param pulumi.Input[str] desktop_access_type: Connect to the Cloud Desktop Allows the Use of the Access Mode of. Valid values: `Any`, `Internet`, `VPC`.
        :param pulumi.Input[bool] enable_admin_access: Whether to Use Cloud Desktop User Empowerment of Local Administrator Permissions.
        :param pulumi.Input[bool] enable_cross_desktop_access: Enable Cross-Desktop Access.
        :param pulumi.Input[bool] enable_internet_access: Whether the Open Internet Access Function.
        :param pulumi.Input[bool] mfa_enabled: Whether to Enable Multi-Factor Authentication MFA.
        :param pulumi.Input[str] office_site_name: The office site name.
        :param pulumi.Input[bool] sso_enabled: Whether to Enable Single Sign-on (SSO) for User-Based SSO.
        """
        pulumi.set(__self__, "cidr_block", cidr_block)
        if bandwidth is not None:
            warnings.warn("""Field 'bandwidth' has been deprecated from provider version 1.142.0.""", DeprecationWarning)
            pulumi.log.warn("""bandwidth is deprecated: Field 'bandwidth' has been deprecated from provider version 1.142.0.""")
        if bandwidth is not None:
            pulumi.set(__self__, "bandwidth", bandwidth)
        if cen_id is not None:
            pulumi.set(__self__, "cen_id", cen_id)
        if cen_owner_id is not None:
            pulumi.set(__self__, "cen_owner_id", cen_owner_id)
        if desktop_access_type is not None:
            pulumi.set(__self__, "desktop_access_type", desktop_access_type)
        if enable_admin_access is not None:
            pulumi.set(__self__, "enable_admin_access", enable_admin_access)
        if enable_cross_desktop_access is not None:
            pulumi.set(__self__, "enable_cross_desktop_access", enable_cross_desktop_access)
        if enable_internet_access is not None:
            warnings.warn("""Field 'enable_internet_access' has been deprecated from provider version 1.142.0.""", DeprecationWarning)
            pulumi.log.warn("""enable_internet_access is deprecated: Field 'enable_internet_access' has been deprecated from provider version 1.142.0.""")
        if enable_internet_access is not None:
            pulumi.set(__self__, "enable_internet_access", enable_internet_access)
        if mfa_enabled is not None:
            pulumi.set(__self__, "mfa_enabled", mfa_enabled)
        if office_site_name is not None:
            pulumi.set(__self__, "office_site_name", office_site_name)
        if sso_enabled is not None:
            pulumi.set(__self__, "sso_enabled", sso_enabled)

    @property
    @pulumi.getter(name="cidrBlock")
    def cidr_block(self) -> pulumi.Input[str]:
        """
        Workspace Corresponds to the Security Office Network of IPv4 Segment.
        """
        return pulumi.get(self, "cidr_block")

    @cidr_block.setter
    def cidr_block(self, value: pulumi.Input[str]):
        pulumi.set(self, "cidr_block", value)

    @property
    @pulumi.getter
    def bandwidth(self) -> Optional[pulumi.Input[int]]:
        """
        The Internet Bandwidth Peak. It has been deprecated from version 1.142.0 and can be found in the new resource alicloud_ecd_network_package.
        """
        return pulumi.get(self, "bandwidth")

    @bandwidth.setter
    def bandwidth(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "bandwidth", value)

    @property
    @pulumi.getter(name="cenId")
    def cen_id(self) -> Optional[pulumi.Input[str]]:
        """
        Cloud Enterprise Network Instance ID.
        """
        return pulumi.get(self, "cen_id")

    @cen_id.setter
    def cen_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "cen_id", value)

    @property
    @pulumi.getter(name="cenOwnerId")
    def cen_owner_id(self) -> Optional[pulumi.Input[str]]:
        """
        The cen owner id.
        """
        return pulumi.get(self, "cen_owner_id")

    @cen_owner_id.setter
    def cen_owner_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "cen_owner_id", value)

    @property
    @pulumi.getter(name="desktopAccessType")
    def desktop_access_type(self) -> Optional[pulumi.Input[str]]:
        """
        Connect to the Cloud Desktop Allows the Use of the Access Mode of. Valid values: `Any`, `Internet`, `VPC`.
        """
        return pulumi.get(self, "desktop_access_type")

    @desktop_access_type.setter
    def desktop_access_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "desktop_access_type", value)

    @property
    @pulumi.getter(name="enableAdminAccess")
    def enable_admin_access(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether to Use Cloud Desktop User Empowerment of Local Administrator Permissions.
        """
        return pulumi.get(self, "enable_admin_access")

    @enable_admin_access.setter
    def enable_admin_access(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "enable_admin_access", value)

    @property
    @pulumi.getter(name="enableCrossDesktopAccess")
    def enable_cross_desktop_access(self) -> Optional[pulumi.Input[bool]]:
        """
        Enable Cross-Desktop Access.
        """
        return pulumi.get(self, "enable_cross_desktop_access")

    @enable_cross_desktop_access.setter
    def enable_cross_desktop_access(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "enable_cross_desktop_access", value)

    @property
    @pulumi.getter(name="enableInternetAccess")
    def enable_internet_access(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether the Open Internet Access Function.
        """
        return pulumi.get(self, "enable_internet_access")

    @enable_internet_access.setter
    def enable_internet_access(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "enable_internet_access", value)

    @property
    @pulumi.getter(name="mfaEnabled")
    def mfa_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether to Enable Multi-Factor Authentication MFA.
        """
        return pulumi.get(self, "mfa_enabled")

    @mfa_enabled.setter
    def mfa_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "mfa_enabled", value)

    @property
    @pulumi.getter(name="officeSiteName")
    def office_site_name(self) -> Optional[pulumi.Input[str]]:
        """
        The office site name.
        """
        return pulumi.get(self, "office_site_name")

    @office_site_name.setter
    def office_site_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "office_site_name", value)

    @property
    @pulumi.getter(name="ssoEnabled")
    def sso_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether to Enable Single Sign-on (SSO) for User-Based SSO.
        """
        return pulumi.get(self, "sso_enabled")

    @sso_enabled.setter
    def sso_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "sso_enabled", value)


@pulumi.input_type
class _SimpleOfficeSiteState:
    def __init__(__self__, *,
                 bandwidth: Optional[pulumi.Input[int]] = None,
                 cen_id: Optional[pulumi.Input[str]] = None,
                 cen_owner_id: Optional[pulumi.Input[str]] = None,
                 cidr_block: Optional[pulumi.Input[str]] = None,
                 desktop_access_type: Optional[pulumi.Input[str]] = None,
                 enable_admin_access: Optional[pulumi.Input[bool]] = None,
                 enable_cross_desktop_access: Optional[pulumi.Input[bool]] = None,
                 enable_internet_access: Optional[pulumi.Input[bool]] = None,
                 mfa_enabled: Optional[pulumi.Input[bool]] = None,
                 office_site_name: Optional[pulumi.Input[str]] = None,
                 sso_enabled: Optional[pulumi.Input[bool]] = None,
                 status: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering SimpleOfficeSite resources.
        :param pulumi.Input[int] bandwidth: The Internet Bandwidth Peak. It has been deprecated from version 1.142.0 and can be found in the new resource alicloud_ecd_network_package.
        :param pulumi.Input[str] cen_id: Cloud Enterprise Network Instance ID.
        :param pulumi.Input[str] cen_owner_id: The cen owner id.
        :param pulumi.Input[str] cidr_block: Workspace Corresponds to the Security Office Network of IPv4 Segment.
        :param pulumi.Input[str] desktop_access_type: Connect to the Cloud Desktop Allows the Use of the Access Mode of. Valid values: `Any`, `Internet`, `VPC`.
        :param pulumi.Input[bool] enable_admin_access: Whether to Use Cloud Desktop User Empowerment of Local Administrator Permissions.
        :param pulumi.Input[bool] enable_cross_desktop_access: Enable Cross-Desktop Access.
        :param pulumi.Input[bool] enable_internet_access: Whether the Open Internet Access Function.
        :param pulumi.Input[bool] mfa_enabled: Whether to Enable Multi-Factor Authentication MFA.
        :param pulumi.Input[str] office_site_name: The office site name.
        :param pulumi.Input[bool] sso_enabled: Whether to Enable Single Sign-on (SSO) for User-Based SSO.
        :param pulumi.Input[str] status: Workspace State. Valid Values: `REGISTERED`,`REGISTERING`.
        """
        if bandwidth is not None:
            warnings.warn("""Field 'bandwidth' has been deprecated from provider version 1.142.0.""", DeprecationWarning)
            pulumi.log.warn("""bandwidth is deprecated: Field 'bandwidth' has been deprecated from provider version 1.142.0.""")
        if bandwidth is not None:
            pulumi.set(__self__, "bandwidth", bandwidth)
        if cen_id is not None:
            pulumi.set(__self__, "cen_id", cen_id)
        if cen_owner_id is not None:
            pulumi.set(__self__, "cen_owner_id", cen_owner_id)
        if cidr_block is not None:
            pulumi.set(__self__, "cidr_block", cidr_block)
        if desktop_access_type is not None:
            pulumi.set(__self__, "desktop_access_type", desktop_access_type)
        if enable_admin_access is not None:
            pulumi.set(__self__, "enable_admin_access", enable_admin_access)
        if enable_cross_desktop_access is not None:
            pulumi.set(__self__, "enable_cross_desktop_access", enable_cross_desktop_access)
        if enable_internet_access is not None:
            warnings.warn("""Field 'enable_internet_access' has been deprecated from provider version 1.142.0.""", DeprecationWarning)
            pulumi.log.warn("""enable_internet_access is deprecated: Field 'enable_internet_access' has been deprecated from provider version 1.142.0.""")
        if enable_internet_access is not None:
            pulumi.set(__self__, "enable_internet_access", enable_internet_access)
        if mfa_enabled is not None:
            pulumi.set(__self__, "mfa_enabled", mfa_enabled)
        if office_site_name is not None:
            pulumi.set(__self__, "office_site_name", office_site_name)
        if sso_enabled is not None:
            pulumi.set(__self__, "sso_enabled", sso_enabled)
        if status is not None:
            pulumi.set(__self__, "status", status)

    @property
    @pulumi.getter
    def bandwidth(self) -> Optional[pulumi.Input[int]]:
        """
        The Internet Bandwidth Peak. It has been deprecated from version 1.142.0 and can be found in the new resource alicloud_ecd_network_package.
        """
        return pulumi.get(self, "bandwidth")

    @bandwidth.setter
    def bandwidth(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "bandwidth", value)

    @property
    @pulumi.getter(name="cenId")
    def cen_id(self) -> Optional[pulumi.Input[str]]:
        """
        Cloud Enterprise Network Instance ID.
        """
        return pulumi.get(self, "cen_id")

    @cen_id.setter
    def cen_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "cen_id", value)

    @property
    @pulumi.getter(name="cenOwnerId")
    def cen_owner_id(self) -> Optional[pulumi.Input[str]]:
        """
        The cen owner id.
        """
        return pulumi.get(self, "cen_owner_id")

    @cen_owner_id.setter
    def cen_owner_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "cen_owner_id", value)

    @property
    @pulumi.getter(name="cidrBlock")
    def cidr_block(self) -> Optional[pulumi.Input[str]]:
        """
        Workspace Corresponds to the Security Office Network of IPv4 Segment.
        """
        return pulumi.get(self, "cidr_block")

    @cidr_block.setter
    def cidr_block(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "cidr_block", value)

    @property
    @pulumi.getter(name="desktopAccessType")
    def desktop_access_type(self) -> Optional[pulumi.Input[str]]:
        """
        Connect to the Cloud Desktop Allows the Use of the Access Mode of. Valid values: `Any`, `Internet`, `VPC`.
        """
        return pulumi.get(self, "desktop_access_type")

    @desktop_access_type.setter
    def desktop_access_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "desktop_access_type", value)

    @property
    @pulumi.getter(name="enableAdminAccess")
    def enable_admin_access(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether to Use Cloud Desktop User Empowerment of Local Administrator Permissions.
        """
        return pulumi.get(self, "enable_admin_access")

    @enable_admin_access.setter
    def enable_admin_access(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "enable_admin_access", value)

    @property
    @pulumi.getter(name="enableCrossDesktopAccess")
    def enable_cross_desktop_access(self) -> Optional[pulumi.Input[bool]]:
        """
        Enable Cross-Desktop Access.
        """
        return pulumi.get(self, "enable_cross_desktop_access")

    @enable_cross_desktop_access.setter
    def enable_cross_desktop_access(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "enable_cross_desktop_access", value)

    @property
    @pulumi.getter(name="enableInternetAccess")
    def enable_internet_access(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether the Open Internet Access Function.
        """
        return pulumi.get(self, "enable_internet_access")

    @enable_internet_access.setter
    def enable_internet_access(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "enable_internet_access", value)

    @property
    @pulumi.getter(name="mfaEnabled")
    def mfa_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether to Enable Multi-Factor Authentication MFA.
        """
        return pulumi.get(self, "mfa_enabled")

    @mfa_enabled.setter
    def mfa_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "mfa_enabled", value)

    @property
    @pulumi.getter(name="officeSiteName")
    def office_site_name(self) -> Optional[pulumi.Input[str]]:
        """
        The office site name.
        """
        return pulumi.get(self, "office_site_name")

    @office_site_name.setter
    def office_site_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "office_site_name", value)

    @property
    @pulumi.getter(name="ssoEnabled")
    def sso_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether to Enable Single Sign-on (SSO) for User-Based SSO.
        """
        return pulumi.get(self, "sso_enabled")

    @sso_enabled.setter
    def sso_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "sso_enabled", value)

    @property
    @pulumi.getter
    def status(self) -> Optional[pulumi.Input[str]]:
        """
        Workspace State. Valid Values: `REGISTERED`,`REGISTERING`.
        """
        return pulumi.get(self, "status")

    @status.setter
    def status(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "status", value)


class SimpleOfficeSite(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 bandwidth: Optional[pulumi.Input[int]] = None,
                 cen_id: Optional[pulumi.Input[str]] = None,
                 cen_owner_id: Optional[pulumi.Input[str]] = None,
                 cidr_block: Optional[pulumi.Input[str]] = None,
                 desktop_access_type: Optional[pulumi.Input[str]] = None,
                 enable_admin_access: Optional[pulumi.Input[bool]] = None,
                 enable_cross_desktop_access: Optional[pulumi.Input[bool]] = None,
                 enable_internet_access: Optional[pulumi.Input[bool]] = None,
                 mfa_enabled: Optional[pulumi.Input[bool]] = None,
                 office_site_name: Optional[pulumi.Input[str]] = None,
                 sso_enabled: Optional[pulumi.Input[bool]] = None,
                 __props__=None):
        """
        Provides a ECD Simple Office Site resource.

        For information about ECD Simple Office Site and how to use it, see [What is Simple Office Site](https://help.aliyun.com/document_detail/188382.html).

        > **NOTE:** Available in v1.140.0+.

        ## Example Usage

        Basic Usage

        ```python
        import pulumi
        import pulumi_alicloud as alicloud

        default = alicloud.eds.SimpleOfficeSite("default",
            bandwidth=5,
            cidr_block="172.16.0.0/12",
            desktop_access_type="Internet",
            office_site_name="site_name")
        ```

        ## Import

        ECD Simple Office Site can be imported using the id, e.g.

        ```sh
         $ pulumi import alicloud:eds/simpleOfficeSite:SimpleOfficeSite example <id>
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[int] bandwidth: The Internet Bandwidth Peak. It has been deprecated from version 1.142.0 and can be found in the new resource alicloud_ecd_network_package.
        :param pulumi.Input[str] cen_id: Cloud Enterprise Network Instance ID.
        :param pulumi.Input[str] cen_owner_id: The cen owner id.
        :param pulumi.Input[str] cidr_block: Workspace Corresponds to the Security Office Network of IPv4 Segment.
        :param pulumi.Input[str] desktop_access_type: Connect to the Cloud Desktop Allows the Use of the Access Mode of. Valid values: `Any`, `Internet`, `VPC`.
        :param pulumi.Input[bool] enable_admin_access: Whether to Use Cloud Desktop User Empowerment of Local Administrator Permissions.
        :param pulumi.Input[bool] enable_cross_desktop_access: Enable Cross-Desktop Access.
        :param pulumi.Input[bool] enable_internet_access: Whether the Open Internet Access Function.
        :param pulumi.Input[bool] mfa_enabled: Whether to Enable Multi-Factor Authentication MFA.
        :param pulumi.Input[str] office_site_name: The office site name.
        :param pulumi.Input[bool] sso_enabled: Whether to Enable Single Sign-on (SSO) for User-Based SSO.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: SimpleOfficeSiteArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a ECD Simple Office Site resource.

        For information about ECD Simple Office Site and how to use it, see [What is Simple Office Site](https://help.aliyun.com/document_detail/188382.html).

        > **NOTE:** Available in v1.140.0+.

        ## Example Usage

        Basic Usage

        ```python
        import pulumi
        import pulumi_alicloud as alicloud

        default = alicloud.eds.SimpleOfficeSite("default",
            bandwidth=5,
            cidr_block="172.16.0.0/12",
            desktop_access_type="Internet",
            office_site_name="site_name")
        ```

        ## Import

        ECD Simple Office Site can be imported using the id, e.g.

        ```sh
         $ pulumi import alicloud:eds/simpleOfficeSite:SimpleOfficeSite example <id>
        ```

        :param str resource_name: The name of the resource.
        :param SimpleOfficeSiteArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(SimpleOfficeSiteArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 bandwidth: Optional[pulumi.Input[int]] = None,
                 cen_id: Optional[pulumi.Input[str]] = None,
                 cen_owner_id: Optional[pulumi.Input[str]] = None,
                 cidr_block: Optional[pulumi.Input[str]] = None,
                 desktop_access_type: Optional[pulumi.Input[str]] = None,
                 enable_admin_access: Optional[pulumi.Input[bool]] = None,
                 enable_cross_desktop_access: Optional[pulumi.Input[bool]] = None,
                 enable_internet_access: Optional[pulumi.Input[bool]] = None,
                 mfa_enabled: Optional[pulumi.Input[bool]] = None,
                 office_site_name: Optional[pulumi.Input[str]] = None,
                 sso_enabled: Optional[pulumi.Input[bool]] = None,
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
            __props__ = SimpleOfficeSiteArgs.__new__(SimpleOfficeSiteArgs)

            if bandwidth is not None and not opts.urn:
                warnings.warn("""Field 'bandwidth' has been deprecated from provider version 1.142.0.""", DeprecationWarning)
                pulumi.log.warn("""bandwidth is deprecated: Field 'bandwidth' has been deprecated from provider version 1.142.0.""")
            __props__.__dict__["bandwidth"] = bandwidth
            __props__.__dict__["cen_id"] = cen_id
            __props__.__dict__["cen_owner_id"] = cen_owner_id
            if cidr_block is None and not opts.urn:
                raise TypeError("Missing required property 'cidr_block'")
            __props__.__dict__["cidr_block"] = cidr_block
            __props__.__dict__["desktop_access_type"] = desktop_access_type
            __props__.__dict__["enable_admin_access"] = enable_admin_access
            __props__.__dict__["enable_cross_desktop_access"] = enable_cross_desktop_access
            if enable_internet_access is not None and not opts.urn:
                warnings.warn("""Field 'enable_internet_access' has been deprecated from provider version 1.142.0.""", DeprecationWarning)
                pulumi.log.warn("""enable_internet_access is deprecated: Field 'enable_internet_access' has been deprecated from provider version 1.142.0.""")
            __props__.__dict__["enable_internet_access"] = enable_internet_access
            __props__.__dict__["mfa_enabled"] = mfa_enabled
            __props__.__dict__["office_site_name"] = office_site_name
            __props__.__dict__["sso_enabled"] = sso_enabled
            __props__.__dict__["status"] = None
        super(SimpleOfficeSite, __self__).__init__(
            'alicloud:eds/simpleOfficeSite:SimpleOfficeSite',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            bandwidth: Optional[pulumi.Input[int]] = None,
            cen_id: Optional[pulumi.Input[str]] = None,
            cen_owner_id: Optional[pulumi.Input[str]] = None,
            cidr_block: Optional[pulumi.Input[str]] = None,
            desktop_access_type: Optional[pulumi.Input[str]] = None,
            enable_admin_access: Optional[pulumi.Input[bool]] = None,
            enable_cross_desktop_access: Optional[pulumi.Input[bool]] = None,
            enable_internet_access: Optional[pulumi.Input[bool]] = None,
            mfa_enabled: Optional[pulumi.Input[bool]] = None,
            office_site_name: Optional[pulumi.Input[str]] = None,
            sso_enabled: Optional[pulumi.Input[bool]] = None,
            status: Optional[pulumi.Input[str]] = None) -> 'SimpleOfficeSite':
        """
        Get an existing SimpleOfficeSite resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[int] bandwidth: The Internet Bandwidth Peak. It has been deprecated from version 1.142.0 and can be found in the new resource alicloud_ecd_network_package.
        :param pulumi.Input[str] cen_id: Cloud Enterprise Network Instance ID.
        :param pulumi.Input[str] cen_owner_id: The cen owner id.
        :param pulumi.Input[str] cidr_block: Workspace Corresponds to the Security Office Network of IPv4 Segment.
        :param pulumi.Input[str] desktop_access_type: Connect to the Cloud Desktop Allows the Use of the Access Mode of. Valid values: `Any`, `Internet`, `VPC`.
        :param pulumi.Input[bool] enable_admin_access: Whether to Use Cloud Desktop User Empowerment of Local Administrator Permissions.
        :param pulumi.Input[bool] enable_cross_desktop_access: Enable Cross-Desktop Access.
        :param pulumi.Input[bool] enable_internet_access: Whether the Open Internet Access Function.
        :param pulumi.Input[bool] mfa_enabled: Whether to Enable Multi-Factor Authentication MFA.
        :param pulumi.Input[str] office_site_name: The office site name.
        :param pulumi.Input[bool] sso_enabled: Whether to Enable Single Sign-on (SSO) for User-Based SSO.
        :param pulumi.Input[str] status: Workspace State. Valid Values: `REGISTERED`,`REGISTERING`.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _SimpleOfficeSiteState.__new__(_SimpleOfficeSiteState)

        __props__.__dict__["bandwidth"] = bandwidth
        __props__.__dict__["cen_id"] = cen_id
        __props__.__dict__["cen_owner_id"] = cen_owner_id
        __props__.__dict__["cidr_block"] = cidr_block
        __props__.__dict__["desktop_access_type"] = desktop_access_type
        __props__.__dict__["enable_admin_access"] = enable_admin_access
        __props__.__dict__["enable_cross_desktop_access"] = enable_cross_desktop_access
        __props__.__dict__["enable_internet_access"] = enable_internet_access
        __props__.__dict__["mfa_enabled"] = mfa_enabled
        __props__.__dict__["office_site_name"] = office_site_name
        __props__.__dict__["sso_enabled"] = sso_enabled
        __props__.__dict__["status"] = status
        return SimpleOfficeSite(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def bandwidth(self) -> pulumi.Output[int]:
        """
        The Internet Bandwidth Peak. It has been deprecated from version 1.142.0 and can be found in the new resource alicloud_ecd_network_package.
        """
        return pulumi.get(self, "bandwidth")

    @property
    @pulumi.getter(name="cenId")
    def cen_id(self) -> pulumi.Output[Optional[str]]:
        """
        Cloud Enterprise Network Instance ID.
        """
        return pulumi.get(self, "cen_id")

    @property
    @pulumi.getter(name="cenOwnerId")
    def cen_owner_id(self) -> pulumi.Output[Optional[str]]:
        """
        The cen owner id.
        """
        return pulumi.get(self, "cen_owner_id")

    @property
    @pulumi.getter(name="cidrBlock")
    def cidr_block(self) -> pulumi.Output[str]:
        """
        Workspace Corresponds to the Security Office Network of IPv4 Segment.
        """
        return pulumi.get(self, "cidr_block")

    @property
    @pulumi.getter(name="desktopAccessType")
    def desktop_access_type(self) -> pulumi.Output[str]:
        """
        Connect to the Cloud Desktop Allows the Use of the Access Mode of. Valid values: `Any`, `Internet`, `VPC`.
        """
        return pulumi.get(self, "desktop_access_type")

    @property
    @pulumi.getter(name="enableAdminAccess")
    def enable_admin_access(self) -> pulumi.Output[bool]:
        """
        Whether to Use Cloud Desktop User Empowerment of Local Administrator Permissions.
        """
        return pulumi.get(self, "enable_admin_access")

    @property
    @pulumi.getter(name="enableCrossDesktopAccess")
    def enable_cross_desktop_access(self) -> pulumi.Output[bool]:
        """
        Enable Cross-Desktop Access.
        """
        return pulumi.get(self, "enable_cross_desktop_access")

    @property
    @pulumi.getter(name="enableInternetAccess")
    def enable_internet_access(self) -> pulumi.Output[bool]:
        """
        Whether the Open Internet Access Function.
        """
        return pulumi.get(self, "enable_internet_access")

    @property
    @pulumi.getter(name="mfaEnabled")
    def mfa_enabled(self) -> pulumi.Output[bool]:
        """
        Whether to Enable Multi-Factor Authentication MFA.
        """
        return pulumi.get(self, "mfa_enabled")

    @property
    @pulumi.getter(name="officeSiteName")
    def office_site_name(self) -> pulumi.Output[Optional[str]]:
        """
        The office site name.
        """
        return pulumi.get(self, "office_site_name")

    @property
    @pulumi.getter(name="ssoEnabled")
    def sso_enabled(self) -> pulumi.Output[bool]:
        """
        Whether to Enable Single Sign-on (SSO) for User-Based SSO.
        """
        return pulumi.get(self, "sso_enabled")

    @property
    @pulumi.getter
    def status(self) -> pulumi.Output[str]:
        """
        Workspace State. Valid Values: `REGISTERED`,`REGISTERING`.
        """
        return pulumi.get(self, "status")

