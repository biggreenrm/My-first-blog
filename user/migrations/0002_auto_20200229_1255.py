# Generated by Django 2.2.10 on 2020-02-29 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("user", "0001_initial")]

    operations = [
        migrations.AlterField(
            model_name="customuser",
            name="sex",
            field=models.CharField(
                choices=[("man", "Мужчина"), ("woman", "Женщина"), ("secret", "Скрыт")],
                default="Скрыт",
                max_length=255,
                verbose_name="Пол",
            ),
        )
    ]
