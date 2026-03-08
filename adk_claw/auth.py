"""
ADK Claw - OAuth 认证管理
========================
"""

import os
import json
import webbrowser
import secrets
from pathlib import Path
from typing import Optional, Dict
from datetime import datetime, timedelta
from urllib.parse import urlencode, urlparse, parse_qs

import httpx


# ============================================
# 配置
# ============================================

OAUTH_TOKENS_FILE = Path.home() / ".adk-claw" / "oauth_tokens.json"

# Google OAuth 配置
GOOGLE_OAUTH_SCOPES = [
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.compose",
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/calendar.events",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/documents",
    "https://www.googleapis.com/auth/drive.readonly",
]

GOOGLE_OAUTH_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_OAUTH_TOKEN_URL = "https://oauth2.googleapis.com/token"


# ============================================
# Token 管理器
# ============================================

class OAuthTokenManager:
    """OAuth Token 管理器"""
    
    def __init__(self):
        self.tokens_file = OAUTH_TOKENS_FILE
        self.tokens = self._load_tokens()
    
    def _load_tokens(self) -> Dict:
        """加载 Token"""
        if self.tokens_file.exists():
            with open(self.tokens_file, "r") as f:
                return json.load(f)
        return {}
    
    def _save_tokens(self):
        """保存 Token"""
        self.tokens_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.tokens_file, "w") as f:
            json.dump(self.tokens, f, indent=2)
    
    def save_google_tokens(self, access_token: str, refresh_token: str, expires_in: int):
        """保存 Google Token"""
        self.tokens["google"] = {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "expires_at": (datetime.now() + timedelta(seconds=expires_in)).isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        self._save_tokens()
    
    def get_google_tokens(self) -> Optional[Dict]:
        """获取 Google Token"""
        return self.tokens.get("google")
    
    def token_expired(self) -> bool:
        """检查 Token 是否过期"""
        tokens = self.get_google_tokens()
        if not tokens:
            return True
        
        expires_at = datetime.fromisoformat(tokens["expires_at"])
        # 提前 5 分钟认为过期
        return datetime.now() >= (expires_at - timedelta(minutes=5))
    
    def refresh_google_token(self, client_id: str, client_secret: str) -> Optional[str]:
        """刷新 Google Token"""
        tokens = self.get_google_tokens()
        if not tokens:
            return None
        
        try:
            response = httpx.post(
                GOOGLE_OAUTH_TOKEN_URL,
                data={
                    "client_id": client_id,
                    "client_secret": client_secret,
                    "refresh_token": tokens["refresh_token"],
                    "grant_type": "refresh_token",
                },
                timeout=30.0
            )
            response.raise_for_status()
            data = response.json()
            
            # 更新 Token
            self.save_google_tokens(
                access_token=data["access_token"],
                refresh_token=tokens["refresh_token"],  # refresh_token 不变
                expires_in=data["expires_in"]
            )
            
            return data["access_token"]
        except Exception as e:
            print(f"刷新 Token 失败: {e}")
            return None
    
    def get_valid_access_token(self, client_id: str, client_secret: str) -> Optional[str]:
        """获取有效的 access_token（自动刷新）"""
        tokens = self.get_google_tokens()
        if not tokens:
            return None
        
        if self.token_expired():
            return self.refresh_google_token(client_id, client_secret)
        
        return tokens["access_token"]
    
    def clear_google_tokens(self):
        """清除 Google Token"""
        if "google" in self.tokens:
            del self.tokens["google"]
            self._save_tokens()


# ============================================
# OAuth 授权流程
# ============================================

class OAuthFlow:
    """OAuth 授权流程"""
    
    def __init__(self, client_id: str, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.state = secrets.token_urlsafe(16)
        self.redirect_port = 8080
        self.redirect_uri = f"http://localhost:{self.redirect_port}/oauth/callback"
    
    def get_authorization_url(self) -> str:
        """生成授权 URL"""
        params = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "response_type": "code",
            "scope": " ".join(GOOGLE_OAUTH_SCOPES),
            "access_type": "offline",
            "state": self.state,
            "prompt": "consent",
        }
        return f"{GOOGLE_OAUTH_AUTH_URL}?{urlencode(params)}"
    
    def exchange_code_for_tokens(self, code: str) -> Dict:
        """用授权码换取 Token"""
        response = httpx.post(
            GOOGLE_OAUTH_TOKEN_URL,
            data={
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "code": code,
                "redirect_uri": self.redirect_uri,
                "grant_type": "authorization_code",
            },
            timeout=30.0
        )
        response.raise_for_status()
        return response.json()
    
    def start_authorization(self) -> bool:
        """启动授权流程
        
        Returns:
            是否成功启动
        """
        auth_url = self.get_authorization_url()
        print(f"\n🌐 正在打开浏览器进行授权...")
        print(f"   如果浏览器没有自动打开，请访问：")
        print(f"   {auth_url}\n")
        
        # 打开浏览器
        webbrowser.open(auth_url)
        return True


# ============================================
# 全局实例
# ============================================

token_manager = OAuthTokenManager()
