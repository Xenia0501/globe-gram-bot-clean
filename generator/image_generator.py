import openai
from config import OPENAI_API_KEY

client = openai.OpenAI(api_key=OPENAI_API_KEY)

def generate_image(topic: str) -> str:
    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=f"Иллюстрация к тревел-блогу на тему: {topic}",
            size="1024x1024",
            quality="standard",
            n=1
        )
        return response.data[0].url
    except Exception as e:
        return f"[ОШИБКА при генерации изображения]: {e}"
