## 1. AES

The _`AES`_ class uses the AES-CTR algorithm (counter mode) to encrypt and decrypt data.

### 1.1. _AES_ methods & parameters

`AES(key: bytes)`

The required `key` parameter of AES class must be `bytes` type and will be used to encrypt or decrypt data.

`AES(key: bytes).encrypt(plaintext: bytes) -> bytes`

The `encrypt` method is used to encrypt data and return a `bytes` type object that contains the ciphertext of the `plaintext` parameter.

`AES(key: bytes).decrypt(ciphertext: bytes) -> bytes`

The `decrypt` method is used to decrypt data and return a `bytes` type object that contains the plaintext of the `ciphertext` parameter.

### 1.2. AES useful variables

There are three possible lengths of keys for AES: 128-bit, 192-bit, and 256-bit. The constants `AES128_SIZE`, `AES192_SIZE`, `AES256_SIZE` hold those values.  The constant `IV_SIZE` holds the length of the IV.

These constants can be imported directly from the library .

### 1.3. AES example

```
from py2crypt import AES, AES256_SIZE
from os import urandom

plain_text = b'Hello World!'
shared_key = urandom(AES256_SIZE)

sender = AES(shared_key)
receiver = AES(shared_key)

encrypted_text = sender.encrypt(plain_text)
decrypted_text = receiver.decrypt(encrypted_text)

print('Encrypted message:', encrypted_text.hex())
print('Decrypted message:', decrypted_text.decode('utf-8'))
```

The output:

```
Encrypted message: 6875fdb9774b10c5ca8aa51ac0f75662926552fb2320fa53d6345bb6c09d20
Decrypted message: Hello World!
```

## 2. ECDH

The _`ECDH`_ class is used to exchange keys using Elliptic Curve Diffie-Hellman algorithm.

### 2.1. ECDH curves

All curves can be imported directly from the library.

`SECP192R1`: NIST P-192

`SECP224R1`: NIST P-224

`SECP256R1`: NIST P-256

`SECP384R1`: NIST P-384

`SECP521R1`: NIST P-521

### 2.2. ECDH methods & parameters

The _`ECDH`_ class uses by default the `SECP521R1` curve (NIST P-521), but others can be used instead:

```
from py2crypt import ECDH, SECP192R1, SECP224R1, SECP256R1, SECP384R1, SECP521R1

dh = ECDH(SECP256R1)
```

`ECDH.private_key() -> _EllipticCurvePrivateKey`

The `private_key` method is used to return the private key object.

`ECDH.public_key() -> _EllipticCurvePublicKey`

The `public_key` method is used to return the public key object.

`ECDH.exchange(public_key: _EllipticCurvePublicKey) -> bytes`

The `exchange` method requires the `public_key` parameter (the peer public key) that must be the same object type returned by the `public_key` method.

### 2.3. ECDH example

```
from py2crypt import ECDH

alice = ECDH()
bob = ECDH()

alice_key = alice.exchange(bob.public_key())
bob_key = bob.exchange(alice.public_key())

print('Alice key:', alice_key.hex())
print('Bob key:', bob_key.hex())
```

The output:

```
Alice key: 01ae679b954c796ed030e0b658e20f8670d1bcea9778508b4036a91849353b9b4567723fe7a360612f355bb362bcbbc1885ada0aaea76ada2b71278bfc6d32a19be2
Bob key: 01ae679b954c796ed030e0b658e20f8670d1bcea9778508b4036a91849353b9b4567723fe7a360612f355bb362bcbbc1885ada0aaea76ada2b71278bfc6d32a19be2
```
## 3. HKDF

HKDF converts a secret into key material suitable for use in encryption, integrity checking or authentication. It is suitable for deriving keys of a fixed size used for other cryptographic operations.

### 3.1. HKDF methods & parameters

`HKDF(info: bytes, length: int = 32)`

The `info` parameter objective is to bind the derived key material to application. It is not recommended using it as a salt.

The `length` parameter specify the length to the output of the derived material. The default value is 32.

`HKDF.derive(material: bytes, salt: bytes|None = None)`

The `material` parameter is the input key material.

The `salt` parameter must be randomly generated or defined as `None`.

### 3.2. HKDF useful variables

You may want to change the default digest algorithm. It is possible to use `SHA256`, `SHA384`, and `SHA512`. The default digest is `SHA512`. 

### 3.3. HKDF example

```
from py2crypt import HKDF, SHA256, SHA384, SHA512

key = b'Material for KDF'

kdf = HKDF(info = b'HKDF', length = 32)

# Define SHA256 as the digest
kdf.digest = SHA256()

print('HKDF:', kdf.derive(key).hex())
print('HKDF salted:', kdf.derive(key, salt=b'salt').hex())
```

The output:

```
HKDF: 5acb02152e347b8d4515af7c4b99d050f75998354ea32df299f8f344044d58ff
HKDF salted: dcb3c321cc90f67bbb642db33a1bad0332f0632c7a6fa8b4d821021d9f4dfbdb
```

## 4. HKDFExpand

HKDF consists of two stages, extract and expand. This class exposes an expand only version of HKDF that is suitable when the key material is already cryptographically strong. _`HKDFExpand`_ should only be used if the key material is cryptographically strong. You should use _`HKDF`_ if you are unsure.

### 4.1. HKDFExpand methods & parameters

`HKDFExpand(info: bytes, length: int = 32) `

The `info` parameter objective is to bind the derived key material to application. It is not recommended using it as a salt.

The `length` parameter specify the length to the output of the derived material. The default value is 32.

`HKDFExpand.derive(material: bytes)`

The `material` parameter is the input key material.

### 4.2. HKDFExpand example

