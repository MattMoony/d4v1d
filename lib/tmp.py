from lib.api import params
import io, os
from typing import Union

def ensure_path(p: str) -> None:
    os.makedirs(p)

def fopen(uname: str, fname: str, mode: str = 'w') -> Union[io.TextIOWrapper, io.BufferedWriter, io.BufferedReader]:
    p: str = os.path.join(params.TMP_PATH, uname, fname)
    ensure_path(p)
    return open(p, mode)

def mkdir(uname: str, dname: str, *dnames: str) -> None:
    ensure_path(os.path.join(params.TMP_PATH, uname, dname, *dnames))

def resolve(uname: str, p: str, *ps: str) -> str:
    return os.path.join(params.TMP_PATH, uname, p, *ps)