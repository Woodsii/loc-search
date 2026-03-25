import os
from sqlalchemy import create_engine

CSV_DIR = '/var/tmp/csvs'

TABLES = [
    ('books', 'id, author, title, title_remainder'),
    ('identifiers', 'book_id, number'),
    ('publications', 'book_id, place, name, date'),
    ('series', 'book_id, name, volume'),
    ('subjects', 'book_id, heading, subheading, form, general, chron, geo'),
]

if __name__ == '__main__':
    url = os.environ.get('LOCDB_URL', 'postgresql:///locdb')
    engine = create_engine(url)

    all_csvs = sorted(os.listdir(CSV_DIR))

    with engine.connect() as conn:
        raw = conn.connection.dbapi_connection
        cursor = raw.cursor()

        for table, columns in TABLES:
            csv_files = [f for f in all_csvs if f'.{table}.' in f]
            for filename in csv_files:
                path = os.path.join(CSV_DIR, filename)
                print(f'{filename} -> {table}')
                with open(path, 'r') as f:
                    cursor.copy_expert(f'COPY {table} ({columns}) FROM STDIN WITH (FORMAT csv)', f)
            raw.commit()

    print('Done')