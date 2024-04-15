# -*- coding: utf-8 -*-
import sys
from datetime import datetime
from pathlib import Path
import sys
import json
import os

def main(argv):
    """
    WebPerf Core - Software update
    """

    update_software_info()

def update_software_info():
    collection = get_software_sources('software-full.json')

    set_softwares('software-full.json', collection)


def set_softwares(filename, collection):
    dir = Path(os.path.dirname(
        os.path.realpath(__file__)) + os.path.sep)
    
    file_path = '{0}{1}data{1}{2}'.format(dir, os.path.sep, filename)
    if not os.path.isfile(file_path):
        file_path = '{0}{1}{2}'.format(dir, os.path.sep, filename)
    if not os.path.isfile(file_path):
        print("ERROR: No {0} file found!".format(filename))

    print('set_software_sources', file_path)

    collection["loaded"] = True
    collection["updated"] = '{0}'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    data = json.dumps(collection, indent=4)
    with open(file_path, 'w', encoding='utf-8', newline='') as file:
        file.write(data)

def get_software_sources(filename):
    dir = Path(os.path.dirname(
        os.path.realpath(__file__)) + os.path.sep)

    file_path = '{0}{1}data{1}{2}'.format(dir, os.path.sep, filename)
    if not os.path.isfile(file_path):
        file_path = '{0}{1}{2}'.format(dir, os.path.sep, filename)
    if not os.path.isfile(file_path):
        print("ERROR: No {0} file found!".format(filename))
        return {
            'loaded': False
        }

    print('get_software_sources', file_path)
    collection = {}
    with open(file_path) as json_file:
        collection = json.load(json_file)

    if 'aliases' not in collection:
        collection['aliases'] = {}

    if 'softwares' not in collection:
        collection['softwares'] = {}

    # sort on software names
    if len(collection['aliases'].keys())> 0:
        tmp = {}
        issue_aliases_keys = list(collection['aliases'].keys())
        issue_aliases_keys_sorted = sorted(issue_aliases_keys, reverse=False)

        for key in issue_aliases_keys_sorted:
            tmp[key] = collection['aliases'][key]

        collection['aliases'] = tmp
        if issue_aliases_keys != issue_aliases_keys_sorted:
            set_softwares(filename, collection)

    # sort on software names
    if len(collection['softwares'].keys())> 0:
        tmp = {}
        issue_keys = list(collection['softwares'].keys())
        issue_keys_sorted = sorted(issue_keys, reverse=False)

        for key in issue_keys_sorted:
            tmp[key] = collection['softwares'][key]

        collection['softwares'] = tmp
        if issue_keys != issue_keys_sorted:
            set_softwares(filename, collection)

    return collection


"""
If file is executed on itself then call a definition, mostly for testing purposes
"""
if __name__ == '__main__':
    main(sys.argv[1:])
