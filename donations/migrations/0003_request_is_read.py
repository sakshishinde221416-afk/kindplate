from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donations', '0002_donation_food_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='request',
            name='is_read',
            field=models.BooleanField(default=False),
        ),
    ]
