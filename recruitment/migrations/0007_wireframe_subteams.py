from django.db import migrations

# Sub-teams per the Team Choice wireframe: Sea runs Vital Spark and an
# Energy Class entry, Air runs an Energy Class entry.
NEW_TEAMS = {
    'sea': [
        ('Vital Spark', 'Our hydrogen race craft for the Monaco Energy Boat Challenge.'),
        ('Energy Class', 'The open Energy Class entry raced at Monaco.'),
    ],
    'air': [
        ('Energy Class', 'The Energy Class entry for the air division.'),
    ],
}

OLD_SEA_TEAMS = [
    'Powertrain', 'Thermal Management', 'Aerodynamics',
    'CAD & Design', 'Mechanics', 'Testing & Documentation',
]
OLD_AIR_TEAMS = ['Concept Design', 'Propulsion', 'Structures']


def reseed(apps, schema_editor):
    Team = apps.get_model('recruitment', 'Team')
    for division, names in (('sea', OLD_SEA_TEAMS), ('air', OLD_AIR_TEAMS)):
        for team in Team.objects.filter(division=division, name__in=names):
            if not (
                team.first_pick_applications.exists()
                or team.alternative_applications.exists()
                or team.wildcard_applications.exists()
            ):
                team.delete()
    for division, teams in NEW_TEAMS.items():
        for name, tagline in teams:
            Team.objects.get_or_create(
                division=division, name=name, defaults={'tagline': tagline}
            )


def undo(apps, schema_editor):
    Team = apps.get_model('recruitment', 'Team')
    for division, teams in NEW_TEAMS.items():
        Team.objects.filter(
            division=division, name__in=[n for n, _ in teams]
        ).delete()


class Migration(migrations.Migration):
    dependencies = [('recruitment', '0006_seed_division_teams')]
    operations = [migrations.RunPython(reseed, undo)]
