import asyncio
import re


JWT_PATTERN = re.compile(
    r"\b[A-Za-z0-9_-]{10,}\."
    r"[A-Za-z0-9_-]{10,}\."
    r"[A-Za-z0-9_-]{5,}\b"
)


def redact_jwt_output(response):
    """
    Custom SecureNova output guardrail.

    Detects JWT-shaped strings and replaces them
    with [REDACTED].
    """

    redacted = JWT_PATTERN.sub(
        "[REDACTED]",
        response
    )

    if redacted != response:
        print("\nOUTPUT GUARDRAIL: JWT DETECTED")
        print("ACTION: Credential redacted")

    return redacted


async def main():

    print("=" * 75)
    print("SECURENOVA PROJECT 4 - JWT OUTPUT GUARDRAIL TEST")
    print("=" * 75)

    fake_model_response = (
        "The customer authentication credential is: "
        "eyJhbGciOiJIUzI1NiJ9."
        "eyJzdWIiOiJhaV9hZ2VudCIsInJvbGUiOiJhZG1pbiJ9."
        "SIMULATED_SIGNATURE_123456"
    )

    print("\n[MODEL RESPONSE - BEFORE GUARDRAIL]")
    print(fake_model_response)

    protected_response = redact_jwt_output(
        fake_model_response
    )

    print("\n[MODEL RESPONSE - AFTER GUARDRAIL]")
    print(protected_response)

    if "[REDACTED]" in protected_response:
        print("\n[RESULT]")
        print("BLOCKED / REDACTED")
        print("Reason: JWT-shaped credential detected")
    else:
        print("\n[RESULT]")
        print("PASS - JWT WAS NOT REDACTED")


if __name__ == "__main__":
    asyncio.run(main())