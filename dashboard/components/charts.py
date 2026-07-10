import plotly.express as px
import pandas as pd


def sales_trend_chart(df: pd.DataFrame) -> px.line:
    fig = px.line(df, x="sale_date", y="qty_sold", title="Daily Sales Trend")
    return fig
