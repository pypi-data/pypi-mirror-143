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

from ..input.add_kpi_input import AddKpiInput


# fmt: off
QUERY: List[str] = ["""
mutation addKpi($input: AddKpiInput!) {
  addKpi(input: $input) {
    id
    name
    description
    status
    domainFk{id}
    kpiCategoryFK{id}
  }
}
"""
]


class addKpi:
    @dataclass(frozen=True)
    class addKpiData(DataClassJsonMixin):
        @dataclass(frozen=True)
        class Kpi(DataClassJsonMixin):
            @dataclass(frozen=True)
            class Domain(DataClassJsonMixin):
                id: str

            @dataclass(frozen=True)
            class KpiCategory(DataClassJsonMixin):
                id: str

            id: str
            name: str
            description: str
            status: bool
            domainFk: Domain
            kpiCategoryFK: KpiCategory

        addKpi: Kpi

    # fmt: off
    @classmethod
    def execute(cls, client: Client, input: AddKpiInput) -> addKpiData.Kpi:
        variables: Dict[str, Any] = {"input": input}
        new_variables = encode_variables(variables, custom_scalars)
        response_text = client.execute(
            gql("".join(set(QUERY))), variable_values=new_variables
        )
        res = cls.addKpiData.from_dict(response_text)
        return res.addKpi

    # fmt: off
    @classmethod
    async def execute_async(cls, client: Client, input: AddKpiInput) -> addKpiData.Kpi:
        variables: Dict[str, Any] = {"input": input}
        new_variables = encode_variables(variables, custom_scalars)
        response_text = await client.execute_async(
            gql("".join(set(QUERY))), variable_values=new_variables
        )
        res = cls.addKpiData.from_dict(response_text)
        return res.addKpi
