from django.db import migrations

# Display order from the Team Choice wireframe
ORDER = {
    'land': ['Aerodynamics', 'Electrical', 'Dynamics', 'Data & Telemetry', 'Chassis', 'HFC'],
    'sea': ['Vital Spark', 'Energy Class'],
    'air': ['Energy Class'],
    'operations': ['Business', 'Finance & Contracts', 'Social Media'],
}


def apply_order(apps, schema_editor):
    Team = apps.get_model('recruitment', 'Team')
    for division, names in ORDER.items():
        for i, name in enumerate(names, start=1):
            Team.objects.filter(division=division, name=name).update(sort_order=i)


class Migration(migrations.Migration):
    dependencies = [('recruitment', '0008_alter_team_options_team_sort_order')]
    operations = [migrations.RunPython(apply_order, migrations.RunPython.noop)]
