#!/usr/bin/env python3
# @generated AUTOGENERATED file. Do not Change!

from dataclasses import dataclass, field as _field
from ...config import custom_scalars, datetime
from gql_client.runtime.variables import encode_variables
from gql import gql, Client
from gql.transport.exceptions import TransportQueryError
from functools import partial
from numbers import Number
from typing import Any, AsyncGenerator, Dict, List, Generator, Optional
from time import perf_counter
from dataclasses_json import DataClassJsonMixin, config

from ..input.edit_comparator_input import EditComparatorInput


# fmt: off
QUERY: List[str] = ["""
mutation editComparator($input: EditComparatorInput!) {
  editComparator(input: $input) {
    id
    name
  }
}
"""
]


class editComparator:
    @dataclass(frozen=True)
    class editComparatorData(DataClassJsonMixin):
        @dataclass(frozen=True)
        class Comparator(DataClassJsonMixin):
            id: str
            name: str

        editComparator: Comparator

    # fmt: off
    @classmethod
    def execute(cls, client: Client, input: EditComparatorInput) -> editComparatorData.Comparator:
        variables: Dict[str, Any] = {"input": input}
        new_variables = encode_variables(variables, custom_scalars)
        response_text = client.execute(
            gql("".join(set(QUERY))), variable_values=new_variables
        )
        res = cls.editComparatorData.from_dict(response_text)
        return res.editComparator

    # fmt: off
    @classmethod
    async def execute_async(cls, client: Client, input: EditComparatorInput) -> editComparatorData.Comparator:
        variables: Dict[str, Any] = {"input": input}
        new_variables = encode_variables(variables, custom_scalars)
        response_text = await client.execute_async(
            gql("".join(set(QUERY))), variable_values=new_variables
        )
        res = cls.editComparatorData.from_dict(response_text)
        return res.editComparator
