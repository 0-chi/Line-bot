"""不動産業界の最新ニュースをGoogle News RSSから取得する"""
import json
import re
from pathlib import Path
from xml.etree import ElementTree

import requests

ROOT = Path(__file__).parent.parent
POSTED_LOG = ROOT / "content" / "posted_news.json"

RSS_URL = "https://news.google.com/rss/search"
QUERY = (
    "不動産 OR 住宅市場 OR マンション市場 OR 不動産トラブル OR 空き家問題 OR "
    "住宅ローン OR 賃貸トラブル OR 不動産詐欺"
)

# 決算説明資料・適時開示など、事務的すぎて一般読者に刺さりにくい記事の特徴語。
# 該当する記事は他に選べる記事がある限り後回しにする。
_LOW_APPEAL_KEYWORDS = ("決算", "適時開示", "説明資料", "四半期報告", "有価証券報告書")


def _is_low_appeal(title: str) -> bool:
    return any(keyword in title for keyword in _LOW_APPEAL_KEYWORDS)

_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
}


def _load_posted() -> set[str]:
    if POSTED_LOG.exists():
        return set(json.loads(POSTED_LOG.read_text(encoding="utf-8")))
    return set()


def _save_posted(posted: set[str]) -> None:
    POSTED_LOG.parent.mkdir(exist_ok=True)
    # 直近500件だけ保持（ファイル肥大化防止）
    trimmed = sorted(posted)[-500:]
    POSTED_LOG.write_text(
        json.dumps(trimmed, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def _strip_source(title: str) -> str:
    """Google Newsのタイトル末尾の ' - 媒体名' を取り除く"""
    return re.sub(r"\s+-\s+[^-]+$", "", title)


def fetch_latest_unposted() -> dict | None:
    """未投稿の最新ニュース記事を1件取得する。なければNoneを返す"""
    resp = requests.get(
        RSS_URL,
        params={"q": QUERY, "hl": "ja", "gl": "JP", "ceid": "JP:ja"},
        headers=_HEADERS,
        timeout=30,
    )
    resp.raise_for_status()
    root = ElementTree.fromstring(resp.content)

    posted = _load_posted()

    fallback = None
    for item in root.findall("./channel/item"):
        link = item.findtext("link", "").strip()
        if not link or link in posted:
            continue

        title = _strip_source(item.findtext("title", "").strip())
        article = {
            "title": title,
            "link": link,
            "source": item.findtext("source", "").strip(),
            "pub_date": item.findtext("pubDate", "").strip(),
        }

        if not _is_low_appeal(title):
            return article
        if fallback is None:
            fallback = article

    return fallback


def mark_posted(link: str) -> None:
    """記事を投稿済みとして記録する"""
    posted = _load_posted()
    posted.add(link)
    _save_posted(posted)


if __name__ == "__main__":
    article = fetch_latest_unposted()
    print(article)
