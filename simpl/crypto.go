package main

import (
    "crypto/sha512"
    "os"
    "io/ioutil"
    "fmt"
    "encoding/hex"
    "net/http"
)

func SanityCheck() bool {
    f, err := ioutil.ReadFile(os.Args[0])
    if err != nil {
        panic(err)
    }
    hash := sha512.New()
    hash.Write(f)
    selfSum := hex.EncodeToString(hash.Sum([]byte{}))
    resp, err := http.Get("https://raw.githubusercontent.com/tuxxy/simpl/go/CHECKSUM")
    if err != nil {
        fmt.Println("%s -- Error grabbing current simpl checksum! It is recommended to verify the checksum manually before continuing.\n\n", err)
        return false
    }
    defer resp.Body.Close()
    body, err := ioutil.ReadAll(resp.Body)
    if err != nil {
        fmt.Println("%s -- Error grabbing current simpl checksum! It is recommended to verify the checksum manually before continuing.\n\n", err)
        return false
    }
    if selfSum == string(body[:len(body)-1]) {
        fmt.Println("Checksum verification SUCCESS!\n\n")
        return true
    } else {
        fmt.Println("Checksum verification FAILED! It is recommended to not continue until this verification succeeds with the checksum from https://raw.githubusercontent.com/tuxxy/simpl/go/CHECKSUM\n\n")
        return false
    }
}
