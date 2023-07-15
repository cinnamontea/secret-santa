from os import urandom
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from base64 import b64encode, b64decode


def b64str_to_bytes(b64str):
    return b64decode(b64str.encode('utf-8'))

def bytes_to_b64str(bs):
    return b64encode(bs).decode('utf-8')


def generateKey256():
    """
    Generates a 256-bit (32 bytes) key for AES-CTR.

    Returns
    -------
        str - Key encoded as a Base64 string.
    """
    return bytes_to_b64str(urandom(32))


def importKFile(path):
    """
    Imports a symmetric key from a PEM formatted file in [path].
    NOTE!: For simplicity, this function assumes that the PEM file has *exactly* 3 lines,
    with the key being the 2nd line (index 1).

    Returns
    -------
        str - Key encoded as a Base64 string.
    """
    raw_key = None
    with open(path, "rb") as kf:
        raw_key = kf.read()
    lines = raw_key.decode('utf-8').splitlines()
    if (len(lines) == 3):
        return lines[1]    


def encrypt(plaintxt, key):
    """
    Encrypts [plaintxt] with [key] using AES in CTR mode.
    Uses a 16-byte (128 bit) counter, which is included in the resulting ciphertext.

    Arguments
    ---------
        plaintxt : str - Plaintext to encrypt.
        key : str - Symmetric key as a Base64 string.

    Returns
    -------
        str - Base64 encoding of the resulting ciphertext, which includes the counter in the first 16 bytes (decoded).
    """

    # Generate a random 16-byte (128 bit) counter, using the operating system's random number generator.
    ctr = urandom(16)

    decoded_key = b64str_to_bytes(key)
    cipher = Cipher(algorithms.AES(decoded_key), modes.CTR(ctr))
    encryptor = cipher.encryptor()

    ctxt = encryptor.update(plaintxt.encode('utf-8')) + encryptor.finalize()

    # Combine [ctr] with [ctxt].
    ctr_ctxt_arr = bytearray(ctr)
    ctr_ctxt_arr.extend(ctxt)

    # Return the Base64 encoding of ctr||ctxt.
    return b64encode(ctr_ctxt_arr).decode('utf-8')


def decrypt(ciphertxt, key):
    """
    Decrypts [ciphertxt] with [key] using AES in CTR mode.
    Recovers the counter from the first 16 bytes of the decoded ciphertext.

    Arguments
    ---------
        ciphertxt : str - Base64 encoding of the ciphertext to decrypt.
        key : str - Symmetric key as a Base64 string.

    Returns
    -------
        str - Plaintext.
    """

    # Decode the ciphertext and recover the counter.
    decoded_ctr_ctxt = b64decode(ciphertxt.encode('utf-8'))
    ctr = decoded_ctr_ctxt[0:16]
    ctxt = decoded_ctr_ctxt[16:]

    decoded_key = b64str_to_bytes(key)
    cipher = Cipher(algorithms.AES(decoded_key), modes.CTR(ctr))
    decryptor = cipher.decryptor()

    raw_ptxt = decryptor.update(ctxt) + decryptor.finalize()

    return raw_ptxt.decode('utf-8')