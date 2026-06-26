---
name: realistic-image
description: 素人がスマホで撮ったような「リアルな画像」を対話形式で生成するスキル。被写体・見た目・顔の見え方・シーン・リアルさ等を選択肢で選んでもらい、プロっぽさ/AIっぽさを排した詳細なプロンプトを組み立てて、実際に画像ファイルまで生成する。ユーザーが「リアルな画像を作りたい」「ショート動画の1シーン素材」「TikTok切り抜き風」「BeReal風」「自然なスマホ写真」などを求めたときに使う。
---

# リアルな画像生成スキル

「いかにも生成AIで作りました」感や、プロのスタジオ撮影感を**徹底的に排除**し、
**素人がスマホで何気なく撮った生活感のあるリアルな写真**に寄せた画像を生成する。

## ゴール

- プロっぽい / AIっぽい / 盛れすぎた写真を避ける
- 微ブレ・ノイズ・白飛び・不完全な構図など「リアルな粗さ」をあえて入れる
- ショート動画の一時停止フレームや、友達に撮られた油断した瞬間のような自然さ

## 進め方（対話フロー）

ユーザーに以下を順番に聞いていく。**全部聞くのではなく、テンポよく**進める。
- ユーザーが最初から細かく指定してきたら、不足分だけ確認する
- 「おまかせ」と言われたら、自然で無難な組み合わせをこちらで決めて即生成する
- 各ステップは番号で答えてもらってもいいし、自由入力でもいい

各ステップの選択肢を提示し、回答を集めてから「プロンプト組み立てルール」に従って
英語のポジティブ／ネガティブプロンプトを作り、最後に画像を生成する。

### STEP 1. 画像のタイプ
```
[1] ショート動画の1シーン素材
[2] TikTok切り抜き風
[3] ストーリー投稿風
[4] BeReal風
[5] プロフィール画像
[6] 広告・訴求用素材
[7] その他：自由入力
```

### STEP 2. 被写体（誰を撮るか）
```
[1] 20代女性   [2] 30代女性   [3] 20代男性   [4] 30代男性
[5] 主婦・母親 [6] 会社員     [7] 看護師     [8] 転職希望者
[9] 副業に興味がある人 [10] 学生 [11] 店員・アルバイト
[12] コンビニ店員 [13] カフェ店員 [14] 事務職 [15] 営業職
[16] 元面接官  [17] 顔なし・手元だけ  [自由入力可]
```

### STEP 3. 見た目【B】
```
[1] 日本人風  [2] 韓国人風  [3] アジア系ミックス風
[4] 海外風    [5] 指定なし  [6] その他：自由入力
```

### STEP 4. 顔の見え方【C】
```
[1] 顔あり   [2] 横顔   [3] 後ろ姿   [4] 顔の一部だけ
[5] スマホで顔を隠す  [6] 手元だけ  [7] 顔なし
[8] 遠目で顔がはっきり見えない  [9] その他：自由入力
```

### STEP 5. シーン
```
【A】場所
 [1] カフェの席 [2] 自宅の机 [3] 駅前 [4] 電車内
 [5] 友達といる居酒屋 [6] 鏡の前 [7] 街中の歩道 [自由入力可]

【B】何をしている瞬間か
 [1] スマホを見ている
 [2] スマホで顔の一部を隠している
 [3] 飲み物を持って少し横を向いている
 [4] 友達に撮られて少し油断している
 [5] 歩きながらスマホを確認している
 [6] 鏡越しにスマホを持っている
 [7] その他：自由入力

【C】時間帯・明るさ
 [1] 朝・自然光 [2] 昼・明るい [3] 夕方・西日
 [4] 夜・室内照明 [5] 夜・コンビニの蛍光灯 [6] 夜・居酒屋の暖色照明
 [7] 少し暗め [8] 明るいけど白飛び気味 [9] 曇りの日の柔らかい光
 [10] 駅や街灯の光 [11] その他：自由入力
```

### STEP 6. 仕上がりのリアルさ／服装・小物
```
【リアルさ】
 [1] 少しだけ素人っぽい [2] かなり自然なスマホ写真 [3] 生活感強め
 [4] 少しブレ・ノイズ多め [5] 清潔感あり [6] その他：自由入力

【服装・小物】
 [1] おまかせ [2] 仕事着・制服風 [3] 私服寄り [4] スマホを目立たせる
 [5] 飲み物や小物も入れる [6] 生活感のある背景小物を増やす [7] その他
```

### STEP 7. サイズ【D】
```
[1] 自動でOK(縦長 9:16) [2] 1:1 [3] 9:16 [4] 16:9 [5] その他
```

