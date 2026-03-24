"""
鼠标绘制模块
"""

import threading
import time

import keyboard
import pyautogui

from utils import read_bin


def draw_from_bin(
    bin_path: str,
    stroke: int = 1,
    delay: float = 0.000001,
    start_x: int | None = None,
    start_y: int | None = None,
    pause: float = 2.0,
    check_interval: int = 16,
) -> None:
    """
    从 bin 文件读取数据并控制鼠标绘制

    Args:
        bin_path: bin 文件路径
        stroke: 画笔粗细（像素宽度），决定鼠标移动步长
        delay: 鼠标移动速度（秒/像素），默认 0.0001 几乎无延迟
        start_x: 起始 X 坐标（屏幕绝对坐标），None 表示使用当前鼠标位置
        start_y: 起始 Y 坐标（屏幕绝对坐标），None 表示使用当前鼠标位置
        pause: 开始前的等待时间（秒）
        check_interval: 坐标校正间隔，默认 16 像素
    """
    width, height, binary = read_bin(bin_path)

    print(f"bin 文件尺寸：{width} x {height}")
    print(f"画笔粗细：{stroke}")
    print(f"延迟：{delay} s")
    print(f"检查间隔：{check_interval} 像素")
    print(f"将在 {pause} 秒后开始绘制，请切换到绘图软件...")
    print("按 ESC 键停止绘制")

    # 停止标志
    stop_flag = threading.Event()

    # 监听键盘事件
    def check_stop():
        if keyboard.is_pressed("esc"):
            stop_flag.set()

    # 设置 pyautogui 安全设置
    pyautogui.FAILSAFE = True  # 鼠标移到屏幕角落可停止
    pyautogui.PAUSE = 0.0  # 禁用默认暂停，使用自定义延迟控制

    # 等待用户切换到绘图软件
    time.sleep(pause)

    # 获取起始位置（如果未指定，使用当前鼠标位置）
    if start_x is None or start_y is None:
        current_pos = pyautogui.position()
        if start_x is None:
            start_x = current_pos.x
        if start_y is None:
            start_y = current_pos.y
        print(f"起始位置：({start_x}, {start_y})")

        # 移动到起始位置
        pyautogui.moveTo(start_x, start_y)

    # 扫描式绘制 - 使用 x 轴相对移动优化性能
    # 策略：连续绘制时保持鼠标按下，减少 mouseDown/mouseUp 次数
    # 移动步长等于画笔粗细
    step = stroke

    # 记录初始 Y 坐标，用于绝对坐标移动
    initial_y = start_y

    step_count = 0

    for row in range(height):
        # 检查是否停止
        check_stop()
        if stop_flag.is_set():
            print("\n用户中断，绘制停止")
            pyautogui.mouseUp()
            return

        # 确定当前行的绘制方向
        col_range = range(width)
        dx = step

        is_drawing = False  # 当前是否处于绘制状态（鼠标按下）

        x_rel = 0
        for i, col in enumerate(col_range):
            # 检查是否停止
            check_stop()
            if stop_flag.is_set():
                print("\n用户中断，绘制停止")
                pyautogui.mouseUp()
                return

            should_draw = binary[row, col] == 1

            if should_draw and not is_drawing:
                # 开始绘制：按下鼠标
                pyautogui.mouseDown()
                is_drawing = True
            elif not should_draw and is_drawing:
                # 停止绘制：释放鼠标
                pyautogui.mouseUp()
                is_drawing = False

            # 移动到下一个像素（相对移动 step 像素）
            # 注意：最后一个像素后不需要移动
            if i < width - 1:
                x_rel += 1
                expected_x = start_x + dx * x_rel
                expected_y = initial_y + row * step

                if step_count % check_interval == 0:
                    pyautogui.moveTo(expected_x, expected_y, duration=0)
                else:
                    pyautogui.moveRel(dx, 0, duration=0)

                step_count += 1
                time.sleep(delay)

        # 行末处理：确保鼠标释放，然后移动到下一行的起始位置
        if is_drawing:
            pyautogui.mouseUp()
            is_drawing = False

        # 使用绝对坐标移动到下一行的起始位置（提供绘图容错）
        # 无论当前行方向如何，下一行总是从左侧 (start_x) 开始
        if row < height - 1:
            next_y = initial_y + (row + 1) * step
            pyautogui.moveTo(start_x, next_y, duration=0)
            time.sleep(delay)

    print("绘制完成！")
