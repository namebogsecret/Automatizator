import logging
from datetime import datetime
from os import mkdir, makedirs, remove, walk
from os.path import exists, join, getsize
from shutil import make_archive
from time import time

logs_dir = 'logs'

if not exists(logs_dir):
    mkdir(logs_dir)

def write_to_file(error):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open('error.txt', 'a') as f:
        f.write(f"{current_time} - {repr(error)}\n\n")

def archive_large_logs(logs_dir, max_size_mb=10):
    try:
        max_size_bytes = max_size_mb * 1024 * 1024
        for root, dirs, files in walk(logs_dir):
            for file in files:
                if file.endswith('.log'):
                    file_path = join(root, file)
                    if getsize(file_path) > max_size_bytes:
                        archive_dir = join(root, 'archive')
                        if not exists(archive_dir):
                            makedirs(archive_dir)
                        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
                        file_date_str = file.split('_')[0]
                        archive_name = f'{file_date_str}_{timestamp}_large'
                        archive_file = join(archive_dir, f'{archive_name}.zip')
                        make_archive(join(archive_dir, archive_name), 'zip', root, file)
                        remove(file_path)
    except Exception as e:
        logging.error(f"Error archiving large logs: {e}")

def archive_old_logs(logs_dir):
    try:
        today = datetime.now().date()
        for root, dirs, files in walk(logs_dir):
            for file in files:
                if file.endswith('.log'):
                    file_date_str = file.split('_')[0]
                    try:
                        file_date = datetime.strptime(file_date_str, "%Y-%m-%d").date()
                        if file_date < today:
                            archive_dir = join(root, 'archive')
                            if not exists(archive_dir):
                                makedirs(archive_dir)
                            archive_file = join(archive_dir, f'{file_date_str}.zip')
                            if not exists(archive_file):
                                make_archive(join(archive_dir, file_date_str), 'zip', root, file)
                                remove(join(root, file))
                    except ValueError as ve:
                        logging.error(f"Date format error in filename {file}: {ve}")
    except Exception as e:
        logging.error(f"Error archiving old logs: {e}")

def create_handler(log_dir, level, formatter):

    try:
        handler = logging.FileHandler(join(log_dir, f'{datetime.now().strftime("%Y-%m-%d")}_{level}.log'))
        handler.setLevel(logging.getLevelName(level.upper()))
        handler.setFormatter(formatter)
        return handler
    except Exception as e:
        write_to_file(f"Ошибка при создании обработчика: {e}")

def set_logger(logger, logs_dir):
    try:
        component_name = logger.name
        logger.setLevel(logging.DEBUG)

        # Архивация логов перед созданием новых обработчиков
        archive_old_logs(logs_dir)
        archive_large_logs(logs_dir)

        # Создание форматтера для обработчиков
        formatter = logging.Formatter('%(levelname)s:%(asctime)s:%(name)s:%(message)s')

        # Список уровней логирования для создания обработчиков
        levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        for level in levels:
            # Создание директории для уровня логирования, если необходимо
            level_dir = join(logs_dir, level.lower())
            if not exists(level_dir):
                mkdir(level_dir)

            # Создание обработчика для уровня логирования
            handler = create_handler(level_dir, level, formatter)
            logger.addHandler(handler)

        # Проверка и создание директории для компонента
        log_components_dir = join(logs_dir, 'components', component_name)
        if not exists(log_components_dir):
            mkdir(log_components_dir)

        # Создание обработчика для компонента
        file_handler_component = create_handler(log_components_dir, 'DEBUG', formatter)
        logger.addHandler(file_handler_component)

        return logger
    except Exception as e:
        write_to_file(f"Ошибка при настройке логгера: {e}")

# Функция для создания директорий, если они еще не существуют
def ensure_dir(directory):
    if not exists(directory):
        makedirs(directory)

