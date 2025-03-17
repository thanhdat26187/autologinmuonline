import os

# Đường dẫn đến các file dữ liệu
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

ACCOUNTS_FILE = os.path.join(DATA_DIR, "accounts.xlsx")
SERVERS_FILE = os.path.join(DATA_DIR, "servers.xlsx")
CLICKS_FILE = os.path.join(DATA_DIR, "clicks.xlsx")

# Độ trễ giữa các lần click (để tránh lỗi thao tác quá nhanh)
CLICK_DELAY = 0.5
INPUT_DELAY = 0.3

# Các độ phân giải hỗ trợ (nếu cần mở rộng thì thêm vào đây)
SUPPORTED_RESOLUTIONS = [
    (800, 600), (1024, 768), (1152, 864), (1280, 720),
    (1280, 800), (1280, 960), (1600, 900), (1600, 1050),
    (1920, 1080)
]

# Thời gian chờ game load (điều chỉnh theo máy)
GAME_LOAD_TIME = 10
