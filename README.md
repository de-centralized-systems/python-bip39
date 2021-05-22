# BIP39

This aims to be a simple and well tested BIP39 implementation in Python, which intentionally only supports the core
properties of the [specification](https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki) i.e.,:

* encode data to mnemonic 
* decode mnemonic phrase
* convert mnemonic phrase to seed value (which than can be further process e.g., in [BIP32](https://github.com/bitcoin/bips/blob/master/bip-0032.mediawiki))

## Command line usage

You can also used the basic features on the command line:: 

```bash
$ ./bip39.py encode "00000000000000000000000000000000" 
abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about
$ python -m bip39 encode "00000000000000000000000000000000" # or like so
abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about
$ ./bip39.py decode "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about"
00000000000000000000000000000000
$ ./bip39.py toseed "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about" "TREZOR"
c55257c360c07c72029aebc1b53c05ed0362ada38ead3e3e9efa3708e53495531f09a6987599d18264c1e1c92f2cf141630c7a3c4ab7c81b2f001698e746
```

