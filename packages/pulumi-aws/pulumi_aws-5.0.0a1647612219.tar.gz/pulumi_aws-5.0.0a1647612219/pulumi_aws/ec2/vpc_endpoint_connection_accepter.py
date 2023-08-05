# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['VpcEndpointConnectionAccepterArgs', 'VpcEndpointConnectionAccepter']

@pulumi.input_type
class VpcEndpointConnectionAccepterArgs:
    def __init__(__self__, *,
                 vpc_endpoint_id: pulumi.Input[str],
                 vpc_endpoint_service_id: pulumi.Input[str]):
        """
        The set of arguments for constructing a VpcEndpointConnectionAccepter resource.
        :param pulumi.Input[str] vpc_endpoint_id: AWS VPC Endpoint ID.
        :param pulumi.Input[str] vpc_endpoint_service_id: AWS VPC Endpoint Service ID.
        """
        pulumi.set(__self__, "vpc_endpoint_id", vpc_endpoint_id)
        pulumi.set(__self__, "vpc_endpoint_service_id", vpc_endpoint_service_id)

    @property
    @pulumi.getter(name="vpcEndpointId")
    def vpc_endpoint_id(self) -> pulumi.Input[str]:
        """
        AWS VPC Endpoint ID.
        """
        return pulumi.get(self, "vpc_endpoint_id")

    @vpc_endpoint_id.setter
    def vpc_endpoint_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "vpc_endpoint_id", value)

    @property
    @pulumi.getter(name="vpcEndpointServiceId")
    def vpc_endpoint_service_id(self) -> pulumi.Input[str]:
        """
        AWS VPC Endpoint Service ID.
        """
        return pulumi.get(self, "vpc_endpoint_service_id")

    @vpc_endpoint_service_id.setter
    def vpc_endpoint_service_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "vpc_endpoint_service_id", value)