```
from py2crypt import HKDFExpand, SHA256, SHA384, SHA512

key = b'Material for KDF'

kdf = HKDFExpand(info=b'HKDF', length=64)

# Define SHA256 as the digest
kdf.digest = SHA256()

print('HKDF expanded:', kdf.derive(key).hex())
```

The output:
```
HKDF expanded: 69b89488c7a33d4a2a129be7e5bb3f22ed395029ea6d61c97f6a67565a31eff45ed24bb7f24ba2eb3a1bd4dd22110e849caad5b710aeac328857ac7c0979c667
```

## 5. HMAC

HMAC may be used to simultaneously verify both the data integrity and authenticity of a message.

### 5.1. HMAC methods & parameters

`HMAC(key: bytes)`

The `key` is a bytes object giving the secret key.

`HMAC.digest(message: bytes)`

The `digest` method return digest of `message` for given secret `key` and `digest`.

### 5.2. HMAC useful variables

You may want to change the default digest algorithm. It is possible to use `sha256`, `sha384`, and `sha512`. The default digest is `sha512`.

### 5.3. hmac_compare

`hmac_compare(message: bytes, key: bytes, hmac: bytes, digest=sha512)`

It will compare the digest of `message` for given secret `key` and `digest` with another `hmac`.

### 5.4. HMAC examples

```
from py2crypt import HMAC, hmac_compare, sha256, sha384, sha512

shared_key = b'ThisIsASecret'
message = b'The message'

hmac = HMAC(shared_key)

# Define sha256 as the digest
hmac.hash_algorithm = sha256

hmac_digest = hmac.digest(message)

print('HMAC:', hmac_digest.hex())
print('Is valid?', hmac_compare(message, shared_key, hmac_digest, sha256))
```

The output:

```
HMAC: 71fa6d82dba7ee1653c4a524f948a9ffd3ed97f3edf1fa39806da0e7d6639cb9
Is valid? True
```

## 6. RSA

Generates a local wallet that contains an RSA Private Key.

### 6.1. RSA methods & parameters

`RSA(private_key = None, length: int = 4096)`

Use a previous generated RSA private key in `private_key` parameter or set as `None`. The `length` parameter defines the length of the private key it will generate if `private key` parameter is `None.` 

`RSA.private_key()`

Return the private key object.

`RSA.public_key()`

Return the private key object.

`RSA.encrypt(public_key, plaintext: bytes) -> bytes`

Encrypt `plaintext` using a giving `public_key`.

`RSA.decrypt(ciphertext: bytes) -> bytes`

Decrypt `ciphertext` using the object private key.

`RSA.sign(content: bytes)`

Sign `content` using the object private key. The `content` will be hashed using the algorithm specified in `hash_algorithm` (default is `SHA512`). 

`RSA.verify(public_key, signature: bytes, content: bytes) -> bool`

Verify the `signature` of the `content` using the giving `public_key`.

### 6.2. RSA useful variables

You may want to change the default digest algorithm. It is possible to use `SHA256`, `SHA384`, and `SHA512`. The default digest is `SHA512`. 

### 6.3. RSA example

```
from py2crypt import RSA, SHA256, SHA384, SHA512

alice = RSA()
alice.hash_algorithm = SHA256()

bob = RSA()
bob.hash_algorithm = SHA256()

alice_encrypts_msg = alice.encrypt(bob.public_key(), b'Hello bob')
print('Alice encrypted msg:', alice_encrypts_msg.hex()[::6], end='\n\n')

alice_sign_msg = alice.sign(alice_encrypts_msg)
print('Alice signature:', alice_sign_msg.hex()[::6], end='\n\n')

bob_checks_alice_signature = bob.verify(alice.public_key(), alice_sign_msg, alice_encrypts_msg)
print('Is signature valid?', bob_checks_alice_signature, end='\n\n')

bob_decrypts_alice_msg = bob.decrypt(alice_encrypts_msg)
print('Bob decrypts msg:', bob_decrypts_alice_msg)
```

The output:

```
Alice encrypted msg: 526c76786a777df93dea64ad09c07d36d73926d27682ecf6149a83c885765dfaeb035676fbf590948c29b52376cbb3fd358b655ce1e2e19bfcba4ff7b7100e0ac65d8f8f3ef435d63efd04d50734be479027b812f27

Alice signature: 9c311b10a4613ef8bd78813fc6c320b8b859c5fdf3256c42910bc77477126eebbb9a17425a7692560d711f6df1a00bc1e8f5409362057243b8a0e000bc414d509ae6936616e8c33b96e36221fc590d74f05101c0b09

Is signature valid? True

Bob decrypts msg: b'Hello bob'
```

## 7. Import/Export

`export_private_key(private_key) -> bytes`

Export a private key object as a bytes type.

`export_public_key(public_key) -> bytes`

Export a public key object as a bytes type.

`import_private_key(private_key: bytes)`

Import a bytes type private key as a private key object.

`import_public_key(public_key: bytes)`

Import a bytes type public key as a public key object. 

### 7.1. Import/Export examples

```
from py2crypt import RSA, export_private_key, export_public_key, import_private_key, import_public_key

rsa = RSA()

output_private_key = export_private_key(rsa.private_key())
output_public_key = export_public_key(rsa.public_key())

input_private_key = import_private_key(output_private_key)
input_public_key = import_public_key(output_public_key)

print('output_private_key:', type(output_private_key))
print('output_public_key:', type(output_public_key))
print('input_private_key:', type(input_private_key))
print('input_public_key:', type(input_public_key))
```

The output:

```
output_private_key: <class 'bytes'>
output_public_key: <class 'bytes'>
input_private_key: <class 'cryptography.hazmat.backends.openssl.rsa._RSAPrivateKey'>
input_public_key: <class 'cryptography.hazmat.backends.openssl.rsa._RSAPublicKey'>
```