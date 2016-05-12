package main

import (
    "golang.org/x/crypto/ssh/terminal"
    "bufio"
    "os"
)

type CLI struct {
    Input []byte
    Reader *bufio.Reader
}

func InitCLI() (*CLI) {
    reader := bufio.NewReader(os.Stdin)
    return &CLI{nil, reader}
}

func (c *CLI) GetKey() {
    // Can't put a value directly into the struct, see:
    // https://github.com/golang/go/issues/6842
    key, err := terminal.ReadPassword(0)
    if err != nil {
        panic(err)
    }
    c.Input = key[0:]
}
