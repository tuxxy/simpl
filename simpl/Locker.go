package main

import (
    "os"
)

type Entry struct {
    AccountName string
    Username string
    Comment string
    Password []byte
}

type Locker struct {
    Cli *CLI
    LockerFile *os.File
    Entries *[]Entry
    Cipher *Cryptor
}

func InitLocker(lockerFile *os.File, cli *CLI is_firstRun bool) *Locker {
    Cli := cli
    LockerFile := lockerFile
    var key []byte
    var nonce []byte
    var salt []byte

    if is_firstRun {
        nonce = nil
        salt = getRandBytes(32)

        fmt.Println("Enter a secure key for encryption.\nIf you forget this, you will lose access to your data.")
        Cli.SecureGetInput()

        // Copy and zero passphrase from CLI
        key = make([]byte, len(Cli.Input))
        copy(key, Cli.Input)
        ZeroData(Cli.Input)

        fmt.Println("Enter key again for verification.")
        Cli.SecureGetInput()

        // Copy and zero passphrase from CLI
        keyVerify := make([]byte, len(Cli.Input))
        copy(keyVerify, Cli.Input)
        ZeroData(Cli.Input)

        for key != keyVerify {
            ZeroData(key)
            ZeroData(keyVerify)

            fmt.Println("Keys do not match, enter key again.")
            Cli.SecureGetInput()

            // Copy and zero passphrase from CLI
            key = make([]byte, len(Cli.Input))
            copy(key, Cli.Input)
            ZeroData(Cli.Input)

            fmt.Println("Enter key again for verification.")
            Cli.SecureGetInput()

            // Copy and zero passphrase from CLI
            keyVerify = make([]byte, len(Cli.Input))
            copy(keyVerify, Cli.Input)
            ZeroData(Cli.Input)
        }

        // Key has been verified, wipe the verification key
        ZeroData(keyVerify)
    } else {
        // Get nonce from LockerFile
        nonce = make([]byte, 12)
        lockerFile.Read(nonce)

        // Get key from user
        fmt.Println("Enter Encryption key.")
        Cli.SecureGetInput()
        key = make([]byte, len(Cli.Input))
        ZeroData(Cli.Input)
    }
    // Create cipher
    Cipher := InitCryptor(key, nonce)
}
