package main

import (
    "golang.org/x/crypto/ssh/terminal"
    "bufio"
    "os"
    "fmt"
)

type CLI struct {
    Input []byte
    Reader *bufio.Reader
}

func InitCLI() (*CLI) {
    reader := bufio.NewReader(os.Stdin)
    return &CLI{nil, reader}
}

func (c *CLI) SecureGetInput() {
    fmt.Print(">> ")
    data, err := terminal.ReadPassword(0)
    if err != nil {
        panic(err)
    }
    c.Input = data[0:]
}

func (c *CLI) GetInput() {
    fmt.Print(">> ")
    data, err := c.Reader.ReadBytes('\n')
    if err != nil {
        panic(err)
    }
    c.Input = data[0:]
}
