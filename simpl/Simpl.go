package main

import (
    "strings"
    "fmt"
    "os"
)

type Simpl struct {
    cli *CLI
}

func InitSimpl() *Simpl {
    cli := InitCLI()
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
