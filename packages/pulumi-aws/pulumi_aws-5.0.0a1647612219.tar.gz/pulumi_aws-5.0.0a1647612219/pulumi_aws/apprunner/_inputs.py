# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = [
    'CustomDomainAssociationCertificateValidationRecordArgs',
    'ServiceEncryptionConfigurationArgs',
    'ServiceHealthCheckConfigurationArgs',
    'ServiceInstanceConfigurationArgs',
    'ServiceSourceConfigurationArgs',
    'ServiceSourceConfigurationAuthenticationConfigurationArgs',
    'ServiceSourceConfigurationCodeRepositoryArgs',
    'ServiceSourceConfigurationCodeRepositoryCodeConfigurationArgs',
    'ServiceSourceConfigurationCodeRepositoryCodeConfigurationCodeConfigurationValuesArgs',
    'ServiceSourceConfigurationCodeRepositorySourceCodeVersionArgs',
    'ServiceSourceConfigurationImageRepositoryArgs',
    'ServiceSourceConfigurationImageRepositoryImageConfigurationArgs',
]

@pulumi.input_type
class CustomDomainAssociationCertificateValidationRecordArgs:
    def __init__(__self__, *,
                 name: Optional[pulumi.Input[str]] = None,
                 status: Optional[pulumi.Input[str]] = None,
                 type: Optional[pulumi.Input[str]] = None,
                 value: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] name: The certificate CNAME record name.
        :param pulumi.Input[str] status: The current state of the certificate CNAME record validation. It should change to `SUCCESS` after App Runner completes validation with your DNS.
        :param pulumi.Input[str] type: The record type, always `CNAME`.
        :param pulumi.Input[str] value: The certificate CNAME record value.
        """
        if name is not None:
            pulumi.set(__self__, "name", name)
        if status is not None:
            pulumi.set(__self__, "status", status)
        if type is not None:
            pulumi.set(__self__, "type", type)
        if value is not None:
            pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The certificate CNAME record name.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def status(self) -> Optional[pulumi.Input[str]]:
        """
        The current state of the certificate CNAME record validation. It should change to `SUCCESS` after App Runner completes validation with your DNS.
        """
        return pulumi.get(self, "status")

    @status.setter
    def status(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "status", value)

    @property
    @pulumi.getter
    def type(self) -> Optional[pulumi.Input[str]]:
        """
        The record type, always `CNAME`.
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "type", value)

    @property
    @pulumi.getter
    def value(self) -> Optional[pulumi.Input[str]]:
        """
        The certificate CNAME record value.
        """
        return pulumi.get(self, "value")

    @value.setter
    def value(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "value", value)


@pulumi.input_type
class ServiceEncryptionConfigurationArgs:
    def __init__(__self__, *,
                 kms_key: pulumi.Input[str]):
        """
        :param pulumi.Input[str] kms_key: The ARN of the KMS key used for encryption.
        """
        pulumi.set(__self__, "kms_key", kms_key)

    @property
    @pulumi.getter(name="kmsKey")
    def kms_key(self) -> pulumi.Input[str]:
        """
        The ARN of the KMS key used for encryption.
        """
        return pulumi.get(self, "kms_key")

    @kms_key.setter
    def kms_key(self, value: pulumi.Input[str]):
        pulumi.set(self, "kms_key", value)


