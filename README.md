# SantaG Surge Rules
<a href="https://www.digitalocean.com/?refcode=eb602945d727&utm_campaign=Referral_Invite&utm_medium=Referral_Program&utm_source=badge"><img src="https://web-platforms.sfo2.cdn.digitaloceanspaces.com/WWW/Badge%201.svg" alt="DigitalOcean Referral Badge" /></a>


Personal Surge rule sets for iOS, designed for a setup with a U.S. proxy node.

These rule sets are intended to keep China mainland services direct, route selected global services through a proxy, and separate education-related login traffic for easier troubleshooting.

## Rule Sets

| File | Purpose | Suggested Policy |
| --- | --- | --- |
| `rules/ai.list` | AI services and related domains | `Proxy` |
| `rules/global.list` | Global services, developer tools, Google, YouTube, GitHub, and selected media platforms | `Proxy` |
| `rules/china-direct.list` | China mainland domains and services | `DIRECT` |
| `rules/edu.list` | Education websites, school portals, SSO, Microsoft login, Canvas, and MFA services | `Proxy` |
| `rules/private.list` | Private or custom rules | Depends on your setup |

## Surge Usage

Example rule configuration:

```ini
[Rule]
RULE-SET,https://santag3225.github.io/rules/edu.list,Proxy
RULE-SET,https://santag3225.github.io/rules/ai.list,Proxy
RULE-SET,https://santag3225.github.io/rules/global.list,Proxy
RULE-SET,https://santag3225.github.io/rules/china-direct.list,DIRECT
GEOIP,CN,DIRECT
FINAL,DIRECT
```

If your proxy policy group uses a different name, replace `Proxy` with your own policy name, for example:

```ini
RULE-SET,https://santag3225.github.io/rules/global.list,US
```

## Recommended Routing Logic

For a Malaysia user with a U.S. node:

```text
Education / AI / GitHub / Google / YouTube -> U.S. proxy
China mainland services                  -> DIRECT
Malaysia local services                  -> DIRECT
Unknown traffic                          -> DIRECT
```

This setup does not provide a China mainland return route. If a service requires a China mainland IP address, a China mainland or return-home proxy node is still required.

## Rule Format

Each `.list` file uses Surge-compatible rule set syntax:

```ini
# Comment
DOMAIN-SUFFIX,example.com
DOMAIN,login.example.com
DOMAIN-KEYWORD,example
IP-CIDR,1.1.1.0/24
```

Do not include the policy name inside `.list` files. The policy should be assigned in the main Surge configuration:

```ini
RULE-SET,https://santag3225.github.io/rules/global.list,Proxy
```

## Validation

This repository uses GitHub Actions to validate Surge rule format automatically.

The validation checks for:

- Unsupported rule types
- Missing rule values
- Too many comma-separated fields
- Duplicate rules inside the same file
- Invalid domain values
- URL-style values inside domain rules
- CRLF line endings
- Missing newline at the end of a file

## Notes

- Rules are organized for personal use and may not fit every network environment.
- Some platforms may use additional login, CDN, or tracking domains.
- If a website fails to load, check Surge logs and add the missing domain to the appropriate rule list.
- For China streaming unlocks, a real China mainland exit node is required.

## Disclaimer

These rule sets are provided for personal network routing and learning purposes. Please follow local laws, platform terms, and network policies when using them.
