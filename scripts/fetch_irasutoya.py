"""いらすとやから画像を検索・ダウンロードする（Blogger API使用）"""
import re
import hashlib
import requests
from pathlib import Path

CACHE_DIR = Path("/tmp/irasutoya")
_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
}
_API_BASE = "https://www.irasutoya.com/feeds/posts/default"


def _is_real_illustration(url: str) -> bool:
    """カテゴリサムネイルや非イラスト画像を除外する"""
    filename = url.split("/")[-1].split("\\")[0]
    # thumbnail_ で始まるのはカテゴリページのサムネイル（実際のイラストではない）
    if filename.startswith("thumbnail_"):
        return False
    # サイトUI系
    if any(x in filename for x in ["banner", "button", "logo", "navi", "pyoko", "searchbtn"]):
        return False
    return True


def fetch(keyword: str) -> Path | None:
    """キーワードでいらすとやを検索し、画像のPathを返す。失敗時はNone。"""
    CACHE_DIR.mkdir(exist_ok=True)
    cache_path = CACHE_DIR / f"{hashlib.md5(keyword.encode()).hexdigest()}.png"
    if cache_path.exists():
        return cache_path

    try:
        resp = requests.get(
            _API_BASE,
            params={"q": keyword, "max-results": 20, "alt": "json"},
            headers=_HEADERS,
            timeout=30,
        )
        resp.raise_for_status()
        data = resp.json()

        entries = data.get("feed", {}).get("entry", [])
        if not entries:
            print(f"⚠️  検索結果なし: [{keyword}]")
            return None

        img_url = None
        for entry in entries:
            thumb = entry.get("media$thumbnail", {})
            url = thumb.get("url", "")
            if url and _is_real_illustration(url):
                # s72-c → s600 に変換してフルサイズ取得
                img_url = re.sub(r"/s\d+-c/", "/s600/", url)
                break

        if not img_url:
            print(f"⚠️  適切な画像が見つかりませんでした: [{keyword}]")
            return None

        img_resp = requests.get(
            img_url,
            headers={**_HEADERS, "Referer": "https://www.irasutoya.com/"},
            timeout=30,
        )
        img_resp.raise_for_status()
        cache_path.write_bytes(img_resp.content)
        return cache_path

    except Exception as e:
        print(f"⚠️  いらすとや取得失敗 [{keyword}]: {e}")
        return None