@pulumi.input_type
class ServiceHealthCheckConfigurationArgs:
    def __init__(__self__, *,
                 healthy_threshold: Optional[pulumi.Input[int]] = None,
                 interval: Optional[pulumi.Input[int]] = None,
                 path: Optional[pulumi.Input[str]] = None,
                 protocol: Optional[pulumi.Input[str]] = None,
                 timeout: Optional[pulumi.Input[int]] = None,
                 unhealthy_threshold: Optional[pulumi.Input[int]] = None):
        """
        :param pulumi.Input[int] healthy_threshold: The number of consecutive checks that must succeed before App Runner decides that the service is healthy. Defaults to 1. Minimum value of 1. Maximum value of 20.
        :param pulumi.Input[int] interval: The time interval, in seconds, between health checks. Defaults to 5. Minimum value of 1. Maximum value of 20.
        :param pulumi.Input[str] path: The URL to send requests to for health checks. Defaults to `/`. Minimum length of 0. Maximum length of 51200.
        :param pulumi.Input[str] protocol: The IP protocol that App Runner uses to perform health checks for your service. Valid values: `TCP`, `HTTP`. Defaults to `TCP`. If you set protocol to `HTTP`, App Runner sends health check requests to the HTTP path specified by `path`.
        :param pulumi.Input[int] timeout: The time, in seconds, to wait for a health check response before deciding it failed. Defaults to 2. Minimum value of  1. Maximum value of 20.
        :param pulumi.Input[int] unhealthy_threshold: The number of consecutive checks that must fail before App Runner decides that the service is unhealthy. Defaults to 5. Minimum value of  1. Maximum value of 20.
        """
        if healthy_threshold is not None:
            pulumi.set(__self__, "healthy_threshold", healthy_threshold)
        if interval is not None:
            pulumi.set(__self__, "interval", interval)
        if path is not None:
            pulumi.set(__self__, "path", path)
        if protocol is not None:
            pulumi.set(__self__, "protocol", protocol)
        if timeout is not None:
            pulumi.set(__self__, "timeout", timeout)
        if unhealthy_threshold is not None:
            pulumi.set(__self__, "unhealthy_threshold", unhealthy_threshold)

    @property
    @pulumi.getter(name="healthyThreshold")
    def healthy_threshold(self) -> Optional[pulumi.Input[int]]:
        """
        The number of consecutive checks that must succeed before App Runner decides that the service is healthy. Defaults to 1. Minimum value of 1. Maximum value of 20.
        """
        return pulumi.get(self, "healthy_threshold")

    @healthy_threshold.setter
    def healthy_threshold(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "healthy_threshold", value)

    @property
    @pulumi.getter
    def interval(self) -> Optional[pulumi.Input[int]]:
        """
        The time interval, in seconds, between health checks. Defaults to 5. Minimum value of 1. Maximum value of 20.
        """
        return pulumi.get(self, "interval")

    @interval.setter
    def interval(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "interval", value)

    @property
    @pulumi.getter
    def path(self) -> Optional[pulumi.Input[str]]:
        """
        The URL to send requests to for health checks. Defaults to `/`. Minimum length of 0. Maximum length of 51200.
        """
        return pulumi.get(self, "path")

    @path.setter
    def path(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "path", value)

    @property
    @pulumi.getter
    def protocol(self) -> Optional[pulumi.Input[str]]:
        """
        The IP protocol that App Runner uses to perform health checks for your service. Valid values: `TCP`, `HTTP`. Defaults to `TCP`. If you set protocol to `HTTP`, App Runner sends health check requests to the HTTP path specified by `path`.
        """
        return pulumi.get(self, "protocol")

    @protocol.setter
    def protocol(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "protocol", value)

    @property
    @pulumi.getter
    def timeout(self) -> Optional[pulumi.Input[int]]:
        """
        The time, in seconds, to wait for a health check response before deciding it failed. Defaults to 2. Minimum value of  1. Maximum value of 20.
        """
        return pulumi.get(self, "timeout")

    @timeout.setter
    def timeout(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "timeout", value)

    @property
    @pulumi.getter(name="unhealthyThreshold")
    def unhealthy_threshold(self) -> Optional[pulumi.Input[int]]:
        """
        The number of consecutive checks that must fail before App Runner decides that the service is unhealthy. Defaults to 5. Minimum value of  1. Maximum value of 20.
        """
        return pulumi.get(self, "unhealthy_threshold")

    @unhealthy_threshold.setter
    def unhealthy_threshold(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "unhealthy_threshold", value)


