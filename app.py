import streamlit as st
import plotly.graph_objects as go
import time
import os
from datetime import datetime
import urllib.parse

# ==========================================
# 1. デザイン設定 (CSS injection)
# ==========================================
def apply_custom_style():
    st.markdown("""
    <style>
    /* 全体設定 */
    .stApp {
        background-color: #FAFAFA !important;
    }
    html, body, [class*="css"] {
        font-family: "Helvetica Neue", Arial, "Hiragino Kaku Gothic ProN", "Hiragino Sans", Meiryo, sans-serif;
        color: #333333 !important;
    }
    .block-container {
        padding-top: 3rem;
        padding-bottom: 5rem;
    }

    /* アニメーション (Pulse) */
    @keyframes pulse {
        0% { transform: scale(1); box-shadow: 0 4px 15px rgba(118, 75, 162, 0.4); }
        50% { transform: scale(1.03); box-shadow: 0 0 25px rgba(118, 75, 162, 0.6); }
        100% { transform: scale(1); box-shadow: 0 4px 15px rgba(118, 75, 162, 0.4); }
    }

    /* --------------------------------------------------
       トップ画面
       -------------------------------------------------- */
    .hero-container { text-align: center; padding: 20px 0; }
    .hero-title {
        font-size: 32px; font-weight: 800; line-height: 1.4;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-bottom: 15px; display: inline-block;
    }
    .hero-subtitle {
        font-size: 16px; line-height: 1.8; color: #666;
        margin-bottom: 40px; max-width: 600px; margin-left: auto; margin-right: auto;
    }
    .feature-box {
        background: white; padding: 20px 10px; border-radius: 15px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05); text-align: center; height: 100%; border: 1px solid #f0f0f0;
    }
    .feature-icon { font-size: 28px; margin-bottom: 10px; display: block; color: #764ba2 !important; }
    .feature-title { font-weight: bold; font-size: 14px; color: #333; margin-bottom: 5px; display: block; }
    .feature-desc { font-size: 11px; color: #888; }

    /* --------------------------------------------------
       ボタン
       -------------------------------------------------- */
    div.stButton > button[kind="primary"], a[kind="primary"] {
        width: 100%; border-radius: 50px !important; border: none !important;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important; font-weight: 800 !important; font-size: 18px !important;
        padding: 1rem 2rem !important; transition: all 0.3s ease !important;
        animation: pulse 2s infinite ease-in-out;
        text-decoration: none !important; display: inline-block; text-align: center;
    }
    div.stButton > button[kind="primary"]:hover, a[kind="primary"]:hover {
        animation: none; transform: scale(1.05); color: white !important;
    }
    
    div.stButton > button[kind="secondary"] {
        width: 100%; border-radius: 30px !important;
        background: #FFFFFF !important; color: #666 !important;
        border: 1px solid #E0E0E0 !important; font-size: 14px !important;
        padding: 0.5rem 1rem !important;
        transition: all 0.2s ease !important;
    }
    div.stButton > button[kind="secondary"]:hover {
        border-color: #764ba2 !important; color: #764ba2 !important; transform: translateY(-2px);
    }

    /* SNS Links */
    a[kind="primary"], a[kind="secondary"] {
        width: 100%; display: inline-block; text-align: center; text-decoration: none;
        padding: 0.6rem 1rem; border-radius: 10px; font-weight: bold; transition: all 0.2s;
        margin-bottom: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    a[href*="twitter.com"] { background-color: #000000 !important; color: #ffffff !important; }
    a[href*="line.me"] { background-color: #06C755 !important; color: #ffffff !important; }
    a[href*="facebook.com"] { background-color: #1877F2 !important; color: #ffffff !important; }
    a:hover { transform: translateY(-2px); opacity: 0.9; }

    /* --------------------------------------------------
       質問カード & 結果画面
       -------------------------------------------------- */
    .question-card {
        background-color: #FFFFFF; padding: 40px 20px; border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.05); text-align: center; margin-bottom: 30px; border: 1px solid #F0F0F0;
    }
    .question-number { color: #764ba2; font-size: 14px; font-weight: bold; letter-spacing: 2px; margin-bottom: 10px; text-transform: uppercase; }
    .question-text { font-size: 20px; font-weight: 700; color: #2D3436; line-height: 1.6; }

    .result-container {
        background: white; padding: 30px; border-radius: 20px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.08); margin-top: 20px; text-align: center;
    }
    .result-title {
        font-size: 28px; font-weight: 800; color: #333; margin-bottom: 10px;
    }
    .result-copy {
        font-size: 18px; color: #444; font-weight: bold; font-style: italic;
        margin: 20px 0; padding: 20px;
        background: #F4F6F9; border-left: 5px solid #764ba2; text-align: left;
        line-height: 1.6;
    }
    
    /* 説明文ボックス */
    .result-desc-box {
        background-color: #ffffff !important;
        padding: 25px;
        border-radius: 15px;
        margin-bottom: 25px;
        border: 1px solid #eeeeee;
        box-shadow: 0 2px 10px rgba(0,0,0,0.03);
    }
    .result-desc {
        font-size: 16px; color: #333333 !important; line-height: 1.8; text-align: left;
    }
    .result-desc h4 {
        color: #764ba2; margin-top: 25px; margin-bottom: 15px; font-size: 18px; border-bottom: 2px solid #f0f0f0; padding-bottom: 10px;
    }

    img { border-radius: 15px; }

    /* グラデーション文字設定 */
    .gradient-text-cool {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        font-weight: 800;
    }
    .gradient-text-warm {
        background: linear-gradient(135deg, #ff9a44 0%, #fc6076 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        font-weight: 800;
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. データ定義 (字下げ厳禁：HTMLタグ対策)
# ==========================================

TYPES = {
    "MFSP": {
        "title": "空白のショールーム", 
        "copy": "埃ひとつ、アイコンひとつ許さない", 
        "desc": """生活感という「ノイズ」を極限まで排除した空間です。机の上にはMacBookだけ、配線は壁の裏へ隠し、床には塵一つ落ちていない。あなたの部屋は、居住空間というより<b>「思考の要塞」</b>であり、Apple Storeのような洗練された静寂が支配しています。<br><br><h4>🧠 深層心理と性格</h4>あなたは自他ともに厳しい完璧主義者です。頭の中は常にクリアで論理的。「コントロールできないもの」を嫌うため、予測不可能な感情論や、非効率な会議には強烈なストレスを感じます。常に最適解を探し続けるストイックな求道者でもあります。<br><br><h4>❤️ 人間関係と恋愛</h4>「一人の時間」が何よりのエネルギー源。パートナーにも自立を求め、ベタベタした依存関係は苦手です。しかし、一度心を許した相手には、不器用ながらも深い信頼を寄せます。言葉よりも行動で愛情を示すタイプです。<br><br><h4>💼 才能と仕事</h4>プログラマー、建築家、外科医など、緻密さと論理性が求められる分野で天才的な能力を発揮します。<br><br><h4>💡 アドバイス</h4>他人にも自分と同じ「完璧」を求めがちで、周囲を息苦しくさせてしまうことがあります。「散らかっていても死なない」と自分に言い聞かせ、時にはあえてカオスを受け入れる「遊び」を持つことで、あなたの人生はより彩り豊かになります。""", 
        "color": "#2c3e50"
    },
    "MFSL": {
        "title": "合理的なノマド", 
        "copy": "生活に必要なのは、スマホとベッドだけ", 
        "desc": """所有することへの執着がゼロ。引っ越したてのような殺風景な部屋ですが、それは<b>「いつでも身軽に動ける」という自由の証</b>です。家具を買う手間すら惜しむ究極の合理主義空間で、寝袋や段ボールテーブルでも平気で暮らせる適応力があります。<br><br><h4>🧠 深層心理と性格</h4>過去や場所に縛られない自由人。物理的なモノよりも、知識や経験にお金を使います。人間関係もサッパリしており、来るもの拒まず去るもの追わず。情熱がないわけではなく、「本当に大切な1%」のために、他の99%を容赦なく切り捨てられる決断力の人です。<br><br><h4>❤️ 人間関係と恋愛</h4>束縛を何よりも嫌います。恋愛でも「お互いの自由」を尊重できる相手でないと長続きしません。記念日などの形式的なイベントには興味がないため、ロマンチックな演出を求められると困惑します。<br><br><h4>💼 才能と仕事</h4>コンサルタント、フリーランス、起業家など、場所を選ばずに結果を出せる仕事が天職です。<br><br><h4>💡 アドバイス</h4>「効率」を優先しすぎて、情緒や風情を無視しがち。殺風景すぎる部屋は、時にあなたの心を乾かせます。一輪の花を飾るような「無駄」を楽しむ余裕を持つと、人間的な魅力に深みが出るでしょう。""", 
        "color": "#7f8c8d"
    },
    "MESP": {
        "title": "孤高の美術館", 
        "copy": "余白を愛するアーティスト", 
        "desc": """ただ物が少ないのではなく、選び抜かれた「美しいもの」だけが置かれた空間です。座り心地の悪いデザイナーズチェアも、あなたにとってはアートであり、我慢してでも置く価値があります。<b>生活の利便性よりも、美意識が最優先される聖域</b>です。<br><br><h4>🧠 深層心理と性格</h4>高い美意識と鋭い感受性の持ち主。周囲からは「センスが良いけど少し近寄りがたい」と思われているかもしれません。妥協してレベルの低いものと付き合うくらいなら、高尚な孤独を選びます。自己表現への欲求が強く、自分自身の生き方そのものを作品だと捉えています。<br><br><h4>❤️ 人間関係と恋愛</h4>理想が高く、相手の見た目やセンスにもこだわりがあります。心を開くまでに時間はかかりますが、感性が共鳴する相手とは言葉を交わさずとも深く通じ合えます。<br><br><h4>💼 才能と仕事</h4>デザイナー、アーティスト、編集者など、美意識を形にする仕事で成功します。<br><br><h4>💡 アドバイス</h4>理想が高すぎて、現実とのギャップに苦しみやすい傾向があります。「完璧な美」だけでなく、「不完全な美（わびさび）」や、人間の泥臭さを愛せるようになると、精神的に楽になれるはずです。""", 
        "color": "#34495e"
    },
    "MESL": {
        "title": "未完のアトリエ", 
        "copy": "美意識はあるが、布団からは出られない", 
        "desc": """コンクリート打ちっ放しや無機質な空間に憧れていますが、服や雑誌が散乱しがち。しかし、その散らかり方すら計算された「ラフさ」に見えるのが不思議な才能です。<b>オシャレなカフェのバックヤードのような、制作途中の芸術作品のような空間</b>です。<br><br><h4>🧠 深層心理と性格</h4>理想は高いのに行動が追いつかない、愛すべき夢想家。クリエイティブな才能がありますが、締め切り直前まで動かないズボラな一面も。ルールに縛られるのを嫌い、直感で動く右脳型人間です。「ま、いっか」で許される愛嬌を持っています。<br><br><h4>❤️ 人間関係と恋愛</h4>感受性が豊かで惚れっぽいタイプ。ドラマチックな展開を好みますが、飽きっぽい一面も。あなたの世話を焼いてくれるしっかり者のパートナーとうまくいきます。<br><br><h4>💼 才能と仕事</h4>企画職、ライター、ファッション関係など、自由な発想が許される環境で輝きます。<br><br><h4>💡 アドバイス</h4>「やる気が出たらやる」と言って、永遠にやらないタイプ。大きな目標よりも、まずは「靴下をカゴに入れる」といった小さな習慣から始めましょう。あなたの感性は素晴らしいので、環境さえ整えば大化けします。""", 
        "color": "#95a5a6"
    },
    "MWSP": {
        "title": "現代の茶室", 
        "copy": "整えられた呼吸、整えられた空間", 
        "desc": """禅（Zen）の精神を体現したような部屋。物は少ないですが、冷たさはなく、木の温もりや畳の香りが漂います。毎朝の掃除や換気がルーティン化されており、<b>空間が常に呼吸しています</b>。静寂と清潔を愛する、精神の修行場のような場所です。<br><br><h4>🧠 深層心理と性格</h4>精神的に成熟しており、感情の起伏が穏やか。周囲からは「一緒にいると落ち着く」と言われ、相談役にされやすいタイプです。しかし、内面には確固たる芯があり、自分の聖域（時間や空間）を土足で踏み荒らされると静かに激怒します。<br><br><h4>❤️ 人間関係と恋愛</h4>穏やかで誠実な関係を望みます。派手なデートよりも、家で静かにお茶を飲むような時間を大切にします。嘘や裏切りを最も嫌います。<br><br><h4>💼 才能と仕事</h4>カウンセラー、教師、職人など、人と向き合ったり一つの道を極める仕事に向いています。<br><br><h4>💡 アドバイス</h4>「正しさ」や「丁寧さ」に囚われすぎて、自分を律しすぎてしまうことがあります。たまにはカップ麺を食べたり、掃除をサボったりする「ダラけ」の日を作って、心のガス抜きをしてください。""", 
        "color": "#d35400"
    },
    "MWSL": {
        "title": "陽だまりのナマケモノ", 
        "copy": "床でゴロゴロするのが最高", 
        "desc": """背の高い家具を置かず、視線を低くしたロースタイル。Yogiboやラグマットの上で、一日中動かずに過ごせます。散らかっているわけではないけれど、どこか「隙」のある、<b>世界で一番居心地の良い空間</b>です。窓からの光を何よりも大切にします。<br><br><h4>🧠 深層心理と性格</h4>「なんとかなるさ」が口癖の平和主義者。野心はあまりなく、日々の小さな幸せ（美味しいコーヒーや昼寝）を何よりも大切にする、幸福度の高い人です。競争社会には向いていませんが、癒やしの才能はずば抜けています。<br><br><h4>❤️ 人間関係と恋愛</h4>癒やし系でモテますが、自分からガツガツ行くことはありません。パートナーには、一緒にダラダラできる「居心地の良さ」を最優先で求めます。<br><br><h4>💼 才能と仕事</h4>福祉関係、セラピスト、あるいはのんびりとしたカフェの店員など、競争のない環境で輝きます。<br><br><h4>💡 アドバイス</h4>現状維持バイアスが強く、新しい挑戦を避ける傾向があります。居心地の良い部屋に引きこもりすぎず、たまには外の世界の刺激を取り入れることで、あなたの感性はさらに磨かれます。""", 
        "color": "#f39c12"
    },
    "MWFP": {
        "title": "無印良品のカタログ", 
        "copy": "収納ケースのサイズが揃わないと発狂する", 
        "desc": """ラベリング魔。すべての物に「住所」が決まっていないと気が済みません。機能美とナチュラルさが融合しており、Instagramにそのまま投稿できるレベルで整っています。<b>「整っていること」が精神安定剤</b>になっているタイプです。<br><br><h4>🧠 深層心理と性格</h4>真面目で責任感が強い優等生タイプ（ISTJに近い）。旅行の計画などは分単位で立てるのが得意で、組織の管理者に向いています。混沌を嫌い、ルールやマニュアルを作ることで安心感を得ます。<br><br><h4>❤️ 人間関係と恋愛</h4>約束や時間は絶対に守る誠実な人。パートナーにも同じ誠実さを求めますが、ルーズな相手を放っておけずに世話を焼いてしまう一面も。<br><br><h4>💼 才能と仕事</h4>事務、経理、公務員、プロジェクトマネージャーなど、管理能力が活きる仕事が天職です。<br><br><h4>💡 アドバイス</h4>予定外のトラブルに弱く、想定外のことが起きるとパニックになりがち。人生は整理整頓できないことだらけです。「まあいいか」という魔法の言葉を覚え、曖昧さを許容する訓練をしましょう。""", 
        "color": "#e67e22"
    },
    "MWFL": {
        "title": "サステナブルな実家感", 
        "copy": "古き良き温もりと、少しの生活感", 
        "desc": """流行りの家具よりも、長く使っている愛用品を大切にする部屋。少し散らかっていても、それが生活の「味」になっています。友人が遊びに来た時、<b>「なんか落ち着くわ〜」と言って一番長居してしまう</b>のは、間違いなくこのタイプの部屋です。<br><br><h4>🧠 深層心理と性格</h4>情に厚く、人との縁を大切にします。過去の思い出や人間関係をなかなか捨てられないウェットな性格。新しいものに飛びつくよりも、馴染みの店や古い友人を大切にする、義理人情の人です。<br><br><h4>❤️ 人間関係と恋愛</h4>一途で家庭的なタイプ。付き合いが長く、結婚向きです。相手のダメなところも含めて受け入れる包容力があります。<br><br><h4>💼 才能と仕事</h4>教育、保育、人事、接客業など、人と深く関わりサポートする仕事に向いています。<br><br><h4>💡 アドバイス</h4>過去への執着が強く、部屋が思い出の品で溢れかえり、「捨てられない屋敷」になる予備軍です。思い出は心の中にあります。過去の遺産ではなく、未来の自分のためのスペースを空ける勇気を持って。""", 
        "color": "#d35400"
    },
    "CFSP": {
        "title": "司令官のコックピット", 
        "copy": "全ての操作を、椅子から動かずに", 
        "desc": """マルチモニター、エルゴノミクスチェア、そしてLEDテープライト。デスク周りの構築美に命をかけています。<b>一歩も動かずに全ての作業が完結する</b>、効率とロマンの結晶のようなサイバー空間です。配線の美しさは芸術の域です。<br><br><h4>🧠 深層心理と性格</h4>論理的思考が得意な理系脳。ガジェットのスペック比較や、作業の自動化が大好き。感情論よりもデータや事実を重視するため、少し冷たいと思われがちですが、内には少年のように熱い探究心を秘めています。<br><br><h4>❤️ 人間関係と恋愛</h4>ベタベタした関係よりも、お互いにリスペクトし合える対等な関係を望みます。趣味やゲームを一緒に楽しめる相手なら最高です。<br><br><h4>💼 才能と仕事</h4>エンジニア、データサイエンティスト、金融トレーダーなど、分析力が活きる仕事で活躍します。<br><br><h4>💡 アドバイス</h4>機能性を追い求めるあまり、部屋から「情緒」や「季節感」が失われがち。たまにはデジタルデバイスをすべて切り、アナログな自然に触れる時間を作らないと、脳がショートしてしまうかもしれません。""", 
        "color": "#2980b9"
    },
    "CFSL": {
        "title": "マッドサイエンティストのラボ", 
        "copy": "配線の森に迷い込む", 
        "desc": """機能重視で機材を増やし続けた結果、カオスと化した部屋。足の踏み場はありませんが、本人は<b>「どこに何があるか」を全て把握している「秩序ある混沌」</b>です。未開封の段ボールと絡まったケーブルの山は、進化の過程にすぎません。<br><br><h4>🧠 深層心理と性格</h4>一点集中の天才肌。興味があることには寝食を忘れて没頭しますが、興味がないこと（片付け、手続き、社交）は徹底的に後回しにする極端な性格です。常識に囚われないイノベーターの資質があります。<br><br><h4>❤️ 人間関係と恋愛</h4>自分の世界を理解してくれる相手でないと続きません。「変人」と言われることを褒め言葉だと思っています。知的な会話ができる相手を求めます。<br><br><h4>💼 才能と仕事</h4>研究職、発明家、プログラマーなど、専門性を極める仕事が向いています。<br><br><h4>💡 アドバイス</h4>生活環境の悪化が健康に直結するタイプです。換気不足やホコリに注意。「ルンバが走れる床面積」だけは確保するように心がけると、運気が好転するでしょう。""", 
        "color": "#3498db"
    },
    "CESP": {
        "title": "ストリート・セレクトショップ", 
        "copy": "スニーカーは履くものではなく飾るもの", 
        "desc": """収集癖がありますが、ただ集めるのではなく<b>「見せる（Display）」</b>ことに命をかけています。スニーカー、フィギュア、レコードなどが、ショップのように美しく陳列された原宿スタイルの部屋。ガラスケースはあなたの聖櫃です。<br><br><h4>🧠 深層心理と性格</h4>自己プロデュース能力が高い自信家。トレンドに敏感で、人からどう見られるかを常に意識しています。SNSのフォロワー数や「いいね」の数がモチベーションになりやすいタイプ。承認欲求を健全なエネルギーに変えられる人です。<br><br><h4>❤️ 人間関係と恋愛</h4>華やかで社交的。美男美女カップルに憧れる傾向があります。お互いのファッションや趣味を高め合える、刺激的な関係を望みます。<br><br><h4>💼 才能と仕事</h4>ファッション業界、広報、インフルエンサー、営業職など、人を惹きつける仕事で成功します。<br><br><h4>💡 アドバイス</h4>「見栄」のために散財しがち。本当に自分が好きなものよりも、「自慢できるもの」を買っていませんか？ 他人の評価軸ではなく、自分の魂が震えるものだけを選ぶようになると、本物のカリスマになれます。""", 
        "color": "#8e44ad"
    },
    "CESL": {
        "title": "ネオン・ドンキホーテ", 
        "copy": "カワイイとカオスは紙一重", 
        "desc": """推しグッズ、ぬいぐるみ、極彩色のポスター。色彩の暴力のような空間ですが、そこにはあなたの<b>「好き」が120%詰まっています</b>。天井から何かがぶら下がっている、ヴィレッジヴァンガード的空間。ここはあなたのエネルギーチャージ基地です。<br><br><h4>🧠 深層心理と性格</h4>エネルギーに溢れた行動派。好奇心旺盛で、欲しいものは我慢できません（ドーパミン中毒気味）。金遣いは荒いですが、人生を全力で楽しんでいるため、不思議と憎めない愛されキャラです。退屈が一番の敵。<br><br><h4>❤️ 人間関係と恋愛</h4>情熱的で押しが強いタイプ。好きになったら一直線です。一緒にライブに行ったりイベントを楽しめる、ノリの良いパートナーとうまくいきます。<br><br><h4>💼 才能と仕事</h4>イベント企画、エンタメ業界、販売員など、変化と刺激のある仕事が向いています。<br><br><h4>💡 アドバイス</h4>刺激がないと死んでしまうマグロのような人。部屋の情報量が多すぎて、脳が休まっていない可能性があります。寝室だけは物を減らして真っ暗にするなど、オンオフの切り替えを作ることが長く走り続ける鍵です。""", 
        "color": "#9b59b6"
    },
    "CWSP": {
        "title": "英国紳士の書斎", 
        "copy": "知と歴史を整然と並べる", 
        "desc": """壁一面の本棚、アンティークの照明、革張りのソファ。重厚感のある空間です。物は多いですが、すべてが知的探究心に基づいて分類・整理されており、<b>図書館のような静けさと知性</b>が漂います。歴史あるものへの敬意に満ちた部屋です。<br><br><h4>🧠 深層心理と性格</h4>博識で落ち着いたインテリタイプ。流行には流されず、自分の価値観をしっかり持っています。やや頑固で、自分のルールを曲げることを嫌う保守的な一面も。一人の時間を愛し、内省することで成長します。<br><br><h4>❤️ 人間関係と恋愛</h4>知的で落ち着いた会話を好みます。チャラチャラした関係は苦手。尊敬できる相手と、時間をかけて信頼関係を築いていく大人の恋愛をします。<br><br><h4>💼 才能と仕事</h4>研究者、大学教授、作家、弁護士など、知識と論理を武器にする仕事が適任です。<br><br><h4>💡 アドバイス</h4>知識や理屈が先行して、頭でっかちになりがち。時には本を閉じて、街に出て、理屈では説明できない「生身の体験」を味わってください。知識が経験に変わった時、あなたの深みは増します。""", 
        "color": "#5d4037"
    },
    "CWSL": {
        "title": "ジブリの魔女の隠れ家", 
        "copy": "植物と古道具に埋もれて暮らす", 
        "desc": """吊るされたドライフラワー、拾ってきた流木、用途不明の瓶。雑然としていますが、<b>物語の中に迷い込んだような魔法の空間</b>です。プラスチック製品を嫌い、経年変化した「味のあるもの」に囲まれています。植物と会話ができるタイプです。<br><br><h4>🧠 深層心理と性格</h4>直感やインスピレーションを大切にする感覚派（INFPに近い）。スピリチュアルなことや、目に見えない世界を大切にします。社会のルールや効率性よりも、自分の内なる声や心地よさを優先して生きる自由人です。<br><br><h4>❤️ 人間関係と恋愛</h4>ロマンチストで、運命的な出会いを信じています。相手の条件よりも「波長が合うか」が全て。傷つきやすい繊細な心を持っています。<br><br><h4>💼 才能と仕事</h4>クリエイター、占い師、花屋、カウンセラーなど、感性を活かして人を癒やす仕事に向いています。<br><br><h4>💡 アドバイス</h4>現実逃避しやすく、社会生活に疲れを感じやすいかも。この部屋はあなたのシェルターですが、引きこもりすぎると社会との接点を失います。あなたの優しい世界観を、創作活動などで外に発信してみましょう。""", 
        "color": "#4e342e"
    },
    "CWFP": {
        "title": "プロの厨房", 
        "copy": "道具への愛が、料理の味を変える", 
        "desc": """リビングよりもキッチンやダイニングが主役。スパイスの瓶が整列し、こだわりの調理器具が美しく吊るされています。<b>「生活＝作ること」</b>である、料理研究家のようなスタジオ空間です。道具への投資は惜しみません。<br><br><h4>🧠 深層心理と性格</h4>人に何かをしてあげるのが好きなギバー（与える人）。完璧主義でこだわりが強く、道具や手順にはうるさい職人気質ですが、最終的には自分が作ったもので周りの人が笑顔になることに、無上の喜びを感じます。<br><br><h4>❤️ 人間関係と恋愛</h4>世話好きで、パートナーの胃袋を掴むのが得意。しかし、自分のこだわりを相手にも押し付けてしまうと喧嘩の原因に。感謝の言葉を求めすぎる傾向があります。<br><br><h4>💼 才能と仕事</h4>飲食関係、シェフ、パティシエ、あるいはチームを育成するマネージャー職に向いています。<br><br><h4>💡 アドバイス</h4>「尽くしすぎ」に注意。他人の世話を焼くことに夢中で、自分のケアがおろそかになっていませんか？ 最高のパフォーマンスを発揮するためには、まずシェフ（あなた自身）が満たされている必要があります。""", 
        "color": "#6d4c41"
    },
    "CWFL": {
        "title": "昭和レトロな下宿", 
        "copy": "コタツの上には常にミカン", 
        "desc": """捨てられない性格。「いつか使うかも」で溢れていますが、それが強烈な安心感を生んでいます。冬はコタツから出られない、<b>実家のような強力な引力を持った部屋</b>です。色も柄もバラバラなのに、なぜか落ち着く不思議な空間。<br><br><h4>🧠 深層心理と性格</h4>変化を嫌い、安定を好む保守的なタイプ。過去の思い出を大切にしすぎて、新しい一歩を踏み出すのが苦手かも。でも、あなたがそこにいるだけで周りはホッとする、天然のヒーラー（癒やし手）です。<br><br><h4>❤️ 人間関係と恋愛</h4>駆け引きは苦手で、安心感を求めます。ドキドキするような恋よりも、一緒にテレビを見て笑い合えるような、家族のような関係を築きます。<br><br><h4>💼 才能と仕事</h4>地方公務員、総務、介護職、農業など、地域や組織に根ざしてコツコツ働く仕事が向いています。<br><br><h4>💡 アドバイス</h4>変化を恐れすぎて、チャンスを逃している可能性があります。部屋の空気が淀まないように、毎日窓を開けて風を通すように、人生にも「新しい風（新しい趣味や出会い）」を意識的に取り入れてみてください。""", 
        "color": "#795548"
    },
}

# 全35問
QUESTIONS = [
    {"id": 1, "text": "新しいものを買うときの基準は？", "axis": "I", "options": {"A": "何かを捨てないと買わない", "B": "気に入ったら即買い"}},
    {"id": 2, "text": "旅先でのお土産は？", "axis": "I", "options": {"A": "消えもの（お菓子など）のみ", "B": "記念になる雑貨・置物を買う"}},
    {"id": 3, "text": "理想の棚の状態は？", "axis": "I", "options": {"A": "7割は空いている「余白」", "B": "好きな物で「ぎっしり」"}},
    {"id": 4, "text": "「初回限定版」などの言葉に...", "axis": "I", "options": {"A": "興味がない", "B": "弱い・つい買ってしまう"}},
    {"id": 5, "text": "1年以上使っていないモノは？", "axis": "I", "options": {"A": "迷わず捨てる", "B": "いつか使うかもと取っておく"}},
    {"id": 6, "text": "日用品のストックは？", "axis": "I", "options": {"A": "無くなりそうになったら買う", "B": "安売りで大量に買い込む"}},
    {"id": 7, "text": "壁の装飾（ポスター等）は？", "axis": "I", "options": {"A": "あまり掛けない・シンプルに", "B": "好きなもので埋め尽くしたい"}},
    {"id": 8, "text": "収納家具についてどう思う？", "axis": "I", "options": {"A": "収納家具自体を減らしたい", "B": "収納を増やして整理したい"}},
    {"id": 9, "text": "作業後の机の上は？", "axis": "I", "options": {"A": "何もない状態にする", "B": "お気に入りの小物は残す"}},
    {"id": 10, "text": "椅子の選び方は？", "axis": "II", "options": {"A": "長時間座れる機能性重視", "B": "部屋に合うデザイン重視"}},
    {"id": 11, "text": "部屋の照明の好みは？", "axis": "II", "options": {"A": "全体が見える明るい白", "B": "影を楽しむ薄暗い暖色"}},
    {"id": 12, "text": "家電を選ぶ基準は？", "axis": "II", "options": {"A": "最新スペック・効率", "B": "見た目の可愛さ・愛着"}},
    {"id": 13, "text": "用途のわからない置物は？", "axis": "II", "options": {"A": "掃除の邪魔だから不要", "B": "見て幸せなら必要不可欠"}},
    {"id": 14, "text": "部屋の香りについて", "axis": "II", "options": {"A": "無臭・消臭を徹底", "B": "お香やアロマを楽しみたい"}},
    {"id": 15, "text": "家具の配置で優先するのは？", "axis": "II", "options": {"A": "動線の良さ・効率", "B": "部屋に入った時の見栄え"}},
    {"id": 16, "text": "ゴミ箱はどこに置く？", "axis": "II", "options": {"A": "手が届く便利な場所", "B": "見えないように隠す"}},
    {"id": 17, "text": "時計を置くなら？", "axis": "II", "options": {"A": "正確なデジタル時計", "B": "雰囲気のあるアナログ時計"}},
    {"id": 18, "text": "配線コードの扱いは？", "axis": "II", "options": {"A": "使いやすければ見えててOK", "B": "徹底的に隠したい"}}, 
    {"id": 19, "text": "惹かれる素材感は？", "axis": "III", "options": {"A": "ガラス・金属・モノトーン", "B": "木材・布・アースカラー"}},
    {"id": 20, "text": "落ち着くカフェは？", "axis": "III", "options": {"A": "無機質なコーヒースタンド", "B": "木の温もりのある古民家風"}},
    {"id": 21, "text": "好きな色のトーンは？", "axis": "III", "options": {"A": "白・黒・グレー・寒色", "B": "ベージュ・茶・緑・暖色"}},
    {"id": 22, "text": "植物(グリーン)について", "axis": "III", "options": {"A": "虫が嫌なので置かない", "B": "ジャングルのようにしたい"}},
    {"id": 23, "text": "カーテンの好みは？", "axis": "III", "options": {"A": "ブラインドで直線的に", "B": "布のドレープで柔らかく"}},
    {"id": 24, "text": "好きな柄は？", "axis": "III", "options": {"A": "無地・ストライプ・幾何学", "B": "花柄・チェック・手書き風"}},
    {"id": 25, "text": "PC周辺機器のデザインは？", "axis": "III", "options": {"A": "メカメカしいのが好き", "B": "機械っぽさを隠したい"}},
    {"id": 26, "text": "ラグ・カーペットは？", "axis": "III", "options": {"A": "敷かない・毛足が短い", "B": "ふわふわの手触りがいい"}},
    {"id": 27, "text": "理想の休日の過ごし方は？", "axis": "III", "options": {"A": "都心のホテルラウンジ", "B": "森の中のコテージ・キャンプ"}},
    {"id": 28, "text": "帰宅後のカバンや上着は？", "axis": "IV", "options": {"A": "必ず定位置に戻す", "B": "ソファや床に置きがち"}},
    {"id": 29, "text": "リモコンの場所は？", "axis": "IV", "options": {"A": "位置がミリ単位で決まってる", "B": "「あれ？」と探すことがある"}},
    {"id": 30, "text": "来客時の対応は？", "axis": "IV", "options": {"A": "常に綺麗だから掃除不要", "B": "直前に慌てて片付ける"}},
    {"id": 31, "text": "本や雑誌の並べ方は？", "axis": "IV", "options": {"A": "高さやサイズ順に揃える", "B": "積み上がっていても平気"}},
    {"id": 32, "text": "引き出しの中身は？", "axis": "IV", "options": {"A": "仕切りを使って完璧に", "B": "とりあえず入ればOK"}},
    {"id": 33, "text": "掃除の頻度は？", "axis": "IV", "options": {"A": "毎日少しずつ/ロボット掃除機", "B": "休日にまとめてやる"}},
    {"id": 34, "text": "朝起きたらベッドは？", "axis": "IV", "options": {"A": "必ず綺麗に整える", "B": "夜寝るからそのままでいい"}},
    {"id": 35, "text": "床に髪の毛が落ちていたら？", "axis": "IV", "options": {"A": "すぐ拾わないと気が済まない", "B": "あまり気にならない"}},
]

# ==========================================
# 3. ロジック関数
# ==========================================

def calculate_result(answers):
    scores = {"I": 0, "II": 0, "III": 0, "IV": 0}
    for q_id, choice in answers.items():
        question = next((q for q in QUESTIONS if q["id"] == q_id), None)
        if question:
            if choice == "A": scores[question["axis"]] += 1
            else: scores[question["axis"]] -= 1
    
    c1 = "M" if scores["I"] >= 0 else "C"
    c2 = "S" if scores["III"] >= 0 else "W"
    c3 = "F" if scores["II"] >= 0 else "E"
    c4 = "P" if scores["IV"] >= 0 else "L"
    
    final_key = c1 + c3 + c2 + c4
    if final_key not in TYPES:
        alt_key = c1 + c2 + c3 + c4 
        final_key = alt_key if alt_key in TYPES else "MFSP"
            
    return final_key, scores

def create_radar_chart(scores, color_hex):
    val_i = 5 + (scores["I"] * 0.5)
    val_ii = 5 + (scores["II"] * 0.5)
    val_iii = 5 + (scores["III"] * 0.5)
    val_iv = 5 + (scores["IV"] * 0.5)
    
    categories = ['物量(Mini)', '機能(Func)', 'モダン(Sharp)', '幾帳面(Perf)']
    values = [val_i, val_ii, val_iii, val_iv]
    categories.append(categories[0])
    values.append(values[0])

    fig = go.Figure(data=go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        fillcolor=f'rgba{tuple(int(color_hex.lstrip("#")[i:i+2], 16) for i in (0, 2, 4)) + (0.2,)}',
        line_color=color_hex,
        marker=dict(size=6)
    ))

    fig.update_layout(
        font=dict(family="Helvetica Neue", size=14, color="#333333"),
        polar=dict(
            bgcolor='white',
            radialaxis=dict(
                visible=True, range=[0, 10], 
                linecolor='#999', gridcolor='#eee', 
                showticklabels=False
            ),
            angularaxis=dict(
                linecolor='#999', gridcolor='#eee',
                tickfont=dict(size=14, color='#333333', weight='bold') # 軸文字を濃く・大きく
            )
        ),
        showlegend=False,
        margin=dict(t=40, b=40, l=40, r=40),
        height=300,
        paper_bgcolor='rgba(0,0,0,0)',
    )
    return fig

# ==========================================
# 4. アプリケーション本体
# ==========================================

def main():
    st.set_page_config(page_title="Room Type Diagnosis", page_icon="🏠", layout="centered")
    apply_custom_style()
    
    if 'page' not in st.session_state: st.session_state.page = 'home'
    if 'answers' not in st.session_state: st.session_state.answers = {}
    if 'current_q_index' not in st.session_state: st.session_state.current_q_index = 0
    if 'history' not in st.session_state: st.session_state.history = []

    # 1. ホーム画面
    if st.session_state.page == 'home':
        st.markdown("""
        <div class='hero-container'>
            <div class='hero-title'>
                あなたの「居場所」の正体、暴きます。
            </div>
            <div class='hero-subtitle'>
                部屋は心を映す鏡です。<br>
                たった3分の質問に答えるだけで、<br>
                あなたの隠された<b>「部屋の種族」</b>を判定します。
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # ボタンエリア
        if st.button("📜 過去の履歴を見る", type="secondary", use_container_width=True):
            st.session_state.page = 'history'
            st.rerun()

        st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)

        if st.button("診断をスタートする →", type="primary", use_container_width=True):
            st.session_state.page = 'quiz'
            st.session_state.current_q_index = 0
            st.session_state.answers = {}
            st.rerun()

        st.markdown("""
        <div style='margin-top: 15px; text-align: center; color: #888; font-size: 12px; margin-bottom: 40px;'>
            ✨ 登録不要 / 無料で診断できます
        </div>
        """, unsafe_allow_html=True)

        # 3つの特徴
        f1, f2, f3 = st.columns(3)
        with f1:
            st.markdown("""
            <div class='feature-box'>
                <span class='feature-icon'>⏱</span>
                <span class='feature-title'>所要時間は3分</span>
                <span class='feature-desc'>直感的に答えるだけ。<br>サクサク進みます。</span>
            </div>
            """, unsafe_allow_html=True)
        with f2:
            st.markdown("""
            <div class='feature-box'>
                <span class='feature-icon'>🧠</span>
                <span class='feature-title'>独自の分析ロジック</span>
                <span class='feature-desc'>4つの軸から、あなたの<br>生活スタイルを解析。</span>
            </div>
            """, unsafe_allow_html=True)
        with f3:
            st.markdown("""
            <div class='feature-box'>
                <span class='feature-icon'>🏠</span>
                <span class='feature-title'>全16タイプ</span>
                <span class='feature-desc'>ミニマリストから<br>コレクターまで網羅。</span>
            </div>
            """, unsafe_allow_html=True)

    # 2. 診断画面
    elif st.session_state.page == 'quiz':
        progress = (st.session_state.current_q_index + 1) / len(QUESTIONS)
        st.progress(progress)
        
        q_data = QUESTIONS[st.session_state.current_q_index]
        
        st.markdown(f"""
        <div class='question-card'>
            <div class='question-number'>QUESTION {st.session_state.current_q_index + 1} / {len(QUESTIONS)}</div>
            <div class='question-text'>{q_data['text']}</div>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button(f"{q_data['options']['A']}", type="secondary", use_container_width=True, key=f"q{q_data['id']}_a"):
                st.session_state.answers[q_data['id']] = "A"
                next_question()
        with col2:
            if st.button(f"{q_data['options']['B']}", type="secondary", use_container_width=True, key=f"q{q_data['id']}_b"):
                st.session_state.answers[q_data['id']] = "B"
                next_question()
        
        st.markdown("<div style='margin-top: 30px; text-align: center;'>", unsafe_allow_html=True)
        if st.session_state.current_q_index > 0:
            if st.button("戻る", use_container_width=False):
                st.session_state.current_q_index -= 1
                st.rerun()

    # 3. 結果画面
    elif st.session_state.page == 'result':
        type_key, scores = calculate_result(st.session_state.answers)
        result_data = TYPES[type_key]
        
        if not any(d['date'] == st.session_state.get('last_run') for d in st.session_state.history):
             run_time = datetime.now().strftime("%Y/%m/%d %H:%M")
             st.session_state.history.insert(0, {"date": run_time, "type": type_key, "title": result_data['title']})
             st.session_state.last_run = run_time

        st.markdown(f"""
        <div class='result-container'>
            <p style='color: #888; font-size: 14px; margin-bottom: 5px;'>DIAGNOSIS RESULT</p>
            <h2 class='result-title' style='color: {result_data['color']};'>{type_key}：{result_data['title']}</h2>
        </div>
        """, unsafe_allow_html=True)
        
        image_path = f"assets/{type_key}.png"
        if os.path.exists(image_path):
            st.image(image_path, use_container_width=True)
        else:
            st.warning(f"画像が見つかりません: {image_path}")
            st.image(f"https://placehold.co/800x500/{result_data['color'].replace('#','')}/FFFFFF?text={result_data['title']}", use_container_width=True)
        
        # ★ここが修正ポイント：黒いボックスの原因となるインデントを完全に削除
        st.markdown(f"""
<div class='result-copy'>
{result_data['copy']}
</div>
<div class='result-desc-box'>
<div class='result-desc'>
{result_data['desc']}
</div>
</div>
""", unsafe_allow_html=True)
        
        # ★グラデーション文字を適用
        st.markdown('### <span class="gradient-text-cool">📊 部屋の成分表</span>', unsafe_allow_html=True)
        chart = create_radar_chart(scores, result_data['color'])
        st.plotly_chart(chart, use_container_width=True)
        
        # SNSシェアセクション
        share_text = f"私の部屋タイプは【{result_data['title']}】でした！\n部屋の正体を暴く診断アプリ #部屋タイプ診断"
        share_url = "https://room-diagnosis.streamlit.app"
        encoded_text = urllib.parse.quote(share_text)
        encoded_url = urllib.parse.quote(share_url)
        
        twitter_url = f"https://twitter.com/intent/tweet?text={encoded_text}&url={encoded_url}"
        line_url = f"https://line.me/R/msg/text/?{encoded_text}%20{encoded_url}"
        facebook_url = f"https://www.facebook.com/sharer/sharer.php?u={encoded_url}"
        
        # ★グラデーション文字を適用
        st.markdown('### <span class="gradient-text-warm">🤝 診断結果をシェア</span>', unsafe_allow_html=True)
        s1, s2, s3 = st.columns(3)
        with s1:
            st.link_button("X (Twitter)", twitter_url, use_container_width=True)
        with s2:
            st.link_button("LINE", line_url, use_container_width=True)
        with s3:
            st.link_button("Facebook", facebook_url, use_container_width=True)
            
        st.caption("▼ リンクをコピーしてシェア")
        st.code(share_url, language="text") 
        
        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col2:
            if st.button("🏠 トップへ戻る", type="secondary", use_container_width=True):
                st.session_state.page = 'home'
                st.rerun()

    # 4. 履歴画面
    elif st.session_state.page == 'history':
        st.markdown("<h2 style='text-align: center; color: #333;'>HISTORY</h2>", unsafe_allow_html=True)
        if not st.session_state.history:
            st.info("まだ履歴がありません")
        else:
            for item in st.session_state.history:
                st.markdown(f"""
                <div style='background: white; padding: 15px; border-radius: 10px; margin-bottom: 10px; border-left: 5px solid #ddd; box-shadow: 0 2px 5px rgba(0,0,0,0.05);'>
                    <small style='color: #999'>{item['date']}</small><br>
                    <b style='font-size: 18px; color: #333'>{item['title']}</b>
                    <span style='float: right; color: #aaa'>#{item['type']}</span>
                </div>
                """, unsafe_allow_html=True)
        
        if st.button("戻る", type="secondary", use_container_width=True):
            st.session_state.page = 'home'
            st.rerun()

def next_question():
    if st.session_state.current_q_index < len(QUESTIONS) - 1:
        st.session_state.current_q_index += 1
        st.rerun()
    else:
        with st.spinner('Analying...'):
            time.sleep(1.0) 
        st.session_state.page = 'result'
        st.rerun()

if __name__ == "__main__":
    main()
