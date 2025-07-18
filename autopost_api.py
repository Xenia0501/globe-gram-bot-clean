from flask import Flask, request, jsonify
from datetime import datetime
from generator.post_generator import generate_full_post
from storage import get_group, get_user_settings, get_all_user_settings

app = Flask(__name__)

@app.route("/autopost", methods=["GET"])
def autopost():
    user_id = request.args.get("user_id")
    if not user_id:
        return jsonify({"error": "user_id is required"}), 400

    group_id = get_group(int(user_id))
    settings = get_user_settings(int(user_id))

    if not group_id or not settings:
        return jsonify({"error": "Group or settings not found"}), 404

    style = settings.get("style")
    topics = settings.get("topics", [])
    topic = topics[0] if topics else None

    post = generate_full_post(style=style, topic=topic)

    return jsonify({
        "chat_id": group_id,
        "image_url": post["image_url"],
        "text": post["text"]
    })

@app.route("/autopost/batch", methods=["GET"])
def autopost_batch():
    now = datetime.now().strftime("%H:%M")
    all_settings = get_all_user_settings()
    posts = []

    for user_id_str, data in all_settings.items():
        schedule = data.get("schedule", "").strip()
        group_id = data.get("group_id")
        style = data.get("style")
        topics = data.get("topics", [])
        topic = topics[0] if topics else None

        if not schedule or not group_id:
            continue

        if now in schedule:  # простая проверка: "10:00"
            post = generate_full_post(style=style, topic=topic)
            posts.append({
                "chat_id": group_id,
                "text": post["text"],
                "image_url": post["image_url"]
            })

    return jsonify(posts)

if __name__ == "__main__":
    print("✅ Flask API запускается на http://localhost:5000")
    app.run(debug=True, port=5000)
