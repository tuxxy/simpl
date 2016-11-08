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
	// I've found that 17 rounds is a reasonable wait for assured security.
	key, err := bcrypt.GenerateFromPassword(passphrase[:], 17)
	if err != nil {
		ZeroData(hashPass[:])
		panic(err)
	}
	return key[:]
}