@pulumi.input_type
class _VpcEndpointConnectionAccepterState:
    def __init__(__self__, *,
                 vpc_endpoint_id: Optional[pulumi.Input[str]] = None,
                 vpc_endpoint_service_id: Optional[pulumi.Input[str]] = None,
                 vpc_endpoint_state: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering VpcEndpointConnectionAccepter resources.
        :param pulumi.Input[str] vpc_endpoint_id: AWS VPC Endpoint ID.
        :param pulumi.Input[str] vpc_endpoint_service_id: AWS VPC Endpoint Service ID.
        :param pulumi.Input[str] vpc_endpoint_state: State of the VPC Endpoint.
        """
        if vpc_endpoint_id is not None:
            pulumi.set(__self__, "vpc_endpoint_id", vpc_endpoint_id)
        if vpc_endpoint_service_id is not None:
            pulumi.set(__self__, "vpc_endpoint_service_id", vpc_endpoint_service_id)
        if vpc_endpoint_state is not None:
            pulumi.set(__self__, "vpc_endpoint_state", vpc_endpoint_state)

    @property
    @pulumi.getter(name="vpcEndpointId")
    def vpc_endpoint_id(self) -> Optional[pulumi.Input[str]]:
        """
        AWS VPC Endpoint ID.
        """
        return pulumi.get(self, "vpc_endpoint_id")

    @vpc_endpoint_id.setter
    def vpc_endpoint_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "vpc_endpoint_id", value)

    @property
    @pulumi.getter(name="vpcEndpointServiceId")
    def vpc_endpoint_service_id(self) -> Optional[pulumi.Input[str]]:
        """
        AWS VPC Endpoint Service ID.
        """
        return pulumi.get(self, "vpc_endpoint_service_id")

    @vpc_endpoint_service_id.setter
    def vpc_endpoint_service_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "vpc_endpoint_service_id", value)

    @property
    @pulumi.getter(name="vpcEndpointState")
    def vpc_endpoint_state(self) -> Optional[pulumi.Input[str]]:
        """
        State of the VPC Endpoint.
        """
        return pulumi.get(self, "vpc_endpoint_state")

    @vpc_endpoint_state.setter
    def vpc_endpoint_state(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "vpc_endpoint_state", value)


class VpcEndpointConnectionAccepter(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 vpc_endpoint_id: Optional[pulumi.Input[str]] = None,
                 vpc_endpoint_service_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Provides a resource to accept a pending VPC Endpoint Connection accept request to VPC Endpoint Service.

        ## Example Usage
        ### Accept cross-account request

        ```python
        import pulumi
        import pulumi_aws as aws

        example_vpc_endpoint_service = aws.ec2.VpcEndpointService("exampleVpcEndpointService",
            acceptance_required=False,
            network_load_balancer_arns=[aws_lb["example"]["arn"]])
        example_vpc_endpoint = aws.ec2.VpcEndpoint("exampleVpcEndpoint",
            vpc_id=aws_vpc["test_alternate"]["id"],
            service_name=aws_vpc_endpoint_service["test"]["service_name"],
            vpc_endpoint_type="Interface",
            private_dns_enabled=False,
            security_group_ids=[aws_security_group["test"]["id"]],
            opts=pulumi.ResourceOptions(provider="aws.alternate"))
        example_vpc_endpoint_connection_accepter = aws.ec2.VpcEndpointConnectionAccepter("exampleVpcEndpointConnectionAccepter",
            vpc_endpoint_service_id=example_vpc_endpoint_service.id,
            vpc_endpoint_id=example_vpc_endpoint.id)
        ```

        ## Import

        VPC Endpoint Services can be imported using ID of the connection, which is the `VPC Endpoint Service ID` and `VPC Endpoint ID` separated by underscore (`_`). e.g.

        ```sh
         $ pulumi import aws:ec2/vpcEndpointConnectionAccepter:VpcEndpointConnectionAccepter foo vpce-svc-0f97a19d3fa8220bc_vpce-010601a6db371e263
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] vpc_endpoint_id: AWS VPC Endpoint ID.
        :param pulumi.Input[str] vpc_endpoint_service_id: AWS VPC Endpoint Service ID.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: VpcEndpointConnectionAccepterArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a resource to accept a pending VPC Endpoint Connection accept request to VPC Endpoint Service.

        ## Example Usage
        ### Accept cross-account request

        ```python
        import pulumi
        import pulumi_aws as aws

        example_vpc_endpoint_service = aws.ec2.VpcEndpointService("exampleVpcEndpointService",
            acceptance_required=False,
            network_load_balancer_arns=[aws_lb["example"]["arn"]])
        example_vpc_endpoint = aws.ec2.VpcEndpoint("exampleVpcEndpoint",
            vpc_id=aws_vpc["test_alternate"]["id"],
            service_name=aws_vpc_endpoint_service["test"]["service_name"],
            vpc_endpoint_type="Interface",
            private_dns_enabled=False,
            security_group_ids=[aws_security_group["test"]["id"]],
            opts=pulumi.ResourceOptions(provider="aws.alternate"))
        example_vpc_endpoint_connection_accepter = aws.ec2.VpcEndpointConnectionAccepter("exampleVpcEndpointConnectionAccepter",
            vpc_endpoint_service_id=example_vpc_endpoint_service.id,
            vpc_endpoint_id=example_vpc_endpoint.id)
        ```

        ## Import

        VPC Endpoint Services can be imported using ID of the connection, which is the `VPC Endpoint Service ID` and `VPC Endpoint ID` separated by underscore (`_`). e.g.

        ```sh
         $ pulumi import aws:ec2/vpcEndpointConnectionAccepter:VpcEndpointConnectionAccepter foo vpce-svc-0f97a19d3fa8220bc_vpce-010601a6db371e263
        ```

        :param str resource_name: The name of the resource.
        :param VpcEndpointConnectionAccepterArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(VpcEndpointConnectionAccepterArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 vpc_endpoint_id: Optional[pulumi.Input[str]] = None,
                 vpc_endpoint_service_id: Optional[pulumi.Input[str]] = None,
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
            __props__ = VpcEndpointConnectionAccepterArgs.__new__(VpcEndpointConnectionAccepterArgs)

            if vpc_endpoint_id is None and not opts.urn:
                raise TypeError("Missing required property 'vpc_endpoint_id'")
            __props__.__dict__["vpc_endpoint_id"] = vpc_endpoint_id
            if vpc_endpoint_service_id is None and not opts.urn:
                raise TypeError("Missing required property 'vpc_endpoint_service_id'")
            __props__.__dict__["vpc_endpoint_service_id"] = vpc_endpoint_service_id
            __props__.__dict__["vpc_endpoint_state"] = None
        super(VpcEndpointConnectionAccepter, __self__).__init__(
            'aws:ec2/vpcEndpointConnectionAccepter:VpcEndpointConnectionAccepter',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            vpc_endpoint_id: Optional[pulumi.Input[str]] = None,
            vpc_endpoint_service_id: Optional[pulumi.Input[str]] = None,
            vpc_endpoint_state: Optional[pulumi.Input[str]] = None) -> 'VpcEndpointConnectionAccepter':
        """
        Get an existing VpcEndpointConnectionAccepter resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] vpc_endpoint_id: AWS VPC Endpoint ID.
        :param pulumi.Input[str] vpc_endpoint_service_id: AWS VPC Endpoint Service ID.
        :param pulumi.Input[str] vpc_endpoint_state: State of the VPC Endpoint.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _VpcEndpointConnectionAccepterState.__new__(_VpcEndpointConnectionAccepterState)

        __props__.__dict__["vpc_endpoint_id"] = vpc_endpoint_id
        __props__.__dict__["vpc_endpoint_service_id"] = vpc_endpoint_service_id
        __props__.__dict__["vpc_endpoint_state"] = vpc_endpoint_state
        return VpcEndpointConnectionAccepter(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="vpcEndpointId")
    def vpc_endpoint_id(self) -> pulumi.Output[str]:
        """
        AWS VPC Endpoint ID.
        """
        return pulumi.get(self, "vpc_endpoint_id")

    @property
    @pulumi.getter(name="vpcEndpointServiceId")
    def vpc_endpoint_service_id(self) -> pulumi.Output[str]:
        """
        AWS VPC Endpoint Service ID.
        """
        return pulumi.get(self, "vpc_endpoint_service_id")

    @property
    @pulumi.getter(name="vpcEndpointState")
    def vpc_endpoint_state(self) -> pulumi.Output[str]:
        """
        State of the VPC Endpoint.
        """
        return pulumi.get(self, "vpc_endpoint_state")

