# streamlit_prompt_app.py
import streamlit as st
import openai
import os
import random

# OpenAI APIキー設定（環境変数 or 手動入力）
openai.api_key = os.getenv("OPENAI_API_KEY") or "YOUR_API_KEY_HERE"
client = openai.OpenAI()

st.set_page_config(page_title="プロンプト職人選手権", page_icon="🏆")
st.title("🏆 プロンプト職人選手権")
st.write("プロンプトを工夫して、AIから高評価な返答を引き出そう！")

# セッションステートの初期化
if "user_prompt" not in st.session_state:
    st.session_state["user_prompt"] = ""

# 🎲 お題ガチャ
if st.button("🎲 お題をもらう"):
    examples = [
        "宇宙人になりきって自己紹介して",
        "10歳の子でも安心して聞ける怖い話をして",
        "関西弁でラーメンを紹介して",
        "戦国武将がスマホを初めて使う話を書いて",
        "やる気が出るように応援して",
        "天気予報をテンション高くやって"
    ]
    st.session_state["user_prompt"] = random.choice(examples)

# プロンプト入力欄
user_prompt = st.text_area("📝 AIへのお願い（プロンプト）を入力してみよう：", height=100, key="user_prompt")

# 🚀 実行ボタン
if st.button("🚀 AIに送信して評価を受けよう") and user_prompt.strip():
    with st.spinner("AIが考え中..."):
        try:
            # AI返答生成
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "あなたは親しみやすく面白いアシスタントです。"},
                    {"role": "user", "content": user_prompt}
                ]
            )
            ai_reply = response.choices[0].message.content

            # AIによる自己評価
            eval_prompt = f"""
以下のAIの返答について、次の3つの観点で10点満点で採点し、コメントも添えてください。

【評価観点】
1. 創造性（どれだけユニークで想像力に富んでいるか）
2. 面白さ（どれだけ笑いや興味を引くか）
3. わかりやすさ（伝わりやすさ、表現の工夫）

【返答】
{ai_reply}
"""
            eval_response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "あなたは優秀な教育者として、公平に評価してください。"},
                    {"role": "user", "content": eval_prompt}
                ]
            )
            ai_eval = eval_response.choices[0].message.content

            # 結果表示
            st.success("🎉 AIの返答")
            st.write(ai_reply)

            st.info("📊 AIによる自己採点")
            st.markdown(ai_eval)

        except Exception as e:
            st.error(f"エラーが発生しました: {e}")

# フッター
st.markdown("---")
st.caption("Powered by GPT-4o / Streamlit ✨ 教育目的で使用中")
