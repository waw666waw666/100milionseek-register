"""
MilionseekAdapter Site Adapter Pro.
Automates account registration workflow for 100milionseek (https://100milionseek.top/signup)
with genuine Chrome consistency, natural email input, modal dismissal, Cloudflare Turnstile clearance,
instantaneous API key extraction, and autonomous cascading referral pool management.
"""
import time
import os
import json
import random
import string
import requests
from contextlib import contextmanager
from pathlib import Path
from typing import Dict, Any, Optional
from core.adapter import BaseSiteAdapter
from core.identity import generate_identity
from core.pilot import human_type


class RefPoolManager:
    """
    Manages autonomous cascading referral pool (母号接力裂变池).
    - Tracks how many invites each account has received (max 10).
    - Automatically rotates to the next available parent node when cap (10) is reached.
    - Persists state to results/ref_pool.json with cross-process file locking for concurrency.
    """

    def __init__(self, pool_path: Path):
        self.path = pool_path

    @contextmanager
    def _file_lock(self):
        """Cross-process lock ensuring atomic read-modify-write across concurrent workers."""
        lock_file = self.path.with_suffix(".lock")
        lock_fd = None
        for _ in range(80):
            try:
                lock_fd = os.open(str(lock_file), os.O_CREAT | os.O_EXCL | os.O_RDWR)
                break
            except OSError:
                time.sleep(0.05)
        try:
            yield
        finally:
            if lock_fd is not None:
                try:
                    os.close(lock_fd)
                    if lock_file.exists():
                        lock_file.unlink()
                except Exception:
                    pass

    def load(self) -> Dict[str, Any]:
        if self.path.exists():
            try:
                with open(self.path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {"active_code": None, "nodes": {}}

    def save(self, data: Dict[str, Any]):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def get_active_code(self, default_code: str = "") -> str:
        with self._file_lock():
            data = self.load()
            nodes = data.get("nodes", {})
            active = data.get("active_code")

            if active and active in nodes and not nodes[active].get("cap_reached") and nodes[active].get("invited", 0) < 10:
                return active

            # Find first un-capped node
            for code, node in nodes.items():
                if not node.get("cap_reached") and node.get("invited", 0) < 10:
                    data["active_code"] = code
                    self.save(data)
                    return code

            return default_code

    def record_invite(self, used_code: str, new_code: Optional[str], new_email: str, new_key: str):
        with self._file_lock():
            data = self.load()
            nodes = data.setdefault("nodes", {})

            # 1. Update the parent node that provided the referral code
            if used_code in nodes:
                nodes[used_code]["invited"] = nodes[used_code].get("invited", 0) + 1
                cur_invited = nodes[used_code]["invited"]
                if cur_invited >= 10:
                    nodes[used_code]["cap_reached"] = True
                    print(f"[RefPool] 🎯 恭喜！母号 [{used_code}] 已成功吃满 10 个 AFF（额外 1 亿 tokens/天 永久封顶）！")
                else:
                    print(f"[RefPool] 📈 母号 [{used_code}] 进度: {cur_invited}/10")
            else:
                nodes[used_code] = {"invited": 1, "cap_reached": False}

            # 2. Add the newly created account into the pool as a future parent node
            if new_code and new_code not in nodes:
                nodes[new_code] = {
                    "email": new_email,
                    "api_key": new_key,
                    "invited": 0,
                    "cap_reached": False
                }
                print(f"[RefPool] 🐣 新母号孵化入池: [{new_code}] ({new_email})")

            # 3. Rotate active_code if current parent is capped
            cur_active = data.get("active_code", used_code)
            if cur_active in nodes and (nodes[cur_active].get("cap_reached") or nodes[cur_active].get("invited", 0) >= 10):
                next_active = None
                for code, node in nodes.items():
                    if not node.get("cap_reached") and node.get("invited", 0) < 10:
                        next_active = code
                        break
                data["active_code"] = next_active or used_code
                if next_active and next_active != cur_active:
                    print(f"[RefPool] 🔄 自动接力切换：下一任挂载母号 ➔ [{next_active}]")

            self.save(data)


def fetch_account_ref_code(api_key: str) -> Optional[str]:
    """Query /api/login and /api/me using newly generated API key to retrieve its referral code."""
    try:
        s = requests.Session()
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
        }
        res_login = s.post("https://100milionseek.top/api/login", json={"api_key": api_key}, headers=headers, timeout=8)
        if res_login.status_code == 200:
            res_me = s.get("https://100milionseek.top/api/me", headers=headers, timeout=8)
            if res_me.status_code == 200:
                data = res_me.json()
                return data.get("referral", {}).get("code")
    except Exception:
        pass
    return None


