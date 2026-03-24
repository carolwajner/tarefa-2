import os
import glob
import zipfile
import pandas as pd
import numpy as np
from FeatureExtractor import FeatureExtractor
from VideoCaptureYUV import VideoCaptureYUV
from DatasetManager import DatasetManager
from CTUAnalyzer import CTUAnalyzer

class TracefileProcessor:   
    def __init__(self, video_folder, configs, frame_mapping):
        self.video_folder = video_folder
        self.configs = configs
        self.frame_mapping = frame_mapping
        self.ctu_analyzer = CTUAnalyzer()
        self.db_manager = DatasetManager()
        self.frame_buffer = {}
        

    def process_all(self, path):
        zip_files = glob.glob(os.path.join(path, "*.zip"))
    
        for zip_path in zip_files:
            print(f"Opening: {os.path.basename(zip_path)}")
            with zipfile.ZipFile(zip_path, 'r') as z:
                for filename in z.namelist():
                    if filename.endswith('.csv'):
                        self.ctu_analyzer.cleanup()  
                        self._process_tracefile(z, filename)
            
        self.db_manager.create_zip()


    def _process_tracefile(self, zip_file, filename):
        with zip_file.open(filename) as f:
            # tracefile format
            cols = ['type', 'frame', 'x', 'y', 'w', 'h', 'parameter', 'v1', 'v2', 'v3', 'v4', 'v5', 'v6']
            df_trace = pd.read_csv(f, sep=';', comment='#', header=None, names=cols, index_col=False, engine='python')
                        
            df_trace = df_trace.rename(columns={'v1': 'value'})
            mask_vetor = df_trace['v2'].notna()
                        
            df_y = df_trace[mask_vetor].copy()
            df_y['parameter'] = df_y['parameter'] + '_Y'
            df_y['value'] = df_y['v2']
                    
            df_trace.loc[mask_vetor, 'parameter'] = df_trace.loc[mask_vetor, 'parameter'] + '_X'

            # removes null columns            
            df_final = pd.concat([df_trace, df_y], ignore_index=True).drop(columns=['v2', 'v3', 'v4', 'v5', 'v6'])
                        
            # pivots the dataframe to have parameters as columns and their corresponding values            
            df_pivoted = df_final.pivot_table(
                index=['frame', 'x', 'y', 'w', 'h'], 
                columns='parameter', 
                values='value', 
                aggfunc='first'
            ).reset_index()

            video_key = filename.split('_')[0]
            qp = filename.split('_')[1]

            self._extract_video_data(video_key, qp, df_pivoted)


    def _extract_video_data(self, video_key, qp, df_pivoted):
        conf = self.configs[video_key]
        video_path = os.path.join(self.video_folder, conf['yuv'])
        inter = [0, 2]

        df_pivoted['ctu_x'] = (df_pivoted['x'] // 128) * 128
        df_pivoted['ctu_y'] = (df_pivoted['y'] // 128) * 128

        for _, row in df_pivoted.iterrows():
            if row.get("PredMode", None) in inter:
                mvl0_x = row['MVL0_X'] if pd.notna(row.get('MVL0_X')) else np.nan
                mvl0_y = row['MVL0_Y'] if pd.notna(row.get('MVL0_Y')) else np.nan
                mvdl0_x = row['MVDL0_X'] if pd.notna(row.get('MVDL0_X')) else np.nan
                mvdl0_y = row['MVDL0_Y'] if pd.notna(row.get('MVDL0_Y')) else np.nan
                
                mvl1_x = row['MVL1_X'] if pd.notna(row.get('MVL1_X')) else np.nan
                mvl1_y = row['MVL1_Y'] if pd.notna(row.get('MVL1_Y')) else np.nan
                mvdl1_x = row['MVDL1_X'] if pd.notna(row.get('MVDL1_X')) else np.nan
                mvdl1_y = row['MVDL1_Y'] if pd.notna(row.get('MVDL1_Y')) else np.nan

                self.ctu_analyzer.add_data(
                    frame=int(row['frame']),
                    ctu_x=row['ctu_x'],
                    ctu_y=row['ctu_y'],
                    mv_l0_x=mvl0_x,
                    mv_l0_y=mvl0_y,
                    mvd_l0_x=mvdl0_x,
                    mvd_l0_y=mvdl0_y,
                    mv_l1_x=mvl1_x,
                    mv_l1_y=mvl1_y,
                    mvd_l1_x=mvdl1_x,
                    mvd_l1_y=mvdl1_y
                )

        self.ctu_analyzer.calculate_statistics()

        df_inter = df_pivoted[df_pivoted['PredMode'].isin(inter)].copy()
        df_inter = df_inter.sort_values(by='frame')

        cap = VideoCaptureYUV(video_path, conf['res'], conf['bit_depth'])
        current_frame_idx = -1
        data = []

        for _, row in df_inter.iterrows():
            frame_num = int(row['frame'])
            mapping = self.frame_mapping.get(frame_num, {"ref_frame": None, "level": 5})
            ref_id = mapping.get("ref_frame")
            frame_level = mapping.get("level")

            target_frames = [f for f in [frame_num, ref_id] if f is not None]
            max_needed = max(target_frames) if target_frames else frame_num

            while current_frame_idx < max_needed:
                pixels, _, _ = cap.read_frame()
                current_frame_idx += 1
                if pixels is not None:
                    self.frame_buffer[current_frame_idx] = pixels

            frame_pixels = self.frame_buffer.get(frame_num)
            ref_pixels = self.frame_buffer.get(ref_id) 

            if frame_pixels is not None:
                base_info = FeatureExtractor().compute_features(
                    video_key=video_key,
                    cu=row,
                    frame=frame_pixels,
                    ref_frame=ref_pixels,
                    ctu_analyzer=self.ctu_analyzer,
                    ctu_x=row['ctu_x'],
                    ctu_y=row['ctu_y'],
                    frame_level=frame_level,
                    conf=conf,
                    target_qp=qp                  
                )
                data.append(base_info)

        cap.close()
        self.frame_buffer.clear() 
        self.db_manager.save_data(data)