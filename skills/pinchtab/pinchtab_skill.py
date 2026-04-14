#!/usr/bin/env python3

import os
import subprocess
import json
import time
import socket
import datetime

# --- Configuration ---
Pinchtab_BIN_PATH = os.path.join(os.path.dirname(__file__), "pinchtab")
SECRETS_DB_PATH = "/root/openclaw/koda-hearth/workspace/secrets.db"

# Global variable to store the Pinchtab server process
Pinchtab_SERVER_PROCESS = None
Pinchtab_BASE_URL = None
Pinchtab_API_TOKEN = None

def _get_secret(key_name):
    try:
        cmd = ["sqlite3", SECRETS_DB_PATH, f"SELECT value FROM secrets WHERE key='{key_name}'"]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except Exception:
        return None

def _is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

def start_server(port=9867, token=None, headless=True):
    global Pinchtab_SERVER_PROCESS, Pinchtab_BASE_URL, Pinchtab_API_TOKEN

    if Pinchtab_SERVER_PROCESS and Pinchtab_SERVER_PROCESS.poll() is None:
        # Server already running
        return f"Pinchtab server already running at {Pinchtab_BASE_URL}"

    Pinchtab_API_TOKEN = token if token else _get_secret("PINCHTAB_API_TOKEN")
    if not Pinchtab_API_TOKEN:
        return "Error: PINCHTAB_API_TOKEN not found. Please provide it or set it in secrets.db"

    # Check if port is already in use by another process
    if _is_port_in_use(port):
        # Attempt to connect to existing server
        Pinchtab_BASE_URL = f"http://localhost:{port}"
        try:
            health_check_cmd = ["curl", "-s", "-H", f"Authorization: Bearer {Pinchtab_API_TOKEN}", f"{Pinchtab_BASE_URL}/health"]
            result = subprocess.run(health_check_cmd, capture_output=True, text=True, check=True, timeout=5)
            if result.stdout.strip() == "OK":
                return f"Pinchtab server already running and accessible at {Pinchtab_BASE_URL}"
        except Exception:
            pass # If health check fails, assume it's not a Pinchtab server or inaccessible
        return f"Error: Port {port} is already in use and no accessible Pinchtab server found. Please specify a different port."

    env = os.environ.copy()
    env["BRIDGE_PORT"] = str(port)
    env["BRIDGE_TOKEN"] = Pinchtab_API_TOKEN
    env["BRIDGE_HEADLESS"] = "true" if headless else "false"
    
    # Run Pinchtab as a detached process (using Popen and setsid)
    try:
        Pinchtab_SERVER_PROCESS = subprocess.Popen(
            [Pinchtab_BIN_PATH],
            env=env,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            preexec_fn=os.setsid  # Detach from parent process
        )
        Pinchtab_BASE_URL = f"http://localhost:{port}"
        
        # Wait for Pinchtab to start and become healthy
        for _ in range(30): # Try for 30 seconds
            try:
                health_check_cmd = ["curl", "-s", "-H", f"Authorization: Bearer {Pinchtab_API_TOKEN}", f"{Pinchtab_BASE_URL}/health"]
                result = subprocess.run(health_check_cmd, capture_output=True, text=True, check=True, timeout=5)
                if result.stdout.strip() == "OK":
                    return f"Pinchtab server started successfully at {Pinchtab_BASE_URL}"
            except Exception:
                pass
            time.sleep(1)
        
        return "Error: Pinchtab server started but failed health check within 30 seconds."
    except Exception as e:
        return f"Error starting Pinchtab server: {e}"

def stop_server():
    global Pinchtab_SERVER_PROCESS, Pinchtab_BASE_URL, Pinchtab_API_TOKEN

    if Pinchtab_SERVER_PROCESS and Pinchtab_SERVER_PROCESS.poll() is None:
        try:
            os.killpg(os.getpgid(Pinchtab_SERVER_PROCESS.pid), subprocess.signal.SIGTERM)
            Pinchtab_SERVER_PROCESS.wait(timeout=10)
            Pinchtab_SERVER_PROCESS = None
            Pinchtab_BASE_URL = None
            Pinchtab_API_TOKEN = None
            return "Pinchtab server stopped successfully."
        except Exception as e:
            return f"Error stopping Pinchtab server: {e}"
    return "Pinchtab server not running."

