# Анализ клонированного репозитория

Этот репозиторий содержит скрипт для анализа клонированных репозиториев на GitHub.

## Установка

1. **Клонирование репозитория**: Склонируйте данный репозиторий на свой локальный компьютер с помощью команды:
   ```bash
   https://github.com/DieHardMy/analyzing-a-cloned-repository.git
   ```
2. **Установка зависимостей**:

   ```bash
   pip install tqdm coloredlogs
   ```

## Возможности

1. **Анализ репозитория**: Скрипт `analyze_repo.py` анализирует клонированный репозиторий и извлекает информацию о его структуре, содержимом файлов и README.
2. **Генерация отчета**: После анализа репозитория скрипт создает отчетный файл, содержащий инструкции, содержимое README, структуру репозитория и содержимое файлов.
3. **Игнорирование файлов и папок**: Вы можете указать файл `ignore.txt`, в котором перечислены файлы и папки, которые следует игнорировать при анализе.

## Использование

1. Запустите скрипт `analyze_repo.py`, введите путь к клонированной папке репозитория.
2. Дождитесь завершения анализа.
3. После завершения анализа будет создан отчетный файл в формате `<имя_репозитория>_contents.txt` в корневой директории репозитория.

**Примечание**: Убедитесь, что ваша система поддерживает запуск скриптов Python.