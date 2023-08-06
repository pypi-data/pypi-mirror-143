# String Signer

This module was created to sign strings.

It's only uses building libraries, therefore, it has no external dependency.
It is also lightweight and thread-safe, which makes it ideal for use in services and microservices.

The signed string respects the following format:
    string:hash_algorithm:salt:encoded_signature

## Typical usage example:


### Sign session
```python
string_signer = StringSigner("My Secret")

session_id = "b801692b-135f-40ff-8f7e-016dc7748c45"
session = {"user_uuid": "67fa3e17-4672-4036-8184-7fbe4c097439"}
encoded_session = base64.urlsafe_b64encode(json.dumps(session).encode()).decode()

signed_session = string_signer.sign(encoded_session)

redis.set(session_id, signed_session)
```

### Unsign session
```python
string_signer = StringSigner("My Secret")

session_id = "b801692b-135f-40ff-8f7e-016dc7748c45"

signed_session = redis.get(session_id)

encoded_session = string_signer.unsign(signed_session)
session = json.loads(base64.urlsafe_b64decode(encoded_session).decode())
```