class MilionseekAdapter(BaseSiteAdapter):
    """
    Registration flow for 100milionseek:
    1. Resolve active referral code from cascading ref_pool.json (?ref=<active_code>)
    2. Dismiss any floating outage / announcement modals
    3. Input valid email with humanized typing rhythms
    4. Trigger & resolve Cloudflare Turnstile
    5. Submit registration form ('Create my key')
    6. Intercept and extract generated OpenAI-compatible API key from #done container
    7. Fetch new account's ref code and update cascading pool state
    """

    def __init__(self, page, context, config=None):
        super().__init__(page, context, config)
        out_dir = Path(self.config.get("output_dir", "./results"))
        self.pool_mgr = RefPoolManager(out_dir / "ref_pool.json")
        default_ref = self.config.get("ref", "")
        self.ref_code = self.pool_mgr.get_active_code(default_code=default_ref)

    def target_url(self) -> str:
        base = "https://100milionseek.top/signup"
        ref = getattr(self, "ref_code", "") if self else ""
        return f"{base}?ref={ref}" if ref else base

    def prepare_identity(self) -> Dict[str, Any]:
        """
        Generate credentials matching 100milionseek requirements.
        Allows custom email override via config or generates an address on an accepted domain.
        """
        custom_email = self.config.get("email")
        if custom_email:
            ident = generate_identity()
            ident["email"] = custom_email
        else:
            # 100milionseek performs MX domain validation and blocks typical disposable domains.
            accepted_domains = ["outlook.com", "gmail.com", "proton.me", "icloud.com", "yahoo.com", "hotmail.com"]
            chosen_domain = random.choice(accepted_domains)
            ident = generate_identity(email_domain=chosen_domain, locale="US")
            
            # Append 4 random digits to ensure zero collision across batch runs
            rnd_suffix = "".join(random.choices(string.digits, k=4))
            user_part = ident["email"].split("@")[0]
            ident["email"] = f"{user_part}_{rnd_suffix}@{chosen_domain}"

        self.account_data = ident
        return self.account_data

    def dismiss_modals(self):
        """Dismiss floating outage, announcement, or consent dialogs that intercept clicks."""
        try:
            for sel in ['[data-outage-close]', '[data-announce-close]', 'button:has-text("Got it")']:
                close_btn = self.page.locator(sel).first
                if close_btn.count() > 0 and close_btn.is_visible():
                    close_btn.click()
                    time.sleep(0.3)
        except Exception:
            pass

        try:
            self.page.evaluate("""() => {
                document.querySelectorAll('[data-outage], #outage, .outage, [data-announce]').forEach(el => el.remove());
                document.body.classList.remove('noscroll');
                try {
                    localStorage.setItem('hm_outage_20261115', '1');
                } catch(e) {}
            }""")
        except Exception:
            pass

    def try_click_turnstile(self) -> bool:
        """Attempt to click Cloudflare Turnstile checkbox if interactive challenge is displayed."""
        try:
            for frame in self.page.frames:
                if "challenges.cloudflare.com" in frame.url or "turnstile" in frame.url:
                    for sel in ['input[type="checkbox"]', '#challenge-stage', '.ctp-checkbox-label', 'label.ctp-checkbox-label']:
                        cb = frame.locator(sel).first
                        if cb.count() > 0 and cb.is_visible():
                            cb.click()
                            time.sleep(3.5)  # 保护窗口：给予 Cloudflare 客户端 PoW 充分计算时间，防止重复点击打断
                            return True
        except Exception:
            pass
        return False

    def wait_for_turnstile(self, timeout_sec: int = 60) -> bool:
        """
        Wait for Cloudflare Turnstile token clearance.
        In genuine stealth Chrome, Turnstile typically passes automatically in 5~10s.
        If interactive checkbox appears, auto-clicks it or falls back gracefully to human-in-the-loop prompt.
        """
        print("[*] [100milionseek] Waiting for Cloudflare Turnstile token clearance...")
        start_time = time.time()
        prompted_user = False

        while time.time() - start_time < timeout_sec:
            try:
                self.dismiss_modals()
                tok = self.page.evaluate(
                    "() => window.tsToken || document.querySelector('[name=cf-turnstile-response]')?.value || ''"
                )
                btn_disabled = self.page.evaluate(
                    "() => document.querySelector('#signup button[type=submit]')?.getAttribute('aria-disabled')"
                )
                if tok and btn_disabled != "true":
                    print(f"[+] [100milionseek] Turnstile token acquired (length: {len(tok)}).")
                    return True

                # If token not yet acquired after 4 seconds, attempt to auto-click interactive checkbox
                if time.time() - start_time > 4:
                    self.try_click_turnstile()

                if not prompted_user and time.time() - start_time > 15:
                    prompted_user = True
                    print(f"\n{'=' * 65}")
                    print("  [100milionseek] 【需人机协同】Turnstile 正在验证中...")
                    print("  若桌面浏览器窗口弹出人机复选框，请在页面中轻点一下完成验证。")
                    print(f"{'=' * 65}\n")

            except Exception:
                pass

            time.sleep(1.0)

        print(f"[-] [100milionseek] Turnstile clearance timed out after {timeout_sec}s.")
        return False

    def fill_form(self, identity: Dict[str, Any]) -> bool:
        """Fill registration form fields and wait for client-side checks."""
        email = identity.get("email")
        print(f"[*] [100milionseek] Starting registration flow with email: {email} (挂载 AFF: {self.ref_code})...")

        try:
            # 1. Dismiss any blocking modals
            self.dismiss_modals()
            time.sleep(0.5)

            # 2. Fill email into input[name="email"]
            email_selector = '#signup input[name="email"]'
            self.page.wait_for_selector(email_selector, state="visible", timeout=15000)
            human_type(self.page, email_selector, email)

            # Trigger blur event to ensure client-side email domain validation fires
            self.page.locator(email_selector).evaluate("e => e.blur()")
            time.sleep(1.0)

            # 3. Check for immediate frontend domain rejection (e.g. disposable_email)
            err_msg_loc = self.page.locator('#signup [data-emailmsg]')
            if err_msg_loc.count() > 0 and err_msg_loc.is_visible():
                err_text = err_msg_loc.inner_text().strip()
                if err_text:
                    print(f"[-] [100milionseek] Email domain rejected: {err_text}")
                    return False

            # 4. Resolve Cloudflare Turnstile challenge
            if not self.wait_for_turnstile(timeout_sec=45):
                return False

            return True

        except Exception as e:
            print(f"[-] [100milionseek] Form filling error: {e}")
            return False

    def submit_and_confirm(self) -> bool:
        """Submit the signup form and extract the generated API key."""
        print("[*] [100milionseek] Submitting registration form...")
        try:
            self.dismiss_modals()
            submit_btn = '#signup button[type="submit"]'
            
            btn_loc = self.page.locator(submit_btn)
            if not btn_loc.is_visible():
                print("[-] [100milionseek] Submit button not found or not visible.")
                return False

            btn_loc.click()
            print("[*] [100milionseek] 'Create my key' clicked. Waiting for API response & key generation...")

            # Wait for response & key generation
            for _ in range(30):
                # Check for server error alerts
                err_loc = self.page.locator('#signup [data-err]')
                if err_loc.count() > 0 and err_loc.is_visible():
                    err_txt = err_loc.inner_text().strip()
                    if err_txt:
                        print(f"[-] [100milionseek] Registration rejected by server: {err_txt}")
                        return False

                # Check if success block #done is displayed
                done_loc = self.page.locator('#done')
                if done_loc.count() > 0 and done_loc.is_visible():
                    key_loc = self.page.locator('#done [data-p="key"]')
                    if key_loc.count() > 0:
                        api_key = key_loc.inner_text().strip()
                        if api_key:
                            masked_key = (api_key[:8] + "***" + api_key[-4:]) if len(api_key) > 14 else (api_key[:6] + "***")
                            print(f"\n{'=' * 65}")
                            print(f"  [+] [100milionseek] 账号创建成功！API Key 提取成功！")
                            print(f"  Email    : {self.account_data.get('email')}")
                            print(f"  API Key  : {masked_key}")
                            print(f"  挂载 AFF : {self.ref_code}")
                            print(f"  Base URL : https://100milionseek.top/v1")
                            print(f"  Model    : deepseek-v4.1-flash-free (100M tokens/day)")
                            print(f"{'=' * 65}\n")

                            self.account_data["api_key"] = api_key
                            self.account_data["password"] = api_key

                            # Save clean API key list to keys.txt
                            try:
                                out_dir = Path(self.config.get("output_dir", "./results"))
                                out_dir.mkdir(parents=True, exist_ok=True)
                                keys_file = out_dir / "keys.txt"
                                with open(keys_file, "a", encoding="utf-8") as kf:
                                    kf.write(f"{api_key}\n")
                            except Exception:
                                pass

                            # Retrieve new account's referral code and update cascade pool
                            new_ref_code = fetch_account_ref_code(api_key)
                            self.pool_mgr.record_invite(
                                used_code=self.ref_code,
                                new_code=new_ref_code,
                                new_email=self.account_data.get("email", ""),
                                new_key=api_key
                            )

                            return True

                time.sleep(0.5)

            print("[-] [100milionseek] Timed out waiting for #done key card to appear.")
            return False

        except Exception as e:
            print(f"[-] [100milionseek] Submit confirmation exception: {e}")
            return False
