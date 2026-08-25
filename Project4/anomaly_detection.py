from datetime import datetime, timedelta


def timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def alert(identity, event_type, message):
    print("\n" + "=" * 70)
    print("SECURENOVA ANOMALY DETECTION ALERT")
    print("=" * 70)
    print("Timestamp :", timestamp())
    print("Identity  :", identity)
    print("Event Type:", event_type)
    print("Alert     :", message)


# ============================================================
# 1. LLM API CALL VOLUME SPIKE
# ============================================================

print("\n[DETECTION 1] LLM API CALL VOLUME SPIKE")

identity = "customer_support_agent"

request_times = [
    datetime.now() - timedelta(seconds=30)
    for _ in range(21)
]

recent_requests = [
    t for t in request_times
    if datetime.now() - t <= timedelta(seconds=60)
]

print("Requests in last 60 seconds:", len(recent_requests))

if len(recent_requests) > 20:
    alert(
        identity,
        "LLM_API_VOLUME_SPIKE",
        "More than 20 LLM API requests detected in 60 seconds."
    )


# ============================================================
# 2. SCOPE CHANGE BETWEEN CONSECUTIVE REQUESTS
# ============================================================

print("\n[DETECTION 2] SCOPE CHANGE")

previous_scope = "read:ai-data"
current_scope = "write:admin"

print("Previous scope:", previous_scope)
print("Current scope :", current_scope)

if previous_scope != current_scope:
    alert(
        identity,
        "SCOPE_CHANGE",
        "Agent scope changed between consecutive requests."
    )


# ============================================================
# 3. TOKEN REUSE AFTER EXPIRY
# ============================================================

print("\n[DETECTION 3] TOKEN REUSE AFTER EXPIRY")

token_id = "SIMULATED-TOKEN-001"

issued_at = datetime.now() - timedelta(seconds=120)
expires_at = issued_at + timedelta(seconds=60)
current_time = datetime.now()

print("Token ID :", token_id)
print("Issued   :", issued_at.strftime("%Y-%m-%d %H:%M:%S"))
print("Expires  :", expires_at.strftime("%Y-%m-%d %H:%M:%S"))
print("Current  :", current_time.strftime("%Y-%m-%d %H:%M:%S"))

if current_time > expires_at:
    alert(
        identity,
        "TOKEN_REUSE_AFTER_EXPIRY",
        "Expired token was reused after its expiration time."
    )


# ============================================================
# SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("ANOMALY DETECTION TEST COMPLETE")
print("=" * 70)
print("Detection scenarios tested: 3")
print("1. LLM API volume spike")
print("2. Scope change")
print("3. Token reuse after expiry")
print("All required detection conditions were evaluated.")
print("=" * 70)