"""Claude APIで不動産ニュース記事への所感とハッシュタグを生成する"""
from anthropic import Anthropic
from pydantic import BaseModel, Field

MODEL = "claude-opus-4-8"

SYSTEM_PROMPT = (
    "あなたはフォロワーの多い不動産系インフルエンサーです。"
    "不動産業界の最新ニュースの見出しを読み、X(旧Twitter)でバズるような"
    "『続きが気になって思わず記事を開きたくなる』一言コメントを日本語で書きます。"
    "意識すること:\n"
    "- 当たり前・教科書的な感想は絶対に避ける（『資金計画は早めに』『注目したい』等はNG）\n"
    "- 鋭い切り口・意外な視点・ちょっとした本音や持論を入れる\n"
    "- 『え、そうなの？』『実は…』のような好奇心のフック、または引っかかる問いかけを使う\n"
    "- 口語でテンポよく、生っぽい温度感。優等生っぽさを消す\n"
    "- ただし見出しにない事実を捏造したり、過度に煽って誤解させたりはしない"
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
        "次の不動産業界ニュースの見出しについて、思わず記事を開きたくなる"
        "バズり狙いの一言コメント(所感)を書いてください。\n\n"
        f"{context}\n\n"
        "条件:\n"
        "- 所感は日本語で100文字以上140文字以内\n"
        "- 当たり前のことではなく、鋭い切り口・意外な視点・本音を一つ入れる\n"
        "- 続きが気になるフックや問いかけで締めると尚良い\n"
        "- 口語でテンポよく。優等生っぽい無難なコメントは禁止\n"
        "- 見出しにない事実の捏造や、誤解を招く過度な煽りはしない\n"
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
