import hashlib
import pyDes
import bitstring
from utils import printResult


def DesEncrypt(clear, key):
    key_stream = bitstring.BitStream(key)
    padded_key_bits = bitstring.BitArray()
    for i in range(8):
        padded_key_bits += key_stream.read(7)
        padded_key_bits += '0b1'
    padded_key = padded_key_bits.tobytes()

    des = pyDes.des(padded_key, pyDes.ECB,  b"\0\0\0\0\0\0\0\0", padmode=pyDes.PAD_NORMAL)
    return des.encrypt(clear)


def NtPasswordHash(password):
    md4 = hashlib.new('MD4')
    md4.update(password)
    return md4.digest()


@printResult
def ChallengeHash(peerChallenge, authenticatorChallenge, username):
    hasher = hashlib.sha1()
    hasher.update(peerChallenge)
    hasher.update(authenticatorChallenge)
    hasher.update(username)

    return hasher.digest()[0:8]


def ChallengeResponse(challenge, passwordHash):
    zPasswordHash = passwordHash.ljust(21, b'\0')
    response = b''
    response += DesEncrypt(challenge, zPasswordHash[0:7])
    response += DesEncrypt(challenge, zPasswordHash[7:14])
    response += DesEncrypt(challenge, zPasswordHash[14:21])

    return response


@printResult
def GenerateNTResponse(authenticatorChallenge, peerChallenge, username, password):
    challenge = ChallengeHash(peerChallenge, authenticatorChallenge, username)
    passwordHash = NtPasswordHash(password)
    response = ChallengeResponse(challenge, passwordHash)

    return response

if __name__ == '__main__':
    authenticator_challenge = b'\x5B\x5D\x7C\x7D\x7B\x3F\x2F\x3E\x3C\x2C\x60\x21\x32\x26\x26\x28'
    peer_challenge = b'\x21\x40\x23\x24\x25\x5E\x26\x2A\x28\x29\x5F\x2B\x3A\x33\x7C\x7E'
    username = "User".encode()
    password = "clientPass".encode('utf-16-le')
    response = GenerateNTResponse(authenticator_challenge, peer_challenge, username, password)