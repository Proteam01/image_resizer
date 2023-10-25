import os

class FileTreeIterator:

    def __init__(self):
        self.files_list = []

    def iterate_tree(self, location):
        if os.path.isdir(location):
            child_files = os.listdir(location)
            child_files.sort()
            children = filter(lambda sub: os.path.isdir(sub), map(
                lambda el: os.path.join(location, el), child_files))
            for child in children:
                self.iterate_tree(child)
                if self.__file_has_images(child):
                    self.files_list.append(child)

    def __file_has_images(self, location):
        listing = os.listdir(location)
        for archive in listing:
            if archive.lower().endswith('.jpg') or archive.lower().endswith('.jpeg'):
                return True
        return False

    def get_file_list(self):
        return self.files_list