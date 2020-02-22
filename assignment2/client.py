#!/usr/bin/env python3

import socket
import sys
from multiprocessing import Process, Queue


# Write your code here and in other files you create!
flag = True
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
total_tiles_observed = []
rover_area = None
number_of_tiles_explored = 0
current_position = []
message_queue = Queue()
p = None


def user_input(command, args=[]):
    global flag
    global p
    if command == "connect":
        if len(args) == 2:
            connect_to_server(args[0], int(args[1]))
        else:
            print("Unable to connect to the server, check command arguments")

    elif command == "login":
        if len(args) == 2:
            login(args[0], args[1])
        else:
            print("Incomplete login criteria")

    elif command == "observe":
        observe()

    elif command == "move" or command == 'm':
        if len(args) == 1:
            move(args[0])
        else:
            print("MISSING ARGUMENTS IN MOVE COMMAND")

    elif command == "stats":
        if len(args) == 0:
            send_stats()
        else:
            print("You provided too many arguments. Stats has no arguments.")

    elif command == "inspect":
        if len(args) == 1:
            inspect(args[0])
        else:
            print("MISSING ARGUMENTS IN Inspect."
                  " Please specify inspect <direction>.")

    elif command == "note":
        if len(args) != 0:
            note_message(args, "note")
        else:
            print("You provided no arguments."
                  " Please provide Note some arguments.")

    elif command == "message":
        if len(args) != 0:
            note_message(args, "message")
        else:
            print("You provided no arguments."
                  " Please provide note some arguments.")

    elif command == "commit":
        if len(args) == 0:
            commit()
        else:
            print("You provided too many arguments. Commit has no arguments.")

    elif command == "quit":
        if len(args) == 0:
            quit()
        else:
            print("You provided too many arguments. Quit has no arguments.")

    else:
        invalid_command()


def listening_to_server(queue):
    while True:
        length_received = sock.recv(256)
        receive_msg = sock.recv(256)

        if "event notify" in receive_msg.decode("ascii"):
            clean = receive_msg.decode("ascii")
            print("Server:" + clean[12:])
            print(">", end=" ")
            sys.stdout.flush()
            return

        if "event message" in receive_msg.decode("ascii"):
            clean = receive_msg.decode("ascii").split()
            print(str(clean[2]) + ": " + " ".join(clean[3:]))
            print(">", end=" ")
            sys.stdout.flush()
            return

        queue.put(receive_msg.decode("ascii").rstrip('\x00'))
        num = length_received.decode("ascii").rstrip('\x00')
        if int(num) > 256:
            receive_msg_2 = sock.recv(256)
            queue.put(receive_msg_2.decode("ascii").rstrip('\x00'))

    return


def connect_to_server(ip_address, port):
    global flag
    try:
        sock.connect((ip_address, port))
        length = sock.recv(256)
        msg = sock.recv(256).decode("ascii")
        if "ok connected" in msg:
            print("Connected, please log in")
        elif "error" in msg:
            print("Error: " + msg[6:])
        else:
            print("error in connect_to_server")

        return length
    except socket.error:
        print("Unable to connect to the server, check command arguments")


def login(ident, password):
    global p
    sent_msg = "login " + ident + " " + password
    length_of_msg = str(len(sent_msg))

    final_length = length_of_msg.ljust(256, " ")
    final_msg = sent_msg.ljust(256, " ")
    sock.sendall(final_length.encode("ascii"))
    sock.sendall(final_msg.encode("ascii"))

    length_received = sock.recv(256)
    receive_msg = sock.recv(256).decode("ascii")

    if "ok login" in receive_msg:
        print("Logged In!")
        # Time to start the listening to server child process
        p = Process(target=listening_to_server, args=(message_queue,))
        p.start()

    else:
        print("Invalid login details")

    return length_received


def observe():
    global rover_area
    global total_tiles_observed
    sent_msg = "action observe"
    length_of_msg = str(len(sent_msg))

    final_length = length_of_msg.ljust(256, " ")
    final_msg = sent_msg.ljust(256, " ")
    sock.sendall(final_length.encode("ascii"))
    sock.sendall(final_msg.encode("ascii"))

    part1 = message_queue.get()
    part2 = message_queue.get()
    unclean_str = part1 + part2
    unclean_array = unclean_str[11:].split()
    rover_area = []
    for x in unclean_array:
        current = x[1:-1]
        # Turning x into a list containing integers
        n_list = current.split(',')
        final_array = []
        for item in n_list:
            final_array.append(int(item.strip()))
        rover_area.append(tuple(final_array))
        clean_tuple = "(" + str(final_array[0]) + "," + str(
            final_array[1]) + ")"
        total_tiles_observed.append(clean_tuple)

    list_1 = rover_area[0:7]

    list_2 = rover_area[7:14]

    list_3 = rover_area[14:21]

    list_4 = rover_area[21:28]

    list_5 = rover_area[28:35]

    rover_elevation = list_3[3][2]

    row1 = row_maker(list_1, rover_elevation)
    row2 = row_maker(list_2, rover_elevation)
    row3 = row_maker(list_3, rover_elevation)
    row3[3] = 'RR'
    row4 = row_maker(list_4, rover_elevation)
    row5 = row_maker(list_5, rover_elevation)

    print()
    add_pipes(row1)
    add_pipes(row2)
    add_pipes(row3)
    add_pipes(row4)
    add_pipes(row5)


