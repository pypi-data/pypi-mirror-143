# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['DomainIdentityVerificationArgs', 'DomainIdentityVerification']

@pulumi.input_type
class DomainIdentityVerificationArgs:
    def __init__(__self__, *,
                 domain: pulumi.Input[str]):
        """
        The set of arguments for constructing a DomainIdentityVerification resource.
        :param pulumi.Input[str] domain: The domain name of the SES domain identity to verify.
        """
        pulumi.set(__self__, "domain", domain)

    @property
    @pulumi.getter
    def domain(self) -> pulumi.Input[str]:
        """
        The domain name of the SES domain identity to verify.
        """
        return pulumi.get(self, "domain")

    @domain.setter
    def domain(self, value: pulumi.Input[str]):
        pulumi.set(self, "domain", value)


@pulumi.input_type
class _DomainIdentityVerificationState:
    def __init__(__self__, *,
                 arn: Optional[pulumi.Input[str]] = None,
                 domain: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering DomainIdentityVerification resources.
        :param pulumi.Input[str] arn: The ARN of the domain identity.
        :param pulumi.Input[str] domain: The domain name of the SES domain identity to verify.
        """
        if arn is not None:
            pulumi.set(__self__, "arn", arn)
        if domain is not None:
            pulumi.set(__self__, "domain", domain)

    @property
    @pulumi.getter
    def arn(self) -> Optional[pulumi.Input[str]]:
        """
        The ARN of the domain identity.
        """
        return pulumi.get(self, "arn")

    @arn.setter
    def arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "arn", value)

    @property
    @pulumi.getter
    def domain(self) -> Optional[pulumi.Input[str]]:
        """
        The domain name of the SES domain identity to verify.
        """
        return pulumi.get(self, "domain")

    @domain.setter
    def domain(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "domain", value)


class DomainIdentityVerification(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 domain: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Represents a successful verification of an SES domain identity.

        Most commonly, this resource is used together with `route53.Record` and
        `ses.DomainIdentity` to request an SES domain identity,
        deploy the required DNS verification records, and wait for verification to complete.

        > **WARNING:** This resource implements a part of the verification workflow. It does not represent a real-world entity in AWS, therefore changing or deleting this resource on its own has no immediate effect.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.ses.DomainIdentity("example", domain="example.com")
        example_amazonses_verification_record = aws.route53.Record("exampleAmazonsesVerificationRecord",
            zone_id=aws_route53_zone["example"]["zone_id"],
            name=example.id.apply(lambda id: f"_amazonses.{id}"),
            type="TXT",
            ttl=600,
            records=[example.verification_token])
        example_verification = aws.ses.DomainIdentityVerification("exampleVerification", domain=example.id,
        opts=pulumi.ResourceOptions(depends_on=[example_amazonses_verification_record]))
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] domain: The domain name of the SES domain identity to verify.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: DomainIdentityVerificationArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Represents a successful verification of an SES domain identity.

        Most commonly, this resource is used together with `route53.Record` and
        `ses.DomainIdentity` to request an SES domain identity,
        deploy the required DNS verification records, and wait for verification to complete.

        > **WARNING:** This resource implements a part of the verification workflow. It does not represent a real-world entity in AWS, therefore changing or deleting this resource on its own has no immediate effect.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.ses.DomainIdentity("example", domain="example.com")
        example_amazonses_verification_record = aws.route53.Record("exampleAmazonsesVerificationRecord",
            zone_id=aws_route53_zone["example"]["zone_id"],
            name=example.id.apply(lambda id: f"_amazonses.{id}"),
            type="TXT",
            ttl=600,
            records=[example.verification_token])
        example_verification = aws.ses.DomainIdentityVerification("exampleVerification", domain=example.id,
        opts=pulumi.ResourceOptions(depends_on=[example_amazonses_verification_record]))
        ```

        :param str resource_name: The name of the resource.
        :param DomainIdentityVerificationArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(DomainIdentityVerificationArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 domain: Optional[pulumi.Input[str]] = None,
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
            __props__ = DomainIdentityVerificationArgs.__new__(DomainIdentityVerificationArgs)

            if domain is None and not opts.urn:
                raise TypeError("Missing required property 'domain'")
            __props__.__dict__["domain"] = domain
            __props__.__dict__["arn"] = None
        super(DomainIdentityVerification, __self__).__init__(
            'aws:ses/domainIdentityVerification:DomainIdentityVerification',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            arn: Optional[pulumi.Input[str]] = None,
            domain: Optional[pulumi.Input[str]] = None) -> 'DomainIdentityVerification':
        """
        Get an existing DomainIdentityVerification resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] arn: The ARN of the domain identity.
        :param pulumi.Input[str] domain: The domain name of the SES domain identity to verify.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _DomainIdentityVerificationState.__new__(_DomainIdentityVerificationState)

        __props__.__dict__["arn"] = arn
        __props__.__dict__["domain"] = domain
        return DomainIdentityVerification(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        """
        The ARN of the domain identity.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter
    def domain(self) -> pulumi.Output[str]:
        """
        The domain name of the SES domain identity to verify.
        """
        return pulumi.get(self, "domain")