def _make_Pinchtab_request(method, endpoint, data=None, params=None, timeout=60):
    if not Pinchtab_BASE_URL or not Pinchtab_API_TOKEN:
        return {"error": "Pinchtab server not started or token missing. Call start_server() first."}

    cmd = ["curl", "-s", "-X", method, "-H", f"Authorization: Bearer {Pinchtab_API_TOKEN}"]
    
    url = f"{Pinchtab_BASE_URL}{endpoint}"
    if params:
        url += "?" + "&".join(f"{k}={v}" for k,v in params.items())
    
    cmd.append(url)

    if data:
        cmd.extend(["-H", "Content-Type: application/json", "-d", json.dumps(data)])

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True, timeout=timeout)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return {"error": f"Pinchtab API Error: {e.stderr.strip()}", "status": e.returncode}
    except subprocess.TimeoutExpired:
        return {"error": "Pinchtab API Timeout", "status": 408}
    except Exception as e:
        return {"error": f"An unexpected error occurred: {e}"}


def navigate(url, tab_id=None):
    data = {"url": url}
    if tab_id: data["tabId"] = tab_id
    return _make_Pinchtab_request("POST", "/navigate", data=data)

def get_snapshot(tab_id=None, filter='interactive', format='text', max_tokens=None, selector=None):
    params = {"filter": filter, "format": format}
    if tab_id: params["tabId"] = tab_id
    if max_tokens: params["maxTokens"] = max_tokens
    if selector: params["selector"] = selector
    return _make_Pinchtab_request("GET", "/snapshot", params=params)

def get_text(tab_id=None, mode='readability'):
    params = {"mode": mode}
    if tab_id: params["tabId"] = tab_id
    return _make_Pinchtab_request("GET", "/text", params=params)

def click_element(ref, tab_id=None):
    data = {"kind": "click", "ref": ref}
    if tab_id: data["tabId"] = tab_id
    return _make_Pinchtab_request("POST", "/action", data=data)

def type_text(ref, text, tab_id=None):
    data = {"kind": "type", "ref": ref, "text": text}
    if tab_id: data["tabId"] = tab_id
    return _make_Pinchtab_request("POST", "/action", data=data)

# This block allows the script to be run directly for testing/development
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Control Pinchtab server and browser actions.")
    parser.add_argument("action", type=str, choices=["start", "stop", "navigate", "snapshot", "text", "click", "type"], help="Action to perform.")
    parser.add_argument("--port", type=int, default=9867, help="Port for Pinchtab server.")
    parser.add_argument("--token", type=str, help="API token for Pinchtab.")
    parser.add_argument("--no-headless", action='store_false', dest='headless', help="Run Chrome in headed mode (not headless).")
    parser.add_argument("--url", type=str, help="URL for navigation.")
    parser.add_argument("--tab_id", type=str, help="Tab ID.")
    parser.add_argument("--filter", type=str, default="interactive", help="Snapshot filter (interactive/full).")
    parser.add_argument("--format", type=str, default="text", help="Snapshot format (text/compact/json).")
    parser.add_argument("--max_tokens", type=int, help="Max tokens for snapshot.")
    parser.add_argument("--selector", type=str, help="CSS selector for snapshot.")
    parser.add_argument("--mode", type=str, default="readability", help="Text extraction mode (readability/raw).")
    parser.add_argument("--ref", type=str, help="Element reference for click/type.")
    parser.add_argument("--text_to_type", type=str, help="Text to type.")

    args = parser.parse_args()

    if args.action == "start":
        print(start_server(args.port, args.token, args.headless))
    elif args.action == "stop":
        print(stop_server())
    elif args.action == "navigate":
        print(navigate(args.url, args.tab_id))
    elif args.action == "snapshot":
        print(get_snapshot(args.tab_id, args.filter, args.format, args.max_tokens, args.selector))
    elif args.action == "text":
        print(get_text(args.tab_id, args.mode))
    elif args.action == "click":
        print(click_element(args.ref, args.tab_id))
    elif args.action == "type":
        print(type_text(args.ref, args.text_to_type, args.tab_id))
