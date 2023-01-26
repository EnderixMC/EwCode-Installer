from colorama import Fore, just_fix_windows_console
from tkinter.filedialog import askdirectory
from threading import Thread
from shutil import rmtree
from ctypes import windll
from tkinter import Tk
from time import sleep
import platform
import sys
import os

__version__ = "0.0.1"
credits = f"Ewcode Uninstaller v{__version__} by EnderixMC (https://github.com/EnderixMC/EwCode-Installer)"

loaded = False
sync = False
def uninstall(path):
    global loaded
    global sync
    rmtree(path)
    ospath = os.environ["PATH"].split(os.pathsep)
    ospath = [*set(ospath)]
    ospath.pop(ospath.index(""))
    if path in ospath:
        ospath.pop(ospath.index(path))
        os.system(f'setx PATH "{os.pathsep.join(ospath)}" > nul')
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
if __name__ == "__main__":
    print(credits, "\n")
    if platform.system() != "Windows":
        print(Fore.RED+"Platform not supported!"+Fore.RESET)
    root = Tk()
    root.withdraw()
    install_dir = os.path.abspath(askdirectory(title="EwCode Uninstaller - Select Installation Directory", initialdir="/"))
    if not install_dir:
        input(Fore.RED+"No directory selected! Press enter to exit..."+Fore.RESET)
        sys.exit()
    print("Selected Directory:", install_dir)
    print(Fore.YELLOW+"\n[Warning]: The entire selected directory will be deleted!"+Fore.RESET)
    if input("Are you sure you want to uninstall? (Y/N) ").lower() == "y":
        print()
        progress_thread = Thread(target=progress_bar,args=("Uninstalling...",))
        progress_thread.start()
        uninstall(install_dir)
        print(Fore.GREEN+"\nEwCode has been uninstalled"+Fore.RESET)
