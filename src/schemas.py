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

class SQLQuery(BaseModel):
    sql_query: str  = Field(description="A SQL query that follows the guideline. Do not start with ```sql, do not finish with ```")

class AnalyticsTaskOutput(BaseModel):
    findings: str = Field(description= "The findings of the analytical task")

class PythonCodeChart(BaseModel):
    chart_python_code: str = Field(description="Some Python code to plot a chart. Do not start with ```python, do not finish with ```")

class ExecSummary(BaseModel):
    exec_summary: str = Field(description="The executive summary in HTML format. Do not start with ```html, do not finish with ```")





