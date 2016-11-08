package main

import (
	"golang.org/x/crypto/scrypt"
    "crypto/rand"
    "crypto/aes"
    "crypto/cipher"
)

type Cryptor struct {
    GCMCipher *cipher.AEAD
}

func ZeroData(data []byte) {
	// Zeros the buffer
	// DOES NOT GUARANTEE SAFETY
	for i := range data[:] {
		data[i] = byte(0)
	}
}

func getRandBytes(n int) []byte {
    // Returns a byte array filled with n random bytes
    data := make([]byte, n)
    _, err := rand.Read(data)
    if err != nil {
        panic(err)
    }
    return data
}

func getRandSalt() []byte {
    // Returns a 32-byte random salt
    return getRandBytes(32)
}

func DeriveKey(passphrase, salt []byte) []byte {
    // Best scrypt settings for modern use -- N=2^22, r=4, p=1
	key, err := scrypt.Key(passphrase, salt, 4194304, 4, 1, 32)
	if err != nil {
		ZeroData(passphrase[:])
		panic(err)
	}
    // Return the derived key
	return key
}
