from app.postgres.engine import engine
# ---------------------------
import pandas as pd
from sqlalchemy import text

class Bronze:
    def __init__(self):
        self.engine = engine

    def extract(sql_query: str):
        with engine.begin() as conn:
            data = conn.execute(
            text(sql_query)
            )
        return data.fetchall()

    def to_df(data):
        if_not = 'NO DATA'
        if not data:
            return pd.DataFrame(
            [if_not], columns=['ERROR: def to_df']
            )
        return pd.DataFrame(data)

