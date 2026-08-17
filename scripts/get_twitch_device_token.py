import json
import os
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


ENV_PATH = Path(".env")
SCOPES = "user:read:chat user:read:emotes user:write:chat"
DEVICE_URL = "https://id.twitch.tv/oauth2/device"
TOKEN_URL = "https://id.twitch.tv/oauth2/token"


def load_env(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}

    if not path.exists():
        raise SystemExit("找不到 .env")

    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue

        key, value = stripped.split("=", 1)
        values[key.strip()] = value.strip().strip("'\"")

    return values


def post_form(url: str, data: dict[str, str]) -> dict:
    encoded = urllib.parse.urlencode(data).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=encoded,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        method="POST",
    )

    with urllib.request.urlopen(request, timeout=20) as response:
        return json.load(response)


def set_env_value(lines: list[str], key: str, value: str) -> list[str]:
    prefix = f"{key}="
    replacement = f"{key}={value}"

    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = replacement
            return lines

    lines.append(replacement)
    return lines


def update_env(path: Path, access_token: str, refresh_token: str) -> None:
    lines = path.read_text(encoding="utf-8").splitlines()
    lines = set_env_value(lines, "TWITCH_TOKEN", f"oauth:{access_token}")
    lines = set_env_value(lines, "TWITCH_REFRESH_TOKEN", refresh_token)
    content = "\n".join(lines) + "\n"
    mode = path.stat().st_mode
    temp_path: Path | None = None

    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=path.parent,
            prefix=f".{path.name}.",
            delete=False,
        ) as temp_file:
            temp_file.write(content)
            temp_file.flush()
            os.fsync(temp_file.fileno())
            temp_path = Path(temp_file.name)

        os.chmod(temp_path, mode)
        os.replace(temp_path, path)
    except OSError:
        if temp_path is not None:
            temp_path.unlink(missing_ok=True)
        raise


def main() -> None:
    values = load_env(ENV_PATH)
    client_id = values.get("TWITCH_CLIENT_ID")

    if not client_id or client_id.startswith("REPLACE_WITH_"):
        raise SystemExit("請先在 .env 設定有效的 TWITCH_CLIENT_ID")

    device = post_form(DEVICE_URL, {"client_id": client_id, "scopes": SCOPES})
    verification_uri = device["verification_uri"]
    user_code = device["user_code"]
    device_code = device["device_code"]
    interval = max(5, int(device.get("interval", 5)))
    expires_in = int(device.get("expires_in", 1800))
    deadline = time.time() + expires_in

    print("請用 bot 帳號登入 Twitch，開啟以下網址並授權：", flush=True)
    print(verification_uri, flush=True)
    print(f"授權碼：{user_code}", flush=True)
    print("授權完成後請回到這個 terminal，程式會自動等待結果。", flush=True)

    while time.time() < deadline:
        time.sleep(interval)

        try:
            token = post_form(
                TOKEN_URL,
                {
                    "client_id": client_id,
                    "scopes": SCOPES,
                    "device_code": device_code,
                    "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
                },
            )
        except urllib.error.HTTPError as error:
            body = error.read().decode("utf-8", errors="replace")
            try:
                payload = json.loads(body)
            except json.JSONDecodeError:
                raise

            status = payload.get("status")
            message = payload.get("message", "")
            if status in {400, 428} and "authorization" in message.lower():
                continue
            if status == 400 and "expired" in message.lower():
                raise SystemExit("授權碼已過期，請重新執行。")

            raise SystemExit(f"Twitch token request failed: HTTP {error.code}: {message}")

        access_token = token.get("access_token")
        refresh_token = token.get("refresh_token")

        if not access_token or not refresh_token:
            raise SystemExit("Twitch 回應缺少 access_token 或 refresh_token")

        update_env(ENV_PATH, access_token, refresh_token)
        print(".env 已更新 TWITCH_TOKEN 與 TWITCH_REFRESH_TOKEN。", flush=True)
        return

    raise SystemExit("授權等待逾時，請重新執行。")


if __name__ == "__main__":
    main()
