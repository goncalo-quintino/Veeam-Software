import pytest
from Task_Goncalo_Quintino import (
    write_log,
    remove_file,
    copy_file,
    open_file,
    get_path,
)
import os


def test_write_log():
    path = '/home/goncalo/Downloads/Directory'
    file_name = 'file.txt'
    message = "File created:"
    log_name = 'log_test'

    write_log(path, log_name, file_name, message)

    result = open(path + '/' + log_name, 'r').read()
    assert result == message + ' ' + file_name + '\n'

    os.remove(path + '/' + log_name)


def test_copy_file():
    path = '/home/goncalo/Downloads/Directory'
    replica_path = '/home/goncalo/Downloads/Replica'
    file_name = 'file.txt'
    open(path + '/' + file_name, 'wb+')

    copy_file(path, replica_path, file_name)

    os.remove(path + '/' + file_name)
    os.remove(replica_path + '/' + file_name)


def test_remove_file():
    path = '/home/goncalo/Downloads/Directory'
    file_name = 'file.txt'
    open(path + '/' + file_name, 'wb+')

    remove_file(path, file_name)

    with pytest.raises(FileNotFoundError):
        open(path + '/' + file_name, 'rb')


def test_open_file():
    path = '/home/goncalo/Downloads/Directory'
    file_name = 'file.txt'
    text = "test"
    open(path + '/' + file_name, 'w+').write(text)

    file = open_file(path, file_name, 'r')

    assert file.read() == text


def test_get_path():
    path = '/home/goncalo/Downloads/Replica'
    file_name = 'file.txt'
    expected_result = '/home/goncalo/Downloads/Replica/file.txt'

    result = get_path(path, file_name)

    assert result == expected_result
