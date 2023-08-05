# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['ConfigurationArgs', 'Configuration']

@pulumi.input_type
class ConfigurationArgs:
    def __init__(__self__, *,
                 server_properties: pulumi.Input[str],
                 description: Optional[pulumi.Input[str]] = None,
                 kafka_versions: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a Configuration resource.
        :param pulumi.Input[str] server_properties: Contents of the server.properties file. Supported properties are documented in the [MSK Developer Guide](https://docs.aws.amazon.com/msk/latest/developerguide/msk-configuration-properties.html).
        :param pulumi.Input[str] description: Description of the configuration.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] kafka_versions: List of Apache Kafka versions which can use this configuration.
        :param pulumi.Input[str] name: Name of the configuration.
        """
        pulumi.set(__self__, "server_properties", server_properties)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if kafka_versions is not None:
            pulumi.set(__self__, "kafka_versions", kafka_versions)
        if name is not None:
            pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter(name="serverProperties")
    def server_properties(self) -> pulumi.Input[str]:
        """
        Contents of the server.properties file. Supported properties are documented in the [MSK Developer Guide](https://docs.aws.amazon.com/msk/latest/developerguide/msk-configuration-properties.html).
        """
        return pulumi.get(self, "server_properties")

    @server_properties.setter
    def server_properties(self, value: pulumi.Input[str]):
        pulumi.set(self, "server_properties", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        Description of the configuration.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="kafkaVersions")
    def kafka_versions(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        List of Apache Kafka versions which can use this configuration.
        """
        return pulumi.get(self, "kafka_versions")

    @kafka_versions.setter
    def kafka_versions(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "kafka_versions", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the configuration.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)


@pulumi.input_type
class _ConfigurationState:
    def __init__(__self__, *,
                 arn: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 kafka_versions: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 latest_revision: Optional[pulumi.Input[int]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 server_properties: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering Configuration resources.
        :param pulumi.Input[str] arn: Amazon Resource Name (ARN) of the configuration.
        :param pulumi.Input[str] description: Description of the configuration.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] kafka_versions: List of Apache Kafka versions which can use this configuration.
        :param pulumi.Input[int] latest_revision: Latest revision of the configuration.
        :param pulumi.Input[str] name: Name of the configuration.
        :param pulumi.Input[str] server_properties: Contents of the server.properties file. Supported properties are documented in the [MSK Developer Guide](https://docs.aws.amazon.com/msk/latest/developerguide/msk-configuration-properties.html).
        """
        if arn is not None:
            pulumi.set(__self__, "arn", arn)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if kafka_versions is not None:
            pulumi.set(__self__, "kafka_versions", kafka_versions)
        if latest_revision is not None:
            pulumi.set(__self__, "latest_revision", latest_revision)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if server_properties is not None:
            pulumi.set(__self__, "server_properties", server_properties)

    @property
    @pulumi.getter
    def arn(self) -> Optional[pulumi.Input[str]]:
        """
        Amazon Resource Name (ARN) of the configuration.
        """
        return pulumi.get(self, "arn")

    @arn.setter
    def arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "arn", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        Description of the configuration.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="kafkaVersions")
    def kafka_versions(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        List of Apache Kafka versions which can use this configuration.
        """
        return pulumi.get(self, "kafka_versions")

    @kafka_versions.setter
    def kafka_versions(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "kafka_versions", value)

    @property
    @pulumi.getter(name="latestRevision")
    def latest_revision(self) -> Optional[pulumi.Input[int]]:
        """
        Latest revision of the configuration.
        """
        return pulumi.get(self, "latest_revision")

    @latest_revision.setter
    def latest_revision(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "latest_revision", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the configuration.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="serverProperties")
    def server_properties(self) -> Optional[pulumi.Input[str]]:
        """
        Contents of the server.properties file. Supported properties are documented in the [MSK Developer Guide](https://docs.aws.amazon.com/msk/latest/developerguide/msk-configuration-properties.html).
        """
        return pulumi.get(self, "server_properties")

    @server_properties.setter
    def server_properties(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "server_properties", value)


class Configuration(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 kafka_versions: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 server_properties: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Manages an Amazon Managed Streaming for Kafka configuration. More information can be found on the [MSK Developer Guide](https://docs.aws.amazon.com/msk/latest/developerguide/msk-configuration.html).

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.msk.Configuration("example",
            kafka_versions=["2.1.0"],
            server_properties=\"\"\"auto.create.topics.enable = true
        delete.topic.enable = true

        \"\"\")
        ```

        ## Import

        MSK configurations can be imported using the configuration ARN, e.g.,

        ```sh
         $ pulumi import aws:msk/configuration:Configuration example arn:aws:kafka:us-west-2:123456789012:configuration/example/279c0212-d057-4dba-9aa9-1c4e5a25bfc7-3
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: Description of the configuration.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] kafka_versions: List of Apache Kafka versions which can use this configuration.
        :param pulumi.Input[str] name: Name of the configuration.
        :param pulumi.Input[str] server_properties: Contents of the server.properties file. Supported properties are documented in the [MSK Developer Guide](https://docs.aws.amazon.com/msk/latest/developerguide/msk-configuration-properties.html).
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ConfigurationArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Manages an Amazon Managed Streaming for Kafka configuration. More information can be found on the [MSK Developer Guide](https://docs.aws.amazon.com/msk/latest/developerguide/msk-configuration.html).

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.msk.Configuration("example",
            kafka_versions=["2.1.0"],
            server_properties=\"\"\"auto.create.topics.enable = true
        delete.topic.enable = true

        \"\"\")
        ```

        ## Import

        MSK configurations can be imported using the configuration ARN, e.g.,

        ```sh
         $ pulumi import aws:msk/configuration:Configuration example arn:aws:kafka:us-west-2:123456789012:configuration/example/279c0212-d057-4dba-9aa9-1c4e5a25bfc7-3
        ```

        :param str resource_name: The name of the resource.
        :param ConfigurationArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ConfigurationArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 kafka_versions: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 server_properties: Optional[pulumi.Input[str]] = None,
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
            __props__ = ConfigurationArgs.__new__(ConfigurationArgs)

            __props__.__dict__["description"] = description
            __props__.__dict__["kafka_versions"] = kafka_versions
            __props__.__dict__["name"] = name
            if server_properties is None and not opts.urn:
                raise TypeError("Missing required property 'server_properties'")
            __props__.__dict__["server_properties"] = server_properties
            __props__.__dict__["arn"] = None
            __props__.__dict__["latest_revision"] = None
        super(Configuration, __self__).__init__(
            'aws:msk/configuration:Configuration',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            arn: Optional[pulumi.Input[str]] = None,
            description: Optional[pulumi.Input[str]] = None,
            kafka_versions: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            latest_revision: Optional[pulumi.Input[int]] = None,
            name: Optional[pulumi.Input[str]] = None,
            server_properties: Optional[pulumi.Input[str]] = None) -> 'Configuration':
        """
        Get an existing Configuration resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] arn: Amazon Resource Name (ARN) of the configuration.
        :param pulumi.Input[str] description: Description of the configuration.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] kafka_versions: List of Apache Kafka versions which can use this configuration.
        :param pulumi.Input[int] latest_revision: Latest revision of the configuration.
        :param pulumi.Input[str] name: Name of the configuration.
        :param pulumi.Input[str] server_properties: Contents of the server.properties file. Supported properties are documented in the [MSK Developer Guide](https://docs.aws.amazon.com/msk/latest/developerguide/msk-configuration-properties.html).
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _ConfigurationState.__new__(_ConfigurationState)

        __props__.__dict__["arn"] = arn
        __props__.__dict__["description"] = description
        __props__.__dict__["kafka_versions"] = kafka_versions
        __props__.__dict__["latest_revision"] = latest_revision
        __props__.__dict__["name"] = name
        __props__.__dict__["server_properties"] = server_properties
        return Configuration(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        """
        Amazon Resource Name (ARN) of the configuration.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        Description of the configuration.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="kafkaVersions")
    def kafka_versions(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        List of Apache Kafka versions which can use this configuration.
        """
        return pulumi.get(self, "kafka_versions")

    @property
    @pulumi.getter(name="latestRevision")
    def latest_revision(self) -> pulumi.Output[int]:
        """
        Latest revision of the configuration.
        """
        return pulumi.get(self, "latest_revision")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Name of the configuration.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="serverProperties")
    def server_properties(self) -> pulumi.Output[str]:
        """
        Contents of the server.properties file. Supported properties are documented in the [MSK Developer Guide](https://docs.aws.amazon.com/msk/latest/developerguide/msk-configuration-properties.html).
        """
        return pulumi.get(self, "server_properties")

