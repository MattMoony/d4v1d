from lib.api import params
import time

def pause() -> None:
    time.sleep(params.PAUSE_TIME)