import os
import subprocess

def build_executable():
    # Define paths
    project_dir = r"D:\Aswin Projects\Personal\Selenium\video to text converter"
    main_script = os.path.join(project_dir, "Textify.py")
    icon_path = os.path.join(project_dir, "static", "img", "icon.ico")
    static_dir = os.path.join(project_dir, "static")
    templates_dir = os.path.join(project_dir, "templates")

    # Construct the PyInstaller command
    pyinstaller_cmd = [
        "pyinstaller",
        "--noconfirm",
        "--onefile",
        "--windowed",
        f"--icon={icon_path}",
        f"--add-data={static_dir};static/",
        f"--add-data={templates_dir};templates/",
        main_script
    ]

    # Run the PyInstaller command
    try:
        print("Building executable...")
        subprocess.run(pyinstaller_cmd, check=True)
        print("Build completed successfully. Check the 'dist' directory for the executable.")
    except subprocess.CalledProcessError as e:
        print(f"Build failed: {e}")

if __name__ == "__main__":
    build_executable()
