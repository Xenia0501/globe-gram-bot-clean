def generate_text(style: str, topic: str = None) -> str:
    if topic:
        return f"Вот интересный пост на тему '{topic}', оформленный в стиле '{style}'."
    else:
        return f"Вот вдохновляющий тревел-пост в стиле '{style}'."
