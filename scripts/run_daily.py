"""不動産業界の最新ニュースを1件取得し、所感を添えてLINEに送信する"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from fetch_news import fetch_latest_unposted, mark_posted
from generate_comment import generate_comment
from send_line import send_line_text


def build_message(article: dict, comment: str, hashtags: str) -> str:
    lines = [f"📰 {article['title']}"]
    if article.get("source"):
        lines.append(f"（{article['source']}）")
    lines.append("")
    lines.append(comment)
    lines.append("")
    lines.append(article["link"])
    lines.append("")
    lines.append(hashtags)
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", action="store_true",
                        help="取得と生成のみ。LINEへの送信はスキップ")
    args = parser.parse_args()

    article = fetch_latest_unposted()
    if article is None:
        print("⚠️ 新しい未投稿ニュースが見つかりませんでした。")
        return

    print(f"📰 今日のニュース: {article['title']}")

    print("🤖 所感を生成中...")
    comment, hashtags = generate_comment(article["title"], article.get("source", ""))
    print(f"   所感: {comment}")
    print(f"   ハッシュタグ: {hashtags}")

    message = build_message(article, comment, hashtags)

    if args.test:
        print("✅ テストモード: 送信をスキップしました。")
        print("--- 送信予定メッセージ ---")
        print(message)
        return

    send_line_text(message)
    mark_posted(article["link"])


if __name__ == "__main__":
    main()
