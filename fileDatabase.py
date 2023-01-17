"""
Author: Talya Gross
file database class
"""
# import
import database
import pickle
import logging
import win32file
import win32con
import os

FILE = "database"


class FileDatabase(database.DataBase):
    def __init__(self):
        """
            build function of the FileDatabase class
        """
        super().__init__()
        if not os.path.exists(FILE):  # if the file doesnt exist --> creates a file with an empty dictionary
            self.write({})
        self.handle = None

    def set_value(self, key, val):
        """
        reading the data, setting the key to val in the file and database object.
        :param key: the key of the dictionary
        :param val: the value of the key
        :return: true or false for success or failure
        """
        flag = True
        try:
            self.read()
            logging.debug("read file")
            super().set_value(key, val)  # updating the object of the dictionary
            logging.debug("set value")
            self.write(self.data_dict)
        except Exception as err:
            print('received pickle exception - ' + str(err))
            flag = False
        finally:
            return flag

    def get_value(self, key):
        """
        reading the dictionary file and returning the value for the key
        :param key: the key of the dictionary
        :return: the value for the key
        """
        self.read()
        logging.debug("opened file")
        return super().get_value(key)

    def delete_value(self, key):
        """
        reading the file, deleting the value in the database object and file
        and updating it without the deleted key in the file
        :param key: the key of the dictionary
        :return: the deleted value / None if the key doesnt exists
        """
        self.read()
        val = super().delete_value(key)
        logging.debug("deleted value")
        self.write(self.data_dict)
        return val

    def print_all(self):
        """
        printing the dictionary
        """
        self.read()
        print(self.data_dict)

    def write(self, data):
        """
        creates a handle, writes to the file and closes the handle
        :param data: the data to write to the file
        """
        buf = pickle.dumps(data)
        self.handle = win32file.CreateFile(FILE, win32file.GENERIC_WRITE, 0, None, win32con.OPEN_ALWAYS, 0, None)
        win32file.WriteFile(self.handle, buf, None)
        win32file.CloseHandle(self.handle)

    def read(self):
        """
        creates an handle, reads the file, updates the dictionary and closes the handle
        :return:
        """
        self.handle = win32file.CreateFile(FILE, win32file.GENERIC_READ, win32file.FILE_SHARE_READ, None,
                                           win32con.OPEN_ALWAYS, 0, None)
        result, buf = win32file.ReadFile(self.handle, 100000, None)
        self.data_dict = pickle.loads(buf)
        # if self.handle == None:
        #    raise Exception("error: handle: ", self.handle)
        win32file.CloseHandle(self.handle)


if __name__ == '__main__':
    db = FileDatabase()
    print(db.data_dict)
    assert db.set_value('2', '4') == True
    assert db.set_value('3', '4') == True
    assert db.get_value('2') == '4'
    assert db.delete_value('3') == '4'
    print(db.data_dict)
