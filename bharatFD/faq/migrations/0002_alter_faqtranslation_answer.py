# Generated by Django 5.1.5 on 2025-02-01 19:46

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("faq", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="faqtranslation",
            name="answer",
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
    ]
