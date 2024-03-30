import os
import sys
import logging
import coloredlogs
from tqdm import tqdm


def get_readme_content(repo_path):
    """
    Получает содержимое файла README.md.

    Args:
        repo_path (str): Путь к папке репозитория.

    Returns:
        str: Содержимое файла README.md, или "README.md не найден.", если файл отсутствует.
    """
    readme_path = os.path.join(repo_path, "README.md")
    if os.path.exists(readme_path):
        try:
            with open(readme_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            logging.warning("Ошибка при чтении README.md: %s", e)
    return "README.md не найден."


def traverse_repo_iteratively(repo_path, ignore_file):
    """
    Итеративно обходит структуру репозитория, возвращая пути к файлам и папкам.

    Args:
        repo_path (str): Путь к папке репозитория.
        ignore_file (str): Путь к файлу игнорирования.

    Yields:
        str: Относительный путь к каждому найденному файлу или папке.
    """
    dirs_to_visit = [(repo_path, "")]
    dirs_visited = set()

    with open(ignore_file, "r", encoding="utf-8") as f:
        ignored_paths = [line.strip() for line in f.readlines() if line.strip()]

    while dirs_to_visit:
        current_path, relative_path = dirs_to_visit.pop()
        dirs_visited.add(relative_path)
        for entry in tqdm(os.listdir(current_path), desc=f"Обработка {relative_path}", leave=False):
            entry_path = os.path.join(current_path, entry)
            entry_relative_path = os.path.join(relative_path, entry)
            if entry_relative_path in ignored_paths:
                continue  # Пропустить игнорируемые файлы/папки
            if os.path.isdir(entry_path):
                if entry_relative_path not in dirs_visited:
                    yield entry_relative_path + "/"  # Возвращаем путь к папке
                    dirs_to_visit.append((entry_path, entry_relative_path))
            else:
                yield entry_relative_path  # Возвращаем путь к файлу


def get_file_contents_iteratively(repo_path, ignore_file):
    """
    Итеративно считывает содержимое файлов, пропуская бинарные файлы и игнорируемые пути.

    Args:
        repo_path (str): Путь к папке репозитория.
        ignore_file (str): Путь к файлу игнорирования.

    Yields:
        tuple: Кортеж, содержащий (путь_к_файлу, содержимое_файла) для каждого небинарного файла.
    """
    binary_extensions = [
        ".exe",  # Исполняемый файл Windows
        ".dll",  # Динамическая библиотека Windows
        ".bin",  # Обычный бинарный файл
        ".dat",  # Данные
        ".img",  # Образ диска
        ".iso",  # Образ оптического диска
        ".pdf",  # Портативный формат документа
        ".jpg",  # Изображение в формате JPEG
        ".png",  # Изображение в формате PNG
        ".gif",  # Изображение в формате GIF
        ".tif",  # Изображение в формате TIFF
        ".bmp",  # Изображение в формате BMP
        ".avi",  # Видеофайл в формате AVI
        ".mp4",  # Видеофайл в формате MP4
        ".mp3",  # Аудиофайл в формате MP3
        ".wav",  # Аудиофайл в формате WAV
        ".zip",  # Архив ZIP
        ".rar",  # Архив RAR
        ".tar",  # Архив TAR
        ".gz",  # Архив GZIP
        ".7z",  # Архив 7-Zip
        # Добавьте другие расширения, если необходимо
    ]

    for file_path in traverse_repo_iteratively(repo_path, ignore_file):
        if any(file_path.endswith(ext) for ext in binary_extensions):
            logging.debug("Пропуск бинарного файла: %s", file_path)
        else:
            try:
                with open(os.path.join(repo_path, file_path), "r", encoding="utf-8") as f:
                    file_content = f.read()
                    yield file_path, file_content
            except Exception as e:
                logging.warning("Ошибка при чтении файла '%s': %s", file_path, e)


def analyze_repo(repo_path, ignore_file="ignore.txt"):
    """
    Анализирует клонированный репозиторий.

    Args:
        repo_path (str): Путь к папке репозитория.
        ignore_file (str): Путь к файлу игнорирования (по умолчанию: "ignore.txt").

    Returns:
        tuple: Кортеж, содержащий (имя_репозитория, инструкции, содержимое_readme, структура_репозитория, содержимое_файлов).
    """
    repo_name = os.path.basename(repo_path)

    coloredlogs.install(level='INFO')

    logging.info("Получение README для: %s", repo_name)
    readme_content = get_readme_content(repo_path)

    logging.info("\nПолучение структуры репозитория для: %s", repo_name)
    repo_structure = f"Структура репозитория: {repo_name}\n"
    for path in traverse_repo_iteratively(repo_path, ignore_file):
        repo_structure += path + "\n"

    logging.info("\nПолучение содержимого файлов для: %s", repo_name)
    file_contents = ""
    for file_path, content in get_file_contents_iteratively(repo_path, ignore_file):
        file_contents += f"Файл: {file_path}\nСодержимое:\n{content}\n\n"

    instructions = f"Prompt: Analyze the {repo_name} repository to understand its structure, purpose, and functionality. Follow these steps to study the codebase:\n\n"

    return repo_name, instructions, readme_content, repo_structure, file_contents


if __name__ == "__main__":
    while True:
        repo_path = input("Введите путь к папке репозитория: ")
        if os.path.isdir(repo_path):
            break
        else:
            logging.error("Некорректный путь к репозиторию. Пожалуйста, введите правильный путь.")

    try:
        repo_name, instructions, readme_content, repo_structure, file_contents = analyze_repo(repo_path, "ignore.txt")
        output_filename = f"{repo_name}_contents.txt"
        with open(output_filename, "w", encoding="utf-8") as f:
            f.write(instructions)
            f.write(f"README:\n{readme_content}\n\n")
            f.write(repo_structure)
            f.write("\n\n")
            f.write(file_contents)
        logging.info("Содержимое репозитория сохранено в '%s'", output_filename)

        # Ожидание нажатия Enter перед закрытием
        input("Нажмите Enter, чтобы закрыть окно...")

    except Exception as e:
        logging.error("Произошла ошибка: %s", e)

    finally:
        # Закрытие окна консоли (специфично для Windows)
        if os.name == 'nt':
            os.system("pause")  # Кратковременная пауза для отображения сообщения
            os.system("cls")  # Очистка консоли
