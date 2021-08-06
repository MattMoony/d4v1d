import os.path

BASE_PATH: str = os.path.abspath(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..'))
TMP_PATH: str = os.path.abspath(os.path.join(BASE_PATH, 'tmp'))
SRV_PATH: str = os.path.abspath(os.path.join(BASE_PATH, 'server'))
DATA_PATH: str = os.path.abspath(os.path.join(BASE_PATH, 'data'))
LIB_PATH: str = os.path.abspath(os.path.join(BASE_PATH, 'lib'))