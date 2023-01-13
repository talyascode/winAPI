"""
Author: Talya Gross
file database class
"""

# import
import threading
import multiprocessing
from fileDatabase import *
import win32event


class SyncDatabase:
    def __init__(self, mode):
        """
            build function of the SyncDatabase class
        """
        # lock- only one can get, for writing
        # semaphore- only 10 can get, for reading

        # lock
        # m = win32event.CreateMutex(None, False, 'MyMutex')
        #m = win32event.OpenMutex(win32event.SYNCHRONIZE, False, 'MyMutex')
        #r = win32event.WaitForSingleObject(m, 100)
        #r = win32event. WaitForSingleObject(m, -1)
        #win32event.ReleaseMutex(m)

        # semaphore
        # s = win32event.CreateSemaphore(None, 'MySemaphore')
        #s = win32event.OpenSemaphore(win32event.SYNCHRONIZE, False, 'MySemaphore')
        #r = win32event.WaitForSingleObject(s, 100)
        #r = win32event.WaitForSingleObject(s, -1)
        #win32event.ReleaseSemaphore(s)


        # mode - True for processing, False for threading
        if mode:  # multi
            self.read = win32event.CreateSemaphore(None, 'MySemaphore')
            self.write = win32event.CreateMutex(None, False, 'MyMutex')
        else:  # threading
            self.read = win32event.CreateSemaphore(None, 10, 10, 'MySemaphore')
            self.write = win32event.CreateMutex(None, False, 'MyMutex')
        self.data = FileDatabase()

    def get_value(self, key):
        """
        acquiring the read semaphore, getting the value of the key and releasing the semaphore
        :param key: the key of the dictionary
        :return: the value for the key
        """
        self.read = win32event.OpenSemaphore(win32event.SYNCHRONIZE | win32event.EVENT_MODIFY_STATE, False, 'MySemaphore')
        r = win32event.WaitForSingleObject(self.read, 100)
        r = win32event.WaitForSingleObject(self.read, -1)
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
        self.write = win32event.OpenMutex(win32event.win32event.SYNCHRONIZE | win32event.EVENT_MODIFY_STATE, False, 'MyMutex')
        r = win32event.WaitForSingleObject(self.write, 100)
        r = win32event. WaitForSingleObject(self.write, -1)
        for i in range(10):  # acquire 10 semaphores for reading
            self.read = win32event.OpenSemaphore(win32event.SYNCHRONIZE | win32event.EVENT_MODIFY_STATE, False, 'MySemaphore')
            r = win32event.WaitForSingleObject(self.read, 100)
            r = win32event.WaitForSingleObject(self.read, -1)

    def get_releases(self):
        """
        releasing all the semaphores and the lock
        """
        # release Lock
        win32event.ReleaseMutex(self.write)
        for i in range(10):
            # release semaphore
            self.read.release()

    def print_all(self):
        """
        acquiring the semaphore for reading and printing the dictionary
        """
        #self.read.acquire()
        self.data.print_all()
        #self.read.release()

if __name__ == '__main__':
    db = SyncDatabase(False)
    db.print_all()
    # assert db.set_value('2', '4') == True
    # assert db.set_value('3', '4') == True
    assert db.get_value('2') == None
    # assert db.delete_value('3') == '4'
    #db.print_all()

