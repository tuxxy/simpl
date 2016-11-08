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

    if is_firstRun {
        // Create a cipher
    }
}
