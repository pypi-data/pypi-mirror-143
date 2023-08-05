#!/usr/bin/env python3
# @generated AUTOGENERATED file. Do not Change!

from dataclasses import dataclass, field as _field
from functools import partial
from ...config import custom_scalars, datetime
from numbers import Number
from typing import Any, AsyncGenerator, Dict, List, Generator, Optional

from dataclasses_json import DataClassJsonMixin, config

from gql_client.runtime.enum_utils import enum_field_metadata
from ..enum.filter_operator import FilterOperator
from ..enum.recommendations_sources_filter_type import RecommendationsSourcesFilterType


@dataclass(frozen=True)
class RecommendationsSourcesFilterInput(DataClassJsonMixin):
    filterType: RecommendationsSourcesFilterType = _field(metadata=enum_field_metadata(RecommendationsSourcesFilterType))
    operator: FilterOperator = _field(metadata=enum_field_metadata(FilterOperator))
    idSet: List[str]
    stringSet: List[str]
    stringValue: Optional[str] = None
    maxDepth: Optional[int] = None
