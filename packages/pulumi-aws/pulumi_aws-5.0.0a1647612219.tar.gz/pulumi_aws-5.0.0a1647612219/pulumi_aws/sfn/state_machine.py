# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs
from ._inputs import *

__all__ = ['StateMachineArgs', 'StateMachine']

@pulumi.input_type
class StateMachineArgs:
    def __init__(__self__, *,
                 definition: pulumi.Input[str],
                 role_arn: pulumi.Input[str],
                 logging_configuration: Optional[pulumi.Input['StateMachineLoggingConfigurationArgs']] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 tracing_configuration: Optional[pulumi.Input['StateMachineTracingConfigurationArgs']] = None,
                 type: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a StateMachine resource.
        :param pulumi.Input[str] definition: The [Amazon States Language](https://docs.aws.amazon.com/step-functions/latest/dg/concepts-amazon-states-language.html) definition of the state machine.
        :param pulumi.Input[str] role_arn: The Amazon Resource Name (ARN) of the IAM role to use for this state machine.
        :param pulumi.Input['StateMachineLoggingConfigurationArgs'] logging_configuration: Defines what execution history events are logged and where they are logged. The `logging_configuration` parameter is only valid when `type` is set to `EXPRESS`. Defaults to `OFF`. For more information see [Logging Express Workflows](https://docs.aws.amazon.com/step-functions/latest/dg/cw-logs.html) and [Log Levels](https://docs.aws.amazon.com/step-functions/latest/dg/cloudwatch-log-level.html) in the AWS Step Functions User Guide.
        :param pulumi.Input[str] name: The name of the state machine. To enable logging with CloudWatch Logs, the name should only contain `0`-`9`, `A`-`Z`, `a`-`z`, `-` and `_`.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Key-value map of resource tags. .If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input['StateMachineTracingConfigurationArgs'] tracing_configuration: Selects whether AWS X-Ray tracing is enabled.
        :param pulumi.Input[str] type: Determines whether a Standard or Express state machine is created. The default is `STANDARD`. You cannot update the type of a state machine once it has been created. Valid values: `STANDARD`, `EXPRESS`.
        """
        pulumi.set(__self__, "definition", definition)
        pulumi.set(__self__, "role_arn", role_arn)
        if logging_configuration is not None:
            pulumi.set(__self__, "logging_configuration", logging_configuration)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if tracing_configuration is not None:
            pulumi.set(__self__, "tracing_configuration", tracing_configuration)
        if type is not None:
            pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def definition(self) -> pulumi.Input[str]:
        """
        The [Amazon States Language](https://docs.aws.amazon.com/step-functions/latest/dg/concepts-amazon-states-language.html) definition of the state machine.
        """
        return pulumi.get(self, "definition")

    @definition.setter
    def definition(self, value: pulumi.Input[str]):
        pulumi.set(self, "definition", value)

    @property
    @pulumi.getter(name="roleArn")
    def role_arn(self) -> pulumi.Input[str]:
        """
        The Amazon Resource Name (ARN) of the IAM role to use for this state machine.
        """
        return pulumi.get(self, "role_arn")

    @role_arn.setter
    def role_arn(self, value: pulumi.Input[str]):
        pulumi.set(self, "role_arn", value)

    @property
    @pulumi.getter(name="loggingConfiguration")
    def logging_configuration(self) -> Optional[pulumi.Input['StateMachineLoggingConfigurationArgs']]:
        """
        Defines what execution history events are logged and where they are logged. The `logging_configuration` parameter is only valid when `type` is set to `EXPRESS`. Defaults to `OFF`. For more information see [Logging Express Workflows](https://docs.aws.amazon.com/step-functions/latest/dg/cw-logs.html) and [Log Levels](https://docs.aws.amazon.com/step-functions/latest/dg/cloudwatch-log-level.html) in the AWS Step Functions User Guide.
        """
        return pulumi.get(self, "logging_configuration")

    @logging_configuration.setter
    def logging_configuration(self, value: Optional[pulumi.Input['StateMachineLoggingConfigurationArgs']]):
        pulumi.set(self, "logging_configuration", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the state machine. To enable logging with CloudWatch Logs, the name should only contain `0`-`9`, `A`-`Z`, `a`-`z`, `-` and `_`.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Key-value map of resource tags. .If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter(name="tracingConfiguration")
    def tracing_configuration(self) -> Optional[pulumi.Input['StateMachineTracingConfigurationArgs']]:
        """
        Selects whether AWS X-Ray tracing is enabled.
        """
        return pulumi.get(self, "tracing_configuration")

    @tracing_configuration.setter
    def tracing_configuration(self, value: Optional[pulumi.Input['StateMachineTracingConfigurationArgs']]):
        pulumi.set(self, "tracing_configuration", value)

    @property
    @pulumi.getter
    def type(self) -> Optional[pulumi.Input[str]]:
        """
        Determines whether a Standard or Express state machine is created. The default is `STANDARD`. You cannot update the type of a state machine once it has been created. Valid values: `STANDARD`, `EXPRESS`.
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "type", value)


@pulumi.input_type
class _StateMachineState:
    def __init__(__self__, *,
                 arn: Optional[pulumi.Input[str]] = None,
                 creation_date: Optional[pulumi.Input[str]] = None,
                 definition: Optional[pulumi.Input[str]] = None,
                 logging_configuration: Optional[pulumi.Input['StateMachineLoggingConfigurationArgs']] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 role_arn: Optional[pulumi.Input[str]] = None,
                 status: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 tracing_configuration: Optional[pulumi.Input['StateMachineTracingConfigurationArgs']] = None,
                 type: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering StateMachine resources.
        :param pulumi.Input[str] arn: The ARN of the state machine.
        :param pulumi.Input[str] creation_date: The date the state machine was created.
        :param pulumi.Input[str] definition: The [Amazon States Language](https://docs.aws.amazon.com/step-functions/latest/dg/concepts-amazon-states-language.html) definition of the state machine.
        :param pulumi.Input['StateMachineLoggingConfigurationArgs'] logging_configuration: Defines what execution history events are logged and where they are logged. The `logging_configuration` parameter is only valid when `type` is set to `EXPRESS`. Defaults to `OFF`. For more information see [Logging Express Workflows](https://docs.aws.amazon.com/step-functions/latest/dg/cw-logs.html) and [Log Levels](https://docs.aws.amazon.com/step-functions/latest/dg/cloudwatch-log-level.html) in the AWS Step Functions User Guide.
        :param pulumi.Input[str] name: The name of the state machine. To enable logging with CloudWatch Logs, the name should only contain `0`-`9`, `A`-`Z`, `a`-`z`, `-` and `_`.
        :param pulumi.Input[str] role_arn: The Amazon Resource Name (ARN) of the IAM role to use for this state machine.
        :param pulumi.Input[str] status: The current status of the state machine. Either `ACTIVE` or `DELETING`.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Key-value map of resource tags. .If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags_all: A map of tags assigned to the resource, including those inherited from the provider.
        :param pulumi.Input['StateMachineTracingConfigurationArgs'] tracing_configuration: Selects whether AWS X-Ray tracing is enabled.
        :param pulumi.Input[str] type: Determines whether a Standard or Express state machine is created. The default is `STANDARD`. You cannot update the type of a state machine once it has been created. Valid values: `STANDARD`, `EXPRESS`.
        """
        if arn is not None:
            pulumi.set(__self__, "arn", arn)
        if creation_date is not None:
            pulumi.set(__self__, "creation_date", creation_date)
        if definition is not None:
            pulumi.set(__self__, "definition", definition)
        if logging_configuration is not None:
            pulumi.set(__self__, "logging_configuration", logging_configuration)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if role_arn is not None:
            pulumi.set(__self__, "role_arn", role_arn)
        if status is not None:
            pulumi.set(__self__, "status", status)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if tags_all is not None:
            pulumi.set(__self__, "tags_all", tags_all)
        if tracing_configuration is not None:
            pulumi.set(__self__, "tracing_configuration", tracing_configuration)
        if type is not None:
            pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def arn(self) -> Optional[pulumi.Input[str]]:
        """
        The ARN of the state machine.
        """
        return pulumi.get(self, "arn")

    @arn.setter
    def arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "arn", value)

    @property
    @pulumi.getter(name="creationDate")
    def creation_date(self) -> Optional[pulumi.Input[str]]:
        """
        The date the state machine was created.
        """
        return pulumi.get(self, "creation_date")

    @creation_date.setter
    def creation_date(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "creation_date", value)

    @property
    @pulumi.getter
    def definition(self) -> Optional[pulumi.Input[str]]:
        """
        The [Amazon States Language](https://docs.aws.amazon.com/step-functions/latest/dg/concepts-amazon-states-language.html) definition of the state machine.
        """
        return pulumi.get(self, "definition")

    @definition.setter
    def definition(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "definition", value)

    @property
    @pulumi.getter(name="loggingConfiguration")
    def logging_configuration(self) -> Optional[pulumi.Input['StateMachineLoggingConfigurationArgs']]:
        """
        Defines what execution history events are logged and where they are logged. The `logging_configuration` parameter is only valid when `type` is set to `EXPRESS`. Defaults to `OFF`. For more information see [Logging Express Workflows](https://docs.aws.amazon.com/step-functions/latest/dg/cw-logs.html) and [Log Levels](https://docs.aws.amazon.com/step-functions/latest/dg/cloudwatch-log-level.html) in the AWS Step Functions User Guide.
        """
        return pulumi.get(self, "logging_configuration")

    @logging_configuration.setter
    def logging_configuration(self, value: Optional[pulumi.Input['StateMachineLoggingConfigurationArgs']]):
        pulumi.set(self, "logging_configuration", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the state machine. To enable logging with CloudWatch Logs, the name should only contain `0`-`9`, `A`-`Z`, `a`-`z`, `-` and `_`.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="roleArn")
    def role_arn(self) -> Optional[pulumi.Input[str]]:
        """
        The Amazon Resource Name (ARN) of the IAM role to use for this state machine.
        """
        return pulumi.get(self, "role_arn")

    @role_arn.setter
    def role_arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "role_arn", value)

    @property
    @pulumi.getter
    def status(self) -> Optional[pulumi.Input[str]]:
        """
        The current status of the state machine. Either `ACTIVE` or `DELETING`.
        """
        return pulumi.get(self, "status")

    @status.setter
    def status(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "status", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Key-value map of resource tags. .If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter(name="tagsAll")
    def tags_all(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A map of tags assigned to the resource, including those inherited from the provider.
        """
        return pulumi.get(self, "tags_all")

    @tags_all.setter
    def tags_all(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags_all", value)

    @property
    @pulumi.getter(name="tracingConfiguration")
    def tracing_configuration(self) -> Optional[pulumi.Input['StateMachineTracingConfigurationArgs']]:
        """
        Selects whether AWS X-Ray tracing is enabled.
        """
        return pulumi.get(self, "tracing_configuration")

    @tracing_configuration.setter
    def tracing_configuration(self, value: Optional[pulumi.Input['StateMachineTracingConfigurationArgs']]):
        pulumi.set(self, "tracing_configuration", value)

    @property
    @pulumi.getter
    def type(self) -> Optional[pulumi.Input[str]]:
        """
        Determines whether a Standard or Express state machine is created. The default is `STANDARD`. You cannot update the type of a state machine once it has been created. Valid values: `STANDARD`, `EXPRESS`.
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "type", value)


class StateMachine(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 definition: Optional[pulumi.Input[str]] = None,
                 logging_configuration: Optional[pulumi.Input[pulumi.InputType['StateMachineLoggingConfigurationArgs']]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 role_arn: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 tracing_configuration: Optional[pulumi.Input[pulumi.InputType['StateMachineTracingConfigurationArgs']]] = None,
                 type: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Provides a Step Function State Machine resource

        ## Example Usage
        ### Basic (Standard Workflow)

        ```python
        import pulumi
        import pulumi_aws as aws

        # ...
        sfn_state_machine = aws.sfn.StateMachine("sfnStateMachine",
            role_arn=aws_iam_role["iam_for_sfn"]["arn"],
            definition=f\"\"\"{{
          "Comment": "A Hello World example of the Amazon States Language using an AWS Lambda Function",
          "StartAt": "HelloWorld",
          "States": {{
            "HelloWorld": {{
              "Type": "Task",
              "Resource": "{aws_lambda_function["lambda"]["arn"]}",
              "End": true
            }}
          }}
        }}
        \"\"\")
        ```
        ### Basic (Express Workflow)

        ```python
        import pulumi
        import pulumi_aws as aws

        # ...
        sfn_state_machine = aws.sfn.StateMachine("sfnStateMachine",
            role_arn=aws_iam_role["iam_for_sfn"]["arn"],
            type="EXPRESS",
            definition=f\"\"\"{{
          "Comment": "A Hello World example of the Amazon States Language using an AWS Lambda Function",
          "StartAt": "HelloWorld",
          "States": {{
            "HelloWorld": {{
              "Type": "Task",
              "Resource": "{aws_lambda_function["lambda"]["arn"]}",
              "End": true
            }}
          }}
        }}
        \"\"\")
        ```
        ### Logging

        > *NOTE:* See the [AWS Step Functions Developer Guide](https://docs.aws.amazon.com/step-functions/latest/dg/welcome.html) for more information about enabling Step Function logging.

        ```python
        import pulumi
        import pulumi_aws as aws

        # ...
        sfn_state_machine = aws.sfn.StateMachine("sfnStateMachine",
            role_arn=aws_iam_role["iam_for_sfn"]["arn"],
            definition=f\"\"\"{{
          "Comment": "A Hello World example of the Amazon States Language using an AWS Lambda Function",
          "StartAt": "HelloWorld",
          "States": {{
            "HelloWorld": {{
              "Type": "Task",
              "Resource": "{aws_lambda_function["lambda"]["arn"]}",
              "End": true
            }}
          }}
        }}
        \"\"\",
            logging_configuration=aws.sfn.StateMachineLoggingConfigurationArgs(
                log_destination=f"{aws_cloudwatch_log_group['log_group_for_sfn']['arn']}:*",
                include_execution_data=True,
                level="ERROR",
            ))
        ```

        ## Import

        State Machines can be imported using the `arn`, e.g.,

        ```sh
         $ pulumi import aws:sfn/stateMachine:StateMachine foo arn:aws:states:eu-west-1:123456789098:stateMachine:bar
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] definition: The [Amazon States Language](https://docs.aws.amazon.com/step-functions/latest/dg/concepts-amazon-states-language.html) definition of the state machine.
        :param pulumi.Input[pulumi.InputType['StateMachineLoggingConfigurationArgs']] logging_configuration: Defines what execution history events are logged and where they are logged. The `logging_configuration` parameter is only valid when `type` is set to `EXPRESS`. Defaults to `OFF`. For more information see [Logging Express Workflows](https://docs.aws.amazon.com/step-functions/latest/dg/cw-logs.html) and [Log Levels](https://docs.aws.amazon.com/step-functions/latest/dg/cloudwatch-log-level.html) in the AWS Step Functions User Guide.
        :param pulumi.Input[str] name: The name of the state machine. To enable logging with CloudWatch Logs, the name should only contain `0`-`9`, `A`-`Z`, `a`-`z`, `-` and `_`.
        :param pulumi.Input[str] role_arn: The Amazon Resource Name (ARN) of the IAM role to use for this state machine.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Key-value map of resource tags. .If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input[pulumi.InputType['StateMachineTracingConfigurationArgs']] tracing_configuration: Selects whether AWS X-Ray tracing is enabled.
        :param pulumi.Input[str] type: Determines whether a Standard or Express state machine is created. The default is `STANDARD`. You cannot update the type of a state machine once it has been created. Valid values: `STANDARD`, `EXPRESS`.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: StateMachineArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a Step Function State Machine resource

        ## Example Usage
        ### Basic (Standard Workflow)

        ```python
        import pulumi
        import pulumi_aws as aws

        # ...
        sfn_state_machine = aws.sfn.StateMachine("sfnStateMachine",
            role_arn=aws_iam_role["iam_for_sfn"]["arn"],
            definition=f\"\"\"{{
          "Comment": "A Hello World example of the Amazon States Language using an AWS Lambda Function",
          "StartAt": "HelloWorld",
          "States": {{
            "HelloWorld": {{
              "Type": "Task",
              "Resource": "{aws_lambda_function["lambda"]["arn"]}",
              "End": true
            }}
          }}
        }}
        \"\"\")
        ```
        ### Basic (Express Workflow)

        ```python
        import pulumi
        import pulumi_aws as aws

        # ...
        sfn_state_machine = aws.sfn.StateMachine("sfnStateMachine",
            role_arn=aws_iam_role["iam_for_sfn"]["arn"],
            type="EXPRESS",
            definition=f\"\"\"{{
          "Comment": "A Hello World example of the Amazon States Language using an AWS Lambda Function",
          "StartAt": "HelloWorld",
          "States": {{
            "HelloWorld": {{
              "Type": "Task",
              "Resource": "{aws_lambda_function["lambda"]["arn"]}",
              "End": true
            }}
          }}
        }}
        \"\"\")
        ```
        ### Logging

        > *NOTE:* See the [AWS Step Functions Developer Guide](https://docs.aws.amazon.com/step-functions/latest/dg/welcome.html) for more information about enabling Step Function logging.

        ```python
        import pulumi
        import pulumi_aws as aws

        # ...
        sfn_state_machine = aws.sfn.StateMachine("sfnStateMachine",
            role_arn=aws_iam_role["iam_for_sfn"]["arn"],
            definition=f\"\"\"{{
          "Comment": "A Hello World example of the Amazon States Language using an AWS Lambda Function",
          "StartAt": "HelloWorld",
          "States": {{
            "HelloWorld": {{
              "Type": "Task",
              "Resource": "{aws_lambda_function["lambda"]["arn"]}",
              "End": true
            }}
          }}
        }}
        \"\"\",
            logging_configuration=aws.sfn.StateMachineLoggingConfigurationArgs(
                log_destination=f"{aws_cloudwatch_log_group['log_group_for_sfn']['arn']}:*",
                include_execution_data=True,
                level="ERROR",
            ))
        ```

        ## Import

        State Machines can be imported using the `arn`, e.g.,

        ```sh
         $ pulumi import aws:sfn/stateMachine:StateMachine foo arn:aws:states:eu-west-1:123456789098:stateMachine:bar
        ```

        :param str resource_name: The name of the resource.
        :param StateMachineArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(StateMachineArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 definition: Optional[pulumi.Input[str]] = None,
                 logging_configuration: Optional[pulumi.Input[pulumi.InputType['StateMachineLoggingConfigurationArgs']]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 role_arn: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 tracing_configuration: Optional[pulumi.Input[pulumi.InputType['StateMachineTracingConfigurationArgs']]] = None,
                 type: Optional[pulumi.Input[str]] = None,
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
            __props__ = StateMachineArgs.__new__(StateMachineArgs)

            if definition is None and not opts.urn:
                raise TypeError("Missing required property 'definition'")
            __props__.__dict__["definition"] = definition
            __props__.__dict__["logging_configuration"] = logging_configuration
            __props__.__dict__["name"] = name
            if role_arn is None and not opts.urn:
                raise TypeError("Missing required property 'role_arn'")
            __props__.__dict__["role_arn"] = role_arn
            __props__.__dict__["tags"] = tags
            __props__.__dict__["tracing_configuration"] = tracing_configuration
            __props__.__dict__["type"] = type
            __props__.__dict__["arn"] = None
            __props__.__dict__["creation_date"] = None
            __props__.__dict__["status"] = None
            __props__.__dict__["tags_all"] = None
        super(StateMachine, __self__).__init__(
            'aws:sfn/stateMachine:StateMachine',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            arn: Optional[pulumi.Input[str]] = None,
            creation_date: Optional[pulumi.Input[str]] = None,
            definition: Optional[pulumi.Input[str]] = None,
            logging_configuration: Optional[pulumi.Input[pulumi.InputType['StateMachineLoggingConfigurationArgs']]] = None,
            name: Optional[pulumi.Input[str]] = None,
            role_arn: Optional[pulumi.Input[str]] = None,
            status: Optional[pulumi.Input[str]] = None,
            tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            tracing_configuration: Optional[pulumi.Input[pulumi.InputType['StateMachineTracingConfigurationArgs']]] = None,
            type: Optional[pulumi.Input[str]] = None) -> 'StateMachine':
        """
        Get an existing StateMachine resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] arn: The ARN of the state machine.
        :param pulumi.Input[str] creation_date: The date the state machine was created.
        :param pulumi.Input[str] definition: The [Amazon States Language](https://docs.aws.amazon.com/step-functions/latest/dg/concepts-amazon-states-language.html) definition of the state machine.
        :param pulumi.Input[pulumi.InputType['StateMachineLoggingConfigurationArgs']] logging_configuration: Defines what execution history events are logged and where they are logged. The `logging_configuration` parameter is only valid when `type` is set to `EXPRESS`. Defaults to `OFF`. For more information see [Logging Express Workflows](https://docs.aws.amazon.com/step-functions/latest/dg/cw-logs.html) and [Log Levels](https://docs.aws.amazon.com/step-functions/latest/dg/cloudwatch-log-level.html) in the AWS Step Functions User Guide.
        :param pulumi.Input[str] name: The name of the state machine. To enable logging with CloudWatch Logs, the name should only contain `0`-`9`, `A`-`Z`, `a`-`z`, `-` and `_`.
        :param pulumi.Input[str] role_arn: The Amazon Resource Name (ARN) of the IAM role to use for this state machine.
        :param pulumi.Input[str] status: The current status of the state machine. Either `ACTIVE` or `DELETING`.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Key-value map of resource tags. .If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags_all: A map of tags assigned to the resource, including those inherited from the provider.
        :param pulumi.Input[pulumi.InputType['StateMachineTracingConfigurationArgs']] tracing_configuration: Selects whether AWS X-Ray tracing is enabled.
        :param pulumi.Input[str] type: Determines whether a Standard or Express state machine is created. The default is `STANDARD`. You cannot update the type of a state machine once it has been created. Valid values: `STANDARD`, `EXPRESS`.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _StateMachineState.__new__(_StateMachineState)

        __props__.__dict__["arn"] = arn
        __props__.__dict__["creation_date"] = creation_date
        __props__.__dict__["definition"] = definition
        __props__.__dict__["logging_configuration"] = logging_configuration
        __props__.__dict__["name"] = name
        __props__.__dict__["role_arn"] = role_arn
        __props__.__dict__["status"] = status
        __props__.__dict__["tags"] = tags
        __props__.__dict__["tags_all"] = tags_all
        __props__.__dict__["tracing_configuration"] = tracing_configuration
        __props__.__dict__["type"] = type
        return StateMachine(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        """
        The ARN of the state machine.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="creationDate")
    def creation_date(self) -> pulumi.Output[str]:
        """
        The date the state machine was created.
        """
        return pulumi.get(self, "creation_date")

    @property
    @pulumi.getter
    def definition(self) -> pulumi.Output[str]:
        """
        The [Amazon States Language](https://docs.aws.amazon.com/step-functions/latest/dg/concepts-amazon-states-language.html) definition of the state machine.
        """
        return pulumi.get(self, "definition")

    @property
    @pulumi.getter(name="loggingConfiguration")
    def logging_configuration(self) -> pulumi.Output['outputs.StateMachineLoggingConfiguration']:
        """
        Defines what execution history events are logged and where they are logged. The `logging_configuration` parameter is only valid when `type` is set to `EXPRESS`. Defaults to `OFF`. For more information see [Logging Express Workflows](https://docs.aws.amazon.com/step-functions/latest/dg/cw-logs.html) and [Log Levels](https://docs.aws.amazon.com/step-functions/latest/dg/cloudwatch-log-level.html) in the AWS Step Functions User Guide.
        """
        return pulumi.get(self, "logging_configuration")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the state machine. To enable logging with CloudWatch Logs, the name should only contain `0`-`9`, `A`-`Z`, `a`-`z`, `-` and `_`.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="roleArn")
    def role_arn(self) -> pulumi.Output[str]:
        """
        The Amazon Resource Name (ARN) of the IAM role to use for this state machine.
        """
        return pulumi.get(self, "role_arn")

    @property
    @pulumi.getter
    def status(self) -> pulumi.Output[str]:
        """
        The current status of the state machine. Either `ACTIVE` or `DELETING`.
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Key-value map of resource tags. .If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="tagsAll")
    def tags_all(self) -> pulumi.Output[Mapping[str, str]]:
        """
        A map of tags assigned to the resource, including those inherited from the provider.
        """
        return pulumi.get(self, "tags_all")

    @property
    @pulumi.getter(name="tracingConfiguration")
    def tracing_configuration(self) -> pulumi.Output['outputs.StateMachineTracingConfiguration']:
        """
        Selects whether AWS X-Ray tracing is enabled.
        """
        return pulumi.get(self, "tracing_configuration")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[Optional[str]]:
        """
        Determines whether a Standard or Express state machine is created. The default is `STANDARD`. You cannot update the type of a state machine once it has been created. Valid values: `STANDARD`, `EXPRESS`.
        """
        return pulumi.get(self, "type")

