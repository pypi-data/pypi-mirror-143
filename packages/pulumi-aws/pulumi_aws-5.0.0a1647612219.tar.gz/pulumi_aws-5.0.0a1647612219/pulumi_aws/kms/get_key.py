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
    'GetKeyResult',
    'AwaitableGetKeyResult',
    'get_key',
    'get_key_output',
]

@pulumi.output_type
class GetKeyResult:
    """
    A collection of values returned by getKey.
    """
    def __init__(__self__, arn=None, aws_account_id=None, creation_date=None, customer_master_key_spec=None, deletion_date=None, description=None, enabled=None, expiration_model=None, grant_tokens=None, id=None, key_id=None, key_manager=None, key_state=None, key_usage=None, multi_region=None, multi_region_configurations=None, origin=None, valid_to=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if aws_account_id and not isinstance(aws_account_id, str):
            raise TypeError("Expected argument 'aws_account_id' to be a str")
        pulumi.set(__self__, "aws_account_id", aws_account_id)
        if creation_date and not isinstance(creation_date, str):
            raise TypeError("Expected argument 'creation_date' to be a str")
        pulumi.set(__self__, "creation_date", creation_date)
        if customer_master_key_spec and not isinstance(customer_master_key_spec, str):
            raise TypeError("Expected argument 'customer_master_key_spec' to be a str")
        pulumi.set(__self__, "customer_master_key_spec", customer_master_key_spec)
        if deletion_date and not isinstance(deletion_date, str):
            raise TypeError("Expected argument 'deletion_date' to be a str")
        pulumi.set(__self__, "deletion_date", deletion_date)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if enabled and not isinstance(enabled, bool):
            raise TypeError("Expected argument 'enabled' to be a bool")
        pulumi.set(__self__, "enabled", enabled)
        if expiration_model and not isinstance(expiration_model, str):
            raise TypeError("Expected argument 'expiration_model' to be a str")
        pulumi.set(__self__, "expiration_model", expiration_model)
        if grant_tokens and not isinstance(grant_tokens, list):
            raise TypeError("Expected argument 'grant_tokens' to be a list")
        pulumi.set(__self__, "grant_tokens", grant_tokens)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if key_id and not isinstance(key_id, str):
            raise TypeError("Expected argument 'key_id' to be a str")
        pulumi.set(__self__, "key_id", key_id)
        if key_manager and not isinstance(key_manager, str):
            raise TypeError("Expected argument 'key_manager' to be a str")
        pulumi.set(__self__, "key_manager", key_manager)
        if key_state and not isinstance(key_state, str):
            raise TypeError("Expected argument 'key_state' to be a str")
        pulumi.set(__self__, "key_state", key_state)
        if key_usage and not isinstance(key_usage, str):
            raise TypeError("Expected argument 'key_usage' to be a str")
        pulumi.set(__self__, "key_usage", key_usage)
        if multi_region and not isinstance(multi_region, bool):
            raise TypeError("Expected argument 'multi_region' to be a bool")
        pulumi.set(__self__, "multi_region", multi_region)
        if multi_region_configurations and not isinstance(multi_region_configurations, list):
            raise TypeError("Expected argument 'multi_region_configurations' to be a list")
        pulumi.set(__self__, "multi_region_configurations", multi_region_configurations)
        if origin and not isinstance(origin, str):
            raise TypeError("Expected argument 'origin' to be a str")
        pulumi.set(__self__, "origin", origin)
        if valid_to and not isinstance(valid_to, str):
            raise TypeError("Expected argument 'valid_to' to be a str")
        pulumi.set(__self__, "valid_to", valid_to)

    @property
    @pulumi.getter
    def arn(self) -> str:
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="awsAccountId")
    def aws_account_id(self) -> str:
        return pulumi.get(self, "aws_account_id")

    @property
    @pulumi.getter(name="creationDate")
    def creation_date(self) -> str:
        return pulumi.get(self, "creation_date")

    @property
    @pulumi.getter(name="customerMasterKeySpec")
    def customer_master_key_spec(self) -> str:
        return pulumi.get(self, "customer_master_key_spec")

    @property
    @pulumi.getter(name="deletionDate")
    def deletion_date(self) -> str:
        return pulumi.get(self, "deletion_date")

    @property
    @pulumi.getter
    def description(self) -> str:
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def enabled(self) -> bool:
        return pulumi.get(self, "enabled")

    @property
    @pulumi.getter(name="expirationModel")
    def expiration_model(self) -> str:
        return pulumi.get(self, "expiration_model")

    @property
    @pulumi.getter(name="grantTokens")
    def grant_tokens(self) -> Optional[Sequence[str]]:
        return pulumi.get(self, "grant_tokens")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="keyId")
    def key_id(self) -> str:
        return pulumi.get(self, "key_id")

    @property
    @pulumi.getter(name="keyManager")
    def key_manager(self) -> str:
        return pulumi.get(self, "key_manager")

    @property
    @pulumi.getter(name="keyState")
    def key_state(self) -> str:
        return pulumi.get(self, "key_state")

    @property
    @pulumi.getter(name="keyUsage")
    def key_usage(self) -> str:
        return pulumi.get(self, "key_usage")

    @property
    @pulumi.getter(name="multiRegion")
    def multi_region(self) -> bool:
        return pulumi.get(self, "multi_region")

    @property
    @pulumi.getter(name="multiRegionConfigurations")
    def multi_region_configurations(self) -> Sequence['outputs.GetKeyMultiRegionConfigurationResult']:
        return pulumi.get(self, "multi_region_configurations")

    @property
    @pulumi.getter
    def origin(self) -> str:
        return pulumi.get(self, "origin")

    @property
    @pulumi.getter(name="validTo")
    def valid_to(self) -> str:
        return pulumi.get(self, "valid_to")


