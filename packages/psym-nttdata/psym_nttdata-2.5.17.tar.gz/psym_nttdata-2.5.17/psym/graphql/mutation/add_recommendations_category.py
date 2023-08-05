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

from ..input.add_recommendations_category_input import AddRecommendationsCategoryInput


# fmt: off
QUERY: List[str] = ["""
mutation addRecommendationsCategory($input: AddRecommendationsCategoryInput!) {
  addRecommendationsCategory(input: $input) {
    id
    name
  }
}

"""
]


class addRecommendationsCategory:
    @dataclass(frozen=True)
    class addRecommendationsCategoryData(DataClassJsonMixin):
        @dataclass(frozen=True)
        class RecommendationsCategory(DataClassJsonMixin):
            id: str
            name: str

        addRecommendationsCategory: RecommendationsCategory

    # fmt: off
    @classmethod
    def execute(cls, client: Client, input: AddRecommendationsCategoryInput) -> addRecommendationsCategoryData.RecommendationsCategory:
        variables: Dict[str, Any] = {"input": input}
        new_variables = encode_variables(variables, custom_scalars)
        response_text = client.execute(
            gql("".join(set(QUERY))), variable_values=new_variables
        )
        res = cls.addRecommendationsCategoryData.from_dict(response_text)
        return res.addRecommendationsCategory

    # fmt: off
    @classmethod
    async def execute_async(cls, client: Client, input: AddRecommendationsCategoryInput) -> addRecommendationsCategoryData.RecommendationsCategory:
        variables: Dict[str, Any] = {"input": input}
        new_variables = encode_variables(variables, custom_scalars)
        response_text = await client.execute_async(
            gql("".join(set(QUERY))), variable_values=new_variables
        )
        res = cls.addRecommendationsCategoryData.from_dict(response_text)
        return res.addRecommendationsCategory
