import os
import subprocess
import shutil


def compress_with_upx(directory):
    for root, dirs, files in os.walk(directory):
        if 'lib' in dirs and 'PyQt5' in dirs and 'Qt5' in dirs and 'translations' in dirs:
            translations_path = os.path.join(root, 'translations')
            shutil.rmtree(translations_path)
            print(f"Deleted translations folder at {translations_path}")
            dirs.remove('translations')

        # 排除指定目录，防止发生PyQt5平台错误
        if 'lib' in root and 'PyQt5' in root and 'Qt5' in root and 'plugins' in root:
            continue

        for file in files:
            if file.endswith(('.exe', '.dll', 'pyd')):
                file_path = os.path.join(root, file)
                try:
                    subprocess.run(['upx', '--best', file_path], check=True)
                    print(f"Compressed: {file_path}")
                except subprocess.CalledProcessError as e:
                    print(f"Failed to compress {file_path}: {e}")


if __name__ == "__main__":
    target_directory = ".\\build\\exe.win-amd64-3.10"
    compress_with_upx(target_directory)
