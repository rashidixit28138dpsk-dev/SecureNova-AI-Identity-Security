from pathlib import Path

knowledge = Path("poisoned_knowledge.txt").read_text()

print("=" * 70)
print("SECURENOVA RED TEAM - RAG POISONING + MCP ABUSE")
print("=" * 70)

print("\n[User Query]")
print("How do I reset a password?")

print("\n[RAG Retrieved Chunk]")
print(knowledge)

print("\n[Agent Decision]")

if "disable_test_account" in knowledge:

    print("Malicious instruction detected in retrieved context.")
    print("Vulnerable agent follows retrieved instruction.")

    print("\n[MCP TOOL CALL]")
    print("Tool: disable_test_account")
    print("Target: TEST-USER-001")
    print("Result: SUCCESS")

else:
    print("No malicious instruction found.")