from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization
from pathlib import Path


KEY_DIR = Path(__file__).parent


def generate_keys():
    print("=" * 70)
    print("SECURENOVA - ED25519 AGENT IDENTITY KEY GENERATION")
    print("=" * 70)

    private_key = ed25519.Ed25519PrivateKey.generate()
    public_key = private_key.public_key()

    private_bytes = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )

    public_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )

    private_path = KEY_DIR / "agent_private.pem"
    public_path = KEY_DIR / "agent_public.pem"

    private_path.write_bytes(private_bytes)
    public_path.write_bytes(public_bytes)

    print("\n[KEY GENERATION]")
    print("Algorithm: Ed25519")

    print("\n[PRIVATE KEY]")
    print(f"Created: {private_path}")
    print(f"Exists: {private_path.exists()}")

    print("\n[PUBLIC KEY]")
    print(f"Created: {public_path}")
    print(f"Exists: {public_path.exists()}")

    print("\n[RESULT]")
    print("Ed25519 key pair generated successfully.")


if __name__ == "__main__":
    generate_keys()