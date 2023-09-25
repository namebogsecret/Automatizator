#import psutil
import os

def how_many_files():
    return
    """ pid = os.getpid()
    for proc in psutil.process_iter(['pid', 'name', 'open_files']):
        try:
            if proc.pid == pid:
                files = proc.open_files()
                if files:
                    print(f"Process {proc.name()} (PID {proc.pid}) has{len(files)} open files:")
                    #for file in files:
                        #print(f"\t- {file.path}")
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    """