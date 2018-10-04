from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python_operator import PythonOperator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import requests

from io import StringIO

import pandas as pd


USERNAME = 'python-demo'
PASSWORD = 'claw30_bumps'

DATABASE_URI = 'postgresql+psycopg2://sandervandenoord:''@localhost/hotel_viewer'

CITY_URI = 'http://rachel.maykinmedia.nl/djangocase/city.csv'
HOTEL_URI = 'http://rachel.maykinmedia.nl/djangocase/hotel.csv'


def get_df_from_maykin_csv(uri, username, password):
    resp = requests.get(uri, auth=(username, password))
    print(uri, resp.status_code)
    df = pd.read_csv(
        StringIO(resp.text), 
        sep=';',
        header=None,
    )
    return df

def create_session_for_writing_to_db(database_uri):
    engine = create_engine(database_uri, encoding='utf-8')
    Session = sessionmaker(bind=engine)
    return Session()

def remove_existing_data_from_locations_db(session):
    session.execute("""TRUNCATE public.locations_city CASCADE;""")
    session.commit()
    session.execute("""TRUNCATE public.locations_hotel CASCADE;""")
    session.commit()

def df_to_database(engine, df, schema, table_name, sep='\x01', encoding='utf-8'):

    # Prepare data
    output = StringIO()
    df.to_csv(output, sep=sep, header=False, encoding=encoding, index=False)
    output.seek(0)

    # Insert data
    connection = engine.raw_connection()
    cursor = connection.cursor()
    schema_tablename = '{}.{}'.format(schema, table_name)
    cursor.copy_from(output, schema_tablename, sep=sep, null='')
    connection.commit()
    cursor.close()

def get_csv_and_write_to_db():
    df_city = get_df_from_maykin_csv(CITY_URI, USERNAME, PASSWORD)
    print('success getting cities csv')

    df_hotel = get_df_from_maykin_csv(HOTEL_URI, USERNAME, PASSWORD)
    print('success getting hotels csv')
    
    session = create_session_for_writing_to_db(DATABASE_URI)
    print('success creating a connection to postgres')

    remove_existing_data_from_locations_db(session)
    print('succes truncating table city and table hotel')

    df_to_database(
        engine=session.bind,
        df=df_city,
        schema='public',
        table_name='locations_city',
    )
    print('success writing city to table')

    df_to_database(
        engine=session.bind,
        df=df_hotel,
        schema='public',
        table_name='locations_hotel',
    )

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2018, 10, 1),
    'email': ['example@hotmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=30),
}

dag = DAG(
    'locations_import', 
    default_args=default_args,
    schedule_interval='1 5 1 * *',
)

refresh_locations = PythonOperator(
    dag=dag,
    task_id='refresh_locations',
    python_callable=get_csv_and_write_to_db,
    execution_timeout=timedelta(minutes=30),
)