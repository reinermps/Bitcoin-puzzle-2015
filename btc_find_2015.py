import secp256k1
from Crypto.Hash import RIPEMD
import hashlib
import base58
from tqdm import tqdm
import os


# List of addresses to check
addresses_to_check = ['18ZMbwUFLMHoZBbfpCjUJQTCMCbktshgpe', '13zb1hQbWVsc2S7ZTZnP2G4undNNpdh5so', '1BY8GQbnueYofwSuFAT3USAhGjPrkxDdW9', '1MVDYgVaSN6iKKEsbzRUAYFrYJadLYZvvZ', '19vkiEajfhuZ8bs8Zu2jgmC6oqZbWqhxhG']

# Check if the file exists and is not empty
if os.path.exists("lastiteration.txt") and os.path.getsize("lastiteration.txt") > 0:
    with open("lastiteration.txt", "r") as f:
        private_key_hex = f.read().strip()
        private_key_int = int(private_key_hex, 16)
else:
    private_key_int = int.from_bytes(bytes.fromhex("0000000000000000000000000000000000000000000000020000000000000000"), byteorder='big')

private_key = secp256k1.PrivateKey(private_key_int.to_bytes(32, byteorder='big'))

# Initialize the progress bar
pbar = tqdm(total=2**100)
iteration = 0

while True:

    # Get the corresponding public key
    public_key = private_key.pubkey

    # Get the public key in compressed format
    compressed_public_key = public_key.serialize()

    # Get the SHA-256 hash of the public key
    sha256_hash = hashlib.sha256(compressed_public_key).digest()

    # Get the RIPEMD-160 hash of the SHA-256 hash
    ripemd160_hash = RIPEMD.new(sha256_hash).digest()

    # Add the network byte (0x00 for mainnet, 0x6f for testnet) to the RIPEMD-160 hash
    network_byte = b'\x00'
    address_bytes = network_byte + ripemd160_hash

    # Get the double SHA-256 hash of the address bytes
    checksum = hashlib.sha256(hashlib.sha256(address_bytes).digest()).digest()[:4]

    # Concatenate the address bytes and the checksum
    address_bytes_with_checksum = address_bytes + checksum

    # Encode the address bytes with checksum in base58
    address = base58.b58encode(address_bytes_with_checksum).decode('ascii')

    if address in addresses_to_check:
        with open('matched_addresses.txt', 'a') as file:
            file.write(f'Matched address: {address}\n')
            file.write(f'Private key: {private_key.private_key.hex()}\n\n')
    #save iteration
    if iteration % 2000000 == 0:
        with open('lastiteration.txt', 'w') as f:
            f.write(str(private_key.private_key.hex()))
    iteration += 1

    # Update the progress bar
    pbar.update(1)

    private_key_int = int.from_bytes(private_key.private_key, byteorder='big')
    private_key_int += 1
    private_key = secp256k1.PrivateKey(private_key_int.to_bytes(32, byteorder='big'))


# Close the progress bar
pbar.close()
