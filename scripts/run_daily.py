"""不動産業界の最新ニュースを1件取得してLINEに送信するメインスクリプト"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from fetch_news import fetch_latest_unposted, mark_posted
from send_line import send_line_text

HASHTAGS = "#不動産 #不動産ニュース #住宅 #マンション #マイホーム"


def build_message(article: dict) -> str:
    lines = [f"📰 {article['title']}"]
    if article.get("source"):
        lines.append(f"（{article['source']}）")
    lines.append("")
    lines.append(article["link"])
    lines.append("")
    lines.append(HASHTAGS)
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", action="store_true",
                        help="ニュース取得のみ。LINEへの送信はスキップ")
    args = parser.parse_args()

    article = fetch_latest_unposted()
    if article is None:
        print("⚠️ 新しい未投稿ニュースが見つかりませんでした。")
        return

    print(f"📰 今日のニュース: {article['title']}")
    message = build_message(article)

    if args.test:
        print("✅ テストモード: 送信をスキップしました。")
        print(message)
        return

    send_line_text(message)
    mark_posted(article["link"])


if __name__ == "__main__":
    main()
