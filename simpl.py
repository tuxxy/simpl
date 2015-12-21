#!/usr/bin/env python3.5
import os
import sys
import json
from getpass import getpass

from Crypto.Cipher import AES
from Crypto.Hash import SHA256, HMAC
from Crypto import Random

import bcrypt

import entropy

from termcolor import colored

# File path for the locker file
SIMPL_PATH = os.path.expanduser('~')+'/.simpl'

class CLI:
    """ CLI is a class that acts as an interface (via cli) to the user. """

    def __init__(self):
        pass

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

    def YES_no_prompt(self):
        choice = None
        while choice not in ['', 'y', 'yes', 'n', 'no']:
            choice = self.get_input()
            if choice == '' or choice == 'y' or choice == 'yes':
                return True
            elif choice == 'n' or choice == 'no':
                return False
            else:
                self.ret_error()

    def ret_error(self, error="Input was invalid - try again."):
        print(error)

    def disp_help(self):
        # TODO Clarify these by fixing usage patterns
        print("'help' - Displays this menu.")
        print("'exit' - Exits the program.")
        print("'add [[account_name] [username]]' - Adds entry to Locker.'")
        print("'list' - Displays all the accounts and related comments in the Locker.")
        print("'cat [account_name]' - Displays all info from matching provided account.")
        print("'del [account_name]' - Deletes the entry matching the provided account.")
        print("'update [account_name] [[<attribute>=<value>],[<attribute>=<value>]]' - Updates matching entry from provided account name")
        print("'<query>' - Any string that doesn't match the commands. Searches for all related accounts and returns all the info.\n\n\n")


