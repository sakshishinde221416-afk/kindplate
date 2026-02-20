from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donations', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='donation',
            name='food_image',
            field=models.ImageField(blank=True, null=True, upload_to='donation_images/'),
        ),
    ]
