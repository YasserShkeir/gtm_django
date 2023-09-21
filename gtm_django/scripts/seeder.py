import random
import string
from django.utils import timezone
from content.models import Content, Language


def run():
    # Create 4 languages
    languages = ["French", "English", "Spanish", "German"]

    for language in languages:
        Language.objects.create(name=language)

    # Create 10 contents
    for i in range(10):
        language = Language.objects.get(name=random.choice(languages))
        Content.objects.create(
            title="".join(random.choices(string.ascii_letters, k=10)),
            text="".join(random.choices(string.ascii_letters, k=20)),
            language=language,
            points=random.randint(0, 100),
            creationDate=timezone.now(),
        )

    