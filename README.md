# リアルな画像生成

素人がスマホで何気なく撮ったような、**生活感のあるリアルな画像**を生成するためのリポジトリ。
「いかにも生成AI」「プロのスタジオ撮影」感を徹底的に排除し、ショート動画の一時停止フレームや
友達に撮られた油断した瞬間のような自然さを狙う。

## 使い方（Claude Code スキル）

このリポジトリには `realistic-image` というスキルが入っている。Claude Code 上で

> リアルな画像を作りたい

のように頼むと、スキルが起動し、対話形式で条件を聞いてくる。

1. 画像のタイプ（ショート動画素材 / TikTok切り抜き風 / ストーリー風 / BeReal風 …）
2. 被写体（年代・性別・職業）
3. 見た目（日本人風 / 韓国人風 …）
4. 顔の見え方（顔あり / 横顔 / 手元だけ …）
5. シーン（場所 / 何をしている瞬間 / 時間帯・明るさ）
6. 仕上がりのリアルさ・服装・小物
7. サイズ（9:16 / 1:1 / 16:9）

選び終えると、プロっぽさ/AIっぽさを排した詳細な英語プロンプト（ポジティブ＋ネガティブ）を
組み立て、**実際に画像ファイルを生成**して見せてくれる。「おまかせ」と言えば全部自動で進む。

## 画像生成スクリプト単体での実行

スキルを使わず直接生成することもできる。

```bash
pip install -r requirements.txt

python scripts/generate_image.py \
  --prompt "A realistic vertical short-video app screen style image of ..." \
  --negative "exact TikTok logo, watermark, cinematic lighting, ..." \
  --aspect 9:16 \
  --out output/result.png
```

生成された画像は `output/`（git 管理外）に保存される。

## 画像生成バックエンド

| バックエンド | APIキー | 備考 |
|---|---|---|
| Pollinations (Flux) | 不要 | 完全無料・デフォルト |
| Google Gemini (nano banana) | 必要(無料枠あり) | `GEMINI_API_KEY` を設定すると自動的に使用 |

`GEMINI_API_KEY`（または `GOOGLE_API_KEY`）が設定されていれば Gemini を、
なければ Pollinations を自動で使う。`--backend` で明示指定も可能。

## 注意

- 未成年に見える人物・性的・露出の高い表現は生成しない。
- 実在ブランドのロゴ、実在店舗、特定個人へのなりすまし画像は生成しない。
- あくまで「リアルに見える」生成画像であり、本物の写真ではない。
