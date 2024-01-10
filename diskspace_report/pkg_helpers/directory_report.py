#!/usr/bin/env python3
import os

start_path = "/Applications/"

def get_total_size():
    total_size = 0
    long_path = start_path
    fatale_error = IOError()
    for dirpath, dirnames, filenames in os.walk(start_path, topdown=True, followlinks=False, onerror=None):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            try:
                os.access(fp, os.R_OK)
                total_size += os.path.getsize(fp)
                long_path += os.path.abspath(fp)
            except IOError:
                fatale_error = IOError()
    return total_size

def path_print():
    total_size = 0
    for root, dirs, files in os.walk(start_path, topdown=True, followlinks=False, onerror=None):
        path_size = 0
        for name in files:
            fp = os.path.join(root, name)
            try:
                os.access(fp, os.R_OK)
                total_size += os.path.getsize(fp)
                total_print_size = round((total_size) / (1000 * 1000 * 1000), 2)
                path_size += os.path.getsize(fp)
                path_print_size = round((path_size) / (1000 * 1000), 2)
                print(str(path_print_size) + " MB", str(total_print_size) + " GB", os.path.join(root, name))
            except IOError:
                fatale_error = IOError()
        for name in dirs:
            fp = os.path.join(root, name)
            try:
                os.access(fp, os.R_OK)
                total_size += os.path.getsize(fp)
                total_print_size = round((total_size) / (1000 * 1000 * 1000), 2)
                path_size += os.path.getsize(fp)
                path_print_size = round((path_size) / (1000 * 1000), 2)
                print(str(path_print_size) + " MB", str(total_print_size) + " GB", os.path.join(root, name))
            except IOError:
                fatale_error = IOError()

total_size = get_total_size()
readable_size = round((total_size) / (1000 * 1000 * 1000), 3)

path_print()
print(readable_size, 'Gbytes')
