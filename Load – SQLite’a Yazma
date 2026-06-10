# src/load.py
import sqlite3
import logging

def load_to_sqlite(df, config):
    db_path = config['output']['database_path']
    table_name = config['output']['table_name']
    if_exists = config['output']['if_exists']
    
    with sqlite3.connect(db_path) as conn:
        df.to_sql(table_name, conn, if_exists=if_exists, index=False)
    logging.info(f"Veri yüklendi: {db_path} -> {table_name}, satır: {len(df)}")
