from flask import Flask, render_template, request, jsonify
from openai import OpenAI

app = Flask(__name__)

client = OpenAI(
    api_key="api",
    base_url="https://api.groq.com/openai/v1"
)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/ask", methods=["POST"])
@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    user_input = data.get("message")

    # 先用简单“无状态版本升级”为“有记忆版本（临时）”
    if "history" not in globals():
        global history
        history = []

    history.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "你是一个有帮助的AI助手"}
        ] + history
    )

    reply = response.choices[0].message.content

    history.append({"role": "assistant", "content": reply})

    return jsonify({"reply": reply})


if __name__ == "__main__":
    app.run(debug=True)