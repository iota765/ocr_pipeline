from typing import List, Dict


def redact_text(text: str, pii_list: List[Dict]) -> str:
    """
    Replace PII spans in text with [TYPE REDACTED].
    """
    redacted = text

    # Replace from end to start so indices don't shift
    for item in sorted(pii_list, key=lambda x: x["start"], reverse=True):
        label = item["type"].upper()
        replacement = f"[{label} REDACTED]"
        redacted = redacted[: item["start"]] + replacement + redacted[item["end"] :]

    return redacted
