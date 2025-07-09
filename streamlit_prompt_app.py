import streamlit as st
import openai
import os

# OpenAI APIキー設定（環境変数 or 手動入力）
openai.api_key = os.getenv("OPENAI_API_KEY") or "YOUR_API_KEY_HERE"
client = openai.OpenAI()

# アクセス許可フラグ（Trueの場合、誰でもアクセス可能）
allow_access = True  # ここを変更してアクセス制御

if not allow_access:
    st.warning("アクセスが許可されていません。")
    st.stop()

st.set_page_config(page_title="プロンプト職人選手権", page_icon="🏆")
st.title("🏆 プロンプト職人選手権")
st.write("プロンプトを工夫して、AIから高評価な返答を引き出そう！")

# セッションステートの初期化
if "user_prompt" not in st.session_state:
    st.session_state["user_prompt"] = ""

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

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

# チャット履歴の表示
if st.session_state["chat_history"]:
    for chat in st.session_state["chat_history"]:
        st.markdown(f"**ユーザー**: {chat['user']}")
        st.markdown(f"**エージェント**: {chat['agent']}")

# 🚀 実行ボタン
if st.button("🚀 チャット送信") and user_prompt.strip():
    with st.spinner("AIが考え中..."):
        try:
            # ユーザーとエージェントのチャット履歴を保持
            st.session_state["chat_history"].append({"user": user_prompt, "agent": ""})

            # AI返答生成
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "system", "content": "あなたは親しみやすく面白いアシスタントです。"}] + [
                    {"role": "user", "content": chat["user"]} for chat in st.session_state["chat_history"]
                ] + [{"role": "user", "content": user_prompt}]
            )
            ai_reply = response.choices[0].message.content

            # エージェントの返答を更新
            st.session_state["chat_history"][-1]["agent"] = ai_reply

            # 結果表示
            st.success("🎉 AIの返答")
            st.write(ai_reply)

        except Exception as e:
            st.error(f"エラーが発生しました: {e}")

# フッター
st.markdown("---")
st.caption("Powered by GPT-4o / Streamlit ✨ 教育目的で使用中")
