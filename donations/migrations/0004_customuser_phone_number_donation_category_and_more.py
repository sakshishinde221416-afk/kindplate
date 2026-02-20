from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donations', '0003_request_is_read'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='phone_number',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='donation',
            name='category',
            field=models.CharField(choices=[('vegetarian', 'Vegetarian'), ('vegan', 'Vegan'), ('non_veg', 'Non-Vegetarian'), ('halal', 'Halal'), ('kosher', 'Kosher'), ('gluten_free', 'Gluten Free'), ('dairy_free', 'Dairy Free'), ('other', 'Other')], default='other', max_length=20),
        ),
        migrations.AddField(
            model_name='donation',
            name='pickup_time_end',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='donation',
            name='pickup_time_start',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='request',
            name='notes',
            field=models.TextField(blank=True, null=True),
        ),
    ]
