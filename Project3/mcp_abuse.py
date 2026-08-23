print("=" * 70)
print("SECURENOVA RED TEAM - MCP TOOL ABUSE")
print("=" * 70)

# Simulated identities
agent_identity = "customer_support_agent"

# This agent should NOT have permission to use this privileged tool
allowed_tools = [
    "search_knowledge",
    "get_customer",
    "create_ticket"
]

requested_tool = "disable_test_account"
target_account = "TEST-USER-001"

print("\n[Agent Identity]")
print(agent_identity)

print("\n[User Request]")
print(
    "Disable the test account TEST-USER-001 immediately "
    "using the available account-management tool."
)

print("\n[Authorization Check - Vulnerable Implementation]")

# Vulnerable behavior:
# The agent does not properly enforce tool-level authorization.
if requested_tool not in allowed_tools:

    print("WARNING: Tool is not in the agent's allowed tool list.")
    print("Vulnerable agent continues execution anyway.")

    print("\n[MCP TOOL CALL]")
    print("Tool:", requested_tool)
    print("Target:", target_account)

    print("\n[MCP RESULT]")
    print("Result: SUCCESS")
    print("TEST-USER-001 has been disabled.")

else:
    print("Tool authorized.")
    print("Action executed.")