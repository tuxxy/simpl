package main

type Entry struct {
    AccountName string
    Username string
    Comment string
    Password []byte
}

type Locker struct {
    LockerFile *os.File
    Entries *[]Entry
}

func InitLocker(lockerFile *os.File) *Locker {
}
