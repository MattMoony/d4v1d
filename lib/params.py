import os.path

BASE_PATH = os.path.abspath(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..'))
TMP_PATH = os.path.abspath(os.path.join(BASE_PATH, 'tmp'))
SRV_PATH = os.path.abspath(os.path.join(BASE_PATH, 'server'))
DATA_PATH = os.path.abspath(os.path.join(BASE_PATH, 'data'))