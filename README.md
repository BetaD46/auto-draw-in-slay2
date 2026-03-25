# Auto Draw - 自动鼠标绘制图像脚本

一个将图片转换为二值化数据，并控制鼠标自动绘制图像的 Python 工具。

![](./images/1.png)

## 功能特点

- 🖼️ 图片二值化处理，生成紧凑的 bin 格式
- 🖱️ 控制鼠标自动绘制，支持多种绘图软件
- ⚙️ 可调节画笔粗细、绘制速度、起始位置
- ⏸️ 支持 ESC 键随时中断绘制
- 📐 自动等比缩放，防止图片过大

## 环境要求

- Python >= 3.10
- Windows / macOS / Linux

## 安装

### 1. 安装 uv（如果尚未安装）

```bash
# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.org.cn/uv/install.ps1 | iex"

# macOS / Linux
curl -LsSf https://astral.org.cn/uv/install.sh | sh
```

### 2. 安装项目依赖

```bash
# 创建虚拟环境并安装依赖
uv sync

# 或者直接使用 uv run 运行脚本
```

## 使用方法

### 将图片转为 bin 文件

```bash
# 基本用法
uv run python main.py encode input.png output.bin

# 自定义阈值（0-255，默认 128）
uv run python main.py encode input.png output.bin --threshold 100

# 自定义最大尺寸（默认 128）
uv run python main.py encode input.png output.bin --max-size 256

# 不保存预览图
uv run python main.py encode input.png output.bin --no-preview
```

### 从 bin 文件绘制

```bash
# 基本用法（使用当前鼠标位置作为起点）
uv run python main.py draw output.bin

# 自定义画笔粗细（像素宽度，默认 1）
uv run python main.py draw output.bin --stroke 3

# 自定义起始位置（屏幕绝对坐标）
uv run python main.py draw output.bin --start-x 100 --start-y 100

# 调整鼠标移动延迟（秒，默认 0.000001）
uv run python main.py draw output.bin --delay 0.001

# 调整开始前的等待时间（秒，默认 3.0）
uv run python main.py draw output.bin --pause 5.0

# 调整坐标校正间隔（默认 16 像素）
uv run python main.py draw output.bin --check-interval 8
```

## 使用流程

1. **准备图片**：选择一张清晰的图片（建议线条简单、对比度高）

2. **转换为 bin 文件**：

   ```bash
   uv run python main.py encode your_image.png output.bin
   ```

   会生成 `output.bin` 和 `output.png`（黑白预览图）

3. **打开绘图软件**：如 Windows 画图、Photoshop、SAI 等

4. **选择画笔工具**：设置为铅笔或硬边画笔，关闭防抖/平滑功能

5. **执行绘制**：

   ```bash
   uv run python main.py draw output.bin --stroke 2
   ```

   等待 3 秒后自动开始绘制

6. **中断绘制**：按 `ESC` 键可随时停止

## 参数说明

### encode 命令参数

| 参数           | 简写 | 默认值 | 说明               |
| -------------- | ---- | ------ | ------------------ |
| `input`        | -    | 必填   | 输入图片路径       |
| `output`       | -    | 必填   | 输出 bin 文件路径  |
| `--threshold`  | `-t` | 128    | 二值化阈值 (0-255) |
| `--max-size`   | `-m` | 128    | 最大尺寸限制       |
| `--no-preview` | -    | false  | 不保存预览图       |

### draw 命令参数

| 参数               | 简写 | 默认值   | 说明                 |
| ------------------ | ---- | -------- | -------------------- |
| `input`            | -    | 必填     | bin 文件路径         |
| `--stroke`         | `-s` | 1        | 画笔粗细（像素）     |
| `--delay`          | -    | 0.000001 | 鼠标移动间隔（秒）   |
| `--start-x`        | -    | null     | 起始 X 坐标          |
| `--start-y`        | -    | null     | 起始 Y 坐标          |
| `--pause`          | `-p` | 3.0      | 开始前等待时间（秒） |
| `--check-interval` | -    | 16       | 坐标校正间隔（像素） |

## 注意事项

1. **权限要求**：在 Windows 上可能需要管理员权限才能使用键盘监听功能

2. **绘图软件设置**：
   - 使用铅笔或硬边画笔
   - 关闭画笔平滑/防抖功能
   - 确保画布足够大

3. **绘制过程中**：
   - 不要移动鼠标或切换窗口
   - 按 ESC 键可立即停止绘制

4. **图片建议**：
   - 使用高对比度的线条图
   - 避免过于复杂的图像
   - 尺寸过大自动缩放可能影响细节

## 项目结构

```
auto_draw/
├── main.py          # 主入口，命令行解析
├── encode.py        # 图片转 bin 模块
├── draw.py          # 鼠标绘制模块
├── utils.py         # 共用工具函数
├── pyproject.toml   # 项目配置
└── README.md        # 说明文档
```

## 开发

```bash
# 安装开发依赖
uv sync

# 运行脚本
uv run python main.py --help
```
