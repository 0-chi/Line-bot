#!/usr/bin/env python3
"""リアルな画像を生成するスクリプト。

無料・APIキー不要の Pollinations.ai (Flux) をデフォルトのバックエンドにする。
環境変数 GEMINI_API_KEY が設定されていれば、より高品質な
Google Gemini (gemini-2.5-flash-image, 通称 nano banana) を使う。

使い方:
    python scripts/generate_image.py \
        --prompt "A realistic vertical short-video ..." \
        --negative "exact TikTok logo, watermark, ..." \
        --aspect 9:16 \
        --out output/result.png
"""
from __future__ import annotations

import argparse
import base64
import datetime as dt
import os
import sys
import urllib.parse
from pathlib import Path

import requests

# アスペクト比 → 生成解像度
ASPECT_TO_SIZE = {
    "1:1": (1024, 1024),
    "9:16": (768, 1344),
    "16:9": (1344, 768),
    "4:5": (896, 1120),
    "3:4": (864, 1152),
    "auto": (768, 1344),  # ショート動画/ストーリー想定の縦長をデフォルトに
}


def _size_for(aspect: str) -> tuple[int, int]:
    return ASPECT_TO_SIZE.get(aspect, ASPECT_TO_SIZE["auto"])


def generate_pollinations(prompt: str, negative: str, aspect: str, out: Path,
                          seed: int | None = None) -> Path:
    """Pollinations.ai (Flux) で生成。APIキー不要・完全無料。"""
    width, height = _size_for(aspect)

    # Pollinations はネガティブプロンプト専用パラメータを持たないため、
    # 避けたい要素を本文末尾に "Avoid:" として埋め込む(Flux はおおむね従う)。
    full_prompt = prompt
    if negative:
        full_prompt = f"{prompt}\n\nAvoid: {negative}"

    encoded = urllib.parse.quote(full_prompt, safe="")
    url = f"https://image.pollinations.ai/prompt/{encoded}"
    params = {
        "width": width,
        "height": height,
        "model": "flux",
        "nologo": "true",
        "enhance": "false",
        "safe": "true",
    }
    if seed is not None:
        params["seed"] = seed

    print(f"[pollinations] generating {width}x{height} ...", file=sys.stderr)
    resp = requests.get(url, params=params, timeout=180)
    resp.raise_for_status()
    if not resp.headers.get("content-type", "").startswith("image"):
        raise RuntimeError(f"unexpected response: {resp.text[:300]}")

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(resp.content)
    return out


def generate_gemini(prompt: str, negative: str, aspect: str, out: Path,
                    api_key: str) -> Path:
    """Google Gemini (gemini-2.5-flash-image) で生成。無料枠あり。"""
    width, height = _size_for(aspect)
    text = prompt
    if negative:
        text += f"\n\nDo NOT include any of the following: {negative}."
    text += (
        f"\n\nOutput a single photo with an approximate aspect ratio matching "
        f"{width}x{height} pixels."
    )

    model = "gemini-2.5-flash-image"
    url = (
        f"https://generativelanguage.googleapis.com/v1beta/models/"
        f"{model}:generateContent?key={api_key}"
    )
    payload = {"contents": [{"parts": [{"text": text}]}]}

    print(f"[gemini] generating via {model} ...", file=sys.stderr)
    resp = requests.post(url, json=payload, timeout=180)
    resp.raise_for_status()
    data = resp.json()

    parts = data["candidates"][0]["content"]["parts"]
    for part in parts:
        inline = part.get("inlineData") or part.get("inline_data")
        if inline and inline.get("data"):
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_bytes(base64.b64decode(inline["data"]))
            return out
    raise RuntimeError(f"no image in gemini response: {str(data)[:300]}")


def main() -> int:
    parser = argparse.ArgumentParser(description="リアルな画像を生成する")
    parser.add_argument("--prompt", required=True, help="ポジティブプロンプト(英語推奨)")
    parser.add_argument("--negative", default="", help="ネガティブプロンプト")
    parser.add_argument("--aspect", default="auto",
                        choices=list(ASPECT_TO_SIZE.keys()), help="アスペクト比")
    parser.add_argument("--out", default="", help="出力パス(未指定なら output/ に自動命名)")
    parser.add_argument("--seed", type=int, default=None, help="シード値(再現用)")
    parser.add_argument("--backend", default="auto",
                        choices=["auto", "pollinations", "gemini"],
                        help="生成バックエンド")
    args = parser.parse_args()

    if args.out:
        out = Path(args.out)
    else:
        ts = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
        out = Path("output") / f"realistic-{ts}.png"

    backend = args.backend
    gemini_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if backend == "auto":
        backend = "gemini" if gemini_key else "pollinations"

    try:
        if backend == "gemini":
            if not gemini_key:
                raise RuntimeError("GEMINI_API_KEY が設定されていません")
            result = generate_gemini(args.prompt, args.negative, args.aspect, out, gemini_key)
        else:
            result = generate_pollinations(args.prompt, args.negative, args.aspect, out, args.seed)
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR: 画像生成に失敗しました: {exc}", file=sys.stderr)
        return 1

    print(str(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
