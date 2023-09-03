import subprocess
import os

# 替换下面的 "your_streamlit_app.py" 为您的Streamlit应用程序文件的路径
streamlit_app_path = "main.py"

# 替换下面的 "requirements.txt" 为您的依赖项文件的路径
requirements_file = "requirements.txt"

# 使用 pip 安装依赖项到一个临时目录
subprocess.run(["pip", "install", "--target", "temp_dir", "-r", requirements_file])

# 使用 pyinstaller 打包应用程序，并将临时目录中的依赖项包含进来
subprocess.run(["pyinstaller", "--onefile", "--add-data", f"temp_dir:{os.path.join('lib', 'python3.7', 'site-packages')}", streamlit_app_path])
