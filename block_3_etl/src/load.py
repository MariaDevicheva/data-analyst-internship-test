from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine


DB_PATH = Path("music_analytics.db")


def load_to_sqlite(clean_data: dict[str, pd.DataFrame]) -> None:
    engine = create_engine(f"sqlite:///{DB_PATH}")

    for table_name, df in clean_data.items():
        df.to_sql(
            name=table_name,
            con=engine,
            if_exists="replace",
            index=False,
        )

    print(f"Data loaded to {DB_PATH}")