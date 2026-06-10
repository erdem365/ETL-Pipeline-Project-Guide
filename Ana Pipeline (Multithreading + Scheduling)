# src/main.py
import yaml
import schedule
import time
import threading
from extract import extract_all
from transform import transform_pipeline
from load import load_to_sqlite
from utils import setup_logging

def run_etl():
    logger = setup_logging()
    logger.info("ETL Pipeline başlıyor...")
    try:
        with open("config/config.yaml", 'r') as f:
            config = yaml.safe_load(f)
        
        # Extract
        raw_data = extract_all(config)
        
        # Transform
        transformed_df = transform_pipeline(raw_data, config)
        
        # Load
        load_to_sqlite(transformed_df, config)
        
        logger.info("ETL Pipeline başarıyla tamamlandı.")
    except Exception as e:
        logger.exception(f"Pipeline hatası: {e}")

def schedule_etl(interval_seconds):
    """Zamanlayıcı fonksiyonu (ayrı bir thread'de çalışır)"""
    schedule.every(interval_seconds).seconds.do(run_etl)
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    with open("config/config.yaml", 'r') as f:
        config = yaml.safe_load(f)
    
    # İlk çalıştırma
    run_etl()
    
    # Eğer scheduling aktifse
    if config['scheduling']['interval_seconds'] > 0:
        scheduler_thread = threading.Thread(
            target=schedule_etl,
            args=(config['scheduling']['interval_seconds'],),
            daemon=True
        )
        scheduler_thread.start()
        print("Zamanlayıcı başladı. Ctrl+C ile durdurun.")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("Pipeline durduruldu.")
