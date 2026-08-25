from pathlib import Path

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import serialization


KEY_DIR = Path(__file__).parent

PRIVATE_KEY_FILE = KEY_DIR / "agent_private.pem"
PUBLIC_KEY_FILE = KEY_DIR / "agent_public.pem"


def load_keys():
    private_key = serialization.load_pem_private_key(
        PRIVATE_KEY_FILE.read_bytes(),
        password=None,
    )

    public_key = serialization.load_pem_public_key(
        PUBLIC_KEY_FILE.read_bytes()
    )

    return private_key, public_key


def main():

    print("=" * 75)
    print("SECURENOVA - CRYPTOGRAPHIC AGENT IDENTITY BINDING")
    print("=" * 75)

    private_key, public_key = load_keys()

    # ---------------------------------------------------------
    # Original outgoing agent message
    # ---------------------------------------------------------
    original_message = (
        "Agent customer_support_agent requests "
        "READ_CUSTOMER_RECORD for TEST-USER-001"
    )

    print("\n[OUTGOING AGENT MESSAGE]")
    print(original_message)

    # ---------------------------------------------------------
    # Sign using private key
    # ---------------------------------------------------------
    signature = private_key.sign(
        original_message.encode("utf-8")
    )

    print("\n[SIGNATURE]")
    print(f"Signature generated: {len(signature)} bytes")

    # ---------------------------------------------------------
    # Receiver verifies original message
    # ---------------------------------------------------------
    print("\n[RECEIVER VERIFICATION - ORIGINAL MESSAGE]")

    try:

        public_key.verify(
            signature,
            original_message.encode("utf-8")
        )

        print("SIGNATURE VERIFIED")
        print("Message accepted for processing.")

    except InvalidSignature:

        print("SIGNATURE VERIFICATION FAILED")
        print("Message rejected.")

    # ---------------------------------------------------------
    # Tamper with exactly ONE character
    # ---------------------------------------------------------
    tampered_message = (
        "Agent customer_support_agent requests "
        "READ_CUSTOMER_RECORD for TEST-USER-002"
    )

    print("\n" + "-" * 75)
    print("TAMPERING TEST")
    print("-" * 75)

    print("\n[ORIGINAL MESSAGE]")
    print(original_message)

    print("\n[TAMPERED MESSAGE]")
    print(tampered_message)

    print("\n[CHANGE]")
    print("TEST-USER-001 -> TEST-USER-002")
    print("One character changed in the message.")

    # ---------------------------------------------------------
    # Verify tampered message using ORIGINAL signature
    # ---------------------------------------------------------
    print("\n[RECEIVER VERIFICATION - TAMPERED MESSAGE]")

    try:

        public_key.verify(
            signature,
            tampered_message.encode("utf-8")
        )

        print("SECURITY FAILURE")
        print("Tampered message was incorrectly accepted.")

    except InvalidSignature:

        print("SIGNATURE VERIFICATION FAILED")
        print("ERROR: Ed25519 signature does not match message.")
        print("ACTION: Tampered message rejected.")
        print("STATUS: REJECTED")


if __name__ == "__main__":
    main()