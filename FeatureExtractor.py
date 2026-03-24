from VideoAnalyzer import VideoAnalyzer
import pandas as pd

#TODO: excluir linhas sem vetor de movimento

class FeatureExtractor:
    def compute_features(self,
                        video_key, 
                        cu, 
                        frame, 
                        ref_frame, 
                        ctu_analyzer, 
                        ctu_x, ctu_y, 
                        frame_level, 
                        conf, 
                        target_qp
                        ):
        x, y, w, h = int(cu['x']), int(cu['y']), int(cu['w']), int(cu['h'])
        
        block_stats = VideoAnalyzer.calculate_block_stats(frame, x, y, w, h)
        block_diff_stats = VideoAnalyzer.calculate_block_diff_stats(frame, ref_frame, x, y, w, h)

        mv_l0_x, mv_l0_y = cu.get('MVL0_X', 0), cu.get('MVL0_Y', 0)
        mv_l0_size = (mv_l0_x**2 + mv_l0_y**2) ** 0.5
        
        mv_l1_x, mv_l1_y = cu.get('MVL1_X', 0), cu.get('MVL1_Y', 0)
        mv_l1_size = (mv_l1_x**2 + mv_l1_y**2) ** 0.5

        max_mv_size = max(mv_l0_size, mv_l1_size)

        if pd.isna(max_mv_size):
            max_mv_size = 0

        left_x, top_y = ctu_x - 128, ctu_y - 128 

        ref_ctu_stats = ctu_analyzer.get_ctu_statistics(frame_id=cu['frame'], ctu_x=ctu_x, ctu_y=ctu_y)
        left_ctu_stats = ctu_analyzer.get_ctu_statistics(frame_id=cu['frame'], ctu_x=left_x, ctu_y=ctu_y)
        top_ctu_stats = ctu_analyzer.get_ctu_statistics(frame_id=cu['frame'], ctu_x=ctu_x, ctu_y=top_y)

        return {
            'video': video_key,
            'target_qp': target_qp,
            'frame_num': int(cu['frame']),
            'frame_width': conf['res'][0],
            'frame_height': conf['res'][1],
            'bit_depth': conf['bit_depth'],
            'blk_x_pos': x, 
            'blk_y_pos': y, 
            'blk_width': w, 
            'blk_height': h,
            'blk_area': w * h,
            'frame_level': frame_level,
            'cu_qp': cu.get('QP', None),
            'blk_pixel_mean': block_stats['mean'],
            'blk_pixel_variance': block_stats['variance'],
            'blk_pixel_std_dev': block_stats['std_dev'],
            'blk_pixel_sum': block_stats['sum'],
            'diff_blk_pixel_mean': block_diff_stats['mean'],
            'diff_blk_pixel_variance': block_diff_stats['variance'],
            'diff_blk_pixel_std_dev': block_diff_stats['std_dev'],
            'diff_blk_pixel_sum': block_diff_stats['sum'],
            'mv_min_size_ctu_left': left_ctu_stats['mv_min'],
            'mv_max_size_ctu_left': left_ctu_stats['mv_max'],
            'mv_avg_size_ctu_left': left_ctu_stats['mv_avg'],
            'mv_std_size_ctu_left': left_ctu_stats['mv_std'],
            'mv_min_size_ctu_top': top_ctu_stats['mv_min'],
            'mv_max_size_ctu_top': top_ctu_stats['mv_max'],
            'mv_avg_size_ctu_top': top_ctu_stats['mv_avg'],
            'mv_std_size_ctu_top': top_ctu_stats['mv_std'],
            'mv_min_size_ctu_ref': ref_ctu_stats['mv_min'],
            'mv_max_size_ctu_ref': ref_ctu_stats['mv_max'],
            'mv_avg_size_ctu_ref': ref_ctu_stats['mv_avg'],
            'mv_std_size_ctu_ref': ref_ctu_stats['mv_std'],
            'mvd_min_size_ctu_left': left_ctu_stats['mvd_min'],
            'mvd_max_size_ctu_left': left_ctu_stats['mvd_max'],
            'mvd_avg_size_ctu_left': left_ctu_stats['mvd_avg'],
            'mvd_std_size_ctu_left': left_ctu_stats['mvd_std'],
            'mvd_min_size_ctu_top': top_ctu_stats['mvd_min'],
            'mvd_max_size_ctu_top': top_ctu_stats['mvd_max'],
            'mvd_avg_size_ctu_top': top_ctu_stats['mvd_avg'],
            'mvd_std_size_ctu_top': top_ctu_stats['mvd_std'],
            'mvd_min_size_ctu_ref': ref_ctu_stats['mvd_min'],
            'mvd_max_size_ctu_ref': ref_ctu_stats['mvd_max'],
            'mvd_avg_size_ctu_ref': ref_ctu_stats['mvd_avg'],
            'mvd_std_size_ctu_ref': ref_ctu_stats['mvd_std'],
            'is_within_sr_4': max_mv_size < 4,
            'is_within_sr_8': max_mv_size < 8,
            'is_within_sr_16': max_mv_size < 16,
            'is_within_sr_32': max_mv_size < 32,
            'is_within_sr_64': max_mv_size < 64,
            'is_within_sr_96': max_mv_size < 96,
            'is_within_sr_128': max_mv_size < 128
        }           