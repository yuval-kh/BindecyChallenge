from dataclasses import dataclass
import os
import stat


@dataclass
class PathData:
    read_set: set
    write_set: set
    has_read_before: bool
    has_write_before: bool


class Handler:

    def __init__(self):
        # pathDicts is a dictionary -> the path is the key pathdata class is value
        self.__path_dicts = dict()
        self.__max_index = 0

    def register(self, path: str, read: bool, write: bool) -> int:
        if not read and not write:
            return 0
        if not os.path.exists(path):
            return 0
        is_path_in_dict = False
        my_path = ''
        for path_dict in self.__path_dicts.keys():
            if os.path.samefile(path, path_dict):
                is_path_in_dict = True
                my_path = path_dict
                break

        if not is_path_in_dict:
            my_path = path
            had_read = bool(os.stat(my_path).st_mode & stat.S_IROTH)
            had_write = bool(os.stat(my_path).st_mode & stat.S_IWOTH)
            self.__path_dicts[my_path] = PathData(read_set=set(), write_set=set(),
                                                  has_read_before=had_read, has_write_before=had_write)
        self.__max_index += 1
        my_index = self.__max_index
        if read:
            my_set = (self.__path_dicts[my_path]).read_set
            my_set.add(my_index)
            st = os.stat(my_path)
            os.chmod(my_path, st.st_mode | stat.S_IROTH)

        if write:
            my_set = (self.__path_dicts[my_path]).write_set
            my_set.add(my_index)
            st = os.stat(my_path)
            os.chmod(my_path, st.st_mode | stat.S_IWOTH)
        return my_index

    def unregister(self, handle: int) -> None:
        my_path = None
        is_in_read = False
        is_in_write = False
        for path, path_data in self.__path_dicts.items():
            if handle in path_data.read_set:
                my_path = path
                is_in_read = True
            if handle in path_data.write_set:
                my_path = path
                is_in_write = True
            if is_in_read or is_in_write:
                break
        if my_path is None:
            return
        read_set = self.__path_dicts[my_path].read_set
        write_set = self.__path_dicts[my_path].write_set
        if is_in_read:
            has_read_before = self.__path_dicts[my_path].has_read_before
            read_set.remove(handle)
            if len(read_set) == 0 and not has_read_before:
                st = os.stat(my_path)
                os.chmod(my_path, st.st_mode & ~stat.S_IROTH)
        if is_in_write:
            has_write_before = self.__path_dicts[my_path].has_write_before
            write_set.remove(handle)
            if len(write_set) == 0 and not has_write_before:
                st = os.stat(my_path)
                os.chmod(my_path, st.st_mode & ~stat.S_IWOTH)
        if len(read_set) == 0 and len(write_set) == 0:
            del self.__path_dicts[my_path]
