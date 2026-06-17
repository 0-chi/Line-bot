"""Claude APIで不動産ニュース記事への所感とハッシュタグを生成する"""
from anthropic import Anthropic
from pydantic import BaseModel, Field

MODEL = "claude-opus-4-8"

SYSTEM_PROMPT = (
    "あなたは不動産業界に精通したSNS運用担当者です。"
    "不動産業界の最新ニュースの見出しを読み、個人アカウントがLINEやInstagramに"
    "投稿するための所感コメントを日本語で書きます。"
    "専門的になりすぎず、フォロワーが『なるほど』と思える親しみやすい語り口にします。"
)


class NewsComment(BaseModel):
    comment: str = Field(description="記事の見出しに対する所感。日本語で100〜140文字。")
    hashtags: list[str] = Field(
        description="記事に関連性の高いハッシュタグ。#を除いた語句のみ。5〜8個。"
    )


def generate_comment(title: str, source: str = "") -> tuple[str, str]:
    """ニュース見出しから所感と、整形済みハッシュタグ文字列を生成して返す"""
    client = Anthropic()  # ANTHROPIC_API_KEY を環境変数から読み込む

    context = f"見出し: {title}"
    if source:
        context += f"\n媒体: {source}"

    user_message = (
        "次の不動産業界ニュースの見出しについて、SNS投稿用の所感を書いてください。\n\n"
        f"{context}\n\n"
        "条件:\n"
        "- 所感は日本語で100文字以上140文字以内\n"
        "- 見出しから読み取れる範囲で、業界や生活者への影響にも触れる\n"
        "- 断定しすぎず、誇張や煽りは避ける\n"
        "- ハッシュタグは記事内容に関連性の高いものを5〜8個（#は付けない）"
    )

    response = client.messages.parse(
        model=MODEL,
        max_tokens=2000,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_message}],
        output_format=NewsComment,
    )

    result = response.parsed_output
    hashtags = " ".join(f"#{tag.lstrip('#')}" for tag in result.hashtags)
    return result.comment, hashtags


if __name__ == "__main__":
    c, h = generate_comment("マンション価格、都心部で上昇続く", "日本経済新聞")
    print(c)
    print(h)
