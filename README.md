# python-bip39

This aims to be a simple and well tested BIP39 implementaion in python, which intentionally only supports the core
properties of the [specification](https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki) i.e.,:

* encode data to mnemonic 
* decode mnemonic phrase
* convert mnemonic phrase to seed value (which than can be further process e.g., in [BIP32](https://github.com/bitcoin/bips/blob/master/bip-0032.mediawiki))

