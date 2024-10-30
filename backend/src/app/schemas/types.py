from pydantic import StringConstraints
from pydantic import GetCoreSchemaHandler, GetJsonSchemaHandler
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import core_schema

from typing import Any



class ID(int):
    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        _source: type[Any],
        handler: GetCoreSchemaHandler,
    ) -> core_schema.CoreSchema:
        return core_schema.no_info_after_validator_function(
            cls._validate, core_schema.int_schema()
        )

    @classmethod
    def __get_pydantic_json_schema__(
        cls, core_schema: core_schema.CoreSchema, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        field_schema = handler(core_schema)
        field_schema.update(type="integer", format="uuid")
        return field_schema

    @classmethod
    def _validate(cls, input_value: int, /) -> int:
        if input_value < 0:
            raise ValueError("Negative value")
        return int(input_value)


class Email(StringConstraints):
    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        _source: type[Any],
        handler: GetCoreSchemaHandler,
    ) -> core_schema.CoreSchema:
        return core_schema.no_info_after_validator_function(
            cls._validate, core_schema.str_schema()
        )

    @classmethod
    def __get_pydantic_json_schema__(
        cls, core_schema: core_schema.CoreSchema, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        field_schema = handler(core_schema)
        field_schema.update(type="string")
        return field_schema

    @classmethod
    def _validate(cls, input_value: str, /) -> str:
        if not input_value:
            raise ValueError("Email cannot be empty")
        return input_value


class Str_20(str):
    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        _source: type[Any],
        handler: GetCoreSchemaHandler,
    ) -> core_schema.CoreSchema:
        return core_schema.no_info_after_validator_function(
            cls._validate, core_schema.str_schema()
        )

    @classmethod
    def __get_pydantic_json_schema__(
        cls, core_schema: core_schema.CoreSchema, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        field_schema = handler(core_schema)
        field_schema.update(type="string", maxLength=20)
        return field_schema

    @classmethod
    def _validate(cls, input_value: str, /) -> str:
        if len(input_value) > 20:
            raise ValueError("String length must not exceed 20 characters")
        return input_value


class Str_256(str):
    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        _source: type[Any],
        handler: GetCoreSchemaHandler,
    ) -> core_schema.CoreSchema:
        return core_schema.no_info_after_validator_function(
            cls._validate, core_schema.str_schema()
        )

    @classmethod
    def __get_pydantic_json_schema__(
        cls, core_schema: core_schema.CoreSchema, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        field_schema = handler(core_schema)
        field_schema.update(type="string", maxLength=256)
        return field_schema

    @classmethod
    def _validate(cls, input_value: str, /) -> str:
        if len(input_value) > 256:
            raise ValueError("String length must not exceed 20 characters")
        return input_value
