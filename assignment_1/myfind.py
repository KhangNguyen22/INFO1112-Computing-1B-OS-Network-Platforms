#!/usr/bin/env python3

import sys
import os
import re


usage = "Usage: myfind [--regex=pattern | --name=filename] directory [command]"
number_of_directories_to_search = 0
number_of_forks = 0
# You can change this function signature if desired


def find(directory, regex=None, name=None, command=None):
    """A simplified find command."""
    global number_of_directories_to_search
    if regex is None and name is None and command is None:
        print(directory)

    if command is not None and regex is None and name is None:
        number_of_directories_to_search += 1
        fork_and_exec(directory, regex, name, command)

    for root, dirs, files in os.walk(directory, topdown=True):
        for file in files:
            # Name and Directory
            if name is not None and command is None:
                name_and_directory(name, root, file)

            # Regex and Directory
            elif regex is not None and command is None:
                regex_and_directory(regex, root, file)

            # Regex, Directory and command OR FileName, Directory and command
            elif command is not None:
                command_and_directory(command, root, file, regex, name)

            else:
                print(os.path.join(root, file))

        for folder in dirs:
            # Name and Directory
            if name is not None and command is None:
                name_and_directory(name, root, folder)
            # Regex and Directory
            elif regex is not None and command is None:
                regex_and_directory(regex, root, folder)

            # Regex, Directory and command OR FileName, Directory and command
            elif command is not None:
                command_and_directory(command, root, folder, regex, name)

            else:
                print(os.path.join(root, folder))


def finalise_number_of_searches(directory):
    global number_of_directories_to_search
    for root, dirs, files in os.walk(directory, topdown=True):
        number_of_directories_to_search += len(dirs) + len(files)


def name_and_directory(name, path, current_item):
    if name == current_item and name is not None:
        print(os.path.join(path, current_item))


def regex_and_directory(r, path, current_item):
    if re.search(r, current_item) and r is not None:
        print(os.path.join(path, current_item))


def command_and_directory(command, path, current_item, regex=None, name=None):
    cur_path = os.path.join(path, current_item)
    if regex is None and name is None:
        fork_and_exec(cur_path, regex, name, command)

    elif regex is not None:
        if re.search(regex, current_item):
            fork_and_exec(cur_path, regex, name, command)

    elif name is not None:
        if current_item == name:
            fork_and_exec(cur_path, regex, name, command)


def fork_and_exec(current_path, regex=None, name=None, command=None):
    global number_of_forks
    number_of_forks += 1
    pid = os.fork()
    if pid == 0:
        # child:
        arg_list = command.split()
        error_message = ""
        for index, value in enumerate(arg_list):
            if re.search("{}", value):
                arg_list[index] = value.replace("{}", current_path)
            error_message = error_message + arg_list[index] + " "
        flags_remainder_of_args = arg_list[1:]

        try:
            os.execlp(arg_list[0], "child program", *flags_remainder_of_args)
        except OSError:
            sys.stderr.write("Error: Unable to start process '{}'\n".format(
                error_message.rstrip()))
            sys.exit(1)

    else:
        wait = os.wait()
        if (wait[1] >> 8) != 0:
            # print("DIRECTORIES")
            # print(number_of_directories_to_search)
            # print("FORKS")
            # print(number_of_forks)
            if number_of_directories_to_search == number_of_forks:
                sys.exit(1)


if __name__ == "__main__":
    # TODO parse arguments here
    if len(sys.argv) == 1:
        sys.exit(usage)

    if len(sys.argv) >= 2:
        in_dir = []
        in_regex = None
        in_name = None
        in_command = None
        for cur in sys.argv[1:]:
            if re.search("^--name=", cur):
                in_name = cur[7:]
                continue
            if re.search("^--regex=", cur):
                in_regex = cur[8:]
                continue

            # Check if in_dir is empty and if true, add to in_dir
            if not in_dir:
                in_dir.append(cur)
            else:
                # Check if it is a directory
                if re.match("^/", cur) or (
                        re.match("[^-]", cur) and not re.search("[{}]",  cur)):
                    in_dir.append(cur)

                if (re.search("[{}]", cur) or (
                        cur == sys.argv[-1])) and not re.match("^/", cur):
                    in_command = cur.strip()

            # Check if it is a regex
            # Check if it is a name
            # Check if it is a command
        if (in_regex is not None and in_name is not None) or not in_dir:
            sys.exit(usage)
        else:
            if in_command is None:
                for cur in in_dir:
                    find(cur, in_regex, in_name, in_command)
            else:
                for item in in_dir:
                    finalise_number_of_searches(item)
                for cur in in_dir:
                    find(cur, in_regex, in_name, in_command)
