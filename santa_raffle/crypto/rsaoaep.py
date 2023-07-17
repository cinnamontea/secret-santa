"""
This module provides all the materials to use RSA-OAEP.
It is used to implement the parts of the security protocol that run on the server.
"""


from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from base64 import b64encode, b64decode


def generateKeyPair(pexp=65537, ksize=4096):
    """
    Generates a key pair to be used for RSA-OAEP encryption/decryption.
    By default, it uses 65537 as a public exponent and produces a key of size 4096 bits.

    Returns
    -------
        (RSAPublicKey, RSAPrivateKey) - Tuple containing the public and private keys, respectively.
    """
    sk = rsa.generate_private_key(public_exponent=pexp, key_size=ksize)

    return (sk.public_key(), sk)


def encrypt(plaintxt, pubkey):
    """
    Uses RSA-OAEP to encrypt [plaintxt] using the given public key [pubkey].

    Arguments
    ---------
        plaintxt : str - Text to encrypt.
        pubkey : RSAPublicKey - Public key to use.

    Returns
    -------
        str - Base64 encoding of the resulting ciphertext.
    """

    ctxt = pubkey.encrypt(plaintxt.encode('utf-8'), padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                                                                 algorithm=hashes.SHA256(), label=None))

    return b64encode(ctxt).decode('utf-8')


def decrypt(ciphertxt, privkey):
    """
    Uses RSA-OAEP to decrypt [ciphertxt] using the given private key [privkey].

    Arguments
    ---------
        ciphertxt : str - Base64 encoding of ciphertext.
        privkey : RSAPrivateKey - Private key to use.

    Returns
    -------
        str - Plaintext.
    """

    ptxt = privkey.decrypt(b64decode(ciphertxt.encode('utf-8')), padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                                                                              algorithm=hashes.SHA256(), label=None))

    return ptxt.decode('utf-8')


def import_pk_string(s):
    """
    Imports a public key from a PEM formatted string which contains the key in SPKI format.

    Arguments
    ---------
        s : str - PEM formatted string.

    Returns
    -------
        RSAPublicKey - The imported public key.
    """
    return serialization.load_pem_public_key(s.encode('utf-8'))


def importSKFromFile(path, password=None):
    """
    Imports a private key from a PEM formatted file containing a key in PKCS8 format.

    Arguments
    ---------
        path : str - Path to the file.
        password = None : bytes - Optional password to unwrap the key.

    Returns
    -------
        RSAPrivateKey - The imported private key.
    """

    sk = None
    with open(path, "rb") as skf:
        sk = serialization.load_pem_private_key(skf.read(), password=password)

    return sk


def importPKFromFile(path):
    """
    Imports a public key from a PEM formatted file containing a key in SPKI format.

    Arguments
    ---------
        path : str - Path to the file.

    Returns
    -------
        RSAPublicKey - The imported public key.
    """

    pk = None
    with open(path, "rb") as pkf:
        pk = serialization.load_pem_public_key(pkf.read())

    return pk


def exportPK(pubkey):
    """
    Exports a public key to a PEM formatted bytes object.

    Arguments
    ---------
        pubkey : RSAPublicKey - The key to export.

    Returns
    -------
        bytes - PEM formatted bytes object containing the key in SPKI format.
    """

    return pubkey.public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo)


def exportSK(privkey, password=None):
    """
    Exports a private key to a PEM formatted bytes object.

    Arguments
    ---------
        privkey : RSAPrivateKey - The key to export.
        password = None : bytes - A password to encrypt/wrap the key.

    Returns
    -------
        bytes - PEM formatted bytes object containing the key in PKCS8 format.
    """

    encryption = serialization.BestAvailableEncryption(password) if password else serialization.NoEncryption()
    return privkey.private_bytes(encoding=serialization.Encoding.PEM, format=serialization.PrivateFormat.PKCS8, encryption_algorithm=encryption)


def pemToFile(pem, path):
    """
    Saves a PEM formatted key to a file.

    Arguments
    ---------
        pem : bytes - PEM formatted key.
        path : str - Path to the file where the key must be written.
    """

    with open(path, "wb") as kfile:
        kfile.write(pem)
