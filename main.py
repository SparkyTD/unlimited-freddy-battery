import time
import pymem
import traceback
from pymem import *
from pymem.process import *
from enum import Enum
import os
import keyboard


class ConsoleColor:
    HEADER = '\\033[95m'
    OKBLUE = '\\033[94m'
    OKCYAN = '\\033[96m'
    OKGREEN = '\\033[92m'
    WARNING = '\\033[93m'
    FAIL = '\\033[91m'
    ENDC = '\\033[0m'
    BOLD = '\\033[1m'
    UNDERLINE = '\\033[4m'


class Error(Enum):
    NONE = 0
    NOT_INITIALIZED = 1
    GAME_NOT_FOUND = 2
    ADDRESS_NOT_FOUND = 3


class FreddyProcess:
    __PROCESS_NAME = "fnaf9-Win64-Shipping.exe"
    __MAIN_OFFSETS = [0x0403AB30, 0x60, 0x9A8, 0x240, 0x50]
    __BATTERY_OFFSET = 0xB8

    def __init__(self):
        self.__loaded = False
        self.__proc = None
        self.__game_module = None
        self.__module_address = None
        self.__battery_address = None
        self.__error = Error.NOT_INITIALIZED

    def init(self):
        try:
            self.__proc = pymem.Pymem(self.__PROCESS_NAME)
            self.__game_module = module_from_name(self.__proc.process_handle, self.__PROCESS_NAME)
            self.__module_address = self.__game_module.lpBaseOfDll
            self.__battery_address = self.__get_battery_address()
            self.__loaded = True
            self.__error = Error.NONE
        except pymem.exception.MemoryReadError:
            self.__loaded = False
            self.__error = Error.ADDRESS_NOT_FOUND
        except pymem.exception.ProcessNotFound:
            self.__loaded = False
            self.__error = Error.GAME_NOT_FOUND

    def __get_address(self, base, offsets):
        address = base
        for o in offsets:
            address = self.__proc.read_ulonglong(address + o)
        return address

    def __get_battery_address(self):
        return self.__get_address(self.__module_address, self.__MAIN_OFFSETS) + self.__BATTERY_OFFSET

    def get_battery_counter(self):
        try:
            return self.__proc.read_uint(self.__battery_address)
        except pymem.exception.PymemError:
            self.__loaded = False
            return None

    def get_battery_level(self):
        return self.get_battery_counter() // 20 + 1

    def set_battery_counter(self, value):
        try:
            value = min(100, max(0, value))
            self.__proc.write_uint(self.__battery_address, value)
        except pymem.exception.PymemError:
            self.__loaded = False

    def set_battery_level(self, level):
        level = min(5, max(0, level))
        self.set_battery_counter(max(0, level * 20 - 1))

    def is_loaded(self):
        return self.__loaded

    def get_error(self):
        return self.__error


class FirmwareCorruptException(Exception):
    pass


class BotNotFoundException(Exception):
    pass


def print_logo():
    print(" ___ __  ___ __ ___  __  ___   ___ __  _ _____ ___ ___ _____ __  _ __  _ __ __ ___ __  _ _____ ")
    print("| __/  \\|_  |  \\ __|/  \\| _ \\ | __|  \\| |_   _| __| _ \\_   _/  \\| |  \\| |  V  | __|  \\| |_   _|")
    print("| _| /\\ |/ /| -< _|| /\\ | v / | _|| | ' | | | | _|| v / | || /\\ | | | ' | \\_/ | _|| | ' | | |  ")
    print("|_||_||_|___|__/___|_||_|_|_\\ |___|_|\\__| |_| |___|_|_\\ |_||_||_|_|_|\\__|_| |_|___|_|\\__| |_|  ")
    print("Bot Console [Infinite Freddy Time] v1.0")
    print(" by Sparky [u/Sparky2199; github.com/SparkyTD]")
    print("(Press Ctrl+C to exit)\n")


def print_log(text, delay=0.0):
    print(text)
    time.sleep(delay)


def print_intro():
    print_logo()
    print_log("Connecting to corporate network...", 1)
    print_log("Accessing bot control server...", 0.3)
    print_log("Indexing animatronic database...", 0.8)
    print_log(" > SELECT * FROM FAZ_BOTS WHERE type = 'GLAMROCK';", 0.2)

    bot_ids = ["FAZ_BOT_FR_FBEAR", "FAZ_BOT_GL_CHICA", "FAZ_BOT_MG_GATOR", "FAZ_BOT_RX_WOLF", "FAZ_BOT_GL_BONNIE"]
    for i in range(1, 50):
        bot_ids.append("FAZ_BOT_ENDO_" + str(i))
    bot_ids.append("FAZ_BOT_BL_UNKNOWN")
    bot_ids.append("FAZ_BOT_WA_UNKNOWN")

    ip = 1
    for bot in bot_ids:
        if bot == "FAZ_BOT_GL_BONNIE":
            print_log(f"Found '{bot}' at [TIMEOUT]", 1)
            try:
                raise BotNotFoundException()
            except BotNotFoundException as e:
                traceback.print_exc()
            time.sleep(1)
        else:
            print_log(f"Found '{bot}' at 10.0.1.{ip}")
        ip += 1

    try:
        raise FirmwareCorruptException()
    except FirmwareCorruptException as e:
        traceback.print_exc()

    print_log("Connecting to FAZ_BOT_FR_FBEAR...", 1)
    print_log("Connected!", 0.7)

    os.system("cls")
    print_logo()


if __name__ == '__main__':

    freddy = FreddyProcess()
    while True:
        freddy.init()
        countdown = 5
        if freddy.is_loaded():
            print_intro()
        while freddy.is_loaded():
            sys.stdout.write(f"Recharging battery in {countdown}...\r")
            sys.stdout.flush()
            if countdown == 0:
                freddy.set_battery_counter(100)
                sys.stdout.write("Recharged!                                   \r")
                sys.stdout.flush()
                countdown = 6
            countdown -= 1
            # freddy.set_battery_counter(100)
            time.sleep(1)
        if not freddy.is_loaded():
            error = freddy.get_error()
            os.system("cls")
            print_logo()
            print(f"Connection lost! ({error})")
            if error == Error.GAME_NOT_FOUND:
                print("The game does not appear to be running.")
            elif error == Error.ADDRESS_NOT_FOUND:
                print("Unable to find Freddy's battery. If you're in the menu, load a save first.")
                print("If that still doesn't work, check if there is an updated Bot Console at https://github.com/SparkyTD/infinite-freddy-time")
            freddy.init()
            time.sleep(10)