# Функция для настройки логгера
def set_logger_(logger):
    logs_dir = 'logs'
    try:
        # Устанавливаем общий уровень логгера
        logger.setLevel(logging.DEBUG)

        # Форматтер для всех обработчиков
        formatter = logging.Formatter('%(levelname)s:%(asctime)s:%(name)s:%(message)s')

        # Словарь с уровнями логирования и соответствующими папками
        levels_dirs = {
            'DEBUG': 'debug',
            'INFO': 'info',
            'WARNING': 'warning',
            'ERROR': 'error',
            'CRITICAL': 'critical',
        }

        # Создаем обработчики для каждого уровня логирования
        for level, subdir in levels_dirs.items():
            # Полный путь к директории для текущего уровня логирования
            dir_path = join(logs_dir, subdir)
            ensure_dir(dir_path)  # Создаем директорию, если необходимо

            # Полный путь к файлу лога
            file_path = join(dir_path, f'{datetime.now().strftime("%Y-%m-%d")}_{subdir}.log')

            # Создаем и настраиваем обработчик для файла
            handler = logging.FileHandler(file_path)
            handler.setLevel(getattr(logging, level))
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        # Обработчик для записи всех сообщений компонента
        component_name = logger.name
        log_components_dir = join(logs_dir, 'components', component_name)
        ensure_dir(log_components_dir)
        file_handler_component = logging.FileHandler(
            join(log_components_dir, f'{datetime.now().strftime("%Y-%m-%d")}_{component_name}_all.log')
        )
        file_handler_component.setFormatter(formatter)
        logger.addHandler(file_handler_component)

        return logger
    except Exception as e:
        write_to_file(f"Ошибка при настройке логгера: {e}")

# Пропускаем часть с определениями функций, чтобы избежать повторений

# Тесты для проверки функций
import unittest
from unittest.mock import patch, mock_open, MagicMock

class TestLogArchiver(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open)
    def test_write_to_file(self, mock_file_open):
        test_error = "Test error message"
        write_to_file(test_error)
        mock_file_open.assert_called_once_with('error.txt', 'a')
        mock_file_open().write.assert_any_call(test_error)

    @patch('log_archiver.getsize')
    @patch('log_archiver.make_archive')
    @patch('log_archiver.remove')
    @patch('log_archiver.walk')
    def test_archive_large_logs(self, mock_walk, mock_remove, mock_make_archive, mock_getsize):
        mock_getsize.return_value = 1024 * 1024 * 11  # Возвращаем размер файла, который больше максимального
        mock_walk.return_value = [('/some/dir', ['subdir'], ['file.log'])]
        
        archive_large_logs('/some/dir', max_size_mb=10)
        
        mock_make_archive.assert_called_once()
        mock_remove.assert_called_once()

    @patch('os.walk')
    @patch('os.remove')
    @patch('shutil.make_archive')
    @patch('datetime.datetime')
    def test_archive_old_logs(self, mock_datetime, mock_make_archive, mock_remove, mock_walk):
        mock_datetime.now.return_value = datetime(2020, 1, 2)
        mock_walk.return_value = [('/some/dir', ('subdir',), ('2020-01-01_file.log',))]
        archive_old_logs('/some/dir')
        mock_make_archive.assert_called_once()
        mock_remove.assert_called_once_with('/some/dir/2020-01-01_file.log')

    @patch('logging.FileHandler')
    def test_create_handler(self, mock_file_handler):
        mock_formatter = MagicMock()
        handler = create_handler('/some/dir', 'DEBUG', mock_formatter)
        self.assertTrue(handler)

    @patch('__main__.create_handler')
    def test_set_logger(self, mock_create_handler):
        mock_logger = MagicMock()
        mock_logger.name = 'test_logger'
        set_logger(mock_logger, 'logs')
        self.assertEqual(mock_create_handler.call_count, 5)
        mock_logger.addHandler.assert_called()

# Этот блок позволяет запустить тесты, если скрипт выполняется напрямую
if __name__ == '__main__':

    unittest.main(exit=False)
