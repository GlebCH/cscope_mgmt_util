#!/bin/python
import subprocess
import argparse
import terminaltables

def cs_create(args):
    if not args.name:
        
    print(1)

def cs_delete(args):
    print(1)

def cs_refresh(args):
    print(1)

def cs_show(args):
    print(1)

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
    parser_create.set_defaults(func=cs_delete)
    # refresh
    parser_show = subparsers.add_parser('refresh',
                                        help='refresh cscope dbs')
    parser_show.add_argument('-n', '--name',
                             help='name of project',
                             type=str, required=False)
    parser_create.set_defaults(func=cs_refresh)

    # show
    parser_show = subparsers.add_parser('show',
                                        help='show informations about cscope dbs')
    parser_show.add_argument('-n', '--name',
                             help='name of project',
                             type=str, required=False)
    parser_create.set_defaults(func=cs_show)

    args = parser.parse_args()
    args.func(args)

if __name__ == '__main__':
    main()
