package main

import (
	"golang.org/x/crypto/scrypt"
    "crypto/rand"
    "crypto/aes"
    "crypto/cipher"
)

type Cryptor struct {
    GCMCipher cipher.AEAD
    Nonce []byte
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

func InitCryptor(key, nonce []byte) *Cryptor {
    block, err := aes.NewCipher(key[:])
    if err != nil {
        ZeroData(key)
        panic(err)
    }
    if nonce == nil {
        // Generate a random 96-bit nonce
        Nonce := getRandBytes(12)
    } else {
        Nonce := copy(nonce)
        ZeroData(nonce)
    }
    GCMCipher, err := cipher.NewGCM(block)
    return &Cryptor{GCMCipher, Nonce}
}
