# streamlit_prompt_app.py
import streamlit as st
import openai
import os

# OpenAI APIキーを設定（セキュアな場所で管理してください）
openai.api_key = os.getenv("OPENAI_API_KEY") or "YOUR_API_KEY_HERE"

st.set_page_config(page_title="AIと話そう！", page_icon="🤖")
st.title("🤖 プロンプトでAIと話そう！")
st.write("プロンプト（AIへのお願いの言葉）を工夫して、どんな返事が返ってくるか試してみよう！")

# プロンプト入力欄
user_prompt = st.text_area("📝 プロンプトを入力してね：", height=100)

# お題ボタン（例題をすぐ使える）
if st.button("🎲 お題をもらう"):
    import random
    examples = [
        "宇宙人になりきって自己紹介して",
        "10歳の子でも安心して聞ける怖い話をして",
        "関西弁でラーメンを紹介して",
        "戦国武将がスマホを初めて使う話を書いて",
        "やる気が出るように応援して",
        "天気予報をテンション高くやって"
    ]
    user_prompt = random.choice(examples)
    st.session_state["user_prompt"] = user_prompt
    
client = openai.OpenAI()

# 入力があればAIに送信
if st.button("🚀 AIに送信") and user_prompt.strip():
    with st.spinner("AIが考え中..."):
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "あなたは親しみやすく面白いアシスタントです。"},
                    {"role": "user", "content": user_prompt}
                ]
            )
            
            ai_reply = response.choices[0].message.content
            st.success("✅ AIの返答はこちら！")
            st.write(ai_reply)
        except Exception as e:
            st.error(f"エラーが発生しました: {e}")

# フッター
st.markdown("---")
st.caption("Developed for educational use ✨")
