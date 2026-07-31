from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [('recruitment', '0003_remove_profile_dietary_requirements_and_more')]

    operations = [
        migrations.RemoveField(model_name='application', name='why_join'),
        migrations.RemoveField(model_name='application', name='experience'),
        migrations.RemoveField(model_name='application', name='anything_else'),
        migrations.AddField(
            model_name='application', name='why_society',
            field=models.TextField(default='', verbose_name='Why this society?'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='application', name='why_division',
            field=models.TextField(default='', verbose_name='Why this division?'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='application', name='what_makes_you',
            field=models.TextField(default='', verbose_name='What makes you you?'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='application', name='what_to_learn',
            field=models.TextField(default='', verbose_name='What do you want to learn?'),
            preserve_default=False,
        ),
    ]
