"""
Author: Talya Gross
main file
"""
import time
from syncDatabase import SyncDatabase
import sys

MODE = True


def get(db, key, val):
    """
    the function gets the value for the key and checks that it wasn't changed
    :param key: the key of the dictionary
    :param val: the value of the key
    :param db: the database object
    """
    for i in range(0, 10000):
        assert val == db.get_value(key)
        if val != db.get_value(key):
            print("err : val " + val + ",key: "+key)
    print("get")
    db.print_all()


def sett(db, num):
    """
    the function sets values for keys and deletes them
    :param num: start position for the for loop
    :param db: the database object
    """
    for i in range(num, num + 100):
        assert True == db.set_value(str(i), "t")
    for i in range(num, num + 100):  # deleting the keys that i set
        assert "t" == db.delete_value(str(i))
    print("set")
    db.print_all()


def delete(db, num):
    """
    the function creates and deletes keys in the dictionary
    :param num: start position for the for loop
    :param db: the database object
    """
    for i in range(num, num + 100):
        db.set_value(str(i), "c")
        assert "c" == db.delete_value(str(i))

    print("del")
    db.print_all()


def main():
    """
    calling a function 6 times according to the command from test.py
    """
    sync_database = SyncDatabase(MODE)
    # print(sys.argv)
    # print(sync_database.print_all())

    # get-  returns the value for the key, None if the key doesn't exists
    # delete- deletes the value for key and returns it, if doesnt exists return none
    # set- setting the key to val returns fail or success

    command = sys.argv[1]
    for j in range(1, 6):
        # get
        if command == 'get':
            print("main: command get")
            key = sys.argv[2]
            value = sys.argv[3]
            get(sync_database, key, value)

        # set
        if command == 'set':
            print("main: command set")
            num = int(sys.argv[2]) * j  # from where to start setting (key : val)
            sett(sync_database, num)

        # delete
        if command == 'delete':
            print("main: command delete")
            num = int(sys.argv[2]) * j  # number of (key : val) to delete
            delete(sync_database, num)


if __name__ == "__main__":
    main()
