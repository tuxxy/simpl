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

func InitCryptor(key, salt, nonce []byte) *Cryptor {
    // Derive the key
    derivedKey := make([]byte, 32)
    derivedKey = DeriveKey(key, salt)

    // Wipe unused data
    ZeroData(key)
    ZeroData(salt)

    // Create cipher
    block, err := aes.NewCipher(key[:])
    if err != nil {
        ZeroData(key)
        panic(err)
    }
    // Look into wiping key after block creation
    if nonce == nil {
        // Generate a random 96-bit nonce
        Nonce := getRandBytes(12)
    } else {
        Nonce := make([]byte, 12)
        copy(Nonce, nonce)
        ZeroData(nonce)
    }
    GCMCipher, err := cipher.NewGCM(block)
    return &Cryptor{GCMCipher, Nonce}
}

func (c *Cryptor) EncryptData(data []byte) {
    _, err := c.GCMCipher.Seal(data[:0], Nonce, data, nil)
    if err != nil {
        ZeroData(data)
        ZeroData(Nonce)
        panic(err)
    }
}
