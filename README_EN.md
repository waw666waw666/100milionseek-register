<h1 align="center">100MilionSeek Register</h1>

<p align="center">
  <b>100M Tokens/day Free Compute Automated Key Minting Tool for 100milionseek</b><br>
  <i>Built for zero-configuration, production-grade automated account generation and API key minting.</i>
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-Apache%202.0-22272e.svg?style=flat-square" alt="License"></a>
  <a href="DISCLAIMER.md"><img src="https://img.shields.io/badge/Disclaimer-Legal%20Terms-red.svg?style=flat-square" alt="Disclaimer"></a>
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.10%2B-3776ab.svg?style=flat-square&logo=python&logoColor=white" alt="Python"></a>
  <a href="https://playwright.dev/"><img src="https://img.shields.io/badge/Playwright-Stealth-2EAD33.svg?style=flat-square&logo=playwright&logoColor=white" alt="Playwright"></a>
  <a href="https://github.com/waw666waw666/RegisterHub"><img src="https://img.shields.io/badge/Powered%20By-RegisterHub-purple.svg?style=flat-square" alt="Powered By"></a>
</p>

<p align="center">
  <a href="./README_EN.md">English</a> | <a href="./README.md">简体中文</a>
</p>

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

### 4. AI Co-Pilot Workflow (Cursor / Claude Code / Windsurf / Gemini)

This subproject is optimized for seamless interaction with AI coding assistants:

**Prerequisite**: Open this project folder (**`100milionseek-register`**) as your active workspace root in your AI editor.

Choose between two workflows:

- **Method 1: Direct Prompting (Quick Interaction)**: Ask your AI: `Please inspect the environment, configure config.json, run main.py, and ensure new account records are written to results/accounts.txt`.
- **Method 2: Step-by-Step Prompting (Recommended)**: Instruct your AI:
  1. Verify Python dependencies and Playwright browser installation;
  2. Setup config.json based on config.example.json with proper proxy/mailbox;
  3. Execute python main.py and observe live logs;
  4. Verify extracted API keys in results/accounts.txt.

---

## Ecosystem Portfolio

Part of the RegisterHub open-source automation family:

| Standalone Project | Characteristics | Source Repository |
| :--- | :--- | :--- |
| **RegisterHub** | General Registration Engine & Scaffolding | [GitHub](https://github.com/waw666waw666/RegisterHub) |
| **Deepgram Register** | $200 USD Allowance + reCAPTCHA v2 Penetration | [GitHub](https://github.com/waw666waw666/deepgram-register) |
| **100MilionSeek Register** | 100M Tokens/day + Instant Card Key Harvester | [GitHub](https://github.com/waw666waw666/100milionseek-register) |
| **AMD AI Dev Register** | Official AMD Program + Akamai Telemetry Parity | [GitHub](https://github.com/waw666waw666/amd-register) |
| **Coarena Register** | Post-OAuth Pure REST Protocol Key Minting | [GitHub](https://github.com/waw666waw666/coarena-register) |

---

## Legal Disclaimer

This project is intended strictly for authorized educational research, browser automation benchmarking, and legitimate quality assurance. Users must strictly adhere to the target platform's Terms of Service and all applicable regional laws. See [DISCLAIMER.md](DISCLAIMER.md).

---

## Community & Support

Join our developer community for technical discussions, custom adapter requests, and browser automation best practices:

- **Discord Community**: [Join Discord](https://discord.gg/USnVJ9YQX)
- **QQ Group**: 1130324020
