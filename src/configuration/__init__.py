
import sys
from os.path import dirname, abspath

from .read_strings_from_file import read_strings_from_file
from .read_dictionaries_from_file import read_dictionaries_from_file
from .get_api import get_api

if getattr(sys, 'frozen', False):
    src_path = sys._MEIPASS
else:
    src_path = dirname(abspath(__file__))
sys.path.append(src_path)
