#!/bin/python
import subprocess
import os, fnmatch
import sys, sh
import argparse
import shutil
import json
from terminaltables import DoubleTable


config_path = os.path.expanduser("~/Documents/CSCOPE/config.json")


def ccwrap(code):
    def inner(text, bold=False):
        cc = code
        if bold:
            cc = '1;{0}'.format(cc)
        strs = text.split('\n')
        nl = len(strs)
        if nl > 1:
            ret = ''
            for str in strs:
                ret += '\033[%sm%s\033[0m\n' % (cc, str)
            ret = ret[:-1]
            return ret
        else:
            return "\033[%sm%s\033[0m" % (cc, text)
    return inner


green = ccwrap('32')
white = ccwrap('37')


class Project:
    def __init__(self, id, name, path, is_active, root_path):
        self.id = id
        self.name = name
        self.path = path
        self.is_active = is_active
        self.root_path = root_path + name

    def delete(self):
        shutil.rmtree(self.root_path)

    @property
    def to_json(self):
        return {
                'id': self.id,
                'path': self.path,
                'is_active': self.is_active
               }
    @property
    def to_row(self):
        color = green if self.is_active else white
        return [
                color(str(self.id)),
                color(self.name),
                color(self.path)
               ]


class Profile:
    def __init__(self):
        self.data = []
        self.path = ""
        
    def load(self, path):
        with open(path, 'r') as fp:
            config = json.load(fp)

        self.path = config["path"]
        config = config["Projects"]

        for p in config:
            pr = Project(name=p,
                         id=config[p]["id"],
                         path=config[p]["path"],
                         is_active=config[p]["is_active"],
                         root_path=self.path)
            self.data.append(pr)
        
    def save(self, path):
        json_dic = {
                    "Projects": {p.name: p.to_json for p in self.data},
                    "path": self.path
                   }
        with open(path, 'w') as fp:
            json.dump(json_dic, fp, sort_keys=True, indent=4)

    def delete_project(self, name):
        for p in self.data:
            if p.name == name:
                p.delete()
                self.data.remove(p)
                return True

        return False

    @property
    def table(self):
        table_list = [[white("ID"), white("Name"), white("Path")]]
        for p in self.data:
            table_list.append(p.to_row)
        
        table = DoubleTable(table_list, title=white('Projects', True))
        table.inner_row_border = True
        return table

def get_files_from_dir(dir):
    list = []
    for root, sub_dir, files in os.walk(dir):
        for file_name in files:
            if fnmatch.fnmatch(file_name, '*.c') or \
                    fnmatch.fnmatch(file_name, '*.h'):
                list.append(os.path.join(root, file_name))

    return list

def cs_create(args):
    args.dir = os.path.expanduser(args.dir)
    if not os.path.isdir(args.dir) or \
            not os.path.exists(args.dir):
        print("Coudn't find dir with current pathname {0}".format(args.dir))
        sys.exit(1)

    if not args.name:
        args.name = os.path.basename(args.dir)

    path_name = os.path.expanduser("~/Documents/CSCOPE/{0}".format(args.name))
    if os.path.isdir(path_name):
        print("Project with {0} name already exist!".format(args.name))
        sys.exit(1)

    file_list = get_files_from_dir(args.dir)
    if not file_list:
        print(("Cound't find .c or .h files"
               "with current pathname {0}").format(args.dir))
        sys.exit(1)

    os.mkdir(path_name)
    with open(path_name + "/cscope.files", 'w') as f:
        for item in file_list:
            f.write("%s\n" % item)

    os.chdir(path_name)
    subprocess.call(["cscope", "-b", "-i", path_name + "/cscope.files"])

def cs_delete(args):
    profile = Profile()
    profile.load(config_path)

    ret = profile.delete_project(args.name)
    if not ret:
        print("'{0}' project doesn't exist".format(args.name))
    else:
        print("Success")
        profile.save(config_path)


def cs_refresh(args):
    print(3)

def cs_show(args):
    profile = Profile()
    profile.load(config_path)
    print(profile.table.table)


def main(args=None):
    parser = argparse.ArgumentParser(
        description="cscope configuration util")
    subparsers = parser.add_subparsers(metavar='COMMAND')
    subparsers.required = True

    # create
    parser_create = subparsers.add_parser('create',
                                          help='create new cscope db')
 
    parser_create.add_argument('-d', '--dir',
                               help='dir of src code',
                               type=str, required=True)
    parser_create.add_argument('-n', '--name',
                               help=('name of new project, '
                                     'if not define, used name of dir'),
                               type=str, required=False)
    parser_create.set_defaults(func=cs_create)

    # delete
    parser_delete = subparsers.add_parser('delete',
                                          help='delete cscope db')
    parser_delete.add_argument('-n', '--name',
                               help='name of project',
                               type=str, required=True)
    parser_delete.set_defaults(func=cs_delete)

    # refresh
    parser_refresh = subparsers.add_parser('refresh',
                                        help='refresh cscope dbs')
    parser_refresh.add_argument('-n', '--name',
                                help='name of project',
                                type=str, required=False)
    parser_refresh.set_defaults(func=cs_refresh)

    # show
    parser_show = subparsers.add_parser('show',
                                        help='show informations about cscope dbs')
    parser_show.add_argument('-n', '--name',
                             help='name of project',
                             type=str, required=False)
    parser_show.set_defaults(func=cs_show)

    args = parser.parse_args()
    args.func(args)

if __name__ == '__main__':
    main()
