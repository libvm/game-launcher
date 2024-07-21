import winreg as reg
import proj_strings as prstr
from tools import acfparser as acf
def find_steam_path():
    """
    Ищет каталог по записи из реестра, в котором находится Steam.exe
    :return: None or str
    """
    with reg.ConnectRegistry(None, reg.HKEY_LOCAL_MACHINE) as hkey:
        with reg.OpenKeyEx(hkey, prstr.steam_key) as key:
            value = reg.QueryValueEx(key, 'InstallPath')[0]
            return value
        
def find_game_dir(steam_path: str, app_id):
    """
    Ищет каталог по app_id, в котором находится исполняемый файл игры
    :param steam_path: the path to the steam main folder, where Steam.exe is stored
    :param app_id: app id of the game, which is assigned by Steam
    :return: None or str
    """
    with open(fr'{steam_path}\steamapps\appmanifest_{app_id}.acf', 'r') as f:
        return acf.AcfNode(f)['AppState']['installdir']