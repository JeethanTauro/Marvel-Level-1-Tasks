 
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

# Message to be encrypted
d = input("Enter message to be encrypted and decrypted: ")
data = d.encode()  # Convert to bytes

# Generate a random 128-bit key
key = get_random_bytes(16)

# Encrypting the message
cipher = AES.new(key, AES.MODE_GCM)  # Create a cipher object in GCM mode
nonce = cipher.nonce  # Get the nonce used for this encryption , it means number once
ciphertext, tag = cipher.encrypt_and_digest(data)  # Encrypt data and get the tag

# Print the encrypted message and tag
print("Ciphertext:", ciphertext)
print("Tag:", tag)

# Decryption
# Create a new cipher object using the same key and nonce for decryption
cipher_decrypt = AES.new(key, AES.MODE_GCM, nonce=nonce)

# Decrypt and verify the message using the tag
decrypted_data = cipher_decrypt.decrypt_and_verify(ciphertext, tag)
print("Decrypted message:", decrypted_data.decode())  # Convert bytes back to string





