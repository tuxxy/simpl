package main

type Simpl struct {
    cli *CLI
}

func InitSimpl() {
    cli := InitCLI()
    return &Simpl{cli}
}

func (s *Simpl) Run() {

}