class Locker:
    """ This class acts as the data structure to store passwords. """
    key = None  # This key is used only to decrypt
    bcrypt_salt = None
    bank = {}
    
    # TODO: This can be improved by taking a filelike object instead of a string
    # TODO: Maybe replace with a C-based library for bcrypt
    # TODO: Look into Cryptography.io
    def __init__(self, data, key):
        """ Takes encrypted locker data from ~/.simpl and initializes a Locker. """
        key = SHA256.new(key).digest()
        # bcrypt salt is always 29 bytes, get and remove from the data
        data_size = len(data)
        if data_size >= AES.block_size+29:
            bcrypt_salt = data[:29]
            data = data[29:]
            key = SHA256.new(bcrypt.hashpw(key, bcrypt_salt)).digest()
            IV = data[:AES.block_size]
            if data_size > AES.block_size:
                ciphertext = data[AES.block_size:]
                self._decrypt_into_bank(key, ciphertext, IV)
        # Create a new key
        self.bcrypt_salt = bcrypt.gensalt(16) # 2**16 == 65536 rounds
        self.key = SHA256.new(bcrypt.hashpw(key, self.bcrypt_salt)).digest()

    def add(self, account, username, password, comment=''):
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
            comment = colored(self.bank[account]['comment'], 'blue')
            print("Account: {}\nComment: {}\n".format(account,comment))

    def cat(self, account):
        """ Lists info for only the account it matches. """
        if account in self.bank.keys():
            username = colored(self.bank[account]['username'], 'green')
            password = colored(self.bank[account]['password'], 'yellow',on_color='on_yellow')
            comment = colored(self.bank[account]['comment'], 'blue')
            print("Account: {}\nUsername: {}\nPassword: {}\nComment: {}\n\n".format(account, username, password, comment))
        else:
            raise KeyError('Account doesn\'t exist!')

    def count_entropy(self, password):
        """ Counts shannon entropy of password."""
        print("Shannon Entropy count: {}".format(entropy.shannon_entropy(password)))

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
        entries.sort()
        for account in entries:
            acct = colored(account, 'white')
            username = colored(self.bank[account]['username'], 'green')
            password = colored(self.bank[account]['password'], 'yellow',on_color='on_yellow')
            comment = colored(self.bank[account]['comment'], 'blue')
            print("Account: {}\nUsername: {}\nPassword: {}\nComment: {}\n\n".format(acct, username, password, comment))
        if not entries:
            print("No occurances of '{}' found in the locker.\n\n".format(term))

    def _decrypt_into_bank(self, key, ciphertext, IV):
        cipher = AES.new(key, AES.MODE_CBC, IV)
        # Grab the last 32 bytes of ciphertext (the HMAC) and remove it.
        hmac = ciphertext[-32:]
        ciphertext = ciphertext[:-32]
        try:
            # Verify message against the HMAC
            hmac_msg = HMAC.new(key, msg=ciphertext, digestmod=SHA256).digest()
            if hmac != hmac_msg:
                raise ValueError('HMAC could not be verified.')
            else:
                self.bank = cipher.decrypt(ciphertext)
                # Remove the pad, as per PKCS#7, and load json
                self.bank = json.loads(self.bank[0:-self.bank[-1]].decode('utf8'))
        except ValueError:
            print("Simpl could not read the locker data. Perhaps you used an invalid key?")
            sys.exit()

    def _encrypt_to_file(self):
        """ This is called after ever modification to the locker. """
        cipher = AES.new(self.key, AES.MODE_CBC, Random.new().read(AES.block_size))
        with open(SIMPL_PATH, 'wb') as f:
            plaintext = json.dumps(self.bank).encode('utf8')
            # Pad the data for AES CBC
            pad_length = AES.block_size - (len(plaintext) % AES.block_size)
            if pad_length == 0:
                # Even if it doesn't need the pad, we still add it per PKCS#7
                pad_length = AES.block_size
            pad = pad_length.to_bytes(1, 'big') * pad_length
            plaintext += pad
            ciphertext = cipher.encrypt(plaintext)
            # Get the HMAC of Locker file
            hmac = HMAC.new(self.key, msg=ciphertext, digestmod=SHA256).digest()
            f.write(self.bcrypt_salt+cipher.IV+ciphertext+hmac)

        
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
            terms = self.cli.get_input(precise=True).split()
            if not terms:
                # Do nothing, just reloop again
                pass
            elif terms[0] in ['add', 'touch', 'new', 'create']:
                self._add_entry(terms)
            elif terms[0] in ['cat', 'type']:
                self._cat_entry(terms)
            elif terms[0] in ['list', 'ls', 'dir']:
                self.locker.list()
            elif terms[0] in ['delete', 'del', 'remove', 'rm']:
                self._del_entry(terms)
            elif terms[0] in ['update', 'mod', 'modify', 'change']:
                self._update_entry(terms)
            elif terms[0] in ['entropy', 'shannon']:
                self.locker.count_entropy(self.cli.sensitive_input('Enter a password: '))
            elif terms[0] in ['help', '?']:
                self.cli.disp_help()
            elif terms[0] in ['exit', ':q', ':wq']:
                sys.exit()
            else:
                self.locker.query(''.join(terms))

    def _cat_entry(self, terms):
        try:
            account = terms[1]
        except IndexError:
            account = self.cli.get_input('\n\nEnter the Account name: ')
        finally:
            try:
                self.locker.cat(account)
            except KeyError:
                print("No such account '{}' found in locker.\n\n".format(account))

    def _add_entry(self, terms):
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
            except KeyError:
                print("\n\nThis account already exists. Try an update.")

    def _del_entry(self, terms):
        try:
            account = terms[1]
        except IndexError:
            account = self.cli.get_input("Enter the Account name: ")
        finally:
            try:
                self.locker.delete(account)
            except KeyError:
                print("No account found for '{}'\n\n".format(account))

    def _update_entry(self, terms):
        # TODO Might want to clean this up and make it more clear
        username, password, comment = None, None, None
        try:
            # update <account>
            account = terms[1]
        except IndexError:
            # update
            account = self.cli.get_input('\n\nEnter Account to update: ')
        # update <account> <key>=<value>, <key>=<value>, <key>
        phrases = ' '.join(terms[2:]).split(',')
        for phrase in phrases:
            phrase = phrase.strip()
            try:
                # <key>=<value>
                key, value = phrase.split('=')
                if key == 'username':
                    username = value
                elif key == 'password':
                    password = value
                elif key == 'comment':
                    comment = value
            except ValueError:
                # <key>
                if phrase == 'password':
                    password = self.cli.sensitive_input('\n\nEnter the Password: ')
                elif phrase == 'username':
                    username = self.cli.get_input('\n\nEnter the Username: ', precise=True)
                elif phrase == 'comment':
                    comment = self.cli.get_input('\n\nEnter Comment: ', precise=True)
                elif not phrase:
                    self.cli.ret_error(error='\n\n`update` requires an attribute to modify. See the README for more info.')
                else:
                    self.cli.ret_error(error='\n\nNo such attribute \'{}\''.format(phrase))
        try:
            self.locker.update(account, username=username, password=password, comment=comment)
        except KeyError:
            print("There is no account '{}'. Create it? (YES/no)")
            if self.cli.YES_no_prompt():
                self.locker.add(account, username, password, comment)

    def _create_simpl_file(self):
        print("No simpl locker file found. Would you like to create one? (YES/no)")
        if self.cli.YES_no_prompt():
            if self._init_new_locker():
                with open(SIMPL_PATH, 'x') as f:
                    pass
                print("\n\nsimpl locker file created!\n\n")
        else:
            print("Not creating a simpl locker file. Halting!\n")
            sys.exit()

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
    print("simpl is a Security IMplied Password Locker written in Python!")
    print("Read the README for information on how to use this software.")
    print(colored("Github: https://github.com/tuxxy/simpl/", 'green'))
    print(colored("Developer Twitter: https://twitter.com/__tux", 'green'))
    print("For a basic list of commands, type 'help'.\n\n\n")

    app = Simpl()
    app.loop()
