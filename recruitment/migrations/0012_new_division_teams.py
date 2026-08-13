from django.db import migrations

# Sea and Air now mirror Land's engineering sub-teams rather than carrying a
# single boat or aircraft entry.
NEW_TEAMS = {
    'sea': ['Aerodynamics', 'Electrical', 'Dynamics', 'Chassis'],
    'air': ['Aerodynamics', 'Electrical', 'Dynamics', 'Chassis'],
}

TAGLINES = {
    'sea': {
        'Aerodynamics': 'Hull and surface flow for the Monaco Energy Boat Challenge.',
        'Electrical': 'Wiring, power distribution and control on the water.',
        'Dynamics': 'Handling and stability of the race craft.',
        'Chassis': 'The hull and structure everything else mounts to.',
    },
    'air': {
        'Aerodynamics': 'Lift, drag and surfaces for hydrogen powered flight.',
        'Electrical': 'Avionics, power distribution and control systems.',
        'Dynamics': 'Flight stability and control behaviour.',
        'Chassis': 'Airframe and structures.',
    },
}

# What Sea and Air used to hold before this change
OLD_TEAMS = {
    'sea': ['Vital Spark', 'Energy Class'],
    'air': ['Energy Class', 'Concept Design', 'Propulsion', 'Structures'],
}


def reseed(apps, schema_editor):
    Team = apps.get_model('recruitment', 'Team')

    for division, names in NEW_TEAMS.items():
        for order, name in enumerate(names, start=1):
            Team.objects.update_or_create(
                division=division, name=name,
                defaults={
                    'tagline': TAGLINES[division][name],
                    'sort_order': order,
                    'is_recruiting': True,
                },
            )

    # Retire the old entries, but never delete one an application points at,
    # since that would break someone's draft picks.
    for division, names in OLD_TEAMS.items():
        for team in Team.objects.filter(division=division, name__in=names):
            in_use = (
                team.first_pick_applications.exists()
                or team.alternative_applications.exists()
                or team.wildcard_applications.exists()
            )
            if in_use:
                team.is_recruiting = False
                team.save()
            else:
                team.delete()


def undo(apps, schema_editor):
    Team = apps.get_model('recruitment', 'Team')
    for division, names in NEW_TEAMS.items():
        Team.objects.filter(division=division, name__in=names).delete()


class Migration(migrations.Migration):
    dependencies = [('recruitment', '0011_alter_application_status')]
    operations = [migrations.RunPython(reseed, undo)]
