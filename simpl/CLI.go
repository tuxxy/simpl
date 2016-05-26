package main

import (
	"bufio"
	"errors"
	"fmt"
	"golang.org/x/crypto/ssh/terminal"
	"os"
	"strings"
)

type CLI struct {
	Input  []byte
	Reader *bufio.Reader
}

func InitCLI() *CLI {
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

func (c *CLI) ConfirmPrompt() (bool, error) {
	c.GetInput()
	choice := strings.ToLower(string(c.Input))
	switch choice {
	case "y", "yes":
		return true
	case "n", "no":
		return false
	}
}

func (c *CLI) DisplayHelp() {
	fmt.Println("'help' - Displays this menu.")
	fmt.Println("'exit' - Exits simpl.")
	fmt.Println("'add [account_name] [username]' - Adds entry to Locker.'")
	fmt.Println("'list' - Displays all the accounts and related comments in the Locker.")
	fmt.Println("'cat [account_name]' - Displays all info from matching provided account.")
	fmt.Println("'del [account_name]' - Deletes the entry matching the provided account.")
	fmt.Println("'update [account_name] [[<attribute>=<value>],[<attribute>=<value>]...]' - Updates matching entry from provided account name.")
	fmt.Println("'<query>' - Any string that doesn't match the commands. Searches for all related accounts and returns all the info.\n\n\n")
}
