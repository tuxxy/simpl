#!/usr/bin/env python3.5
import os
import sys
import json
from getpass import getpass

class Password:
    """ This data structure holds a password and its related data. """

    account = None  # A queryable term (and name) to organize passwords.
    comment = None  # A comment on the account.
    username = None
    password = None

    def __init__(self, account, username, password, comment=None):
        self.account = account
        self.username = username
        self.password = password
        self.comment = comment

class Locker:
    """ This class acts as the data structure to store passwords. """
    last_auth = None
    
    def __init__(self, data):
        """ Takes encrypted locker data from ~/.simpl and initializes a Locker. """


class CLI:
    """ CLI is a class that acts as an interface (via cli) to the user. """

    def __init__(self):
        print("simpl is a Security IMplied Password Locker written in Python3.5!")
        print("Github: https://github.com/tuxxy/simpl/")
        print("Developer Twitter: https://twitter.com/__tux")
        print("Read the README for information on how to use this software.\n\n\n")

    def get_input(self, precise=False):
        data = input(">> ")
        # If the data is precise, do not standardize it.
        if not precise:
            data = data.lower()
        return data

    def sensitive_input(self, prompt, precise=True):
        """ Gets input without echoing it back to the user. """
        # TODO If echo free input doesn't exist, how do we handle it?
        # TODO Research how to test echo free input
        data = getpass(prompt=prompt)
        if not precise:
            data = data.lower()
        return data

    def ret_error(self, error="Input was invalid - try again."):
        print(error)

class Simpl:
    """ Main Simpl class. """

    locker = None
    cli = None
    simpl_file = None

    def __init__(self):
        cli = CLI()
        simpl_file = os.path.expanduser('~')+'/.simpl'

        # If a simpl locker file doesn't exist...
        if not os.path.isfile(simpl_file):
            print("No simpl locker file found. Would you like to create one? (YES/no)")
            valid = False
            while not valid:
                choice = cli.get_input()
                if choice == '' or choice == 'y' or choice == 'yes':
                    valid = True
                    with open(simpl_file, 'x') as f:
                        pass
                    print("\n\nsimpl locker file created!\n")
                elif choice == 'n' or choice == 'no': 
                    print("Not creating a simpl locker. Halting!\n")
                    sys.exit()
                else:
                    cli.ret_error()
        else:
            with open(simpl_file, 'r') as f:
                data = f.read()
            



if __name__ == '__main__':
    # Instantiate main application handler class
    app = Simpl()
