from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0004_game_sandbox_ordered_turn"),
    ]

    operations = [
        migrations.AddField(
            model_name="game",
            name="is_private",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="game",
            name="owner",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="owned_games",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]

