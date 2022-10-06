from threading import Lock

class SafeList():
    def __init__(self,maxsize):
        self.__list = list()
        self.__lock = Lock()
        self.__maxsize = maxsize
        self.__logicsize = 0

    def append(self, value):
        with self.__lock:
            if len(self.__list) != self.__maxsize:
                self.__list.append(value)
            else:
                self.__list.append(value)
                self.__list.pop(0)

            self.__logicsize += 1
 
    def pop(self):
        with self.__lock:
            return self.__list.pop()
 
    def get(self, index):
        with self.__lock:
            return self.__list[index]
 
    def length(self):
        with self.__lock:
            return self.__logicsize

    def get(self):
        with self.__lock:
            return self.__list