@pulumi.input_type
class ServiceInstanceConfigurationArgs:
    def __init__(__self__, *,
                 cpu: Optional[pulumi.Input[str]] = None,
                 instance_role_arn: Optional[pulumi.Input[str]] = None,
                 memory: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] cpu: The number of CPU units reserved for each instance of your App Runner service represented as a String. Defaults to `1024`. Valid values: `1024|2048|(1|2) vCPU`.
        :param pulumi.Input[str] instance_role_arn: The Amazon Resource Name (ARN) of an IAM role that provides permissions to your App Runner service. These are permissions that your code needs when it calls any AWS APIs.
        :param pulumi.Input[str] memory: The amount of memory, in MB or GB, reserved for each instance of your App Runner service. Defaults to `2048`. Valid values: `2048|3072|4096|(2|3|4) GB`.
        """
        if cpu is not None:
            pulumi.set(__self__, "cpu", cpu)
        if instance_role_arn is not None:
            pulumi.set(__self__, "instance_role_arn", instance_role_arn)
        if memory is not None:
            pulumi.set(__self__, "memory", memory)

    @property
    @pulumi.getter
    def cpu(self) -> Optional[pulumi.Input[str]]:
        """
        The number of CPU units reserved for each instance of your App Runner service represented as a String. Defaults to `1024`. Valid values: `1024|2048|(1|2) vCPU`.
        """
        return pulumi.get(self, "cpu")

    @cpu.setter
    def cpu(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "cpu", value)

    @property
    @pulumi.getter(name="instanceRoleArn")
    def instance_role_arn(self) -> Optional[pulumi.Input[str]]:
        """
        The Amazon Resource Name (ARN) of an IAM role that provides permissions to your App Runner service. These are permissions that your code needs when it calls any AWS APIs.
        """
        return pulumi.get(self, "instance_role_arn")

    @instance_role_arn.setter
    def instance_role_arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "instance_role_arn", value)

    @property
    @pulumi.getter
    def memory(self) -> Optional[pulumi.Input[str]]:
        """
        The amount of memory, in MB or GB, reserved for each instance of your App Runner service. Defaults to `2048`. Valid values: `2048|3072|4096|(2|3|4) GB`.
        """
        return pulumi.get(self, "memory")

    @memory.setter
    def memory(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "memory", value)


@pulumi.input_type
class ServiceSourceConfigurationArgs:
    def __init__(__self__, *,
                 authentication_configuration: Optional[pulumi.Input['ServiceSourceConfigurationAuthenticationConfigurationArgs']] = None,
                 auto_deployments_enabled: Optional[pulumi.Input[bool]] = None,
                 code_repository: Optional[pulumi.Input['ServiceSourceConfigurationCodeRepositoryArgs']] = None,
                 image_repository: Optional[pulumi.Input['ServiceSourceConfigurationImageRepositoryArgs']] = None):
        """
        :param pulumi.Input['ServiceSourceConfigurationAuthenticationConfigurationArgs'] authentication_configuration: Describes resources needed to authenticate access to some source repositories. See Authentication Configuration below for more details.
        :param pulumi.Input[bool] auto_deployments_enabled: Whether continuous integration from the source repository is enabled for the App Runner service. If set to `true`, each repository change (source code commit or new image version) starts a deployment. Defaults to `true`.
        :param pulumi.Input['ServiceSourceConfigurationCodeRepositoryArgs'] code_repository: Description of a source code repository. See Code Repository below for more details.
        :param pulumi.Input['ServiceSourceConfigurationImageRepositoryArgs'] image_repository: Description of a source image repository. See Image Repository below for more details.
        """
        if authentication_configuration is not None:
            pulumi.set(__self__, "authentication_configuration", authentication_configuration)
        if auto_deployments_enabled is not None:
            pulumi.set(__self__, "auto_deployments_enabled", auto_deployments_enabled)
        if code_repository is not None:
            pulumi.set(__self__, "code_repository", code_repository)
        if image_repository is not None:
            pulumi.set(__self__, "image_repository", image_repository)

    @property
    @pulumi.getter(name="authenticationConfiguration")
    def authentication_configuration(self) -> Optional[pulumi.Input['ServiceSourceConfigurationAuthenticationConfigurationArgs']]:
        """
        Describes resources needed to authenticate access to some source repositories. See Authentication Configuration below for more details.
        """
        return pulumi.get(self, "authentication_configuration")

    @authentication_configuration.setter
    def authentication_configuration(self, value: Optional[pulumi.Input['ServiceSourceConfigurationAuthenticationConfigurationArgs']]):
        pulumi.set(self, "authentication_configuration", value)

    @property
    @pulumi.getter(name="autoDeploymentsEnabled")
    def auto_deployments_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether continuous integration from the source repository is enabled for the App Runner service. If set to `true`, each repository change (source code commit or new image version) starts a deployment. Defaults to `true`.
        """
        return pulumi.get(self, "auto_deployments_enabled")

    @auto_deployments_enabled.setter
    def auto_deployments_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "auto_deployments_enabled", value)

    @property
    @pulumi.getter(name="codeRepository")
    def code_repository(self) -> Optional[pulumi.Input['ServiceSourceConfigurationCodeRepositoryArgs']]:
        """
        Description of a source code repository. See Code Repository below for more details.
        """
        return pulumi.get(self, "code_repository")

    @code_repository.setter
    def code_repository(self, value: Optional[pulumi.Input['ServiceSourceConfigurationCodeRepositoryArgs']]):
        pulumi.set(self, "code_repository", value)

    @property
    @pulumi.getter(name="imageRepository")
    def image_repository(self) -> Optional[pulumi.Input['ServiceSourceConfigurationImageRepositoryArgs']]:
        """
        Description of a source image repository. See Image Repository below for more details.
        """
        return pulumi.get(self, "image_repository")

    @image_repository.setter
    def image_repository(self, value: Optional[pulumi.Input['ServiceSourceConfigurationImageRepositoryArgs']]):
        pulumi.set(self, "image_repository", value)


