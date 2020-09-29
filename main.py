#!/usr/bin/env python

import subprocess
import sys

BLOCK = ''


class Node:

    def __init__(self, module, data, parent=None):
        self.module = module
        self.children = []
        self.data = data
        self.parent = parent
        self.build = ''

    def find_children(self):
        try:
            for data in self.data:
                if len(data) < 2:
                    break
                if self.module in data[1]:
                    self.children.append(Node(data[0], self.data, self))
            del self.data

            if len(self.children) > 0:
                for child in self.children:
                    child.find_children()
        except RecursionError as err:
            print(err)
            print('graph for module to large')
            print('try narrow the search first by using')
            print(f'\n\tgo mod graph | grep {sys.argv[1]}\n')
            sys.exit(1)

    def build_list(self):
        if len(self.children) > 0:
            for child in self.children:
                child.build_list()
        else:
            self.build = self.history()
            self.write_out()

    def history(self):
        history = ''
        if self.parent is not None:
            history = self.parent.history()
            return self.parent.module + '\n' + history
        else:
            return history

    def write_out(self):
        global BLOCK
        BLOCK += self.build
        print(self.build)
        print(f"\n{'='*50}\n\n")

    def __repr__(self):
        return f"<Module: {self.module}>"


def format_string_to_list(string_data):
    output = []
    data = string_data.decode()
    data = data.split('\n')
    for line in data:
        line = line.split(' ')
        output.append(tuple(line))
    return output


def compile_tree(module, data):
    print(f"building tree for {module}")
    print(f"\n{'=' * 50}\n\n")
    tree = Node(module, data)
    tree.find_children()
    tree.build_list()


def format_version_output(version):
    for key in version.keys():
        print(key)
        for version_key in version[key].keys():
            print(f'\t{version_key} : {version[key][version_key]}')
        print()


def act_on_tree_data(data):
    print("Collecting package version usage count\n")
    version = get_version_data(data)
    format_version_output(version)


def get_version_data(data):
    values = {}
    for line in data.split('\n'):
        line = line.split('@')
        package = line[0]
        try:
            version = line[1]
        except IndexError:
            version = "Not Set"

        if package == '':
            break
        if package in values.keys():
            if version in values[package].keys():
                values[package][version] += 1
            else:
                values[package][version] = 1
        else:
            values.setdefault(package, {version: 1})

    return values


def run():
    try:
        print(sys.argv[1])
    except IndexError:
        print("Need module name")
        sys.exit(1)

    raw_data = subprocess.run(['go', 'mod', 'graph'], capture_output=True)
    if raw_data.returncode == 0:
        data = format_string_to_list(raw_data.stdout)
    else:
        print(raw_data)
        print("an error of some kind happened")
        sys.exit(1)

    compile_tree(sys.argv[1].lower(), data)
    act_on_tree_data(BLOCK)


if __name__ == '__main__':
    run()
