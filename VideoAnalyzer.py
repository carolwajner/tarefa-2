import numpy as np

class VideoAnalyzer:
    @staticmethod
    def calculate_block_stats(frame, x, y, w, h):
        target_blk = frame[y : (y + h), x : (x + w)]

        stats = {
            'mean': np.mean(target_blk),
            'variance': np.var(target_blk),
            'std_dev': np.std(target_blk),
            'sum': np.sum(target_blk)
        }

        return stats
    
    def calculate_block_diff_stats(current_frame, reference_frame, x, y, w, h):
        if reference_frame is None:
            return { 'mean': np.nan, 'variance': np.nan, 'std_dev': np.nan, 'sum': np.nan }

        curr_blk = current_frame[y : (y + h), x : (x + w)]
        ref_blk = reference_frame[y : (y + h), x : (x + w)]

        if curr_blk.shape != ref_blk.shape:
            return {k: np.nan for k in ['mean', 'variance', 'std_dev', 'sum']}

        diff_blk = np.abs(curr_blk.astype(np.int32) - ref_blk.astype(np.int32))

        stats = {
            'mean': np.mean(diff_blk),
            'variance': np.var(diff_blk),
            'std_dev': np.std(diff_blk),
            'sum': np.sum(diff_blk)
        }

        return stats