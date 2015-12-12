#!/usr/bin/env python3.5
import os
import sys
import json
from getpass import getpass

from Crypto.Cipher import AES
from Crypto import Random
from hashlib import sha256

from termcolor import colored

# File path for the locker file
SIMPL_PATH = os.path.expanduser('~')+'/.simpl'

class CLI:
    """ CLI is a class that acts as an interface (via cli) to the user. """

    def __init__(self):
        print("simpl is a Security IMplied Password Locker written in Python3.5!")
        print("Github: https://github.com/tuxxy/simpl/")
        print("Developer Twitter: https://twitter.com/__tux")
        print("Read the README for information on how to use this software.\n\n\n")

    def get_input(self, prompt=">> ", precise=False):
        data = input(prompt)
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
    bank = {}
    
    def __init__(self, data, key):
        """ Takes encrypted locker data from ~/.simpl and initializes a Locker. """
        self.key = sha256(key).digest()
        data_size = len(data)
        if data_size >= AES.block_size:
            IV = data[0:AES.block_size]
            if data_size > AES.block_size:
                ciphertext = data[AES.block_size:]
                self._decrypt_into_bank(ciphertext, IV)

    def add(self, account, username, password, comment=None):
        if not account in self.bank.keys():
            self.bank[account] = {'username': username, 'password': password,
                'comment': comment}
            self._encrypt_to_file()
        else:
            raise KeyError('Account already exists!')

    def update(self, account, username=None, password=None, comment=None):
        """ Updates the current entry for account. """
        if account in self.bank.keys():
            if username:
                self.bank[account]['username'] = username
            if password:
                self.bank[account]['password'] = password
            if comment:
                self.bank[account]['comment'] = comment
            self._encrypt_to_file()
        else:
            # TODO Handle this error
            raise KeyError('Account doesn\'t exist!')

    def delete(self, account):
        """ Deletes entry from locker. """
        if account in self.bank.keys():
            del self.bank[account]
            self._encrypt_to_file()
        else:
            raise KeyError('Account doesn\'t exist!')

    def list(self):
        """ Lists all accounts. """
        for account in self.bank.keys():
            print("Account: {}\nComment: {}\n".format(account,self.bank[account]['comment']))

    def query(self, term):
        """ Searches for occurances of the term in the bank. """
        entries = []
        for account in self.bank.keys():
            if term in account:
                entries.append(account)
            elif term in self.bank[account]['username']:
                entries.append(account)
            elif term in self.bank[account]['comment']:
                entries.append(account)
        for account in entries:
            acct = colored(account, 'white')
            username = colored(self.bank[account]['username'], 'green')
            password = colored(self.bank[account]['password'], 'yellow',on_color='on_yellow')
            comment = colored(self.bank[account]['comment'], 'blue')
            print("Account: {}\nUsername: {}\nPassword: {}\nComment: {}\n\n\n".format(acct, username, password, comment))
        if entries == []:
            print("No occurances of '{}' found in the locker.\n\n".format(term))

    def _decrypt_into_bank(self, ciphertext, IV):
        cipher = AES.new(self.key, AES.MODE_CFB, IV)
        try:
            self.bank = json.loads(cipher.decrypt(ciphertext).decode('utf8'))
        except ValueError as e:
            print("Simpl could not read the locker data. Perhaps you used an invalid key?")
            sys.exit()

    def _encrypt_to_file(self):
        """ This is called after ever modification to the locker. """
        cipher = AES.new(self.key, AES.MODE_CFB, Random.new().read(AES.block_size))
        with open(SIMPL_PATH, 'wb') as f:
            f.write(cipher.encrypt(cipher.IV+json.dumps(self.bank).encode('utf8')))
        
class Simpl:
    """ Main Simpl class. """

    cli = CLI()
    locker = None

    def __init__(self):
        if not os.path.isfile(SIMPL_PATH):
            self._create_simpl_file()
        else:
            with open(SIMPL_PATH, 'rb') as f:
                self.locker = Locker(f.read(), self.cli.sensitive_input('Enter your key: ').encode('utf8'))

    def loop(self):
        """ Main loop for interface. """
        # TODO Handle ctrl-c, etc
        is_running = True
        while is_running:
            terms = self.cli.get_input().split()
            if terms[0] == 'add':
                self._add_phrase(terms)
            elif terms[0] == 'list' or terms[0] == 'ls':
                self.locker.list()
            else:
                self.locker.query(''.join(terms))

    def _add_phrase(self, terms):
        try:
            account = terms[1]
        except IndexError:
            account = self.cli.get_input('\n\nEnter the Account name: ')
        try:
            username = terms[2]
        except IndexError:
            username = self.cli.get_input('Enter the Username: ', precise=True)
        finally:
            password = self.cli.sensitive_input('Enter the Password: ')
            comment = self.cli.get_input("Enter comment: ", precise=True)
            try:
                self.locker.add(account, username, password, comment)
            except KeyError as e:
                print("\n\nThis account already exists. Try an update.")

    def _create_simpl_file(self):
        print("No simpl locker file found. Would you like to create one? (YES/no)")
        choice = None
        while choice not in ['', 'y', 'yes', 'n', 'no']:
            choice = self.cli.get_input()
            if choice == '' or choice == 'y' or choice == 'yes':
                if self._init_new_locker():
                    with open(SIMPL_PATH, 'x') as f:
                        pass
                print("\n\nsimpl locker file created!\n\n")
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
            print("The keys didn't match, try again.\n\n")
            key = self.cli.sensitive_input('Enter your key: ')
            key_verify = self.cli.sensitive_input('Verify your key: ')
        # sanity check the keys
        if key == key_verify:
            self.locker = Locker(Random.new().read(AES.block_size), key.encode('utf8'))
            return True
        else:
            # Should never happen, but safety first!
            return False

if __name__ == '__main__':
    # Instantiate main application handler class
    app = Simpl()
    app.loop()