class AwaitableGetKeyResult(GetKeyResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetKeyResult(
            arn=self.arn,
            aws_account_id=self.aws_account_id,
            creation_date=self.creation_date,
            customer_master_key_spec=self.customer_master_key_spec,
            deletion_date=self.deletion_date,
            description=self.description,
            enabled=self.enabled,
            expiration_model=self.expiration_model,
            grant_tokens=self.grant_tokens,
            id=self.id,
            key_id=self.key_id,
            key_manager=self.key_manager,
            key_state=self.key_state,
            key_usage=self.key_usage,
            multi_region=self.multi_region,
            multi_region_configurations=self.multi_region_configurations,
            origin=self.origin,
            valid_to=self.valid_to)


def get_key(grant_tokens: Optional[Sequence[str]] = None,
            key_id: Optional[str] = None,
            opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetKeyResult:
    """
    Use this data source to get detailed information about
    the specified KMS Key with flexible key id input.
    This can be useful to reference key alias
    without having to hard code the ARN as input.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    by_alias = aws.kms.get_key(key_id="alias/my-key")
    by_id = aws.kms.get_key(key_id="1234abcd-12ab-34cd-56ef-1234567890ab")
    by_alias_arn = aws.kms.get_key(key_id="arn:aws:kms:us-east-1:111122223333:alias/my-key")
    by_key_arn = aws.kms.get_key(key_id="arn:aws:kms:us-east-1:111122223333:key/1234abcd-12ab-34cd-56ef-1234567890ab")
    ```


    :param Sequence[str] grant_tokens: List of grant tokens
    :param str key_id: Key identifier which can be one of the following format:
           * Key ID. E.g: `1234abcd-12ab-34cd-56ef-1234567890ab`
           * Key ARN. E.g.: `arn:aws:kms:us-east-1:111122223333:key/1234abcd-12ab-34cd-56ef-1234567890ab`
           * Alias name. E.g.: `alias/my-key`
           * Alias ARN: E.g.: `arn:aws:kms:us-east-1:111122223333:alias/my-key`
    """
    __args__ = dict()
    __args__['grantTokens'] = grant_tokens
    __args__['keyId'] = key_id
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('aws:kms/getKey:getKey', __args__, opts=opts, typ=GetKeyResult).value

    return AwaitableGetKeyResult(
        arn=__ret__.arn,
        aws_account_id=__ret__.aws_account_id,
        creation_date=__ret__.creation_date,
        customer_master_key_spec=__ret__.customer_master_key_spec,
        deletion_date=__ret__.deletion_date,
        description=__ret__.description,
        enabled=__ret__.enabled,
        expiration_model=__ret__.expiration_model,
        grant_tokens=__ret__.grant_tokens,
        id=__ret__.id,
        key_id=__ret__.key_id,
        key_manager=__ret__.key_manager,
        key_state=__ret__.key_state,
        key_usage=__ret__.key_usage,
        multi_region=__ret__.multi_region,
        multi_region_configurations=__ret__.multi_region_configurations,
        origin=__ret__.origin,
        valid_to=__ret__.valid_to)


@_utilities.lift_output_func(get_key)
def get_key_output(grant_tokens: Optional[pulumi.Input[Optional[Sequence[str]]]] = None,
                   key_id: Optional[pulumi.Input[str]] = None,
                   opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetKeyResult]:
    """
    Use this data source to get detailed information about
    the specified KMS Key with flexible key id input.
    This can be useful to reference key alias
    without having to hard code the ARN as input.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    by_alias = aws.kms.get_key(key_id="alias/my-key")
    by_id = aws.kms.get_key(key_id="1234abcd-12ab-34cd-56ef-1234567890ab")
    by_alias_arn = aws.kms.get_key(key_id="arn:aws:kms:us-east-1:111122223333:alias/my-key")
    by_key_arn = aws.kms.get_key(key_id="arn:aws:kms:us-east-1:111122223333:key/1234abcd-12ab-34cd-56ef-1234567890ab")
    ```


    :param Sequence[str] grant_tokens: List of grant tokens
    :param str key_id: Key identifier which can be one of the following format:
           * Key ID. E.g: `1234abcd-12ab-34cd-56ef-1234567890ab`
           * Key ARN. E.g.: `arn:aws:kms:us-east-1:111122223333:key/1234abcd-12ab-34cd-56ef-1234567890ab`
           * Alias name. E.g.: `alias/my-key`
           * Alias ARN: E.g.: `arn:aws:kms:us-east-1:111122223333:alias/my-key`
    """
    ...
