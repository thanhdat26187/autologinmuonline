import pygetwindow as gw
import win32gui
import win32api
import time
import pyautogui
import os

# Định nghĩa thư mục chứa hình ảnh
image_folder = os.path.join(os.path.dirname(__file__), "images")

def find_and_get_coordinates(image_name, confidence=0.8, timeout=10):
    """Tìm hình ảnh trên màn hình và trả về tọa độ trung tâm nếu tìm thấy"""
    image_path = os.path.join(image_folder, image_name)
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            location = pyautogui.locateCenterOnScreen(image_path, confidence=confidence)
            if location:
                print(f"📍 Tìm thấy {image_name} tại tọa độ: {location}")
                pyautogui.moveTo(location)  # Trỏ chuột vào hình ảnh tìm được
                return location  # Trả về tọa độ tìm thấy
        except pyautogui.ImageNotFoundException:
            pass  # Bỏ qua lỗi và tiếp tục thử tìm
        
        time.sleep(0.5)
    
    print(f"⚠ Không tìm thấy {image_name} sau {timeout} giây!")
    return None

def launch_game():
    """Mở game từ icon trên desktop bằng cách nhấp đúp chuột và nhấn nút Start"""
    game_icon = os.path.join(image_folder, "icon_game.png")
    icon_location = find_and_get_coordinates("icon_game.png")
    if not icon_location:
        print("⚠ Không tìm thấy icon game trên desktop!")
        return False
    pyautogui.doubleClick(icon_location)
    time.sleep(5)  # Chờ launcher mở
    
    start_button = "start_button.png"
    for attempt in range(3):
        print(f"🔍 Đang tìm nút Start (lần {attempt + 1})...")
        location = find_and_get_coordinates(start_button, confidence=0.8)
        if location:
            x, y = location
            print(f"📍 Tìm thấy nút Start tại tọa độ: ({x}, {y})")
            time.sleep(1)
            pyautogui.click(x, y)
            print("✅ Đã nhấn nút Start, đang vào game...")
            return wait_for_game_load()
        else:
            print("❌ Chưa tìm thấy, thử lại sau 2 giây...")
            time.sleep(2)
    
    print("⚠ Không tìm thấy nút Start trong launcher!")
    return False

def wait_for_game_load(timeout=90):
    """Chờ game load bằng cách kiểm tra hình ảnh game_loader.png"""
    game_loader = "game_loader.png"
    print("⏳ Đợi 20s trước khi kiểm tra game đã load...")
    time.sleep(20)  # Chờ trước khi kiểm tra
    
    for i in range(30):
        if find_and_get_coordinates(game_loader, confidence=0.8):
            print("✅ Game đã load xong!")
            return True
        print(f"⏳ Đang chờ game load... ({i+1}/30)")
        time.sleep(3)
    
    print("⚠ Quá thời gian chờ, có thể game chưa load xong!")
    return False

def get_game_window():
    """Tìm cửa sổ game dựa trên tiêu đề"""
    window_title = "MU Tien Phong"
    for window in gw.getWindowsWithTitle(window_title):
        if window_title in window.title:
            print(f"\U0001F3AE Tìm thấy cửa sổ game: {window.title}")
            return window
    print("⚠ Không tìm thấy cửa sổ game!")
    return None

def get_game_position():
    """Lấy vị trí và kích thước thực tế của game, không tính viền và tiêu đề"""
    game_window = get_game_window()
    if game_window:
        left, top, width, height = game_window.left, game_window.top, game_window.width, game_window.height
        hwnd = game_window._hWnd  # Handle của cửa sổ
        rect = win32gui.GetClientRect(hwnd)
        client_width, client_height = rect[2] - rect[0], rect[3] - rect[1]
        
        title_bar_height = win32api.GetSystemMetrics(4)  # SM_CYCAPTION - chiều cao tiêu đề
        border_size = (width - client_width) // 2  # Viền cửa sổ
        
        title_bar_height = max(20, min(title_bar_height, 50))
        border_size = max(2, min(border_size, 10))
        
        game_left = left + border_size
        game_top = top + title_bar_height
        game_width = client_width
        game_height = client_height
        
        print(f"\U0001F4CC Vùng game thực tế: ({game_left}, {game_top}), kích thước: ({game_width}x{game_height})")
        return game_left, game_top, game_width, game_height
    return None

if __name__ == "__main__":
    if launch_game():
        time.sleep(5)  # Chờ game load hoàn toàn
        get_game_position()
