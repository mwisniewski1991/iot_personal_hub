from airflow.decorators import dag, task
from datetime import datetime
from airflow.providers.postgres.hooks.postgres import PostgresHook
import jinja2

@dag(
    dag_id='agg_hourly_devices_smartphone_location_details_PROD',
    description='Agregacja godzinowa danych lokalizacji urządzeń',
    start_date=datetime(2025, 8, 21),
    schedule='0 * * * *',
    catchup=False,
    max_active_runs=3,
    tags=['iot_personal_hub','PROD'],
    default_args={
        'owner': 'mateuszwisniewski',
    }
)
def dag_definition(**context):
    """DAG do agregacji godzinowej danych lokalizacji urządzeń"""
    
    # Task 1: Agregacja danych
    @task(task_id='agg_hourly_devices_smartphone_location_details')
    def agg_hourly_devices_smartphone_location_details(**context):
        """Agreguje dane lokalizacji urządzeń"""
        hook = PostgresHook(postgres_conn_id='mikrus_postgres_PROD_iot_writer')
        
        # Odczytaj SQL z pliku
        sql = jinja2.Template(
            open('queries/iot_personal_hub/agg_hourly_devices_smartphone_location_details_INSERT.sql', 'r').read()
        )
        sql = sql.render(data_interval_start=context['data_interval_start'], data_interval_end=context['data_interval_end'])
        print(context['data_interval_start'])
        print(context['data_interval_end'])
        # Wykonaj zapytanie z parametrem timestamp
        hook.run(sql)
    
    agg_hourly_devices_smartphone_location_details()
    # validate_data = validate_data_quality()

dag_definition()