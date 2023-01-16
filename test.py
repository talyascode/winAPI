import os
import time
import win32process as w


def main():
    # run from terminal:  python.exe test.py
    # os.remove('database')

    startupinfo = w.STARTUPINFO()
    print(
        w.CreateProcess(None, "python.exe main.py get color blue", None, None, False, 0, None, None,
                        # 0-> w.CREATE_NEW_CONSOLE
                        startupinfo))
    print(
        w.CreateProcess(None, "python.exe main.py set 10000", None, None, False, 0, None, None,
                        # 0-> w.CREATE_NEW_CONSOLE
                        startupinfo))  # set num --> starting to set 600 (key:val) from num
    print(
        w.CreateProcess(None, "python.exe main.py delete 1000", None, None, False, 0, None, None,
                        # 0-> w.CREATE_NEW_CONSOLE
                        startupinfo))  # delete num --> starting to delete 600 (key:val) from num
    input("Press enter to end process")

    # TODO: waitforsingleobject to wait for all processes to finish before checking the data


if __name__ == '__main__':
    main()

