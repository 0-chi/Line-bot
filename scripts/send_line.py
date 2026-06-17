"""LINE Messaging API でテキストメッセージを送信する"""
import os
import requests


def send_line_text(text: str) -> None:
    token = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
    user_id = os.environ["LINE_USER_ID"]

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    body = {"to": user_id, "messages": [{"type": "text", "text": text}]}
    resp = requests.post(
        "https://api.line.me/v2/bot/message/push",
        headers=headers,
        json=body,
        timeout=30,
    )
    if not resp.ok:
        raise RuntimeError(f"LINE API error {resp.status_code}: {resp.text}")
    print("✅ LINEに送信しました！")
