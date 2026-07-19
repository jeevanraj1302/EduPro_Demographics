"""
EduPro Demographics — Authentication Module
=============================================
Lightweight authentication with hashed passwords,
session management, and role-based access control.
"""

import hashlib
import secrets
from pathlib import Path
from typing import Optional

import yaml
import streamlit as st
from loguru import logger

from src.config import AUTH_CONFIG_FILE


# ══════════════════════════════════════════════
# Password Hashing
# ══════════════════════════════════════════════
def _hash_password(password: str, salt: Optional[str] = None) -> tuple[str, str]:
    """Hash a password with SHA-256 and a salt."""
    if salt is None:
        salt = secrets.token_hex(16)
    hashed = hashlib.sha256(f"{salt}{password}".encode()).hexdigest()
    return hashed, salt


def _verify_password(password: str, hashed: str, salt: str) -> bool:
    """Verify a password against its hash."""
    computed, _ = _hash_password(password, salt)
    return secrets.compare_digest(computed, hashed)


# ══════════════════════════════════════════════
# Config Loading
# ══════════════════════════════════════════════
def _load_auth_config() -> dict:
    """Load authentication configuration from YAML file."""
    if not AUTH_CONFIG_FILE.exists():
        _create_default_config()
    with open(AUTH_CONFIG_FILE, "r") as f:
        return yaml.safe_load(f)


def _create_default_config() -> None:
    """Create default authentication config with preset users."""
    admin_hash, admin_salt = _hash_password("admin123")
    viewer_hash, viewer_salt = _hash_password("viewer123")

    config = {
        "users": {
            "admin": {
                "name": "Administrator",
                "password_hash": admin_hash,
                "salt": admin_salt,
                "role": "admin",
            },
            "viewer": {
                "name": "Viewer",
                "password_hash": viewer_hash,
                "salt": viewer_salt,
                "role": "viewer",
            },
        },
        "settings": {
            "require_auth": False,
            "session_timeout_minutes": 60,
        },
    }

    AUTH_CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(AUTH_CONFIG_FILE, "w") as f:
        yaml.dump(config, f, default_flow_style=False)

    logger.info(f"Created default auth config at: {AUTH_CONFIG_FILE}")


# ══════════════════════════════════════════════
# Authentication Logic
# ══════════════════════════════════════════════
def authenticate(username: str, password: str) -> Optional[dict]:
    """
    Authenticate a user and return their info if valid.

    Parameters
    ----------
    username : str
        The username to authenticate.
    password : str
        The plaintext password.

    Returns
    -------
    dict or None
        User info dict if authenticated, None otherwise.
    """
    config = _load_auth_config()
    users = config.get("users", {})

    if username not in users:
        logger.warning(f"Login attempt with unknown user: {username}")
        return None

    user = users[username]
    if _verify_password(password, user["password_hash"], user["salt"]):
        logger.success(f"User '{username}' authenticated successfully.")
        return {
            "username": username,
            "name": user["name"],
            "role": user["role"],
        }

    logger.warning(f"Failed login attempt for user: {username}")
    return None


def is_auth_required() -> bool:
    """Check if authentication is required based on config."""
    config = _load_auth_config()
    return config.get("settings", {}).get("require_auth", False)


# ══════════════════════════════════════════════
# Session Management
# ══════════════════════════════════════════════
def is_logged_in() -> bool:
    """Check if the current session has an authenticated user."""
    return st.session_state.get("authenticated", False)


def get_current_user() -> Optional[dict]:
    """Get the current logged-in user's info."""
    if is_logged_in():
        return st.session_state.get("user_info", None)
    return None


def logout() -> None:
    """Log out the current user."""
    username = st.session_state.get("user_info", {}).get("username", "unknown")
    st.session_state["authenticated"] = False
    st.session_state["user_info"] = None
    logger.info(f"User '{username}' logged out.")


def render_login_page() -> bool:
    """
    Render the login form and handle authentication.

    Returns
    -------
    bool
        True if the user is authenticated, False otherwise.
    """
    if is_logged_in():
        return True

    st.markdown("""
    <div style="text-align: center; padding: 3rem 0 1rem 0;">
        <h1 style="
            font-size: 3rem;
            font-weight: 800;
            background: linear-gradient(135deg, #6C63FF, #FF6584);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin: 0;
        ">🎓 EduPro Analytics</h1>
        <p style="color: #A0A3B1; font-size: 1.1rem; margin-top: 0.5rem;">
            Sign in to access the Demographics Dashboard
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        with st.container():
            st.markdown("""
            <div style="
                background: linear-gradient(135deg, #1A1D29 0%, #252836 100%);
                border: 1px solid #2D3142;
                border-radius: 16px;
                padding: 2rem;
                margin: 1rem 0;
            ">
            """, unsafe_allow_html=True)

            username = st.text_input(
                "👤 Username",
                placeholder="Enter your username",
                key="login_username",
            )
            password = st.text_input(
                "🔒 Password",
                type="password",
                placeholder="Enter your password",
                key="login_password",
            )

            if st.button("🚀 Sign In", use_container_width=True, type="primary"):
                user_info = authenticate(username, password)
                if user_info:
                    st.session_state["authenticated"] = True
                    st.session_state["user_info"] = user_info
                    st.rerun()
                else:
                    st.error("❌ Invalid username or password.")

            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("""
            <div style="text-align: center; margin-top: 1rem;">
                <p style="color: #6B7280; font-size: 0.8rem;">
                    Default credentials: <code>admin</code> / <code>admin123</code>
                    &nbsp;|&nbsp; <code>viewer</code> / <code>viewer123</code>
                </p>
            </div>
            """, unsafe_allow_html=True)

    return False


def check_auth() -> bool:
    """
    Main auth gate — call this at the top of your app.
    Returns True if auth is not required or user is logged in.
    """
    if not is_auth_required():
        return True
    return render_login_page()

