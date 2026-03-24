import numpy as np

class CTUAnalyzer:
    def __init__(self):
        self.ctu_statistics = {}

    def _init_ctu_entry(self, frame_id, ctu_x, ctu_y):
        if frame_id not in self.ctu_statistics:
            self.ctu_statistics[frame_id] = {}
            
        ctu_key = (ctu_x, ctu_y) 
        if ctu_key not in self.ctu_statistics[frame_id]:
            self.ctu_statistics[frame_id][ctu_key] = {
                'mv_sizes': [],
                'mvd_sizes': [],
                'results': {
                    'mv_min': 0, 'mv_max': 0, 'mv_avg': 0, 'mv_std': 0,
                    'mvd_min': 0, 'mvd_max': 0, 'mvd_avg': 0, 'mvd_std': 0
                }
            }
    

    def add_data(self, frame, ctu_x, ctu_y, 
                 mv_l0_x=np.nan, mv_l0_y=np.nan, mvd_l0_x=np.nan, mvd_l0_y=np.nan,
                 mv_l1_x=np.nan, mv_l1_y=np.nan, mvd_l1_x=np.nan, mvd_l1_y=np.nan):
        
        self._init_ctu_entry(frame, ctu_x, ctu_y)
        
        size_l0 = (mv_l0_x**2 + mv_l0_y**2) ** 0.5 if not np.isnan(mv_l0_x) else np.nan
        size_mvd_l0 = (mvd_l0_x**2 + mvd_l0_y**2) ** 0.5 if not np.isnan(mvd_l0_x) else np.nan
        
        size_l1 = (mv_l1_x**2 + mv_l1_y**2) ** 0.5 if not np.isnan(mv_l1_x) else np.nan
        size_mvd_l1 = (mvd_l1_x**2 + mvd_l1_y**2) ** 0.5 if not np.isnan(mvd_l1_x) else np.nan
        
        valid_mv_sizes = [s for s in (size_l0, size_l1) if not np.isnan(s)]
        valid_mvd_sizes = [s for s in (size_mvd_l0, size_mvd_l1) if not np.isnan(s)]
        
        if valid_mv_sizes:
            self.ctu_statistics[frame][(ctu_x, ctu_y)]['mv_sizes'].append(max(valid_mv_sizes))
            
        if valid_mvd_sizes:
            self.ctu_statistics[frame][(ctu_x, ctu_y)]['mvd_sizes'].append(max(valid_mvd_sizes))


    def calculate_statistics(self):
        for frame_id, ctus in self.ctu_statistics.items():
            for ctu_key, data in ctus.items():
                mv_sizes = data['mv_sizes']
                mvd_sizes = data['mvd_sizes']
                
                if mv_sizes:
                    data['results']['mv_min'] = np.min(mv_sizes)
                    data['results']['mv_max'] = np.max(mv_sizes)
                    data['results']['mv_avg'] = np.mean(mv_sizes)
                    data['results']['mv_std'] = np.std(mv_sizes)
                
                if mvd_sizes:
                    data['results']['mvd_min'] = np.min(mvd_sizes)
                    data['results']['mvd_max'] = np.max(mvd_sizes)
                    data['results']['mvd_avg'] = np.mean(mvd_sizes)
                    data['results']['mvd_std'] = np.std(mvd_sizes)
    
    def get_ctu_statistics(self, frame_id, ctu_x, ctu_y):
        if frame_id not in self.ctu_statistics or (ctu_x, ctu_y) not in self.ctu_statistics[frame_id]:
            return {
                'mv_min': np.nan, 'mv_max': np.nan, 'mv_avg': np.nan, 'mv_std': np.nan,
                'mvd_min': np.nan, 'mvd_max': np.nan, 'mvd_avg': np.nan, 'mvd_std': np.nan
            }
        
        results = self.ctu_statistics[frame_id][(ctu_x, ctu_y)]['results']
        if results['mv_max'] == 0 and results['mv_min'] == 0 and not self.ctu_statistics[frame_id][(ctu_x, ctu_y)]['mv_sizes']:
             return {
                'mv_min': np.nan, 'mv_max': np.nan, 'mv_avg': np.nan, 'mv_std': np.nan,
                'mvd_min': np.nan, 'mvd_max': np.nan, 'mvd_avg': np.nan, 'mvd_std': np.nan
            }

        return results
    
    def cleanup(self):
        self.ctu_statistics = {}