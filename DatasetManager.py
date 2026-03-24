import os
import pandas as pd
import gzip
import zipfile
import shutil

class DatasetManager:
    def __init__(self, inter_filename='inter-dataset.csv.gz'):
        self.inter_path = inter_filename

    def save_data(self, data):
        if data:
            self._append_to_gz(data, self.inter_path)

    def _append_to_gz(self, data_list, path):
        df = pd.DataFrame(data_list)
        file_exists = os.path.exists(path)
        with gzip.open(path, 'at', encoding='utf-8', newline='') as f:
            df.to_csv(f, mode='a', index=False, header=not file_exists)

    def create_zip(self, zip_name='datasets_final.zip'):
        with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as z:
            for gz_path in [self.inter_path]:
                if os.path.exists(gz_path):
                    csv_inside_zip = gz_path.replace('.gz', '')
                    
                    with gzip.open(gz_path, 'rb') as f_in:
                        with z.open(csv_inside_zip, 'w') as f_out:
                            shutil.copyfileobj(f_in, f_out)
                    
                    os.remove(gz_path)
        
        print(f"{zip_name} saved.")