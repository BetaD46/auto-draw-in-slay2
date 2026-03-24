"""
共用工具函数
"""

import struct

import numpy as np

# bin 文件格式：
# 4 字节：宽度 (uint32)
# 4 字节：高度 (uint32)
# 1 字节：阈值 (uint8)
# 剩余：像素数据 (uint8, 0 或 1)
HEADER_FORMAT = "<IIB"  # little-endian: uint32, uint32, uint8


def read_bin(bin_path: str) -> tuple[int, int, np.ndarray]:
    """
    读取 bin 文件

    Returns:
        (width, height, binary_array)
    """
    with open(bin_path, "rb") as f:
        # 读取头部
        header_data = f.read(struct.calcsize(HEADER_FORMAT))
        width, height, threshold = struct.unpack(HEADER_FORMAT, header_data)

        # 读取像素数据
        pixel_data = f.read()
        binary_array = np.frombuffer(pixel_data, dtype=np.uint8).reshape(height, width)

    return width, height, binary_array
