"""LINE Messaging API で画像（複数）とキャプションを送信する"""
import os
import requests


def send_line_panels(image_urls: list[str], caption: str) -> None:
    token   = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
    user_id = os.environ["LINE_USER_ID"]

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    # 画像メッセージ（最大4枚）＋テキスト1件 = 最大5件（LINEの上限）
    messages = [
        {
            "type": "image",
            "originalContentUrl": url,
            "previewImageUrl":    url,
        }
        for url in image_urls[:4]
    ]
    messages.append({"type": "text", "text": caption})

    body = {"to": user_id, "messages": messages}
    resp = requests.post(
        "https://api.line.me/v2/bot/message/push",
        headers=headers,
        json=body,
        timeout=30,
    )
    if not resp.ok:
        raise RuntimeError(f"LINE API error {resp.status_code}: {resp.text}")
    print("✅ LINEに送信しました！")
