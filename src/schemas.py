from pydantic import BaseModel
from pydantic import Field
from enum import Enum

class DatasetField(BaseModel):
    field: str = Field(description="name of the field")
    field_category: str = Field(description="category of the field")
    field_description: str = Field(description="description of the field")

class Dataset(BaseModel):
    fields: list[DatasetField] = Field(description="the fields of the dataset")

class AnalyticsMethod(Enum):
    describe_volume_metric_evolution = "describe_volume_metric_evolution"
    describe_ratio_metric_evolution = "describe_ratio_metric_evolution"
    explain_volume_metric_evolution = "explain_volume_metric_evolution"
    explain_ratio_metric_evolution = "explain_ratio_metric_evolution"

class ListAnalyticsMethods(BaseModel):
    analytics_methods: list[AnalyticsMethod]

