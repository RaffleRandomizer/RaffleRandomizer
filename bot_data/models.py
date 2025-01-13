from django.db import models
from backend.models import TimeBasedModel

class Language(TimeBasedModel):
    name = models.CharField(max_length=128)

    class Meta:
        verbose_name = "Язык"
        verbose_name_plural = "Языки"

    def __str__(self) -> str:
        return self.name


class Text(TimeBasedModel):
    class KeyType(models.TextChoices):
        ILINE = "IK", "InlineKB"
        REPLY = "RK", "ReplyKB"
        TEXT = "TXT", "Text"
        CAPTION = "CAP", "Caption"

    key = models.CharField(max_length=128, verbose_name="ключ")
    key_type = models.CharField(
        "Тип", max_length=3, choices=KeyType.choices, default=KeyType.TEXT
    )

    class Meta:
        verbose_name = "Ключ"
        verbose_name_plural = "Ключи"

    def __str__(self) -> str:
        return self.key


class Translate(TimeBasedModel):
    text_key = models.ForeignKey(
        Text, on_delete=models.CASCADE, related_name="all_translates"
    )
    language = models.ForeignKey(
        Language, on_delete=models.CASCADE, related_name="all_text"
    )
    translate = models.TextField(max_length=4096, verbose_name="Текст")

    class Meta:
        verbose_name = "Текст на языке"
        verbose_name_plural = "Тексты на языках"

    def __str__(self) -> str:
        return f"{self.text_key.key}: {self.translate}"

class Key(models.Model):
    class Meta:
        abstract = True
        
    key = models.CharField(max_length=128, verbose_name="ключ")
    
    def __str__(self) -> str:
        return self.key



class Files(TimeBasedModel, Key):
    class Meta:
        verbose_name = "Файл в боте"
        verbose_name_plural = "Файлы в боте"

    file = models.FileField(verbose_name="Файл", upload_to="files")
    file_id = models.CharField(verbose_name="Идентификатор файла", max_length=512, null=True, blank=True)
    

class Photo(TimeBasedModel, Key):
    class Meta:
        verbose_name = "Фото в боте"
        verbose_name_plural = "Фото в боте"

    photo = models.FileField(verbose_name="Фото", upload_to="photos")
    file_id = models.CharField(verbose_name="Идентификатор файла", max_length=512, null=True, blank=True)
    
    

