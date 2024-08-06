import hashlib
import os
import shutil
import sys
import time


def execute():
    source_path = sys.argv[1]
    replica_path = sys.argv[2]
    sync_time = int(sys.argv[3])
    log_file_path = sys.argv[4]
    log_name = 'log.txt'

    while True:
        start_time = time.time()

        sync_folder(source_path, replica_path, log_file_path, log_name)

        run_time = time.time() - start_time
        sleep_time = sync_time - run_time
        if sleep_time > 0:
            time.sleep(sleep_time)


def sync_folder(source_path, replica_path, log_file_path, log_name):
    folder_names = get_folders(replica_path)
    for folder in folder_names:
        if os.path.exists(get_path(source_path, folder)) == False:
            remove_folder(replica_path, folder)
            message = "Folder removed:"
            write_log(log_file_path, log_name, folder, message)
    
    folder_names = get_folders(source_path)
    for folder in folder_names:
        if os.path.exists(get_path(replica_path, folder)) == False:
            create_folder(replica_path, folder)
            message = "Folder created:"
            write_log(log_file_path, log_name, folder, message)

        sync_folder(
            get_path(source_path, folder),
            get_path(replica_path, folder),
            log_file_path,
            log_name
        )

    sync_files(source_path, replica_path, log_file_path, log_name)


def sync_files(source_path, replica_path, log_file_path, log_name):
    print(f"Syncing {source_path}")

    source_hash_dict = get_file_hashes(source_path)
    replica_hash_dict = get_file_hashes(replica_path)

    for file_name in source_hash_dict:
        if replica_hash_dict.get(file_name) == None:
            copy_file(source_path, replica_path, file_name)
            message = "File created:"
            write_log(log_file_path, log_name, file_name, message)

        elif source_hash_dict[file_name] != replica_hash_dict.get(file_name):
            copy_file(source_path, replica_path, file_name)
            message = "File copied:"
            write_log(log_file_path, log_name, file_name, message)

    for file_name in replica_hash_dict:
        if source_hash_dict.get(file_name) == None:
            remove_file(replica_path, file_name)
            message = "File removed:"
            write_log(log_file_path, log_name, file_name, message)


def get_file_hashes(path):
    # read files in folder
    names = os.listdir(path)
    file_names = []
    for name in names:
        if os.path.isfile(get_path(path, name)):
            file_names.append(name)

    hash_dict = {}
    for file_name in file_names:
        file_path = get_path(path, file_name)
        file_content = open(file_path, 'rb').read()
        hash_dict[file_name] = hashlib.md5(file_content).hexdigest()

    return hash_dict


def get_folders(path):
    names = os.listdir(path)
    folder_names = []
    for name in names:
        if os.path.isdir(get_path(path, name)):
            folder_names.append(name)

    return folder_names


def write_log(log_file_path, log_name, name, message):
    open_file(log_file_path, log_name, 'a+').write(f'{message} {name}\n')
    print(f"{message} {name}")


def create_folder(path, folder_name):
    os.mkdir(get_path(path, folder_name))


def remove_folder(path, folder_name):
    shutil.rmtree(get_path(path, folder_name)) 


def copy_file(source_path, replica_path, file_name):
    file_content = open_file(source_path, file_name, 'rb').read()
    open_file(replica_path, file_name, 'wb+').write(file_content)


def remove_file(path, file_name):
    os.remove(get_path(path, file_name))


def open_file(file_path, file_name, open_as):
    return open(get_path(file_path, file_name), open_as)


def get_path(path, file_name):
    return path + '/' + file_name


if __name__ == "__main__":
    execute()
