import subprocess
from tools import asadminrunner as admin
import proj_strings as prstr
from tools import pathfinder as finder


def main():
    steam_path = finder.find_steam_path()
    subprocess.call(fr'{steam_path}\Steam.exe -applaunch {prstr.app_id}')

if __name__ == "__main__":
    if not admin.isUserAdmin(): 
        admin.runAsAdmin()
    else: 
        main()