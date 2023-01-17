"""
Author: Talya Gross
file database class
"""

# import
from fileDatabase import *
import win32event


class SyncDatabase:
    def __init__(self, mode):
        """
            build function of the SyncDatabase class
        """
        # lock- only one can get, for writing
        # semaphore- only 10 can get, for reading

        # mode - True for processing, False for threading - unused
        self.SEMAPHORE_NAME = "MySemaphore3"
        self.MUTEX_NAME = "MyMutex3"
        self.read = win32event.CreateSemaphore(None, 10, 10, self.SEMAPHORE_NAME)
        self.write = win32event.CreateMutex(None, False, self.MUTEX_NAME)
        self.max_timeout = -1
        self.data = FileDatabase()

    def get_value(self, key):
        """
        acquiring the read semaphore, getting the value of the key and releasing the semaphore
        :param key: the key of the dictionary
        :return: the value for the key
        """
        # print("get value")
        self.read = win32event.OpenSemaphore(win32event.SYNCHRONIZE | win32event.EVENT_MODIFY_STATE,
                                             False, self.SEMAPHORE_NAME)
        r = win32event.WaitForSingleObject(self.read, self.max_timeout)
        if r != win32event.WAIT_OBJECT_0:
            raise Exception("error")
        else:
            logging.debug("reading key")
            data = self.data.get_value(key)
            win32event.ReleaseSemaphore(self.read, 1)
            return data

    def delete_value(self, key):
        """
        acquiring all the 10 semaphores for reading and the lock for writing
        and then deleting the key from the dictionary. releasing all the semaphores and the lock
        :param key: the key of the dictionary
        :return: the deleted value / None if the key doesnt exists
        """
        self.get_acquires()   # waiting until available
        logging.debug("deleted key and value")
        data = self.data.delete_value(key)
        self.get_releases()
        return data

    def set_value(self, key, val):
        """
        acquiring all the 10 semaphores for reading and the lock for writing
        setting the key to val and releasing all the semaphores and the lock.
        :param key: the key of the dictionary
        :param val: the value of the key
        :return  true or false for success or failure
        """
        # print('set value')
        flag = True
        self.get_acquires()
        logging.info(flag)
        flag = self.data.set_value(key, val)
        self.get_releases()
        return flag  # true or false

    def get_acquires(self):
        """
        acquiring all the 10 semaphores for reading and the lock for writing
        """
        # acquire lock for writing
        self.write = win32event.OpenMutex(win32event.SYNCHRONIZE, False, self.MUTEX_NAME)
        r = win32event.WaitForSingleObject(self.write, self.max_timeout)
        if r != win32event.WAIT_OBJECT_0:
            raise Exception("error: r = " + str(r))
        else:
            for i in range(10):  # acquire 10 semaphores for reading
                self.read = win32event.OpenSemaphore(win32event.SYNCHRONIZE | win32event.EVENT_MODIFY_STATE, False,
                                                     self.SEMAPHORE_NAME)
                r = win32event.WaitForSingleObject(self.read, self.max_timeout)
                if r != win32event.WAIT_OBJECT_0:
                    raise Exception("error: r = " + str(r))

    def get_releases(self):
        """
        releasing all the 10 semaphores and the lock
        """
        # release Lock
        # print("get releases")
        win32event.ReleaseMutex(self.write)
        for i in range(10):
            # release semaphore
            win32event.ReleaseSemaphore(self.read, 1)

    def print_all(self):
        """
        acquiring the semaphore for reading and printing the dictionary
        """
        self.read = win32event.OpenSemaphore(win32event.SYNCHRONIZE | win32event.EVENT_MODIFY_STATE, False,
                                             self.SEMAPHORE_NAME)
        r = win32event.WaitForSingleObject(self.read, self.max_timeout)
        if r != win32event.WAIT_OBJECT_0:
            raise Exception("error")
        else:
            logging.debug("reading all data")
            self.data.print_all()
            win32event.ReleaseSemaphore(self.read, 1)


if __name__ == '__main__':
    os.remove('database')
    db = SyncDatabase(False)
    db.print_all()
    assert db.set_value('2', '4') == True
    assert db.set_value('3', '4') == True
    db.print_all()
    assert db.get_value('2') == '4'
    assert db.delete_value('3') == '4'
    db.print_all()



