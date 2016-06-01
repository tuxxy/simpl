package main

import (
	"crypto/bcrypt"
	"crypto/sha512"
)

func ZeroData(data []byte) {
	// Zeros the buffer
	// DOES NOT GUARANTEE SAFETY
	for i := range data[:] {
		data[i] = byte(0)
	}
}

func DeriveKey(passphrase []byte) []byte {
	// The maximum pass length is 72 chars, thus all passowrds will benefit
	// from a sha512 hash for maximum entropy allowance.
	// TODO Get a random 16 bit salt
	hashPass := sha512.New().Sum(passphrase[:])
	go ZeroData(passphrase[:])
	// I've found that 17 rounds is a reasonable wait for assured security.
	key, err := bcrypt.GenerateFromPassword(hashPass[:], 17)
	if err != nil {
		ZeroData(hashPass[:])
		panic(err)
	}
	return key[:]
}
