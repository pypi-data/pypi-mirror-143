# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = [
    'IAppListArgs',
    'IAppMetadataArgs',
    'IAppTableArgs',
    'IAppTableRowArgs',
    'IAppVariableArgs',
]

@pulumi.input_type
class IAppListArgs:
    def __init__(__self__, *,
                 encrypted: Optional[pulumi.Input[str]] = None,
                 value: Optional[pulumi.Input[str]] = None):
        if encrypted is not None:
            pulumi.set(__self__, "encrypted", encrypted)
        if value is not None:
            pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def encrypted(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "encrypted")

    @encrypted.setter
    def encrypted(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "encrypted", value)

    @property
    @pulumi.getter
    def value(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "value")

    @value.setter
    def value(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "value", value)


@pulumi.input_type
class IAppMetadataArgs:
    def __init__(__self__, *,
                 persists: Optional[pulumi.Input[str]] = None,
                 value: Optional[pulumi.Input[str]] = None):
        if persists is not None:
            pulumi.set(__self__, "persists", persists)
        if value is not None:
            pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def persists(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "persists")

    @persists.setter
    def persists(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "persists", value)

    @property
    @pulumi.getter
    def value(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "value")

    @value.setter
    def value(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "value", value)


@pulumi.input_type
class IAppTableArgs:
    def __init__(__self__, *,
                 column_names: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 encrypted_columns: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 rows: Optional[pulumi.Input[Sequence[pulumi.Input['IAppTableRowArgs']]]] = None):
        """
        :param pulumi.Input[str] name: Name of the iApp.
        """
        if column_names is not None:
            pulumi.set(__self__, "column_names", column_names)
        if encrypted_columns is not None:
            pulumi.set(__self__, "encrypted_columns", encrypted_columns)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if rows is not None:
            pulumi.set(__self__, "rows", rows)

    @property
    @pulumi.getter(name="columnNames")
    def column_names(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        return pulumi.get(self, "column_names")

    @column_names.setter
    def column_names(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "column_names", value)

    @property
    @pulumi.getter(name="encryptedColumns")
    def encrypted_columns(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "encrypted_columns")

    @encrypted_columns.setter
    def encrypted_columns(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "encrypted_columns", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the iApp.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def rows(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['IAppTableRowArgs']]]]:
        return pulumi.get(self, "rows")

    @rows.setter
    def rows(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['IAppTableRowArgs']]]]):
        pulumi.set(self, "rows", value)


@pulumi.input_type
class IAppTableRowArgs:
    def __init__(__self__, *,
                 rows: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        if rows is not None:
            pulumi.set(__self__, "rows", rows)

    @property
    @pulumi.getter
    def rows(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        return pulumi.get(self, "rows")

    @rows.setter
    def rows(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "rows", value)


@pulumi.input_type
class IAppVariableArgs:
    def __init__(__self__, *,
                 encrypted: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 value: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] name: Name of the iApp.
        """
        if encrypted is not None:
            pulumi.set(__self__, "encrypted", encrypted)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if value is not None:
            pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def encrypted(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "encrypted")

    @encrypted.setter
    def encrypted(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "encrypted", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the iApp.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def value(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "value")

    @value.setter
    def value(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "value", value)


