# ================== CẤU HÌNH ==================
WIDTH, HEIGHT = 1200, 600
FPS = 60

ROWS, COLS = 3, 3 
GAP = 2

# Tọa độ bàn trái (kích thước hiển thị cố định)
LEFT_BOARD_X, LEFT_BOARD_Y = 40, 80
# Fixed display size for left board (pixels). This area stays the same regardless of ROWS/COLS.
LEFT_BOARD_W, LEFT_BOARD_H = 360, 360



# Tính lại cell size mỗi lần đổi Rows/Cols
BOARD_CELL_SIZE = min(LEFT_BOARD_W // COLS, LEFT_BOARD_H // ROWS)
left_cell_w = max(8, LEFT_BOARD_W // COLS)
left_cell_h = max(8, LEFT_BOARD_H // ROWS)

# Kích thước bàn đích
RIGHT_BOARD_W, RIGHT_BOARD_H =200, 350
GOAL_CELL_SIZE = min(RIGHT_BOARD_W // COLS, RIGHT_BOARD_H // ROWS)
# Tọa độ bàn đích
GOAL_BOARD_X, GOAL_BOARD_Y = 440, 80 # Đặt gần bàn trái hơn
GOAL_BOARD_W, GOAL_BOARD_H = 200, 200 # Đặt lại kích thước để phù hợp
right_cell_w = max(8, RIGHT_BOARD_W // COLS)
right_cell_h = max(8, RIGHT_BOARD_H // ROWS)

# Tọa độ panel
panel_x = 700
panel_y = 70
panel_w = 400 # Tăng chiều rộng để chứa nhiều thông tin hơn
panel_h = 400

# Tọa độ bàn AI
AI_BOARD_X, AI_BOARD_Y = 500, 80
GOAL_X, GOAL_Y =450, 80

# Tọa độ nút
BTN_W, BTN_H = 140, 50
BTN_X, BTN_Y = 830, 40 # Đặt các nút trong panel

# Màu sắc
BG_COLOR = (30, 20, 60)  # Nền vũ trụ (tím-xanh đậm)
BOARD_COLOR = (40, 50, 80)  # Nền board chính
GOAL_BOARD_COLOR = (50, 40, 90)  # Nền goal board
BUTTON_COLOR = (80, 90, 180)  # Nút bấm tím xanh
BUTTON_HOVER_COLOR = (120, 130, 220)  # Hover nút
BUTTON_TEXT_COLOR = (240, 240, 255)  # Chữ trên nút
TEXT_COLOR = (240, 240, 255)  # Chữ chính
TEXT_SUB_COLOR = (180, 200, 255)  # Chữ phụ, label
VIEN_COLOR = (180, 200, 255)  # Viền board, viền input
VIEN_HOVER_COLOR = (255, 230, 120)  # Viền nổi bật khi hover
INPUT_BG_COLOR = (30, 30, 60)  # Nền input
INPUT_TEXT_COLOR = (220, 220, 255)  # Chữ input
PANEL_BG_COLOR = (40, 40, 70)  # Nền panel
PANEL_VIEN_COLOR = (120, 130, 220)  # Viền panel
SHADOW_COLOR = (80, 80, 120, 30)  # Shadow ngoài
STAR_COLOR = (220, 220, 255)  # Sao vũ trụ
WIN_TEXT_COLOR = (255, 230, 120)  # Chữ chúc mừng