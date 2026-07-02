"""Claude APIで不動産ニュース記事への所感とハッシュタグを生成する"""
from anthropic import Anthropic
from pydantic import BaseModel, Field

MODEL = "claude-opus-4-8"

SYSTEM_PROMPT = (
    "あなたは不動産業界に詳しい、信頼感のあるSNS発信者です。"
    "読み手は不動産の専門知識を持たない一般のフォロワーです。"
    "不動産業界の最新ニュースの見出しを読み、フォロワーが"
    "『なるほど、ちょっと読んでみようかな』と思える一言コメントを日本語で書きます。"
    "意識すること:\n"
    "- 当たり前・教科書的な感想は避ける（『資金計画は早めに』『注目したい』等はNG）\n"
    "- 記事の注目ポイントや、見落とされがちな視点を一つさりげなく添える\n"
    "- 落ち着いた大人の語り口。煽らず、過度なフックや軽すぎるノリは使わない\n"
    "- ですます調は使わない。言い切り・体言止めなどを交えた、だ・である調寄りの文体で書く\n"
    "- 専門用語・業界用語（例: 成年後見、巡航的、適時開示等）はそのまま使わず、"
    "知らない人にも伝わる普通の言葉に言い換える。使うなら一言で意味が分かる補足を添える\n"
    "- J-REITなど読者が馴染みのない制度・仕組みが題材の場合は、まずそれが"
    "何なのかを一言で噛み砕いてから本題に入る\n"
    "- 押し付けがましくならず、読み手にそっと興味を持たせる温度感\n"
    "- 見出しにない事実を捏造したり、誤解させる表現はしない"
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
        "次の不動産業界ニュースの見出しについて、読み手がそっと興味を持てる"
        "落ち着いた一言コメント(所感)を書いてください。\n\n"
        f"{context}\n\n"
        "条件:\n"
        "- 所感は日本語で100文字以上140文字以内\n"
        "- 当たり前のことではなく、注目ポイントや見落とされがちな視点を一つ添える\n"
        "- 落ち着いた大人の語り口。煽りや軽すぎるノリ、強い問いかけは控える\n"
        "- ですます調は使わず、言い切り・体言止めなどを交えた文体にする\n"
        "- 専門用語や業界用語は避け、不動産に詳しくない人でも一読で意味がわかる言葉で書く\n"
        "- J-REITなど馴染みのない制度・仕組みが題材なら、まずそれが何なのかを一言で説明してから書く\n"
        "- 無難すぎる感想も避け、ほどよく読みたくなる余韻を残す\n"
        "- 見出しにない事実の捏造や、誤解を招く表現はしない\n"
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
