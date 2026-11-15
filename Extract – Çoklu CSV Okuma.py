# src/extract.py
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import logging

def read_csv(file_path, encoding='utf-8'):
    """Bir CSV dosyasını okur ve DataFrame döndürür."""
    try:
        df = pd.read_csv(file_path, encoding=encoding)
        logging.info(f"Okundu: {file_path} -> {df.shape}")
        return file_path.stem, df   # dosya adı (stem) anahtar olarak
    except Exception as e:
        logging.error(f"Hata okurken {file_path}: {e}")
        return None, None

def extract_all(config):
    paths = config['input']['paths']
    encoding = config['input']['encoding']
    results = {}
    
    with ThreadPoolExecutor(max_workers=4) as executor:
        future_to_file = {executor.submit(read_csv, Path(p), encoding): p for p in paths}
        for future in as_completed(future_to_file):
            key, df = future.result()
            if key:
                results[key] = df
    logging.info(f"Extract tamamlandı. {len(results)} dosya okundu.")
    return results  # dict: {'customers': df_customers, 'orders': df_orders, ...}
