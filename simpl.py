#!/usr/bin/env python3.5
import os
import sys
import json
from getpass import getpass

from Crypto.Cipher import AES
from Crypto import Random

# File path for the locker file
SIMPL_PATH = os.path.expanduser('~')+'/.simpl'

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

class Locker:
    """ This class acts as the data structure to store passwords. """
    key = None
    bank = []
    
    def __init__(self, data, key):
        """ Takes encrypted locker data from ~/.simpl and initializes a Locker. """
        self.key = key
        data_size = len(data)
        if data_size >= AES.block_size:
            IV = data[0:AES.block_size]
            if data_size > AES.block_size:
                ciphertext = data[AES.block_size:]
                _decrypt_into_bank(ciphertext, IV)

    def add(account_name, username, password, comment=None):
        self.bank.append({account_name: [username, password, comment]})
        _encrypt_to_file()

                
    def _decrypt_into_bank(self, ciphertext, IV):
        cipher = AES.new(self.key, AES.MODE_CFB, IV)
        for entry in json.loads(cipher.decrypt(ciphertext).decode('utf8')):
            self.bank.append({'account': entry['account'],
                'username': entry['username'], 'password': entry['password'],
                'comment': entry['comment']})

    def _encrypt_to_file(self):
        """ This is called after ever modification to the locker. """
        cipher = AES.new(self.key, AES.MODE_CFB, Random.new().read(AES.block_size))
        with open(SIMPL_PATH, 'wb') as f:
            f.write(cipher.encrypt(cipher.IV+json.dumps(self.bank)))
        
class Simpl:
    """ Main Simpl class. """

    cli = CLI()
    locker = None

    def __init__(self):
        if not os.path.isfile(SIMPL_PATH):
            self._create_simpl_file()
            self._init_new_locker()
        else:
            with open(SIMPL_PATH, 'rb') as f:
                locker = Locker(f.read(), self.cli.sensitive_input('Enter your key: '))

    def _create_simpl_file(self):
        print("No simpl locker file found. Would you like to create one? (YES/no)")
        choice = None
        while choice not in ['', 'y', 'yes', 'n', 'no']:
            choice = self.cli.get_input()
            if choice == '' or choice == 'y' or choice == 'yes':
                with open(SIMPL_PATH, 'x') as f:
                    pass
                print("\n\nsimpl locker file created!\n")
            elif choice == 'n' or choice == 'no': 
                print("Not creating a simpl locker file. Halting!\n")
                sys.exit()
            else:
                self.cli.ret_error()


    def _init_new_locker(self):
        """ Gets a passphrase from the user and creates a locker. """
        print("simpl uses AES-256 encryption, but it still needs a strong passphrase to be secure.\nChoose something random and at least 50 bits of entropy.\n\n")
        key = self.cli.sensitive_input('Enter your key: ')
        key_verify = self.cli.sensitive_input('Verify your key: ')
        while key != key_verify:
            key = self.cli.sensitive_input('Enter your key: ')
            key_verify = self.cli.sensitive_input('Verify your key: ')
        # sanity check the keys
        if key == key_verify:
            self.locker = Locker(Random.new().read(AES.block_size), key)
            return True
        else:
            # Should never happen, but safety first!
            return False

if __name__ == '__main__':
    # Instantiate main application handler class
    app = Simpl()
