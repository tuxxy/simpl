package main

import (
    "strings"
    "fmt"
    "os"
    "os/user"
)

type Simpl struct {
    cli *CLI
    locker *Locker
}


func InitSimpl() *Simpl {
    cli := InitCLI()

    // Change dir to the home directory of the current user
    usr, err := user.Current()
    CheckErr(err)
    CheckErr(os.Chdir(usr.HomeDir))

    // If the file doesn't exist, this is the first time running!
    if _, err := os.Stat(".simpl"); os.IsNotExist(err) {
        lockerFile := cli.FirstRunSetup()
    }
    locker := InitLocker(lockerFile)

    return &Simpl{cli}
}

func (s *Simpl) Cleanup() int {
    // TODO Wipe memory, etc
    return 0
}

func (s *Simpl) Run() {
    isRunning := true
    for isRunning {
        s.cli.GetInput()
        terms := strings.Split(strings.TrimSpace(string(s.cli.Input)), " ")
        switch terms[0] {
        case "add", "touch", "new", "create":
            s.AddEntry(terms)
        case "help", "?":
            s.cli.DisplayHelp()
        case "exit", ":q", ":wq":
            os.Exit(s.Cleanup())    
        }
    }
}

func (s *Simpl) AddEntry(terms []string) {
    fmt.Println("I ran!", terms)
}
