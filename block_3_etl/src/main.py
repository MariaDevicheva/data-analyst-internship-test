from extract import extract_data
from load import load_to_sqlite
from transform import transform_data


def main() -> None:
    raw_data = extract_data()
    clean_data = transform_data(raw_data)

    load_to_sqlite(clean_data)

    for table_name, df in clean_data.items():
        print(f"{table_name}: {len(df)} rows")


if __name__ == "__main__":
    main()