# Network 4Key Keyboard Controller

一个基于 Flask-SocketIO 的网络键盘控制器，支持通过 WebSocket 远程控制电脑键盘。

## 我想说
我已完全拥抱vibe-coding，编程只是手段，作品才是目的。除了这一段的内容，其他都是vibe-coding。  
这个项目是专门为PC端的音游痴们设计的，你猜猜为什么偏偏是4个按键？  
我的目标就是让键盘也可以像中二节奏（？）一样能搓起来。

## 功能特性

- ✅ WebSocket 实时通信
- ✅ 支持四个按键：D、F、J、K
- ✅ 多点触控支持
- ✅ 触摸滑动检测（手指滑出按钮区域自动释放）
- ✅ 跨平台支持（Linux/Windows）

## 架构设计

```
┌─────────────────────────────────────┐
│         Flask-SocketIO App          │
├─────────────────────────────────────┤
│      KeyboardSimulator (Upper)       │
│      - press(key)                    │
│      - release(key)                  │
├──────────────────┬──────────────────┤
│  LinuxImpl       │  WindowsImpl     │
│  (uinput)        │  (pyautogui)     │
└──────────────────┴──────────────────┘
```

## 技术栈

| 类别             | 工具                        |
| -------------- | ------------------------- |
| 后端框架           | Flask + Flask-SocketIO    |
| 键盘模拟 (Linux)   | python-uinput             |
| 键盘模拟 (Windows) | pyautogui                 |
| 前端测试           | Vitest + @testing-library |
| 后端测试           | pytest                    |

## 快速开始

### 安装依赖

```bash
# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 运行服务

```bash
# Linux 需要配置 uinput 权限
sudo chmod 666 /dev/uinput

# 启动服务
python app.py
```

### 访问地址

- 本地: `http://localhost:5000`
- 局域网: `http://<your-ip>:5000`

## 使用方法

1. 在手机浏览器中打开服务地址
2. 触摸四个按钮（D、F、J、K），可以滑动，可以多点触控
3. 按钮会模拟键盘输入

## 测试

### 后端测试

```bash
source venv/bin/activate
python -m pytest tests/ -v
```

### 前端测试

```bash
npx vitest run
```
