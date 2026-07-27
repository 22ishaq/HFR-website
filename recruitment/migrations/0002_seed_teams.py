from django.db import migrations

# Placeholder draft board. Team list isn't finalised yet, edit freely in admin.
DEFAULT_TEAMS = [
    ('Shell Eco (Land)', 'Ultra-efficient hydrogen land vehicle for Shell Eco-Marathon.'),
    ('Vital Spark (Sea)', 'Hydrogen race craft for the Monaco Energy Boat Challenge.'),
    ('Aero Concept (Air)', 'Future hydrogen-powered aviation concept work.'),
    ('Business & Sponsorship', 'Partnerships, sponsorship and commercial strategy.'),
    ('Marketing & Media', 'Brand, social media, photography, video and comms.'),
    ('Events & Outreach', 'Lectures, site tours, socials and STEM outreach.'),
]


def seed(apps, schema_editor):
    Team = apps.get_model('recruitment', 'Team')
    RecruitmentSettings = apps.get_model('recruitment', 'RecruitmentSettings')
    for name, tagline in DEFAULT_TEAMS:
        Team.objects.get_or_create(name=name, defaults={'tagline': tagline})
    RecruitmentSettings.objects.get_or_create(pk=1)


def unseed(apps, schema_editor):
    Team = apps.get_model('recruitment', 'Team')
    Team.objects.filter(name__in=[n for n, _ in DEFAULT_TEAMS]).delete()


class Migration(migrations.Migration):
    dependencies = [('recruitment', '0001_initial')]
    operations = [migrations.RunPython(seed, unseed)]
