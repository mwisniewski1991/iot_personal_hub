from airflow.decorators import dag, task
from datetime import datetime
from airflow.providers.postgres.hooks.postgres import PostgresHook
import jinja2

@dag(
    dag_id='agg_hourly_devices_smartphone_battery_details_PROD',
    description='Agregacja godzinowa danych baterii',
    start_date=datetime(2025, 8, 21),
    schedule='0 * * * *',
    catchup=False,
    max_active_runs=3,
    tags=['iot_personal_hub','PROD'],
    default_args={
        'owner': 'mateuszwisniewski',
    }
)
def battery_hourly_aggregation(**context):
    """DAG do agregacji godzinowej danych baterii"""
    
    # Task 1: Agregacja danych
    @task(task_id='aggregate_battery_data')
    def aggregate_battery_data(**context):
        """Agreguje dane baterii"""
        hook = PostgresHook(postgres_conn_id='mikrus_postgres_PROD_iot_writer')
        
        # Odczytaj SQL z pliku
        sql = jinja2.Template(
            open('queries/iot_personal_hub/IPH_agg_hourly_battery_details_INSERT.sql', 'r').read()
        )
        sql = sql.render(data_interval_start=context['data_interval_start'], data_interval_end=context['data_interval_end'])
        print(context['data_interval_start'])
        print(context['data_interval_end'])
        # Wykonaj zapytanie z parametrem timestamp
        hook.run(sql)
    
    aggregate_data = aggregate_battery_data()
    # validate_data = validate_data_quality()

battery_hourly_aggregation()