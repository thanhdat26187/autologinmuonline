import os
import time
import pandas as pd
import pygetwindow as gw
import win32gui
import pyautogui

"""
Module hỗ trợ tự động hóa đăng nhập MU Online:
- Đọc dữ liệu từ các file Excel nằm trong thư mục 'data'
- Xác định vị trí và kích thước vùng hiển thị (client area) của cửa sổ game
- Tìm và click vào hình ảnh trên màn hình dựa theo các file ảnh trong thư mục 'images'
"""

# Định nghĩa thư mục chứa hình ảnh
image_folder = os.path.join(os.path.dirname(__file__), "images")

# Hàm load_data: đọc file Excel từ thư mục 'data'
def load_data(file_name):
    file_path = os.path.join(os.path.dirname(__file__), "data", file_name)
    try:
        df = pd.read_excel(file_path)
        data = df.to_dict(orient="records")
        print(f"✅ Đã tải {len(data)} bản ghi từ {file_name}")
        return data
    except Exception as e:
        print(f"⚠ Lỗi khi đọc file {file_name}: {e}")
        return []

# Tải dữ liệu từ các file Excel
accounts = load_data("accounts.xlsx")
click_positions = load_data("clicks.xlsx")
servers = load_data("servers.xlsx")

def find_and_get_coordinates(image_name, confidence=0.8, timeout=10):
    """Tìm hình ảnh trên màn hình và trả về tọa độ trung tâm nếu tìm thấy"""
    image_path = os.path.join(image_folder, image_name)
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            location = pyautogui.locateCenterOnScreen(image_path, confidence=confidence)
            if location:
                print(f"📍 Tìm thấy {image_name} tại tọa độ: {location}")
                pyautogui.moveTo(location)  # Trỏ chuột đến vị trí để kiểm tra trực quan
                return location
        except Exception:
            pass
        time.sleep(0.5)
    print(f"⚠ Không tìm thấy {image_name} sau {timeout} giây, tiếp tục chương trình...")
    return None

def get_game_position():
    """Lấy vị trí và kích thước vùng hiển thị (client area) của cửa sổ game, không tính tiêu đề và viền."""
    window_title = "MU Tien Phong"
    for window in gw.getWindowsWithTitle(window_title):
        if window_title in window.title:
            hwnd = window._hWnd
            # Lấy client rect: vùng hiển thị thực tế (không tính tiêu đề và viền)
            client_rect = win32gui.GetClientRect(hwnd)
            client_left, client_top = win32gui.ClientToScreen(hwnd, (client_rect[0], client_rect[1]))
            client_width = client_rect[2] - client_rect[0]
            client_height = client_rect[3] - client_rect[1]
            print(f"📌 Vùng game thực tế (client area): ({client_left}, {client_top}), kích thước: ({client_width}x{client_height})")
            return client_left, client_top, client_width, client_height
    print("⚠ Không tìm thấy cửa sổ game!")
    return None

def click_position(name):
    """Click vào vị trí đã lưu trong file Excel (click_positions) dựa theo key 'name'."""
    game_pos = get_game_position()
    if game_pos:
        for pos in click_positions:
            if pos.get("name") == name:
                x = int(game_pos[0] + game_pos[2] * pos.get("x_ratio", 0))
                y = int(game_pos[1] + game_pos[3] * pos.get("y_ratio", 0))
                pyautogui.click(x, y)
                print(f"✅ Đã click tại {name} ({x}, {y})")
                return
    print(f"⚠ Không tìm thấy vị trí click cho {name}")

def select_server_group():
    """Chọn cụm server từ file servers.xlsx dựa trên key 'name'."""
    file_path = os.path.join(os.path.dirname(__file__), "data", "servers.xlsx")
    try:
        df = pd.read_excel(file_path)
        if df.empty:
            raise ValueError("File servers.xlsx không có dữ liệu")
        for record in df.to_dict(orient="records"):
            if record.get("name") == "server_group":
                click_position("server_group")
                print(f"✅ Đã chọn cụm server với dữ liệu: {record}")
                time.sleep(2)
                return
        print("⚠ Không tìm thấy dữ liệu cụm server trong file servers.xlsx")
    except Exception as e:
        print(f"⚠ Lỗi khi chọn cụm server: {e}, tiếp tục chương trình...")

def select_server():
    """Chọn server từ file servers.xlsx dựa trên key 'name'."""
    file_path = os.path.join(os.path.dirname(__file__), "data", "servers.xlsx")
    try:
        df = pd.read_excel(file_path)
        if df.empty:
            raise ValueError("File servers.xlsx không có dữ liệu")
        for record in df.to_dict(orient="records"):
            if record.get("name") == "server":
                click_position("server")
                print(f"✅ Đã chọn server với dữ liệu: {record}")
                time.sleep(2)
                return
        print("⚠ Không tìm thấy dữ liệu server trong file servers.xlsx")
    except Exception as e:
        print(f"⚠ Lỗi khi chọn server: {e}, tiếp tục chương trình...")

def login_with_account(account):
    """Nhập tài khoản và mật khẩu từ file accounts.xlsx."""
    click_position("username_field")
    pyautogui.write(account.get("username", ""), interval=0.1)
    print("✅ Đã nhập tên tài khoản!")
    
    click_position("password_field")
    pyautogui.write(account.get("password", ""), interval=0.1)
    print("✅ Đã nhập mật khẩu!")
    
    click_position("login_button")
    print("✅ Đã nhấn nút đăng nhập!")

def launch_game():
    """Mở game từ icon trên desktop và nhấn nút Start."""
    icon_location = find_and_get_coordinates("icon_game.png")
    if not icon_location:
        print("⚠ Không tìm thấy icon game trên desktop!")
        return False
    pyautogui.doubleClick(icon_location)
    time.sleep(5)
    
    for _ in range(3):
        print("🔍 Đang tìm nút Start...")
        location = find_and_get_coordinates("start_button.png", confidence=0.8)
        if location:
            pyautogui.click(location)
            print("✅ Đã nhấn nút Start, đang vào game...")
            return wait_for_game_load()
        time.sleep(2)
    
    print("⚠ Không tìm thấy nút Start trong launcher!")
    return False

def wait_for_game_load(timeout=90):
    """Chờ game load bằng cách kiểm tra hình ảnh game_loader.png và trỏ chuột đến đó để theo dõi."""
    print("⏳ Đợi 20s trước khi kiểm tra game đã load...")
    time.sleep(20)
    
    for i in range(30):
        location = find_and_get_coordinates("game_loader.png", confidence=0.8)
        if location:
            print("✅ Game đã load xong!")
            pyautogui.moveTo(location)  # Chỉ trỏ chuột để theo dõi, không click
            return True
        print(f"⏳ Đang chờ game load... ({i+1}/30)")
        time.sleep(3)
    
    print("⚠ Quá thời gian chờ, có thể game chưa load xong!")
    return False

if __name__ == "__main__":
    if launch_game():
        time.sleep(5)
        get_game_position()
        click_position("server_group")
        time.sleep(2)
        click_position("server")
        time.sleep(2)
        if accounts:
            login_with_account(accounts[0])
        else:
            print("⚠ Không có tài khoản để đăng nhập!")
