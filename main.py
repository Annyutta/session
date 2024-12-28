import subprocess

# Список файлов, которые нужно запустить
files_to_run = [
    "server.py",
    "table.py"
]
for file in files_to_run:
    print(f"Запуск {file}...")
    subprocess.run(["python", file])
