from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0003_clear_user_first_last_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="game",
            name="sandbox_ordered_turn",
            field=models.BooleanField(default=False),
        ),
    ]

