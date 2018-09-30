#!/bin/python
import subprocess
import os, fnmatch
import sys, sh
import argparse
import terminaltables


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
    exec(open("/home/nightwolf/Documents/CSCOPE/set_env.sh").read())
#    subprocess.call(["source", "~/Documents/CSCOPE/set_env.sh"], shell=True)


def cs_delete(args):
    print(2)

def cs_refresh(args):
    print(3)

def cs_show(args):
    print(4)

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
