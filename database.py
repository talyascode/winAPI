"""
Author: Talya Gross
database class
"""

# import
import logging


class DataBase:
    def __init__(self):
        """
        build function of the database class
        """
        self.data_dict = {}

    def set_value(self, key, val):
        """
        setting the value of key to val
        if key doesnt exist-> creates new key and val, if key exists-> the value will be changed to val
        :param key: the key of the dictionary
        :param val: the value of the key
        :return  true or false for success or failure
        """
        logging.debug("setting" + key + "to value:" + val)
        self.data_dict.update({key: val})
        return True

    def get_value(self, key):
        """
        :param key: the key of the dictionary
        :return: the value of the key/ None - if the key doesnt exist
        """
        logging.debug("return" + key)
        if key in self.data_dict.keys():
            return self.data_dict[key]
        return None

    def delete_value(self, key):
        """
        deletes the key from the dictionary
        :param key: the key of the dictionary
        :return: the deleted value / None if the key doesnt exists
        """
        logging.debug("return dict after deleting:" + key)
        return self.data_dict.pop(key, None)


if __name__ == '__main__':
    db = DataBase()
    assert db.set_value('2', '4') == True
    assert db.get_value('2') == '4'
    assert db.delete_value('2') == '4'