def row_maker(list, rover_elevation):
    row = []
    for item in list:
        cell = ''
        # Checking left column item first
        if item[3] == 1 and item[4] == 1:
            cell += 'R'
        elif item[3] == 1:
            cell += 'R'
        elif item[4] == 1:
            cell += 'M'
        else:
            cell += ' '

        # Checking right column elevation
        relative_elevation = item[2] - rover_elevation
        if relative_elevation > 9:
            cell += '9'
        elif relative_elevation < 0:
            cell += '-'
        elif relative_elevation == 0:
            cell += ' '
        else:
            cell += str(relative_elevation)

        row.append(cell)

    return row


def add_pipes(cur):
    final_str = "|"
    for x in cur:
        final_str += x + "|"
    print(final_str)


def move(direction):
    global number_of_tiles_explored
    global current_position
    sent_msg = "action move " + direction
    length_of_msg = str(len(sent_msg))

    final_length = length_of_msg.ljust(256, " ")
    final_msg = sent_msg.ljust(256, " ")
    sock.sendall(final_length.encode("ascii"))
    sock.sendall(final_msg.encode("ascii"))

    response = message_queue.get()
    x_y = response[9:-1]
    current_position = x_y.split(',')

    error(response)


def error(msg_received):
    if "error" in msg_received:
        print(msg_received.replace("error", "Error:"))
        return True
    return False


def send_stats():
    global number_of_tiles_explored
    global current_position
    sent_msg = "action stats"
    length_of_msg = str(len(sent_msg))

    final_length = length_of_msg.ljust(256, " ")
    final_msg = sent_msg.ljust(256, " ")
    sock.sendall(final_length.encode("ascii"))
    sock.sendall(final_msg.encode("ascii"))

    stat_msg = message_queue.get()

    if not error(stat_msg):
        split_array = stat_msg[10:-1].split(',')
        current_position = split_array
        number_of_tiles_explored = split_array[2]
        print("Number of tiles explored: " + number_of_tiles_explored)
        print("Current position: (" +
              current_position[0] + "," + current_position[1] + ")")


def inspect(direction):
    sent_msg = "action inspect " + direction
    length_of_msg = str(len(sent_msg))

    final_length = length_of_msg.ljust(256, " ")
    final_msg = sent_msg.ljust(256, " ")
    sock.sendall(final_length.encode("ascii"))
    sock.sendall(final_msg.encode("ascii"))

    server_response = message_queue.get()
    note_message = server_response[12:-1]

    if not error(server_response):
        if "" == note_message:
            print("Nothing interesting was found here")
        else:
            print("You found a note: " + note_message)


def note_message(args, type):
    msg = ""
    for x in args:
        msg += " " + x

    if type == "note":
        sent_msg = "action note" + msg
        length_of_msg = str(len(sent_msg))
    elif type == "message":
        sent_msg = "action message" + msg
        length_of_msg = str(len(sent_msg))

    final_length = length_of_msg.ljust(256, " ")
    final_msg = sent_msg.ljust(256, " ")
    sock.sendall(final_length.encode("ascii"))
    sock.sendall(final_msg.encode("ascii"))

    response = message_queue.get()

    error(response)


def commit():
    msg = ""
    for item in total_tiles_observed:
        msg += " " + item
    sent_msg = "action commit" + msg
    length_of_msg = str(len(sent_msg))

    final_length = length_of_msg.ljust(256, " ")
    final_msg = sent_msg.ljust(256, " ")
    sock.sendall(final_length.encode("ascii"))
    sock.sendall(final_msg.encode("ascii"))

    response = message_queue.get()
    error(response)


def quit():
    global flag
    global p
    sent_msg = "quit"
    length_of_msg = str(len(sent_msg))

    final_length = length_of_msg.ljust(256, " ")
    final_msg = sent_msg.ljust(256, " ")
    flag = False
    if p is not None:
        p.terminate()

    try:
        sock.sendall(final_length.encode("ascii"))
        sock.sendall(final_msg.encode("ascii"))

        length_received = sock.recv(256).decode("ascii")
        receive_msg = sock.recv(256).decode("ascii")

        if "ok quit" in receive_msg or "7" in length_received:
            sys.exit()
    except socket.error:
        return


def invalid_command():
    print("invalid command")


if __name__ == "__main__":
    while flag:
        input_array = input("> ").split()
        if len(input_array) == 0:
            invalid_command()
        elif len(input_array) == 1:
            command = input_array[0].lower()
            user_input(command)
        else:
            command = input_array[0].lower()
            args = input_array[1:]
            user_input(command, args)
