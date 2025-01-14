import os
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox
import ctypes

def is_admin():
    """Проверяет, запущен ли скрипт от имени администратора."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    """Перезапускает скрипт от имени администратора."""
    if not is_admin():
        try:
            script_path = os.path.abspath(__file__)
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, script_path, None, 1)
            sys.exit() # Exit текущий запуск
        except Exception as e:
             messagebox.showerror("Ошибка", f"Не удалось перезапустить скрипт от имени администратора:\n{e}")
             sys.exit() # Exit текущий запуск


def set_ownership_and_access(path):
    """Изменяет владельца и права доступа к указанному файлу/папке."""

    if not os.path.exists(path):
        messagebox.showerror("Ошибка", f"Путь '{path}' не существует.")
        return

    try:
        # 1. Изменение владельца
        print(f"Изменение владельца для '{path}'...")
        takeown_process = subprocess.run(['takeown', '/F', path, '/R', '/D', 'Y'],
                                        check=True, capture_output=True, text=True)
        print(takeown_process.stdout)

        # 2. Предоставление полного доступа администраторам
        print(f"Настройка прав доступа для '{path}'...")
        icacls_process = subprocess.run(['icacls', path, '/grant', 'administrators:F', '/T'],
                                        check=True, capture_output=True, text=True)
        print(icacls_process.stdout)

        messagebox.showinfo("Успех", f"Владелец и права доступа для '{path}' изменены.")


    except subprocess.CalledProcessError as e:
        messagebox.showerror("Ошибка", f"Ошибка при изменении владельца или прав доступа для '{path}':\n{e.stderr}")

def browse_file_or_folder():
    """Открывает диалог выбора файла/папки."""
    filename = filedialog.askdirectory(title="Выберите папку")
    if filename:
        path_entry.delete(0, tk.END)
        path_entry.insert(0, filename)

def process_path():
    """Обрабатывает выбранный путь."""
    path = path_entry.get()
    if path:
        set_ownership_and_access(path)
    else:
        messagebox.showerror("Ошибка", "Пожалуйста, выберите папку.")


if __name__ == "__main__":
    import sys # Добавляем модуль sys здесь
    if not is_admin():
        run_as_admin()

    # Настройка главного окна
    window = tk.Tk()
    window.title("Изменение прав доступа")
    window.geometry("400x200")

    # Заголовок
    header_label = tk.Label(window, text="Выберите путь к папке", font=("Arial", 12))
    header_label.pack(pady=10)

    # Текстовое поле для пути
    path_entry = tk.Entry(window, width=50)
    path_entry.pack(pady=5)

    # Кнопка для выбора пути
    browse_button = tk.Button(window, text="Обзор...", command=browse_file_or_folder)
    browse_button.pack(pady=5)

    # Кнопка для обработки пути
    process_button = tk.Button(window, text="Изменить права доступа", command=process_path)
    process_button.pack(pady=10)


    # Метка для авторства иконки (внизу окна)
    attribution_label = tk.Label(window,
                                text="Иконка: Flaticon.com, UIcons",
                                font=("Arial", 8),
                                fg="gray")
    attribution_label.pack(pady=5, side="bottom")



    # Запуск главного цикла обработки событий
    window.mainloop()
