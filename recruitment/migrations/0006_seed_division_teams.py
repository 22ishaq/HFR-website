from django.db import migrations

# Sub-teams per division, from the wireframes (Land: p3 team structure,
# Sea: p4 roles, Operations: draft board wireframe). Air is placeholder
# until that division's structure is decided. Edit freely in admin.
DIVISION_TEAMS = {
    'land': [
        ('Aerodynamics', 'Shape the Shell Eco car that cuts through the air.'),
        ('Electrical', 'Wiring, power distribution and control systems.'),
        ('Dynamics', 'Suspension, steering and handling.'),
        ('Data & Telemetry', 'Live data from the car, turned into lap decisions.'),
        ('Chassis', 'The structure everything else bolts onto.'),
        ('HFC', 'The hydrogen fuel cell at the heart of the car.'),
    ],
    'sea': [
        ('Powertrain', 'Drive systems for the Vital Spark race craft.'),
        ('Thermal Management', 'Keeping the fuel cell and drivetrain cool at race pace.'),
        ('Aerodynamics', 'Hull and surface flow for the Monaco Energy Boat Challenge.'),
        ('CAD & Design', 'Modelling the boat before a single part is cut.'),
        ('Mechanics', 'Build, assembly and race-day repairs.'),
        ('Testing & Documentation', 'Prove it works, then write down how.'),
    ],
    'air': [
        ('Concept Design', 'Define what a hydrogen aircraft from HFR looks like.'),
        ('Propulsion', 'Hydrogen power for flight.'),
        ('Structures', 'Lightweight airframes that hold together.'),
    ],
    'operations': [
        ('Business', 'Partnerships and the commercial side of HFR.'),
        ('Finance & Contracts', 'Budgets, purchasing and agreements.'),
        ('Social Media', 'Tell the HFR story across every channel.'),
    ],
}

OLD_PLACEHOLDER_NAMES = [
    'Shell Eco (Land)', 'Vital Spark (Sea)', 'Aero Concept (Air)',
    'Business & Sponsorship', 'Marketing & Media', 'Events & Outreach',
]


def seed(apps, schema_editor):
    Team = apps.get_model('recruitment', 'Team')
    # Drop the old flat placeholder teams where nothing references them
    for team in Team.objects.filter(name__in=OLD_PLACEHOLDER_NAMES):
        if not (
            team.first_pick_applications.exists()
            or team.alternative_applications.exists()
            or team.wildcard_applications.exists()
        ):
            team.delete()
    for division, teams in DIVISION_TEAMS.items():
        for name, tagline in teams:
            Team.objects.get_or_create(
                division=division, name=name, defaults={'tagline': tagline}
            )


def unseed(apps, schema_editor):
    Team = apps.get_model('recruitment', 'Team')
    for division, teams in DIVISION_TEAMS.items():
        Team.objects.filter(
            division=division, name__in=[n for n, _ in teams]
        ).delete()


class Migration(migrations.Migration):
    dependencies = [('recruitment', '0005_alter_team_options_team_division_alter_team_name_and_more')]
    operations = [migrations.RunPython(seed, unseed)]
