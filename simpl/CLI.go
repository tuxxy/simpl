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

func CheckErr(e error) {
    if e != nil {
        panic(e)
    }
}

func InitCLI() *CLI {
	reader := bufio.NewReader(os.Stdin)
	return &CLI{nil, reader}
}

func (c *CLI) FirstRunSetup() *os.File {
    fmt.Println("Simpl has detected this is the first run!\nWe will now setup your Simpl Locker file!")
    fmt.Println("Would you like to continue? y/n")
    is_cont := cli.ConfirmPromptLoop()
    if !is_cont {
        fmt.Println("See ya!")
        os.Exit(0)
    }
    file, err := os.Create(".simpl")
    CheckErr(err)

    return file
}

func (c *CLI) SecureGetInput() {
	fmt.Print(">> ")
	data, err := terminal.ReadPassword(0)
    CheckErr(err)

	c.Input = data[:]
}

func (c *CLI) GetInput() {
	fmt.Print(">> ")
	data, err := c.Reader.ReadBytes('\n')
    CheckErr(err)

	c.Input = data[:]
}

func (c *CLI) ConfirmPrompt() (bool, error) {
	c.GetInput()
	choice := strings.ToLower(string(c.Input))
	switch choice {
	case "y", "yes":
		return true, nil
	case "n", "no":
		return false, nil
    default:
        return false, errors.New("Invalid choice")
	}
}

func (c *CLI) ConfirmPromptLoop() (bool) {
    for is_cont, err = cli.ConfirmPrompt(); !is_cont; is_cont, err = cli.ConfirmPrompt() {
        if err != nil {
            fmt.Println("Invalid choice!")
            continue
        }
        return is_cont
    }
    return is_cont
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
