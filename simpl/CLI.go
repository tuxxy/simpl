package main

import (
    "golang.org/x/crypto/ssh/terminal"
    "bufio"
    "os"
    "fmt"
    "strings"
    "errors"
)

type CLI struct {
    Input []byte
    Reader *bufio.Reader
    validChoices *map[string]bool
}

func InitCLI() (*CLI) {
    reader := bufio.NewReader(os.Stdin)
    return &CLI{nil, reader,
        &map[string]bool{"y": true, "yes": true, "n": false, "no": false}}
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

func (c *CLI) ConfirmPrompt() (bool, error) {
    c.GetInput()
    choice := strings.ToLower(string(c.Input))
    if (*c.validChoices)[choice] {
        return (*c.validChoices)[choice], nil
    } else {
        return false, errors.New("Input was invalid - try again.")
    }
}
