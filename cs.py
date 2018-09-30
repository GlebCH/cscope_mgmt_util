#! /bin/python
import subprocess
import argparse

parser = argparse.ArgumentParser(
    description="cscope configuration util")
subparsers = parser.add_subparsers()

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

# delete
parser_create = subparsers.add_parser('delete',
                                      help='delete cscope db')

parser_create.add_argument('-n', '--name',
                           help='dir of src code',
                           type=str, required=True)

subprocess.call("pwd")