## プロンプト組み立てルール

集めた選択肢から英語のプロンプトを組み立てる。日本語の選択肢は下の対応表で英語へ変換する。

### ポジティブプロンプトの雛形
```
A realistic <TYPE> style image of <SUBJECT> <LOOK>, at <PLACE> <LIGHTING>,
<ACTION>. <CLOTHING_AND_PROPS>. <FACE_VISIBILITY>.
The image should look like a paused frame from a casual short video / an
amateur smartphone snapshot — <REALISM>, with <ASPECT> vertical framing,
compressed social media video quality, slight motion blur, imperfect framing,
slight overexposure in highlights, uneven indoor lighting, realistic skin
texture, smartphone camera noise, low sharpness, compression artifacts,
accidental composition, lived-in realism, non-professional snapshot, casual
daily life mood, asymmetry, unposed expression, natural body posture.
Not cinematic, not studio photography, not over-retouched.
<UI_OVERLAY>
```

- `<TYPE>` … STEP1。例: "vertical short-video app screen", "TikTok-style clip",
  "casual story post", "BeReal-style dual snapshot", "casual profile photo",
  "low-key product/service promo snapshot"
- TikTok切り抜き風/ストーリー投稿風/ショート動画素材の場合は `<UI_OVERLAY>` に
  「実在ロゴではない汎用のショート動画アプリ風UI(右側の縦並びアイコン、丸いプロフィール、
  下部のキャプション、ハッシュタグ風テキスト、小さな音楽トラックバー)を自然に重ねる。
  ただしロゴや細かい文字は読めない程度に」という指示を英語で入れる。それ以外は空にする。
- 個人が特定できる文字情報(顔のはっきりした有名人、実在の店名ロゴ、ナンバープレート、
  本名・電話番号等)は出さない。

### ネガティブプロンプト（基本は固定。必要なら追記）
```
exact TikTok logo, exact branded app screenshot, watermark, overly detailed
tiny text, broken large text, cinematic lighting, studio photography, perfect
symmetry, ultra detailed skin, glossy CG, AI beauty look, over-retouched skin,
unrealistic anatomy, fashion editorial pose, perfect composition, plastic skin,
dramatic lighting, luxury advertisement, overly smooth skin, professional
portrait, professional model pose, exaggerated beauty filter, overly sharp
image, fantasy-like lighting, sexualized pose, underage appearance, revealing
outfit, cosplay look, luxury restaurant, professional influencer post, perfect
still photo, clean commercial photo, readable private information
```

### 日本語→英語 対応のヒント
- 見た目: 日本人風=Japanese, 韓国人風=Korean, アジア系ミックス風=mixed-Asian,
  海外風=Western/non-Asian, 指定なし=（記述しない）
- 顔の見え方: 顔あり=face visible / 横顔=profile view / 後ろ姿=seen from behind /
  顔の一部だけ=only part of the face visible / スマホで顔を隠す=face partly hidden
  behind a smartphone / 手元だけ=hands only / 顔なし=face not shown /
  遠目=face not clearly visible from a distance
- 時間帯: コンビニの蛍光灯=cold convenience-store fluorescent light /
  居酒屋の暖色照明=warm izakaya indoor lighting / 西日=late afternoon sunlight /
  白飛び気味=slightly overexposed / 曇りの柔らかい光=soft overcast light

## 画像生成（実行）

プロンプトが固まったら、必ずスクリプトを実行して**実際の画像ファイルを生成する**。

```bash
python scripts/generate_image.py \
  --prompt "<組み立てたポジティブプロンプト>" \
  --negative "<ネガティブプロンプト>" \
  --aspect <1:1|9:16|16:9|auto> \
  --out output/realistic-<分かりやすい名前>.png
```

- バックエンドは自動選択。`GEMINI_API_KEY` があれば Gemini、なければ無料・キー不要の
  Pollinations(Flux) を使う。どちらも無料で動く。
- 生成後、出力パスを `SendUserFile`(status: normal) でユーザーに見せる。
- 「もう少し暗く」「別バリエーション」等の要望には、該当部分のプロンプトだけ調整するか
  `--seed` を変えて再生成する。1回で複数案が欲しい場合はシードを変えて複数回呼ぶ。

## 注意（安全・リアルさ）

- 未成年に見える人物・性的・露出の高い表現は作らない（ネガティブにも明記済み）。
- 実在ブランドのロゴや実在の店舗、特定個人になりすます画像は作らない。
- これはあくまで「リアルに見える」加工であり、本物の写真ではないことを前提に扱う。
