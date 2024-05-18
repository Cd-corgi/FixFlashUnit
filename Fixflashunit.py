from ctypes import *
import os
import ctypes
import string
import shutil
import readchar as key
import time
import subprocess
from bitmath import Byte
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

# (Windows) Detect all removable drives in Windows

def detect_rm_devices():
    try:
        wmi = ctypes.windll.kernel32.GetLogicalDrives()
        all_drives = [letter for i, letter in enumerate(string.ascii_uppercase) if wmi & (1 << i)]
        rm_ones = [letter + ":\\" for letter in all_drives if ctypes.windll.kernel32.GetDriveTypeW(letter + ":") == 2]
        return rm_ones
    except Exception as e:
        print(e)
        return None

# (Windows) get details of the mounted drives

def getDetailsDrives(driveList: list):
    detailedList = []
    try:
        for ll in driveList:
            drv = shutil.disk_usage(ll)
            drvByte = Byte(drv.total)
            KB = 1024
            MB = KB ** 2
            GB = KB ** 3
            TB = KB ** 4
            if drvByte < KB:
                detailedList.append(f"{ll}{"."*15}{drv} Bytes")
            elif drvByte < MB:
                drvF = f"{drvByte / KB}"
                detailedList.append(f"{ll}{"."*15}{drvF:.5} KB")
            elif drvByte < GB:
                drvF = f"{drvByte / MB}"
                detailedList.append(f"{ll}{"."*15}{drvF:.5} MB")
            elif drvByte < TB:
                drvF = f"{drvByte / GB}"
                detailedList.append(f"{ll}{"."*15}{drvF:.5} GB")
            else:
                drvF = f"{drvByte / TB}"
                detailedList.append(f"{ll}{"."*15}{drvF:.5} TB")  
        return detailedList
    except Exception as e:
        print(e)
        os.system("exit()")
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
    print("FixFlashUnit v 1.0.3 By cd-corgi")
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
            while blank(unit) == True:
                devs = list(detect_rm_devices())
                if len(devs) < 1:
                    print("There's not drives to select... Please plug in one.")
                    key2conti()
                    return os.system("exit()")
                print("Select an unit drive to rescue (ONLY THE DAMAGED ONE)\n")
                print("==================================================")
                print("||\tChoose a drive to repair\t\t||")
                print("==================================================")
                print("||\t"+"\t\t||\n||\t".join(getDetailsDrives(devs))+"\t\t||")
                print("==================================================")
                print("\nType 'cancel' to exit/cancel the process.\n")
                unit = str(input("\n>> "))
                if unit == "cancel":
                    os.system("cls")
                    print("==============================================")
                    print("The process just got cancelled.")
                    print("==============================================")
                    key2conti()
                    return os.system("exit()")
                if blank(unit):
                    os.system("cls")
                    print("The unit letter should be given!")
                    key2conti()
            pathTarget = f"{unit}:\\"
            if pathTarget not in devs:
                print("\n==================================================")
                print("The selected drive to repair doesn't exists...")
                key2conti()
                os.system("exit()")
            else:
                print("Starting the fixing process ...")
                setTimeout(2.5)
                os.system("cls")
                os.system(f"chkdsk /F {unit}:")
                if os.path.exists(pathTarget):
                    try:
                        os.chdir(pathTarget)
                        os.system(f"start {pathTarget}")
                        print("The drive is working now!")
                    except FileNotFoundError as e:
                        print(f"Error: {e}")
                        return
                    except Exception as e:
                        print(f"Error: {e}")
                        return
                else:
                    return
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
