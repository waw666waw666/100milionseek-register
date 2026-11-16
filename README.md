# 100MilionSeek RegisterHub

> **100milionseek 每日一亿 Token 免费算力一键自动领 Key 工具**  
> 遵循“开箱即用，极简交付”原则，零复杂配置，一键下号并提取可用 API Key。

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%2B-brightgreen.svg)](https://www.python.org/)
[![Playwright](https://img.shields.io/badge/playwright-stealth-orange.svg)](https://playwright.dev/)
[![Powered By](https://img.shields.io/badge/Powered%20By-RegisterHub-purple.svg)](https://github.com/waw666waw666/RegisterHub)

---

## 框架母港与生态互链 (Ecosystem Backlink)

> **项目背景与互相引流说明**：  
> 本独立工程由 **[RegisterHub](https://github.com/waw666waw666/RegisterHub)** 开源注册自动化主框架一键解耦派生。  
> 
> 如果你需要探索**更多站点的自动化支持**（如 Deepgram、100MilionSeek、AMD、Coarena 等）、**三通道公网临时邮箱轮换**、**账号资产全生命周期审计**、或通过**脚手架一键生成新站点适配器**，欢迎前往并 Star 我们的主框架仓库：  
> 
> **主框架项目传送门**：**[https://github.com/waw666waw666/RegisterHub](https://github.com/waw666waw666/RegisterHub)**

---

## 项目简介

专为 100milionseek (https://100milionseek.top) 打造的一键领 Key 工具。免收激活邮件，过完 Cloudflare Turnstile 验证码后页面秒级直出 OpenAI 兼容 API Key，并内置母号裂变接力管理机制。

### 核心优势与技术特征

- **每天免费送 1 亿 Tokens**：新号直接享受 100M tokens/day 的 DeepSeek V4.1 免费算力
- **零邮箱验证门槛**：输入任意合规格式邮箱即可，完全无需接收验证码或激活信
- **Turnstile 3.5s 保护窗口**：针对 Cloudflare 算力挑战注入防打断保护窗，极大提升自主通过率
- **母号裂变接力池**：内置跨进程文件锁，每满 10 个 AFF 自动轮换至下一母号，吃满翻倍上限

---

## 极速上手

### 1. 环境准备与依赖安装

确保你的系统已安装 **Python ≥ 3.10**：

```bash
# 1. 克隆本项目
git clone https://github.com/waw666waw666/100milionseek-register.git
cd 100milionseek-register

# 2. 安装核心依赖
pip install -r requirements.txt

# 3. 安装 Playwright 浏览器驱动内核
playwright install chromium
```

### 2. 运行配置与核心实操说明

项目根目录提供开箱即用的 `config.example.json`。可复制为 `config.json` 进行配置：

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

### 核心必读：免邮箱验证与 Turnstile 人机协同 (Zero-Email Guide)

1. **零邮箱收信门槛（完全无需验证码）**：
   - 100MilionSeek 物理层面**不发送任何激活邮件或验证码**！
   - 脚本默认自动生成合规格式邮箱；若你想固定使用自己的邮箱，也可在 `config.json` 中配置 `"email": "your_name@outlook.com"`。
2. **Cloudflare Turnstile 算力验证**：
   - 启动有头窗口（双击 `run.bat` 选 1）；
   - 脚本会自动填入邮箱并预留 3.5 秒算力计算窗口；
   - 若屏幕上弹出 Cloudflare “请确认您是人类” 复选框，在真实窗口中轻点一下；
   - 验证通过后，前端卡片 `#done` 10 秒内直接渲染出明文 API Key，脚本毫秒级提纯并存入 `results/accounts.txt` 与 `results/keys.txt`！

### 3. 一键启动下号

在 Windows 终端中直接双击 **`run.bat`** 交互菜单，或在命令行运行：

```bash
# 默认生成 1 个账号凭据
python main.py

# 批量生成指定数量账号（如 5 个）
python main.py -n 5

# 无头静默模式运行
python main.py --headless -n 1
```

执行完毕后，所有生成的账号凭据将原子持久化落盘至 **`results/accounts.txt`**：
```text
邮箱----密码----有效API_Key----时间戳
```

---

## 体系化生态矩阵

本工程为 RegisterHub 家族核心实战矩阵之一：

| 独立开源项目 | 核心特色与福利 | 源码直达 |
| :--- | :--- | :--- |
| **RegisterHub** | 通用自动化注册母港与脚手架引擎 | [GitHub](https://github.com/waw666waw666/RegisterHub) |
| **Deepgram RegisterHub** | 官方 $200 免费额度 + 谷歌人机穿透 + 纯协议提 Key | [GitHub](https://github.com/waw666waw666/deepgram-register) |
| **100MilionSeek RegisterHub** | 每天免费 1 亿 Token 算力 + 免收信秒出 Key + 母号裂变 | [GitHub](https://github.com/waw666waw666/100milionseek-register) |
| **AMD AI Dev RegisterHub** | AMD 官方大厂计划 + Akamai 遥测 + OneTrust 穿透 | [GitHub](https://github.com/waw666waw666/amd-register) |
| **Coarena RegisterHub** | 谷歌登录后 100% 协议提 Key 与每日额度审计 | [GitHub](https://github.com/waw666waw666/coarena-register) |

---

## 免责声明 (Disclaimer)

本项目仅供软件工程自动化、浏览器驾驶协议与网络可用性技术交流与合法测试使用。使用者必须严格遵守目标平台服务条款与当地法律法规，严禁将本项目用于未经授权的大规模滥用或非法用途。作者不对任何因使用本项目造成的损失承担法律责任。详见 [DISCLAIMER.zh.md](DISCLAIMER.zh.md)。
