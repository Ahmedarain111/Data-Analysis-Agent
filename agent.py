import os
import duckdb
import pandas as pd
from pydantic_ai import Agent, RunContext
from typing import Dict, Any
from dataclasses import dataclass

os.environ["GOOGLE_API_KEY"] = "" # <-- API KEY HERE


@dataclass
class AgentDeps:
    df: pd.DataFrame
    path: str


agent = Agent(
    "google-gla:gemini-3.1-flash-lite-preview",
    deps_type=Dict[str, Any],
    system_prompt=(
    "You are a professional Data Analysis Assistant."
    "Your goal is to help users explore, clean, and transform datasets using SQL and Python."
    "1. For data exploration or answering questions, use the 'query_data' tool."
    "2. For any request that modifies the data (delete, update, rename, clean), you MUST use 'transform_and_save_data' tool. "
    "3. After using a transformation tool, always call 'summarize_dataset' to confirm the change to the user. "
    "4. All SQL queries must target the table name 'df'. "
    "5. If a SQL query fails, explain the error simply to the user and suggest a correction. "
    "6. You MUST format all data outputs using Markdown. Use bold headers for sections and tables for data previews. "
    "7. When displaying tables, only show the first 10 rows to keep the UI clean. "
    "8. Be concise, professional, and strictly data-driven. Do not speculate beyond what is in the dataset."
    "9. Don't mention the actual file name of the datast. When you have to refer to the dataset, use 'The dataset' or similar."
)
)


@agent.tool
async def summarize_dataset(ctx: RunContext[Dict[str, Any]]) -> dict:
    df = ctx.deps["df"]
    return {
        "filename": os.path.basename(ctx.deps["path"]),
        "rows": int(df.shape[0]),
        "columns": list(df.columns),
        "missing_values": int(df.isnull().sum().sum()),
        "dtypes": {k: str(v) for k, v in df.dtypes.to_dict().items()},
    }


@agent.tool
async def query_data(ctx: RunContext[Dict[str, Any]], sql_query: str) -> str:
    """Read-only SQL execution for analysis."""
    df = ctx.deps["df"]
    try:
        result = duckdb.query(sql_query).to_df()
        if result.empty:
            return "The query returned no results."
        preview = result.head(10).to_markdown(index=False)
        return f"Found {len(result)} rows. Showing top 10:\n\n{preview}"
    except Exception as e:
        return f"Error executing SQL: {str(e)}"


@agent.tool
async def transform_and_save_data(
    ctx: RunContext[Dict[str, Any]], sql_transformation: str
) -> str:
    """
    Use this to MODIFY the data.
    Example: 'SELECT * EXCLUDE(unnamed_col) FROM df'
    """
    
    df_to_transform = ctx.deps["df"]
    path = ctx.deps["path"]

    try:
        con = duckdb.connect(database=":memory:")
        con.register("df", df_to_transform)

        new_df = con.execute(sql_transformation).df()

        ctx.deps["df"] = new_df


        if path.endswith(".csv"):
            new_df.to_csv(path, index=False)
        else:
            new_df.to_excel(path, index=False)

        return f"Success! Data transformed. New row count: {len(new_df)}. File updated."

    except Exception as e:
        return f"Transformation failed: {str(e)}"
