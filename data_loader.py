import pandas as pd
import os
from config import ACCOUNTS_FILE, SERVERS_FILE, CLICKS_FILE

def load_accounts():
    """Đọc danh sách tài khoản từ file Excel."""
    if not os.path.exists(ACCOUNTS_FILE):
        print(f"Không tìm thấy file: {ACCOUNTS_FILE}")
        return []
    df = pd.read_excel(ACCOUNTS_FILE)
    return df.to_dict(orient='records')

def load_servers():
    """Đọc danh sách server và tọa độ từ file Excel."""
    if not os.path.exists(SERVERS_FILE):
        print(f"Không tìm thấy file: {SERVERS_FILE}")
        return []
    df = pd.read_excel(SERVERS_FILE)
    return df.to_dict(orient='records')

def load_clicks():
    """Đọc danh sách tọa độ click từ file Excel."""
    if not os.path.exists(CLICKS_FILE):
        print(f"Không tìm thấy file: {CLICKS_FILE}")
        return []
    df = pd.read_excel(CLICKS_FILE)
    return df.to_dict(orient='records')

if __name__ == "__main__":
    accounts = load_accounts()
    servers = load_servers()
    clicks = load_clicks()
    print("Accounts:", accounts)
    print("Servers:", servers)
    print("Clicks:", clicks)
