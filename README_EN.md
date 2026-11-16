# 100MilionSeek RegisterHub

> **100M Tokens/day Free Compute Automated Key Minting Tool for 100milionseek**  
> Built for zero-configuration, production-grade automated account generation and API key minting.

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%2B-brightgreen.svg)](https://www.python.org/)
[![Playwright](https://img.shields.io/badge/playwright-stealth-orange.svg)](https://playwright.dev/)
[![Powered By](https://img.shields.io/badge/Powered%20By-RegisterHub-purple.svg)](https://github.com/waw666waw666/RegisterHub)

---

## Ecosystem & Backlink Notice

> **Framework Origin**:  
> This standalone tool is derived directly from **[RegisterHub](https://github.com/waw666waw666/RegisterHub)**, a general-purpose automated account registration and credential management framework.  
> 
> If you need multi-site orchestration, tri-channel disposable mailbox rotators, lifecycle credential verification, or automated adapter code generation scaffolds, check out our primary repository:  
> 
> **Main Framework Repository**: **[https://github.com/waw666waw666/RegisterHub](https://github.com/waw666waw666/RegisterHub)**

---

## Overview

An automated key minting tool built for 100milionseek (https://100milionseek.top). Bypasses email verification completely, resolves Cloudflare Turnstile, extracts OpenAI-compatible API keys in seconds, and manages cascading referral pools.

### Key Highlights

- **100M Tokens/day Free Allowance**: Instant access to DeepSeek V4.1 free compute quota
- **Zero Email Verification**: Accepts any standard email address without requiring code verification
- **Turnstile 3.5s Protection Window**: Prevents PoW interruption during Cloudflare challenges
- **Referral Pool Management**: Atomic file locking and automatic referral rotation to maximize allowances

---

## Quickstart

### 1. Prerequisites and Installation

Requires **Python ≥ 3.10**:

```bash
# Clone the repository
git clone https://github.com/waw666waw666/100milionseek-register.git
cd 100milionseek-register

# Install dependencies
pip install -r requirements.txt

# Install Playwright browser binaries
playwright install chromium
```

### 2. Configuration & Crucial Guidance

Copy `config.example.json` to `config.json` to configure proxies or headless mode:

```json
{
  "email": null,
  "browser": {
    "headless": false,
    "slow_mo": 50,
    "timeout": 35000,
    "channel": "chrome",
    "proxy": "http://127.0.0.1:7897"
  },
  "output_dir": "./results"
}
```

### Crucial: Zero-Email Friction & Turnstile Assistance

1. **Zero Email Verification Required**:
   - 100MilionSeek physically does NOT send any confirmation emails or OTP codes!
   - Synthetic emails are auto-generated. You can also specify `"email": "your_email@outlook.com"` in `config.json`.
2. **Cloudflare Turnstile Assistance**:
   - Run in headed window mode (double-click `run.bat` and select 1);
   - If Cloudflare prompts with "Verify you are human", click the checkbox in the window;
   - Once cleared, the `#done` card displays the API key within 10 seconds, and the script saves it to `results/accounts.txt` and `results/keys.txt`.

### 3. Execution

Launch via **`run.bat`** on Windows or execute directly via CLI:

```bash
# Mint 1 account & API key
python main.py

# Batch generate multiple accounts
python main.py -n 5

# Run headlessly in the background
python main.py --headless -n 1
```

Extracted credentials will be safely recorded in **`results/accounts.txt`**:
```text
email----password----api_key----timestamp
```

---

## Ecosystem Portfolio

Part of the RegisterHub open-source automation family:

| Standalone Project | Characteristics | Source Repository |
| :--- | :--- | :--- |
| **RegisterHub** | General Registration Engine & Scaffolding | [GitHub](https://github.com/waw666waw666/RegisterHub) |
| **Deepgram RegisterHub** | $200 USD Allowance + reCAPTCHA v2 Penetration | [GitHub](https://github.com/waw666waw666/deepgram-register) |
| **100MilionSeek RegisterHub** | 100M Tokens/day + Instant Card Key Harvester | [GitHub](https://github.com/waw666waw666/100milionseek-register) |
| **AMD AI Dev RegisterHub** | Official AMD Program + Akamai Telemetry Parity | [GitHub](https://github.com/waw666waw666/amd-register) |
| **Coarena RegisterHub** | Post-OAuth Pure REST Protocol Key Minting | [GitHub](https://github.com/waw666waw666/coarena-register) |

---

## Legal Disclaimer

This project is intended strictly for authorized educational research, browser automation benchmarking, and legitimate quality assurance. Users must strictly adhere to the target platform's Terms of Service and all applicable regional laws. See [DISCLAIMER.md](DISCLAIMER.md).
