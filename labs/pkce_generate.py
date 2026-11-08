#!/usr/bin/env python3
"""Demonstrate RFC 7636 S256; verifier is a transient secret, never commit it."""
import base64
import hashlib
import secrets


def generate_pair():
    verifier = secrets.token_urlsafe(32)
    digest = hashlib.sha256(verifier.encode('ascii')).digest()
    challenge = base64.urlsafe_b64encode(digest).decode('ascii').rstrip('=')
    return verifier, challenge


if __name__ == '__main__':
    verifier, challenge = generate_pair()
    print('PKCE code_challenge (safe to send in authorization request):', challenge)
    print('Verifier generated and held in memory. Use it only in the subsequent token request.')