@pulumi.input_type
class ServiceSourceConfigurationAuthenticationConfigurationArgs:
    def __init__(__self__, *,
                 access_role_arn: Optional[pulumi.Input[str]] = None,
                 connection_arn: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] access_role_arn: ARN of the IAM role that grants the App Runner service access to a source repository. Required for ECR image repositories (but not for ECR Public)
        :param pulumi.Input[str] connection_arn: ARN of the App Runner connection that enables the App Runner service to connect to a source repository. Required for GitHub code repositories.
        """
        if access_role_arn is not None:
            pulumi.set(__self__, "access_role_arn", access_role_arn)
        if connection_arn is not None:
            pulumi.set(__self__, "connection_arn", connection_arn)

    @property
    @pulumi.getter(name="accessRoleArn")
    def access_role_arn(self) -> Optional[pulumi.Input[str]]:
        """
        ARN of the IAM role that grants the App Runner service access to a source repository. Required for ECR image repositories (but not for ECR Public)
        """
        return pulumi.get(self, "access_role_arn")

    @access_role_arn.setter
    def access_role_arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "access_role_arn", value)

    @property
    @pulumi.getter(name="connectionArn")
    def connection_arn(self) -> Optional[pulumi.Input[str]]:
        """
        ARN of the App Runner connection that enables the App Runner service to connect to a source repository. Required for GitHub code repositories.
        """
        return pulumi.get(self, "connection_arn")

    @connection_arn.setter
    def connection_arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "connection_arn", value)


@pulumi.input_type
class ServiceSourceConfigurationCodeRepositoryArgs:
    def __init__(__self__, *,
                 repository_url: pulumi.Input[str],
                 source_code_version: pulumi.Input['ServiceSourceConfigurationCodeRepositorySourceCodeVersionArgs'],
                 code_configuration: Optional[pulumi.Input['ServiceSourceConfigurationCodeRepositoryCodeConfigurationArgs']] = None):
        """
        :param pulumi.Input[str] repository_url: The location of the repository that contains the source code.
        :param pulumi.Input['ServiceSourceConfigurationCodeRepositorySourceCodeVersionArgs'] source_code_version: The version that should be used within the source code repository. See Source Code Version below for more details.
        :param pulumi.Input['ServiceSourceConfigurationCodeRepositoryCodeConfigurationArgs'] code_configuration: Configuration for building and running the service from a source code repository. See Code Configuration below for more details.
        """
        pulumi.set(__self__, "repository_url", repository_url)
        pulumi.set(__self__, "source_code_version", source_code_version)
        if code_configuration is not None:
            pulumi.set(__self__, "code_configuration", code_configuration)

    @property
    @pulumi.getter(name="repositoryUrl")
    def repository_url(self) -> pulumi.Input[str]:
        """
        The location of the repository that contains the source code.
        """
        return pulumi.get(self, "repository_url")

    @repository_url.setter
    def repository_url(self, value: pulumi.Input[str]):
        pulumi.set(self, "repository_url", value)

    @property
    @pulumi.getter(name="sourceCodeVersion")
    def source_code_version(self) -> pulumi.Input['ServiceSourceConfigurationCodeRepositorySourceCodeVersionArgs']:
        """
        The version that should be used within the source code repository. See Source Code Version below for more details.
        """
        return pulumi.get(self, "source_code_version")

    @source_code_version.setter
    def source_code_version(self, value: pulumi.Input['ServiceSourceConfigurationCodeRepositorySourceCodeVersionArgs']):
        pulumi.set(self, "source_code_version", value)

    @property
    @pulumi.getter(name="codeConfiguration")
    def code_configuration(self) -> Optional[pulumi.Input['ServiceSourceConfigurationCodeRepositoryCodeConfigurationArgs']]:
        """
        Configuration for building and running the service from a source code repository. See Code Configuration below for more details.
        """
        return pulumi.get(self, "code_configuration")

    @code_configuration.setter
    def code_configuration(self, value: Optional[pulumi.Input['ServiceSourceConfigurationCodeRepositoryCodeConfigurationArgs']]):
        pulumi.set(self, "code_configuration", value)


@pulumi.input_type
class ServiceSourceConfigurationCodeRepositoryCodeConfigurationArgs:
    def __init__(__self__, *,
                 configuration_source: pulumi.Input[str],
                 code_configuration_values: Optional[pulumi.Input['ServiceSourceConfigurationCodeRepositoryCodeConfigurationCodeConfigurationValuesArgs']] = None):
        """
        :param pulumi.Input[str] configuration_source: The source of the App Runner configuration. Valid values: `REPOSITORY`, `API`. Values are interpreted as follows:
        :param pulumi.Input['ServiceSourceConfigurationCodeRepositoryCodeConfigurationCodeConfigurationValuesArgs'] code_configuration_values: Basic configuration for building and running the App Runner service. Use this parameter to quickly launch an App Runner service without providing an apprunner.yaml file in the source code repository (or ignoring the file if it exists). See Code Configuration Values below for more details.
        """
        pulumi.set(__self__, "configuration_source", configuration_source)
        if code_configuration_values is not None:
            pulumi.set(__self__, "code_configuration_values", code_configuration_values)

    @property
    @pulumi.getter(name="configurationSource")
    def configuration_source(self) -> pulumi.Input[str]:
        """
        The source of the App Runner configuration. Valid values: `REPOSITORY`, `API`. Values are interpreted as follows:
        """
        return pulumi.get(self, "configuration_source")

    @configuration_source.setter
    def configuration_source(self, value: pulumi.Input[str]):
        pulumi.set(self, "configuration_source", value)

    @property
    @pulumi.getter(name="codeConfigurationValues")
    def code_configuration_values(self) -> Optional[pulumi.Input['ServiceSourceConfigurationCodeRepositoryCodeConfigurationCodeConfigurationValuesArgs']]:
        """
        Basic configuration for building and running the App Runner service. Use this parameter to quickly launch an App Runner service without providing an apprunner.yaml file in the source code repository (or ignoring the file if it exists). See Code Configuration Values below for more details.
        """
        return pulumi.get(self, "code_configuration_values")

    @code_configuration_values.setter
    def code_configuration_values(self, value: Optional[pulumi.Input['ServiceSourceConfigurationCodeRepositoryCodeConfigurationCodeConfigurationValuesArgs']]):
        pulumi.set(self, "code_configuration_values", value)


@pulumi.input_type
class ServiceSourceConfigurationCodeRepositoryCodeConfigurationCodeConfigurationValuesArgs:
    def __init__(__self__, *,
                 runtime: pulumi.Input[str],
                 build_command: Optional[pulumi.Input[str]] = None,
                 port: Optional[pulumi.Input[str]] = None,
                 runtime_environment_variables: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 start_command: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] runtime: A runtime environment type for building and running an App Runner service. Represents a programming language runtime. Valid values: `PYTHON_3`, `NODEJS_12`.
        :param pulumi.Input[str] build_command: The command App Runner runs to build your application.
        :param pulumi.Input[str] port: The port that your application listens to in the container. Defaults to `"8080"`.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] runtime_environment_variables: Environment variables available to your running App Runner service. A map of key/value pairs. Keys with a prefix of `AWSAPPRUNNER` are reserved for system use and aren't valid.
        :param pulumi.Input[str] start_command: The command App Runner runs to start your application.
        """
        pulumi.set(__self__, "runtime", runtime)
        if build_command is not None:
            pulumi.set(__self__, "build_command", build_command)
        if port is not None:
            pulumi.set(__self__, "port", port)
        if runtime_environment_variables is not None:
            pulumi.set(__self__, "runtime_environment_variables", runtime_environment_variables)
        if start_command is not None:
            pulumi.set(__self__, "start_command", start_command)

    @property
    @pulumi.getter
    def runtime(self) -> pulumi.Input[str]:
        """
        A runtime environment type for building and running an App Runner service. Represents a programming language runtime. Valid values: `PYTHON_3`, `NODEJS_12`.
        """
        return pulumi.get(self, "runtime")

    @runtime.setter
    def runtime(self, value: pulumi.Input[str]):
        pulumi.set(self, "runtime", value)

    @property
    @pulumi.getter(name="buildCommand")
    def build_command(self) -> Optional[pulumi.Input[str]]:
        """
        The command App Runner runs to build your application.
        """
        return pulumi.get(self, "build_command")

    @build_command.setter
    def build_command(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "build_command", value)

    @property
    @pulumi.getter
    def port(self) -> Optional[pulumi.Input[str]]:
        """
        The port that your application listens to in the container. Defaults to `"8080"`.
        """
        return pulumi.get(self, "port")

    @port.setter
    def port(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "port", value)

    @property
    @pulumi.getter(name="runtimeEnvironmentVariables")
    def runtime_environment_variables(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Environment variables available to your running App Runner service. A map of key/value pairs. Keys with a prefix of `AWSAPPRUNNER` are reserved for system use and aren't valid.
        """
        return pulumi.get(self, "runtime_environment_variables")

    @runtime_environment_variables.setter
    def runtime_environment_variables(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "runtime_environment_variables", value)

    @property
    @pulumi.getter(name="startCommand")
    def start_command(self) -> Optional[pulumi.Input[str]]:
        """
        The command App Runner runs to start your application.
        """
        return pulumi.get(self, "start_command")

    @start_command.setter
    def start_command(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "start_command", value)


@pulumi.input_type
class ServiceSourceConfigurationCodeRepositorySourceCodeVersionArgs:
    def __init__(__self__, *,
                 type: pulumi.Input[str],
                 value: pulumi.Input[str]):
        """
        :param pulumi.Input[str] type: The type of version identifier. For a git-based repository, branches represent versions. Valid values: `BRANCH`.
        :param pulumi.Input[str] value: A source code version. For a git-based repository, a branch name maps to a specific version. App Runner uses the most recent commit to the branch.
        """
        pulumi.set(__self__, "type", type)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def type(self) -> pulumi.Input[str]:
        """
        The type of version identifier. For a git-based repository, branches represent versions. Valid values: `BRANCH`.
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: pulumi.Input[str]):
        pulumi.set(self, "type", value)

    @property
    @pulumi.getter
    def value(self) -> pulumi.Input[str]:
        """
        A source code version. For a git-based repository, a branch name maps to a specific version. App Runner uses the most recent commit to the branch.
        """
        return pulumi.get(self, "value")

    @value.setter
    def value(self, value: pulumi.Input[str]):
        pulumi.set(self, "value", value)


