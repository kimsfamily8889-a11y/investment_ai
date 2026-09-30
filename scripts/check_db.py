"""Verify the local PostgreSQL connection without creating permanent tables."""
from decimal import Decimal
from pathlib import Path

from dotenv import dotenv_values
from sqlalchemy import URL, create_engine, text


def main() -> None:
    config = dotenv_values(Path(__file__).resolve().parents[1] / '.env')
    required = ('PGHOST', 'PGPORT', 'PGDATABASE', 'PGUSER', 'PGPASSWORD')
    if any(not config.get(key) for key in required):
        raise SystemExit('Missing database settings. Configure the local .env file.')
    url = URL.create(
        'postgresql+psycopg', username=config['PGUSER'],
        password=config['PGPASSWORD'], host=config['PGHOST'],
        port=int(config['PGPORT']), database=config['PGDATABASE'],
    )
    engine = create_engine(url, connect_args={'connect_timeout': 5})
    try:
        with engine.connect() as connection:
            info = connection.execute(text(
                'SELECT current_database(), current_user, version()'
            )).one()
            print(f'Database: {info[0]} | User: {info[1]}')
            print(info[2])
            # A temporary table checks write access, Korean text and exact decimals.
            connection.execute(text(
                'CREATE TEMP TABLE connection_probe '
                '(label text, amount numeric(18,4)) ON COMMIT DROP'
            ))
            connection.execute(text(
                'INSERT INTO connection_probe VALUES (:label, :amount)'
            ), {'label': '\ud55c\uad6d ETF', 'amount': Decimal('1234.5678')})
            row = connection.execute(text(
                'SELECT label, amount FROM connection_probe'
            )).one()
            if row != ('\ud55c\uad6d ETF', Decimal('1234.5678')):
                raise RuntimeError('Data round-trip mismatch.')
            connection.rollback()
            print('PASS: connection, temporary write, Korean text, exact decimal, rollback.')
    finally:
        engine.dispose()


if __name__ == '__main__':
    main()
