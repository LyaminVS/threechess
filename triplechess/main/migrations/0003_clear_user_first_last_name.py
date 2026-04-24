from django.db import migrations


def clear_first_last_names(apps, schema_editor):
    User = apps.get_model("auth", "User")
    User.objects.all().update(first_name="", last_name="")


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0002_add_game_is_sandbox"),
    ]

    operations = [
        migrations.RunPython(clear_first_last_names, noop),
    ]
