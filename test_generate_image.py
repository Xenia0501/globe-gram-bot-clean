from generator.image_generator import generate_image

topic = "Пляжи Португалии"
image_url = generate_image(topic)

print("\nСгенерированное изображение:\n", image_url)
