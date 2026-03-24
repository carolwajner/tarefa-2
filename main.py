from TracefileProcessor import TracefileProcessor

tracefile_folder = '/home/research-data/tracefiles-zipped'
video_folder = '/home/research-data/video-sequences/'

if __name__ == '__main__':
    VIDEOS = {
        # --- CLASSE A1 (4K - High Dynamics / Natural Movement) ---
        'Tango2': {'yuv': 'Tango2_3840x2160_60fps_10bit_420.yuv', 'res': (3840, 2160), 'bitdepth': 10},
        'FoodMarket4': {'yuv': 'FoodMarket4_3840x2160_60fps_10bit_420.yuv', 'res': (3840, 2160), 'bitdepth': 10},
        'Campfire': {'yuv': 'Campfire_3840x2160_30fps_bt709_420_videoRange.yuv', 'res': (3840, 2160), 'bitdepth': 10},


        # --- CLASSE A2 (4K - Complex Textures / Fine Details) ---
        'CatRobot': {'yuv': 'CatRobot_3840x2160_60fps_10bit_420_jvet.yuv', 'res': (3840, 2160), 'bitdepth': 10},
        'DaylightRoad2': {'yuv': 'DaylightRoad2_3840x2160_60fps_10bit_420.yuv', 'res': (3840, 2160), 'bitdepth': 10},
        'ParkRunning3': {'yuv': 'ParkRunning3_3840x2160_50fps_10bit_420.yuv', 'res': (3840, 2160), 'bitdepth': 10},


        # --- CLASSE B (1080p - High Definition) ---
        'MarketPlace': {'yuv': 'MarketPlace_1920x1080_60fps_10bit_420.yuv', 'res': (1920, 1080), 'bitdepth': 10},
        'RitualDance': {'yuv': 'RitualDance_1920x1080_60fps_10bit_420.yuv', 'res': (1920, 1080), 'bitdepth': 10},
        'Cactus': {'yuv': 'Cactus_1920x1080_50.yuv', 'res': (1920, 1080), 'bitdepth': 8},
        'BasketballDrive': {'yuv': 'BasketballDrive_1920x1080_50.yuv', 'res': (1920, 1080), 'bitdepth': 8},
        'BQTerrace': {'yuv': 'BQTerrace_1920x1080_60.yuv', 'res': (1920, 1080), 'bitdepth': 8},


        # --- CLASSE C (WVGA - Standard Definition) ---
        'BasketballDrill': {'yuv': 'BasketballDrill_832x480_50.yuv', 'res': (832, 480), 'bitdepth': 8},
        'BQMall': {'yuv': 'BQMall_832x480_60.yuv', 'res': (832, 480), 'bitdepth': 8},
        'PartyScene': {'yuv': 'PartyScene_832x480_50.yuv', 'res': (832, 480), 'bitdepth': 8},
        'RaceHorsesC': {'yuv': 'RaceHorsesC_832x480_30.yuv', 'res': (832, 480), 'bitdepth': 8},


        # --- CLASSE D (QWVGA - Low Resolution) ---
        'BasketballPass': {'yuv': 'BasketballPass_416x240_50.yuv', 'res': (416, 240), 'bitdepth': 8},
        'BQSquare': {'yuv': 'BQSquare_416x240_60.yuv', 'res': (416, 240), 'bitdepth': 8},
        'BlowingBubbles': {'yuv': 'BlowingBubbles_416x240_50.yuv', 'res': (416, 240), 'bitdepth': 8},
        'RaceHorses': {'yuv': 'RaceHorses_416x240_30.yuv', 'res': (416, 240), 'bitdepth': 8},


        # --- CLASSE E (720p - Video Conferencing) ---
        'FourPeople': {'yuv': 'FourPeople_1280x720_60.yuv', 'res': (1280, 720), 'bitdepth': 8},
        'Johnny': {'yuv': 'Johnny_1280x720_60.yuv', 'res': (1280, 720), 'bitdepth': 8},
        'KristenAndSara': {'yuv': 'KristenAndSara_1280x720_60.yuv', 'res': (1280, 720), 'bitdepth': 8},


        # --- CLASSE F (Screen Content Coding - SCC) ---
        'ArenaOfValor': {'yuv': 'ArenaOfValor_1920x1080_60.yuv', 'res': (1920, 1080), 'bitdepth': 8},
        'BasketballDrillText': {'yuv': 'BasketballDrillText_832x480_50.yuv', 'res': (832, 480), 'bitdepth': 8},
        'SlideEditing': {'yuv': 'SlideEditing_1280x720_30.yuv', 'res': (1280, 720), 'bitdepth': 8},
        'SlideShow': {'yuv': 'SlideShow_1280x720_20.yuv', 'res': (1280, 720), 'bitdepth': 8},
    }

    FRAME_MAPPING = {
        # { frame_id: {"ref_frame": ID, "level": N} }
        0: {"ref_frame": None, "level": 0},
        1: {"ref_frame": 2, "level": 5},
        2: {"ref_frame": 4, "level": 4},
        3: {"ref_frame": 2, "level": 5},
        4: {"ref_frame": 8, "level": 3},
        5: {"ref_frame": 6, "level": 5},
        6: {"ref_frame": 4, "level": 4},
        7: {"ref_frame": 6, "level": 5},
        8: {"ref_frame": 16, "level": 2},
        9: {"ref_frame": 10, "level": 5},
        10: {"ref_frame": 8, "level": 4},
        11: {"ref_frame": 10, "level": 5},
        12: {"ref_frame": 8, "level": 3},
        13: {"ref_frame": 14, "level": 5},
        14: {"ref_frame": 12, "level": 4},
        15: {"ref_frame": 14, "level": 5},
        16: {"ref_frame": 32, "level": 1},
        17: {"ref_frame": 18, "level": 5},
        18: {"ref_frame": 20, "level": 4},
        19: {"ref_frame": 18, "level": 5},
        20: {"ref_frame": 24, "level": 3},
        21: {"ref_frame": 22, "level": 5},
        22: {"ref_frame": 20, "level": 4},
        23: {"ref_frame": 22, "level": 5},
        24: {"ref_frame": 16, "level": 2},
        25: {"ref_frame": 26, "level": 5},
        26: {"ref_frame": 28, "level": 4},
        27: {"ref_frame": 26, "level": 5},
        28: {"ref_frame": 24, "level": 3},
        29: {"ref_frame": 30, "level": 5},
        30: {"ref_frame": 28, "level": 4},
        31: {"ref_frame": 30, "level": 5},
        32: {"ref_frame": 0, "level": 0},
        33: {"ref_frame": 34, "level": 5},
        34: {"ref_frame": 36, "level": 4},
        35: {"ref_frame": 34, "level": 5},
        36: {"ref_frame": 40, "level": 3},
        37: {"ref_frame": 38, "level": 5},
        38: {"ref_frame": 36, "level": 4},
        39: {"ref_frame": 38, "level": 5},
        40: {"ref_frame": 48, "level": 2},
        41: {"ref_frame": 42, "level": 5},
        42: {"ref_frame": 40, "level": 4},
        43: {"ref_frame": 42, "level": 5},
        44: {"ref_frame": 40, "level": 3},
        45: {"ref_frame": 46, "level": 5},
        46: {"ref_frame": 44, "level": 4},
        47: {"ref_frame": 46, "level": 5},
        48: {"ref_frame": 64, "level": 1},
        49: {"ref_frame": 50, "level": 5},
        50: {"ref_frame": 52, "level": 4},
        51: {"ref_frame": 50, "level": 5},
        52: {"ref_frame": 56, "level": 3},
        53: {"ref_frame": 54, "level": 5},
        54: {"ref_frame": 52, "level": 4},
        55: {"ref_frame": 54, "level": 5},
        56: {"ref_frame": 48, "level": 2},
        57: {"ref_frame": 58, "level": 5},
        58: {"ref_frame": 60, "level": 4},
        59: {"ref_frame": 58, "level": 5},
        60: {"ref_frame": 56, "level": 3},
        61: {"ref_frame": 62, "level": 5},
        62: {"ref_frame": 60, "level": 4},
        63: {"ref_frame": 62, "level": 5},
        64: {"ref_frame": 32, "level": 0},
        65: {"ref_frame": 66, "level": 5},
        66: {"ref_frame": 68, "level": 4},
        67: {"ref_frame": 66, "level": 5},
        68: {"ref_frame": 72, "level": 3},
        69: {"ref_frame": 70, "level": 5},
        70: {"ref_frame": 68, "level": 4},
        71: {"ref_frame": 70, "level": 5},
        72: {"ref_frame": 80, "level": 2},
        73: {"ref_frame": 74, "level": 5},
        74: {"ref_frame": 72, "level": 4},
        75: {"ref_frame": 74, "level": 5},
        76: {"ref_frame": 72, "level": 3},
        77: {"ref_frame": 78, "level": 5},
        78: {"ref_frame": 76, "level": 4},
        79: {"ref_frame": 78, "level": 5},
        80: {"ref_frame": 96, "level": 1},
        81: {"ref_frame": 82, "level": 5},
        82: {"ref_frame": 84, "level": 4},
        83: {"ref_frame": 82, "level": 5},
        84: {"ref_frame": 88, "level": 3},
        85: {"ref_frame": 86, "level": 5},
        86: {"ref_frame": 84, "level": 4},
        87: {"ref_frame": 86, "level": 5},
        88: {"ref_frame": 80, "level": 2},
        89: {"ref_frame": 90, "level": 5},
        90: {"ref_frame": 92, "level": 4},
        91: {"ref_frame": 90, "level": 5},
        92: {"ref_frame": 88, "level": 3},
        93: {"ref_frame": 94, "level": 5},
        94: {"ref_frame": 92, "level": 4},
        95: {"ref_frame": 94, "level": 5},
        96: {"ref_frame": 64, "level": 0}
    }
    processor = TracefileProcessor(video_folder=video_folder, configs=VIDEOS, frame_mapping=FRAME_MAPPING)    
    processor.process_all(path=tracefile_folder)  