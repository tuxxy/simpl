package main

type Entry struct {
    AccountName string
    Username string
    Comment string
    Password []byte
}

type Locker struct {
    Entries *[]Entry
}
