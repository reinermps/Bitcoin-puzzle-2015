# Bitcoin-puzzle-2015
A python code to brute force the puzzle. More info on this site https://privatekeys.pw/puzzles/bitcoin-puzzle-tx.

Made this code for fun (with chatGPT help), I get ~19000 it/s with a Ryzen 5600x. 

Looks like only works on Linux because of the secp256k1 module.

The code is setup to start with the private key (PK) 000000000000000000000000000000000000000000000001a838b13505b26857 and it will find the PK to the address 18ZMbwUFLMHoZBbfpCjUJQTCMCbktshgpe, which is the puzzle 65, already solved. It's also searching the PK of the puzzles 66, 67, 68 and 69.

Don't know why (yet), sometimes the code stops with a segmentation fault error. Could be a problem in my PC.



If you like this code, please share some love in form of BTC, my address is bc1qrnqgj3aa9zp9fvn5rgeegpfccz79sn0humtwup.
