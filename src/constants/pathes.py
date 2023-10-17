# src/constants/pathes.py

from os.path import join, abspath
from logging import getLogger

from src.log_scripts import set_logger

# logger setup
logger = getLogger(__name__)
logger = set_logger(logger)

# Получение абсолютного пути проекта
project_path = abspath('.')
stop_file = join('files', 'stop.txt')
logger.debug('Project path: %s', project_path)
# Соединение пути с файлом базы данных
#db_path = join(project_path, 'files', 'repetitors.db')
db_path = join('files', 'repetitors.db')
logger.debug('Database path: %s', db_path)