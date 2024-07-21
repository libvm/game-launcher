import requests as rq
import subprocess
import proj_strings as prstr
import tools.pathfinder as finder
import os
import run_game
       
def download_and_apply_reg():
    steam_path = finder.find_steam_path()  
    game_dir = finder.find_game_dir(steam_path, prstr.app_id)
    response = rq.get(prstr.url) # HTTP GET

    filename = f'{steam_path}\steamapps\common\{game_dir}\settings.reg' # путь к reg файлу

    if response.status_code == 200:
        with open(filename, 'wb') as file:
            file.write(response.content) # сохраняем файл в каталог с игрой
    else:
        raise TypeError('GET FAILED')
    
    subprocess.call(['reg', 'import', filename]) # обновляем значения в выбранном ключе реестра

def main():
    download_and_apply_reg()
    run_game_path = os.path.abspath(run_game.__file__)
    subprocess.call(['Python', f'{run_game_path}']) # запускаем игру через дочерний скрипт

if __name__ == "__main__":
    main()