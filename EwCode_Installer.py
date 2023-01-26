from colorama import Fore, just_fix_windows_console
from urllib.request import urlretrieve, urlopen
from tkinter.filedialog import askdirectory
from threading import Thread
from zipfile import ZipFile
from random import choice
from ctypes import windll
from tkinter import Tk
from time import sleep
import platform
import json
import sys
import os

__version__ = "0.0.1"
credits = f"Ewcode Installer v{__version__} by EnderixMC (https://github.com/EnderixMC/EwCode-Installer)"

loaded = False
sync = False
def download(path):
    global loaded
    global sync
    url = "https://api.github.com/repos/EnderixMC/EwCode/releases/tags/v1.0.0-beta"
    try:
        with urlopen(url) as conn:
            url = json.loads(conn.read().decode("utf8"))["assets_url"]
        with urlopen(url) as conn:
            url = json.loads(conn.read().decode("utf8"))[0]["browser_download_url"]
        urlretrieve(url,os.path.join(path,"ewcode.zip"))
    except Exception as e:
        loaded = True
        while not sync:
            sleep(0.01)
            if sync:
                break
        print(Fore.RED+"Download failed:", e+Fore.RESET)
        sys.exit()
    loaded = True
    while not sync:
        sleep(0.01)
        if sync:
            break

def install(path):
    global options
    global loaded
    global sync
    try:
        with ZipFile(os.path.join(path,"ewcode.zip")) as z:
            z.extractall(path)
        os.remove(os.path.join(path,"ewcode.zip"))
        if options["add_to_path"]:
            os.system(f'setx PATH "{os.environ["PATH"]+os.pathsep+path}" > nul')
    except Exception as e:
        loaded = True
        while not sync:
            sleep(0.01)
            if sync:
                break
        print(Fore.RED+"Install failed:", e+Fore.RESET)
        sys.exit()
    loaded = True
    while not sync:
        sleep(0.01)
        if sync:
            break

def progress_bar(text):
    global loaded
    global sync
    while not loaded:
        for c in ['-','\\','|','/']:
            sys.stdout.write(f"\r{text} " + c)
            sys.stdout.flush()
            if loaded:
                break
            sleep(0.2)
    sys.stdout.write(f"\r{text} done!")
    sys.stdout.flush()
    print()
    sync = True

windll.shcore.SetProcessDpiAwareness(1)
just_fix_windows_console()
options = {}
if __name__ == "__main__":
    print(credits, "\n")
    if platform.system() != "Windows":
        print(Fore.RED+"Platform not supported!"+Fore.RESET)
    root = Tk()
    root.withdraw()
    install_dir = askdirectory(title="EwCode Installer - Select Installation Directory", initialdir="/")
    if not install_dir:
        input(Fore.RED+"No directory selected! Press enter to exit..."+Fore.RESET)
        sys.exit()
    if len(os.listdir(install_dir)) != 0:
        try:
            if not sys.argv[1] == "-f":
                print(Fore.RED+"Directory not empty!"+Fore.RESET)
                sys.exit()
        except IndexError:
            print(Fore.RED+"Directory not empty!"+Fore.RESET)
            sys.exit()
    print("Selected Directory:", install_dir)
    print("\nOptions: (Y/N)")
    options["add_to_path"] = True if input(" *Add to PATH: ").lower() == "y" else False
    if input("\nAre you sure you want to install? (Y/N) ").lower() == "y":
        print()
        progress_thread = Thread(target=progress_bar,args=("Downloading...",))
        progress_thread.start()
        download(install_dir)
        loaded = False
        sync  = False
        progress_thread = Thread(target=progress_bar,args=("Installing...",))
        progress_thread.start()
        install(install_dir)
        print("\nInstallation complete")
    else:
        print("\nExiting...")