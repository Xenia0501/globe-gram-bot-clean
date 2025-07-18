from generator.post_generator import generate_full_post

# Задаём стиль, а тему оставляем пустой — будет авто-выбор
post = generate_full_post(style="креативный", topic=None)

print(f"\n🎯 Тема: {post['topic']}")
print(f"\n📝 Текст:\n{post['text']}")
print(f"\n🖼️ Изображение:\n{post['image_url']}")
