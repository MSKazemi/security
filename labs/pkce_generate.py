#!/usr/bin/env python3
"""RFC 7636 PKCE S256 demonstration with an offline, public test-vector check.

Never print or log real verifiers in production. The --show-verifier option exists
ONLY for an isolated disposable classroom demonstration.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import re
import secrets

# Published RFC 7636 Appendix B test vector, not an operational credential.
RFC_VERIFIER = "dBjftJeZ4CVP-mB92K27uhbUJU1p1r_wW1gFWFOEjXk"
RFC_CHALLENGE = "E9Melhoa2OwvFrEMTJguCHaoeK1t8URWbuGJSstw-cM"
VERIFIER_RE = re.compile(r"[A-Za-z0-9._~-]{43,128}\Z")


def s256_challenge(verifier: str) -> str:
    """Compute BASE64URL(SHA256(ASCII(verifier))) without '=' padding."""
    if not VERIFIER_RE.fullmatch(verifier):
        raise ValueError("Verifier must contain 43-128 RFC 7636 unreserved characters")
    digest = hashlib.sha256(verifier.encode("ascii")).digest()
    return base64.urlsafe_b64encode(digest).decode("ascii").rstrip("=")


def generate_pair() -> tuple[str, str]:
    """Generate a fresh 256-bit-entropy PKCE verifier and its S256 challenge."""
    verifier = secrets.token_urlsafe(32)
    return verifier, s256_challenge(verifier)


def self_test() -> None:
    assert s256_challenge(RFC_VERIFIER) == RFC_CHALLENGE, "RFC 7636 vector mismatch"
    verifier, challenge = generate_pair()
    assert VERIFIER_RE.fullmatch(verifier), "Unexpected verifier character or length"
    assert len(verifier) == 43, "Expected 43-character verifier from 32 random bytes"
    assert len(challenge) == 43, "Unexpected S256 challenge length"
    assert challenge == s256_challenge(verifier), "Generated verifier/challenge mismatch"
    assert generate_pair()[0] != verifier, "Unexpected duplicate verifier"
    try:
        s256_challenge("too-short")
    except ValueError:
        pass
    else:
        raise AssertionError("Invalid verifier was accepted")


def main() -> None:
    parser = argparse.ArgumentParser(description="RFC 7636 PKCE S256 classroom tool")
    parser.add_argument("--self-test", action="store_true", help="Check published RFC vector and local invariants")
    parser.add_argument("--show-verifier", action="store_true",
                        help="LAB ONLY: print the generated secret verifier to the terminal")
    args = parser.parse_args()
    if args.self_test:
        self_test()
        print("PASS: RFC 7636 S256 test vector and format checks")
        return
    verifier, challenge = generate_pair()
    print("code_challenge:", challenge)
    print("code_challenge_method: S256")
    if args.show_verifier:
        print("LAB ONLY code_verifier:", verifier)
    else:
        print("code_verifier generated but hidden. Keep it secret for the token request.")


if __name__ == "__main__":
    main()
