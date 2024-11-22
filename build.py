import subprocess
import os

def run_pyinstaller():
    # Define the paths for your assets and Python script
    icon_path = r"D:/Aswin Projects/Personal/Selenium/video to text converter/textify/img/icon.ico"
    gif_path1 = r"D:/Aswin Projects/Personal/Selenium/video to text converter/backblue.gif"
    gif_path2 = r"D:/Aswin Projects/Personal/Selenium/video to text converter/fade.gif"
    log_path = r"D:/Aswin Projects/Personal/Selenium/video to text converter/hts-log.txt"
    html_path = r"D:/Aswin Projects/Personal/Selenium/video to text converter/index.html"
    cache_path = r"D:/Aswin Projects/Personal/Selenium/video to text converter/hts-cache"
    pagead_path = r"D:/Aswin Projects/Personal/Selenium/video to text converter/pagead2.googlesyndication.com"
    textify_path = r"D:/Aswin Projects/Personal/Selenium/video to text converter/textify"
    webpage_path = r"D:/Aswin Projects/Personal/Selenium/video to text converter/webpage"
    app_path = r"D:/Aswin Projects/Personal/Selenium/video to text converter/app.py"

    # Define the PyInstaller command and arguments
    pyinstaller_cmd = [
        'pyinstaller',
        '--noconfirm', '--onefile', '--windowed',
        f'--icon={icon_path}',
        f'--add-data={gif_path1};.',
        f'--add-data={gif_path2};.',
        f'--add-data={log_path};.',
        f'--add-data={html_path};.',
        f'--add-data={cache_path};hts-cache/',
        f'--add-data={pagead_path};pagead2.googlesyndication.com/',
        f'--add-data={textify_path};textify/',
        app_path
    ]

    # Run the PyInstaller command
    print("Running PyInstaller...")
    try:
        subprocess.run(pyinstaller_cmd, check=True)
        print("Build completed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error during build process: {e}")

if __name__ == "__main__":
    run_pyinstaller()
