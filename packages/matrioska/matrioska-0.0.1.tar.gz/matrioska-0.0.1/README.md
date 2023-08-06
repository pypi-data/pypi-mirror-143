# matrioska

Command line tool and Python library for data symmetric encryption

# Features
- Generate a random (base64 encoded) 32 bytes passphrase (for AES256)
- Key provided via environment variable name (to avoid command line exposure)
- Encrypts from stdin or filename into stdout/filename
- Decrypts from stdin or filename into stdout/filename

The encryption is performed using [AES-256](Advanced_Encryption_Standard) in [EAX](https://en.wikipedia.org/wiki/EAX_mode) mode via the [PyCryptodome](https://pycryptodome.readthedocs.io/en/latest/) library.

# Install
```sh
pip install matrioska
```

# Usage
```sh
# Generate a random encryption key and story in an environment variable
export KEY=$(matrioska --gen-key)

# Encrypt stdin
echo "This is a very secret sentence" | matrioska -k KEY > /tmp/secret

# Decrypt stdin
cat /tmp/secret | matrioska -k KEY -d

# Encrypt file omitting both source and destioname filenames from command line
matrioska -k KEY < /etc/passwd > /tmp/secret_file

# Decrypt file omitting both source and destioname filenames from command line
matrioska -k KEY -d < /tmp/secret_file > /tmp/secret
```
