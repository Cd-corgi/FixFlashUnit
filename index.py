from ctypes import *
import os
import readchar as key
import time
import subprocess
from platform import system


# Defines if the app runs as admin!
def is_admin():
    try:
        return windll.shell32.IsUserAnAdmin() != 0
    except AttributeError:
        return False


# Make the console gets in timeout!
def setTimeout(ms: float):
    time.sleep(ms)


# Returns a boolean if the string is empty
def blank(un: str) -> bool:
    return not un.strip()


# Make the classic "Press any key to continue"
def key2conti():
    print("\n\nPress Any key to continue...")
    key.readchar()
    if system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")


# Verify the Operative System
def checkSO() -> int:
    if system() == "Linux":
        return 0
    if system() == "Windows":
        return 1


# Verify if the machine has python installed
def verifyPython():
    try:
        subprocess.check_output(["python", "--version"], stderr=subprocess.STDOUT)
        os.system("pip install -r requirements.txt")
        if system() == "Windows":
            os.system("cls")
        else:
            os.system("clear")
        return
    except subprocess.CalledProcessError:
        print("It seems like you have not python installed in your machine...")
        print("")
        print("Please visit https://www.python.org/ and install the latest version!")
        key2conti()
        os.system("exit()")
        return


# Validate the path target
def validatePath(un: str, pat: str) -> bool:
    try:
        if "/" in pat:
            raise ValueError("The following path has illegal characters (\\ or /)")
            key2conti()
        else:
            os.chdir(pat)
            print("The drive is accesible now!")
    except FileNotFoundError:
        print(f"The drive {un}: couldn't be found!")
        return
    except PermissionError:
        print(f"The drive {un}: has not enough permissions!")
        return
    except ValueError as e:
        print(f"The drive {un}: {e}")
        return


# (Only 4 Linux) Returns a dictionary that it shows every removable drive.
def detectPathDestiny(unit: str):
    try:
        output = subprocess.check_output(["df", "--exclude-type=tmpfs", "--exclude-type=ext4", "-T"])
        dec = output.decode("utf-8")
        lines = dec.splitlines()
        plugged_devices = {}
        for line in lines[1:]:
            parts = line.split()
            device = parts[0]
            fs = parts[1]
            if fs == "vfat":
                if device not in plugged_devices:
                    plugged_devices[device] = []
                filterWS = line.split(" ")
                filtrerOPT = list(filter(lambda ln: len(ln) >= 1 and "/" in ln, filterWS))
                for give in filtrerOPT:
                    plugged_devices[device].append(give)
        if f"/dev/{unit}" in plugged_devices:
            return plugged_devices
        else:
            return plugged_devices            
    except subprocess.CalledProcessError as e:
        return None


# Main programm process
def main():
    unit = ""
    verifyPython()
    so = checkSO()
    print("FixFlashUnit v 1.0.0 By cd-corgi")
    print("")
    print(
        "This is a tiny application that can make an attempt to repair an inaccessible drive.\nBe careful when selecting a drive to repair...\nIf you choose an already functional drive,\nyour files may be formatted (a possibility) But it fulfills its function of repairing and leaving the app functional"
    )
    setTimeout(2.5)
    key2conti()
    if so == 0:
        while blank(unit) == True:
            os.system("clear")
            os.system("sudo -v")
            os.system("clear")
            print("Please provide one of the valid Flash unit to rescue:")
            print("")
            print("=========================================")
            print("")
            os.system("df --exclude-type=tmpfs --exclude-type=ext4 -T")
            print("")
            print("=========================================")
            print("")
            print(
                "Please write the Filesystem's last route name to select the media.\n\nExample: sbd, sdc1, sdd\n\n"
            )
            unit = str(input(">> "))
            if blank(unit):
                print(
                    "You didn't selected any Filesystem name to repair... Try again..."
                )
                key2conti()
        try:
            os.system("clear")
            print("It should take a while.. Please wait.")
            setTimeout(3)
            os.system("clear")
            lista = detectPathDestiny(unit)
            if f"/dev/{unit}" not in lista:
                print("Error!\n\nThe selected Filesystem is not valid or exists... Aborting program...")
                key2conti()
                return os.system("exit()")
            else:
                os.system(f"sudo fsck -p -y -v /dev/{unit}")
                print("=========================================")
                key2conti()
                for check in lista:
                    if check == f"/dev/{unit}":
                        try:
                            if os.path.exists(lista[check][1]):
                                os.chdir(lista[check][1])
                                print(f"The device with the path '{lista[check][1]}' is working again!")
                        except FileNotFoundError as e:
                            print(e)
                            os.system("exit()")
                        except FileExistsError as e:
                            print(e)
                            os.system("exit()")
            return
        except Exception as e:
            print(e)
            key2conti()
            os.system("exit()")
    elif so == 1:
        os.system("cls")
        unit = ""
        if is_admin():
            unit = str(input("Select an unit drive to rescue (ONLY THE DAMAGED ONE): "))
            if blank(unit):
                os.system("cls")
                print("The unit letter should be given!")
                key2conti()
                os.system("exit()")
            else:
                print("Starting the fixing process ...")
                setTimeout(2.5)
                os.system("cls")
                os.system(f"chkdsk /f {unit}:")
                os.system("cls")
                pathTarget = f"{unit}:\\"
                validatePath(unit, pathTarget)
                key2conti()
                os.system("exit()")
        else:
            os.system("cls")
            print("This app only works with administrator!")
            key2conti()
            os.system("exit()")
            return
    else:
        print("This system couldn't run this program: No Operative System Supported")
        return


main()
