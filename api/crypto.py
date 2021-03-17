import os
from abc import ABC, abstractmethod
from enum import Enum

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


class CryptoCipher(ABC):
    """
    Abstract Base class for Asymmetric and Symmetric Ciphers
    """

    @abstractmethod
    def encrypt(self, plain_text):
        raise NotImplementedError

    @abstractmethod
    def decrypt(self, cipher_text):
        raise NotImplementedError


# ------------------------------------------------------------------------------
# ASymmetric Ciphers
# ------------------------------------------------------------------------------
class AsymmetricCipher(CryptoCipher):
    def __init__(self, pub_key, secret_key):
        self.pub_key = pub_key
        self.secret_key = secret_key


# ------------------------------------------------------------------------------
# Symmetric Ciphers
# ------------------------------------------------------------------------------
class SymmetricCipher(CryptoCipher):
    def __init__(self, key):
        self.key = key


class AESCipher(SymmetricCipher):
    iv = os.urandom(16)
    block_size = algorithms.AES.block_size / 8

    def __init__(self, key):
        super().__init__(key)

    @property
    def _cipher(self):
        return Cipher(algorithms.AES(self.key), modes.CBC(AESCipher.iv))

    def encrypt(self, plain_text):
        padder = int(self.block_size - len(plain_text) % self.block_size)
        final_text = plain_text + padder * chr(padder)
        encryptor = self._cipher.encryptor()
        cipher_text = encryptor.update(final_text.encode('utf-8')) + encryptor.finalize()
        return cipher_text

    def decrypt(self, cipher_text):
        decryptor = self._cipher.decryptor()
        plain_text = decryptor.update(cipher_text) + decryptor.finalize()

        return plain_text[:-ord(plain_text[len(plain_text) - 1:])]


class TDESCipher(SymmetricCipher):
    pass


# ------------------------------------------------------------------------------
# Cipher Backends
# ------------------------------------------------------------------------------
class SymmetricCipherBackend:
    def handle_ct(self, key, cipher_text):
        raise NotImplementedError

    def handle_pt(self, key, plain_text):
        raise NotImplementedError


class AESCipherBackend(SymmetricCipherBackend):
    def handle_pt(self, key, plain_text):
        return AESCipher(key=key).encrypt(plain_text)

    def handle_ct(self, key, cipher_text):
        return AESCipher(key=key).decrypt(cipher_text)


class TDESCipherBackend:
    pass


# ------------------------------------------------------------------------------
# NIST Approved Algorithims
# ------------------------------------------------------------------------------
class NISTApprovedCryptoAlgo(Enum):
    AES = AESCipherBackend()
    TDES = TDESCipherBackend()

