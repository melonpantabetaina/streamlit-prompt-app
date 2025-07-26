import streamlit as st
import openai
import os

# OpenAI APIキー設定（環境変数 or 手動入力）
openai.api_key = os.getenv("OPENAI_API_KEY") or "YOUR_API_KEY_HERE"
client = openai.OpenAI()

# アクセス許可フラグ（Trueの場合、誰でもアクセス可能）
allow_access = False  # ここを変更してアクセス制御

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

# リセットボタン：チャット履歴をリセット
if st.button("リセット"):
    st.session_state["chat_history"] = []
    st.session_state["user_prompt"] = ""

# 2つ目のプロンプト入力欄（AIエージェントの返信を制御する）
control_prompt = st.text_area("📝 AIの反応を制御するプロンプトを入力：", height=100, key="control_prompt")

# 1つ目のプロンプト入力欄（AIエージェントとのチャット）
user_message = st.text_area("📝 AIとのチャットメッセージを入力：", height=100, key="user_message")

# チャット履歴の表示
if st.session_state["chat_history"]:
    for chat in st.session_state["chat_history"]:
        # ユーザーのメッセージ表示
        st.markdown(f"**👤 ユーザー**: {chat['user']}")
        # エージェントのメッセージ表示
        st.markdown(f"**🤖 エージェント**: {chat['agent']}")

# 🚀 チャット送信ボタン
if st.button("🚀 チャット送信") and user_message.strip():
    with st.spinner("AIが考え中..."):
        try:
            # ユーザーのメッセージを履歴に追加
            st.session_state["chat_history"].append({"user": user_message, "agent": ""})

            # ユーザーのメッセージを含めてエージェントへのプロンプトを作成
            prompt_for_ai = user_message

            # 制御プロンプトが入力されていれば、それをAIに伝える
            if control_prompt.strip():
                prompt_for_ai = control_prompt + "\n" + user_message

            # AI返答生成
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "system", "content": "あなたは親しみやすく面白いアシスタントです。"}] + [
                    {"role": "user", "content": chat["user"]} for chat in st.session_state["chat_history"]
                ] + [{"role": "user", "content": prompt_for_ai}]
            )
            ai_reply = response.choices[0].message.content

            # エージェントの返答を履歴に追加
            st.session_state["chat_history"][-1]["agent"] = ai_reply

            # 結果表示
            st.success("🎉 AIの返答")
            st.write(ai_reply)

        except Exception as e:
            st.error(f"エラーが発生しました: {e}")

# フッター
st.markdown("---")
st.caption("Powered by GPT-4o / Streamlit ✨ 教育目的で使用中")