@pulumi.input_type
class ServiceSourceConfigurationImageRepositoryArgs:
    def __init__(__self__, *,
                 image_identifier: pulumi.Input[str],
                 image_repository_type: pulumi.Input[str],
                 image_configuration: Optional[pulumi.Input['ServiceSourceConfigurationImageRepositoryImageConfigurationArgs']] = None):
        """
        :param pulumi.Input[str] image_identifier: The identifier of an image. For an image in Amazon Elastic Container Registry (Amazon ECR), this is an image name. For the
               image name format, see Pulling an image in the Amazon ECR User Guide.
        :param pulumi.Input[str] image_repository_type: The type of the image repository. This reflects the repository provider and whether the repository is private or public. Valid values: `ECR` , `ECR_PUBLIC`.
        :param pulumi.Input['ServiceSourceConfigurationImageRepositoryImageConfigurationArgs'] image_configuration: Configuration for running the identified image. See Image Configuration below for more details.
        """
        pulumi.set(__self__, "image_identifier", image_identifier)
        pulumi.set(__self__, "image_repository_type", image_repository_type)
        if image_configuration is not None:
            pulumi.set(__self__, "image_configuration", image_configuration)

    @property
    @pulumi.getter(name="imageIdentifier")
    def image_identifier(self) -> pulumi.Input[str]:
        """
        The identifier of an image. For an image in Amazon Elastic Container Registry (Amazon ECR), this is an image name. For the
        image name format, see Pulling an image in the Amazon ECR User Guide.
        """
        return pulumi.get(self, "image_identifier")

    @image_identifier.setter
    def image_identifier(self, value: pulumi.Input[str]):
        pulumi.set(self, "image_identifier", value)

    @property
    @pulumi.getter(name="imageRepositoryType")
    def image_repository_type(self) -> pulumi.Input[str]:
        """
        The type of the image repository. This reflects the repository provider and whether the repository is private or public. Valid values: `ECR` , `ECR_PUBLIC`.
        """
        return pulumi.get(self, "image_repository_type")

    @image_repository_type.setter
    def image_repository_type(self, value: pulumi.Input[str]):
        pulumi.set(self, "image_repository_type", value)

    @property
    @pulumi.getter(name="imageConfiguration")
    def image_configuration(self) -> Optional[pulumi.Input['ServiceSourceConfigurationImageRepositoryImageConfigurationArgs']]:
        """
        Configuration for running the identified image. See Image Configuration below for more details.
        """
        return pulumi.get(self, "image_configuration")

    @image_configuration.setter
    def image_configuration(self, value: Optional[pulumi.Input['ServiceSourceConfigurationImageRepositoryImageConfigurationArgs']]):
        pulumi.set(self, "image_configuration", value)


