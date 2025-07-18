from generator.content_generator import generate_text
from generator.image_generator import generate_image
from generator.topic_suggester import suggest_topic  # пока создадим заглушку

def generate_full_post(style: str = "дружелюбный", topic: str = None) -> dict:
    # Если темы нет — создаём её автоматически
    if not topic:
        topic = suggest_topic()

    text = generate_text(topic, style)
    image_url = generate_image(topic)

    return {
        "topic": topic,
        "text": text,
        "image_url": image_url
    }
