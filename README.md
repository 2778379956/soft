# 悬浮摄像头

Windows 7 悬浮摄像头窗口，始终置顶显示，可拖动，透明度和大小可调。

## 功能

- ✅ 摄像头实时预览
- ✅ 置顶显示（可开关）
- ✅ 水平翻转（镜像）
- ✅ 透明度调节 30%-100%
- ✅ 大小调节 20%-100%
- ✅ 可拖动位置
- ✅ 无边框极简设计

## 构建 exe

### 方式一：GitHub Actions（推荐 ✅）

1. **上传代码到 GitHub 仓库**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/你的用户名/floating-camera.git
   git push -u origin main
   ```

2. **触发构建**
   - 进入 GitHub 仓库 → Actions → Build Windows EXE → Run workflow

3. **下载 exe**
   - 构建完成后在 Actions 页面下载 artifact

### 方式二：本地 Windows 构建

1. 安装 Python 3.7+ ([下载](https://www.python.org/downloads/))
2. 双击运行 `build.bat`
3. 在 `dist` 文件夹获取 `悬浮摄像头.exe`

## 依赖

- opencv-python >= 4.5.0
- Pillow >= 8.0.0
- PyInstaller >= 6.0.0

## 使用说明

1. 运行 exe 后选择摄像头（默认第一个）
2. 底部工具栏：
   - **置顶** — 开关置顶窗口
   - **翻转** — 水平镜像
   - **透明度/大小** — 滑块调节
   - **关闭** — 退出程序
3. 拖动窗口空白处移动位置

## 注意事项

- Windows 7 可能需要安装摄像头驱动
- 如果打不开摄像头，尝试在 `main.py` 中修改 `cv2.VideoCapture(0)` 的索引
