"""
Author: Talya Gross
test file
"""
import os
import time
import win32event
import win32process as w
from fileDatabase import *
MAX_TIMEOUT = -1


def create_data():
    """
    creating the data
    """
    db = FileDatabase()
    for i in range(0, 1000):
        assert db.set_value(str(i), "c")
    assert db.set_value("color", "blue")


def check_data():
    """
    checking that the data didn't change after the processes finished.
    """
    db = FileDatabase()
    for i in range(0, 1000):
        assert db.get_value(str(i)) == "c"
    assert db.get_value("color") == "blue"


def main():
    """
    the main function, creating the processes for the get set and delete functions by running the main.py and sending it
    the function to run by string variables. waiting for the processes to end and then checking the data.
    """
    # os.remove("database")
    create_data()

    startupinfo = w.STARTUPINFO()
    g = w.CreateProcess(None, "python.exe main.py get color blue", None, None, False, 0, None, None,  startupinfo)
    # 0-> w.CREATE_NEW_CONSOLE

    s = w.CreateProcess(None, "python.exe main.py set 10000", None, None, False, 0, None, None, startupinfo)
    # set num --> starting to set 600 (key:val) from num

    d = w.CreateProcess(None, "python.exe main.py delete 1000", None, None, False, 0, None, None, startupinfo)
    # delete num --> starting to delete 600 (key:val) from num

    wait_list = [g[0], s[0], d[0]]
    r = win32event.WaitForMultipleObjects(wait_list, True, MAX_TIMEOUT)  # waiting for the processes
    # checking that every process succeeded and finished by checking the return value in r
    if win32event.WAIT_OBJECT_0 <= r < win32event.WAIT_OBJECT_0 + len(wait_list):
        check_data()
        print('test: Done')
    else:
        raise Exception(f'error: wait failed {r}')


if __name__ == '__main__':
    main()

