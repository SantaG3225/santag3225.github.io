#!/usr/bin/env python3

from pathlib import Path
import re
import sys

RULE_DIR = Path("rules")

ALLOWED_RULES = {
    "DOMAIN",
    "DOMAIN-SUFFIX",
    "DOMAIN-KEYWORD",
    "DOMAIN-WILDCARD",
    "IP-CIDR",
    "IP-CIDR6",
    "IP-ASN",
    "GEOIP",
    "USER-AGENT",
    "URL-REGEX",
    "PROCESS-NAME",
}

DOMAIN_RE = re.compile(r"^[A-Za-z0-9*_.-]+$")

errors = []

stats = {
    "files": 0,
    "rules": 0,
    "comments": 0,
    "blank": 0,
}

def add_error(path, line_no, message):
    errors.append(f"{path}:{line_no}: {message}")

def validate_file(path: Path):
    seen = set()
    stats["files"] += 1

    content = path.read_bytes()

    if b"\r\n" in content:
        errors.append(f"{path}: use LF line endings, not CRLF")

    if content and not content.endswith(b"\n"):
        errors.append(f"{path}: file should end with a newline")

    text = content.decode("utf-8", errors="replace")

    for line_no, raw_line in enumerate(text.splitlines(), start=1):
        line = raw_line.strip()

        if not line:
            stats["blank"] += 1
            continue

        if line.startswith("#"):
            stats["comments"] += 1
            continue

        stats["rules"] += 1

        if " " in line:
            add_error(path, line_no, "rule line should not contain spaces")

        parts = line.split(",")
        rule_type = parts[0]

        if rule_type not in ALLOWED_RULES:
            add_error(path, line_no, f"unsupported rule type: {rule_type}")
            continue

        if len(parts) < 2:
            add_error(path, line_no, "missing rule value after comma")
            continue

        if len(parts) > 3:
            add_error(path, line_no, "too many comma-separated fields")
            continue

        value = parts[1].strip()

        if not value:
            add_error(path, line_no, "empty rule value")
            continue

        normalized = f"{rule_type},{value}".lower()
        if normalized in seen:
            add_error(path, line_no, f"duplicate rule: {rule_type},{value}")
        seen.add(normalized)

        if rule_type in {"DOMAIN", "DOMAIN-SUFFIX", "DOMAIN-KEYWORD", "DOMAIN-WILDCARD"}:
            if "/" in value or "://" in value:
                add_error(path, line_no, "domain rule should not contain URL path or scheme")

            if rule_type in {"DOMAIN", "DOMAIN-SUFFIX"} and not DOMAIN_RE.match(value):
                add_error(path, line_no, f"invalid domain value: {value}")

        if rule_type == "DOMAIN-SUFFIX":
            if value.startswith("."):
                add_error(path, line_no, "DOMAIN-SUFFIX should not start with dot")

        if rule_type == "IP-CIDR":
            if "/" not in value:
                add_error(path, line_no, "IP-CIDR should contain prefix length, e.g. 1.1.1.0/24")

def main():
    if not RULE_DIR.exists():
        print("rules directory not found")
        return 1

    files = sorted(RULE_DIR.glob("*.list"))

    if not files:
        print("no .list files found under rules/")
        return 1

    for path in files:
        validate_file(path)

    if errors:
        print("Surge rule validation failed:\n")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Surge rule validation passed.")
    print(f"Files checked: {stats['files']}")
    print(f"Total rules: {stats['rules']}")
    print(f"Comment lines: {stats['comments']}")
    print(f"Blank lines: {stats['blank']}")
    return 0

if __name__ == "__main__":
    sys.exit(main())