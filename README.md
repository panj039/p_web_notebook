# P_Web_NoteBook

个人知识库系统 - 安全的文档管理平台

## 🚀 快速开始

### 本地运行
```bash
# 激活Python环境
conda activate p_web_notebook

# 安装依赖
pip install -r requirements.txt

# 启动应用
python main.py
```

### Docker运行
```bash
# 进入docker目录
cd docker

# 启动服务
docker-compose up -d
```

## 🔐 默认登录信息

- **用户名**: `admin`
- **密码**: `hello`
- **TOTP密钥**: `S3UFJI5B366IPFC4N77PAJSKNYOF6Q7A`

在Google Authenticator中添加该密钥以获取验证码。

## 📁 项目结构

```
p_web_notebook/
├── .env                 # ⚙️ 环境变量配置文件
├── main.py              # 🚀 应用入口文件 (简化的启动脚本)
├── start.py             # 🛠️ 快速启动工具
├── requirements.txt     # 📦 Python依赖
├── README.md           # 📖 项目说明
├── app/                # 💻 应用核心代码
│   ├── __init__.py
│   ├── server.py       # 🌐 Flask应用主体
│   ├── auth.py         # 🔐 认证模块
│   └── config.py       # ⚙️ 配置管理
├── util/               # 🛠️ 工具函数库
│   ├── __init__.py
│   └── paths.py        # 📍 统一路径管理
├── config/             # 📋 配置文件目录
│   └── users.json      # 👤 用户配置
├── docker/             # 🐳 Docker配置
│   ├── Dockerfile
│   └── docker-compose.yml
├── tool/               # 🔧 工具目录
│   └── setup_users.py  # 👥 用户管理工具
├── temp/               # 📁 临时文件目录 (工具输出)
├── templates/          # 🎨 HTML模板
├── static/             # 🎭 静态资源 
└── data/              # 💾 数据文件存储
```

## ✨ 功能特性

- 🔐 **双因素认证**: 用户名+密码+Google Authenticator
- 📝 **文件管理**: 创建、编辑、查看、删除文本文件
- 🎨 **Markdown渲染**: 美观的Markdown文件显示
- 🔍 **全文搜索**: 按文件名和内容搜索
- 📤 **文件上传**: 直接上传文本文件
- 📂 **目录组织**: 文件夹分类管理
- 🐳 **Docker支持**: 容器化部署

## ⚙️ 应用配置

### 自定义应用标题

P_Web_NoteBook 支持自定义应用名称和描述，所有配置都在 `app/config.py` 中统一管理。

#### 方法1: 环境变量配置

```bash
# Windows PowerShell
$env:APP_NAME='我的知识库'
$env:APP_DESCRIPTION='个人笔记管理系统'
python main.py

# Linux/macOS
export APP_NAME='我的知识库'
export APP_DESCRIPTION='个人笔记管理系统'
python main.py
```

#### 方法2: .env 文件配置

1. 编辑 `.env` 文件：

```bash
APP_NAME=我的知识库
APP_DESCRIPTION=个人笔记管理系统
DEBUG=false
HOST=0.0.0.0
PORT=5000
SECRET_KEY=your-secret-key-here
```

2. 重启应用即可生效

## 🛠️ 用户管理

### 生成新用户配置

使用`tool/setup_users.py`工具生成新的用户配置和Google Authenticator设置：

```bash
# 进入项目根目录
cd p_web_notebook

# 运行用户设置工具
python tool/setup_users.py
```

工具会在`temp/`目录中生成：

- `users.json` - 新的用户配置文件
- `authenticator_setup.html` - Google Authenticator设置页面

### 应用新配置

1. 将生成的`temp/users.json`复制到`config/users.json`
2. 重启应用
3. 打开`temp/authenticator_setup.html`设置Google Authenticator

## AI Coding Rules (for Copilot & ChatGPT)

当使用 AI 生成代码时，必须遵循以下规则：

1. 不要生成任何非代码内容。
2. 不要生成测试文件，如果必须要生成，则放在 `temp/` 文件夹中。
3. 不需要生成说明文件。
4. 不要保持向后兼容的内容。
5. 不要过度设计，没有用到的东西一律不生成。
6. 不论是同步还是异步，都只需要一个有效的可用接口。
7. 代码尽量简练，简单清晰。
8. 一个功能只要一个实现即可。
9. Python 版本固定为 **3.12.12**。
10. Typing 的使用, 请使用对应 Python 版本的语法。
11. 激活 Python 环境的方法：

    ```ps
    conda activate p_web_notebook
    ```

12. 安装 Python 库时使用 **pip**。
13. 运行代码时, 直接使用`python xxx.py`运行即可
14. 除了 `__init__.py` 以外，不要使用相对导入。
15. 当前环境为 **powershell 7.5.4**，请使用该环境可用的命令。
16. 不需要提供任何`Mock`代码。
