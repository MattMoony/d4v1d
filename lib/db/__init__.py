import os, json
import lib.params
from lib.misc import print_wrn
from lib.db.dbc import DBController
from lib.db.sqlitec import SQLiteController
from typing import *

"""A list of all configured DB controllers"""
CONTROLLERS: List[DBController] = []

"""A list of all available controller types"""
CONTROLLER_TYPES: List[Type] = [ SQLiteController, ]

def controller_type(name: str) -> Optional[Type]:
    """Get a controller type by its name"""
    try:
        return next(filter(lambda c: c.__name__ == name, CONTROLLER_TYPES))
    except StopIteration:
        return None

def reset_config():
    """Reset the configuration stored on the hard disk"""
    with open(os.path.join(lib.params.LIB_PATH, 'db', 'controllers.json'), 'w') as f:
        json.dump([], f)

def write_config():
    """Write the configuration for the current controllers to disk"""
    with open(os.path.join(lib.params.LIB_PATH, 'db', 'controllers.json'), 'w') as f:
        json.dump([c.json() for c in CONTROLLERS], f)

def init():
    """Initializes the CONTROLLERS list with the values stored on the hard disk"""
    global CONTROLLERS
    contr_p: str = os.path.join(lib.params.LIB_PATH, 'db', 'controllers.json')
    if not os.path.isfile(contr_p):
        reset_config()
        return
    with open(contr_p, 'r') as f:
        try:
            contr: List[Dict[str, Any]] = json.load(f)
            if type(contr) != list:
                raise json.decoder.JSONDecodeError()
        except json.decoder.JSONDecodeError:
            print_wrn('Corrupted db controllers config', 'Resetting it ... ')
            reset_config()
            return
        # TODO: PROBABLY NEED TO RE-WRITE THE FOLLOWING AS IT'S PROBABLY NOT THE BEST IDEA TO HAVE SUCH
        # TODO: LOOSE RESTRICTIONS ON "CODE EXECUTION" FROM CONFIG FILES ... 
        for c in contr:
            cc: DBController = controller_type(c['type']).unjson(c)
            if not cc.healthy():
                print(cc)
                del CONTROLLERS[CONTROLLERS.index(cc)]

def register_controller(c: DBController) -> None:
    """Registers a new DB Controller, both in memory and on disk"""
    global CONTROLLERS
    if c not in CONTROLLERS:
        CONTROLLERS.append(c)
        write_config()

if __name__ != '__main__':
    init()
