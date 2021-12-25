import os
import time
import pymem
import traceback
from pymem import *
from pymem.process import *
from enum import Enum
import colorama
from colorama import Fore, Style


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


def print_header():
    print(Fore.GREEN + "Unlimited Freddy Battery v1.0 by Sparky [u/Sparky2199; github.com/SparkyTD]")
    print(Fore.LIGHTBLACK_EX + "(Press Ctrl+C to exit)\n")


if __name__ == '__main__':
    try:
        freddy = FreddyProcess()
        while True:
            freddy.init()
            countdown = 5
            os.system("cls")
            print_header()
            while freddy.is_loaded():
                sys.stdout.write(Fore.BLUE + f"Recharging battery in {countdown}...\r")
                sys.stdout.flush()
                if countdown == 0:
                    freddy.set_battery_counter(100)
                    sys.stdout.write(Fore.GREEN + "Recharged!                                   \r")
                    sys.stdout.flush()
                    countdown = 6
                countdown -= 1
                # freddy.set_battery_counter(100)
                time.sleep(1)
            if not freddy.is_loaded():
                error = freddy.get_error()
                os.system("cls")
                print_header()
                # print(Fore.RED + f"Connection lost! ({error})")
                if error == Error.GAME_NOT_FOUND:
                    print(Fore.RED + "The game does not appear to be running.")
                elif error == Error.ADDRESS_NOT_FOUND:
                    print(Fore.RED + "Unable to find Freddy's battery. If you're in the menu, load a save slot first.")
                    print(Fore.RED + "If that still doesn't work, check if there is an updated Bot Console at https://github.com/SparkyTD/infinite-freddy-time")
                freddy.init()
                time.sleep(10)
    except KeyboardInterrupt:
        print(Fore.WHITE + "Exiting...")
        sys.exit(0)
