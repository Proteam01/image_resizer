import yaml
from scale import ImageScaling
from typing import List
import os
from click import progressbar
from simple_threadpool import ThreadPool
from filetree import FileTreeIterator
from helper import logger

def read_options():
    with open('options.yml', 'r') as file:
        return yaml.load(file.read(), Loader=yaml.BaseLoader)


OPTIONS = read_options()

image_scaling = ImageScaling(OPTIONS['scale_factor'])
BASE_DIR = OPTIONS['scan_directory']
TARGET_DIR = OPTIONS['target_dir']
THREADS = OPTIONS['threads']


def contains_images(full_path) -> bool:
    image = False
    files = os.listdir(full_path)
    for file in files:
        if file.lower().endswith('.jpeg') or file.lower().endswith('.jpg'):
            image = True
            break
    return image


def traverse_dir(base_dir):
    file_tree = FileTreeIterator()
    file_tree.iterate_tree(base_dir)
    dirs = file_tree.get_file_list()
    return dirs


def scan_directories() -> List[str]:
    dirs = traverse_dir(BASE_DIR)
    return dirs


def save_image(jpeg_file, data, dir_part):
    target = TARGET_DIR + dir_part
    os.makedirs(target, exist_ok=True)
    file = os.path.join(target, jpeg_file)
    with open(file, 'wb') as jpeg:
        jpeg.write(data)


def scale_image(params):
    jpeg_file = params[0]
    directory = params[1]
    dir_part = params[2]
    source_file =  os.path.join(directory, jpeg_file)
    file = open(source_file, 'rb')
    data = file.read()
    file.close()
    try:
        rescaled_data = image_scaling.image_scale(data)
        save_image(jpeg_file, rescaled_data, dir_part)
    except Exception as error:
        logger.error(error)
        logger.error('source_file: ' + source_file)


def optimize_images(directory):
    dir_part = directory[len(BASE_DIR):]
    jpegs = list(filter(lambda file: file.lower().endswith(
        '.jpeg') or file.lower().endswith('.jpg'), os.listdir(directory)))
    threadpool = ThreadPool(scale_image, 4)
    arr = list()
    for jpeg_file in jpegs:
        arr.append((jpeg_file, directory, dir_part))
    threadpool.feed(arr)


def main():
    directories = scan_directories()
    with progressbar(directories) as iterator:
        for directory in iterator:
            optimize_images(directory)


if __name__ == '__main__':
    import time
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))