@pulumi.input_type
class ServiceSourceConfigurationImageRepositoryImageConfigurationArgs:
    def __init__(__self__, *,
                 port: Optional[pulumi.Input[str]] = None,
                 runtime_environment_variables: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 start_command: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] port: The port that your application listens to in the container. Defaults to `"8080"`.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] runtime_environment_variables: Environment variables available to your running App Runner service. A map of key/value pairs. Keys with a prefix of `AWSAPPRUNNER` are reserved for system use and aren't valid.
        :param pulumi.Input[str] start_command: A command App Runner runs to start the application in the source image. If specified, this command overrides the Docker image’s default start command.
        """
        if port is not None:
            pulumi.set(__self__, "port", port)
        if runtime_environment_variables is not None:
            pulumi.set(__self__, "runtime_environment_variables", runtime_environment_variables)
        if start_command is not None:
            pulumi.set(__self__, "start_command", start_command)

    @property
    @pulumi.getter
    def port(self) -> Optional[pulumi.Input[str]]:
        """
        The port that your application listens to in the container. Defaults to `"8080"`.
        """
        return pulumi.get(self, "port")

    @port.setter
    def port(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "port", value)

    @property
    @pulumi.getter(name="runtimeEnvironmentVariables")
    def runtime_environment_variables(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Environment variables available to your running App Runner service. A map of key/value pairs. Keys with a prefix of `AWSAPPRUNNER` are reserved for system use and aren't valid.
        """
        return pulumi.get(self, "runtime_environment_variables")

    @runtime_environment_variables.setter
    def runtime_environment_variables(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "runtime_environment_variables", value)

    @property
    @pulumi.getter(name="startCommand")
    def start_command(self) -> Optional[pulumi.Input[str]]:
        """
        A command App Runner runs to start the application in the source image. If specified, this command overrides the Docker image’s default start command.
        """
        return pulumi.get(self, "start_command")

    @start_command.setter
    def start_command(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "start_command", value)


