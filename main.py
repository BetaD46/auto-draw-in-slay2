#!/usr/bin/env python3
"""
自动鼠标绘制图像脚本

功能：
1. 将图片二值化后保存为 bin 文件
2. 读取 bin 文件，控制鼠标在绘图软件中绘制图像

使用方法：
    # 将图片转为 bin
    python main.py encode input.png output.bin

    # 从 bin 文件绘制（可设置画笔粗细）
    python main.py draw output.bin --stroke 2
"""

import argparse

from draw import draw_from_bin
from encode import image_to_bin


def main():
    parser = argparse.ArgumentParser(
        description="自动鼠标绘制图像脚本",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 将图片转为 bin 文件
  python main.py encode input.png output.bin

  # 使用默认参数绘制
  python main.py draw output.bin

  # 设置画笔粗细为 3，起始位置 (100, 100)
  python main.py draw output.bin --stroke 3 --start-x 100 --start-y 100
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="命令")

    # encode 命令
    encode_parser = subparsers.add_parser("encode", help="将图片转为 bin 文件")
    encode_parser.add_argument("input", help="输入图片路径")
    encode_parser.add_argument("output", help="输出 bin 文件路径")
    encode_parser.add_argument(
        "--threshold", "-t", type=int, default=128, help="二值化阈值 (0-255), 默认 128"
    )
    encode_parser.add_argument(
        "--max-size",
        "-m",
        type=int,
        default=128,
        help="最大尺寸限制，长宽任一不得超过此值，超过则等比缩放，默认 128",
    )
    encode_parser.add_argument(
        "--no-preview",
        action="store_true",
        help="不保存黑白预览 png 文件",
    )

    # draw 命令
    draw_parser = subparsers.add_parser("draw", help="从 bin 文件绘制")
    draw_parser.add_argument("input", help="bin 文件路径")
    draw_parser.add_argument(
        "--stroke", "-s", type=int, default=1, help="画笔粗细（像素宽度）, 默认 1"
    )
    draw_parser.add_argument(
        "--delay",
        type=float,
        default=0.000001,
        help="鼠标移动间隔，单位为秒, 默认 0.000001",
    )
    draw_parser.add_argument(
        "--start-x",
        type=int,
        default=None,
        help="起始 X 坐标（屏幕绝对坐标）, 默认使用当前鼠标位置",
    )
    draw_parser.add_argument(
        "--start-y",
        type=int,
        default=None,
        help="起始 Y 坐标（屏幕绝对坐标）, 默认使用当前鼠标位置",
    )
    draw_parser.add_argument(
        "--pause",
        "-p",
        type=float,
        default=3.0,
        help="开始前的等待时间（秒）, 默认 3.0",
    )
    draw_parser.add_argument(
        "--check-interval",
        type=int,
        default=16,
        help="坐标校正间隔，越小越抗干扰，默认 16 像素",
    )

    args = parser.parse_args()

    if args.command == "encode":
        image_to_bin(
            args.input,
            args.output,
            args.threshold,
            args.max_size,
            save_preview=not args.no_preview,
        )
    elif args.command == "draw":
        draw_from_bin(
            args.input,
            stroke=args.stroke,
            delay=args.delay,
            start_x=args.start_x,
            start_y=args.start_y,
            pause=args.pause,
            check_interval=args.check_interval,
        )
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
