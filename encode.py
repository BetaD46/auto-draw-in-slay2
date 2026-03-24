"""
图片转 bin 文件模块
"""

import struct

import cv2
import numpy as np

from utils import HEADER_FORMAT


def image_to_bin(
    image_path: str,
    output_path: str,
    threshold: int = 128,
    max_size: int = 128,
    save_preview: bool = True,
) -> None:
    """
    将图片二值化并写入 bin 文件

    Args:
        image_path: 输入图片路径
        output_path: 输出 bin 文件路径
        threshold: 二值化阈值 (0-255), 大于此值为深色 (1), 否则为浅色 (0)
        max_size: 最大尺寸限制，长宽任一不得超过此值，超过则等比缩放
        save_preview: 是否同时保存黑白预览 png 文件
    """
    # 读取图片
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"无法读取图片：{image_path}")

    height, width = img.shape[:2]
    print(f"原始尺寸：{width} x {height}")

    # 等比缩放，确保长宽任一不超过 max_size
    if width > max_size or height > max_size:
        scale = max_size / max(width, height)
        new_width = int(width * scale)
        new_height = int(height * scale)
        img = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_AREA)
        width, height = new_width, new_height
        print(f"缩放后尺寸：{width} x {height}")

    # 转换为灰度图
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 二值化：深色 (小于阈值) 为 1, 浅色为 0
    # 注意：在灰度图中，值越小越暗
    _, binary = cv2.threshold(gray, threshold, 1, cv2.THRESH_BINARY_INV)

    # 写入 bin 文件
    with open(output_path, "wb") as f:
        # 写入头部：宽度、高度、阈值
        header = struct.pack(HEADER_FORMAT, width, height, threshold)
        f.write(header)
        # 写入像素数据
        f.write(binary.astype(np.uint8).tobytes())

    print(f"已保存至：{output_path}")
    print(f"最终尺寸：{width} x {height}")
    print(f"二值化阈值：{threshold}")

    # 保存黑白预览 png 文件
    if save_preview:
        # 将 binary 反转回正常显示（0 为黑，1 为白）
        preview = (1 - binary) * 255
        preview_path = output_path.replace(".bin", ".png")
        cv2.imwrite(preview_path, preview)
        print(f"预览图已保存至：{preview_path}")
