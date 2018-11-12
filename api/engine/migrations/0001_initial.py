# Generated by Django 2.0 on 2018-11-11 20:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dormitory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
                ('history', models.CharField(max_length=1000)),
                ('geo_longitude', models.CharField(max_length=20)),
                ('geo_latitude', models.CharField(max_length=20)),
                ('address', models.CharField(max_length=150)),
                ('category', models.CharField(choices=[('0', 'public'), ('1', 'private')], default='0', max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='Filter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
        ),
        migrations.CreateModel(
            name='Option',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='RoomCharacteristics',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_quota', models.IntegerField(default=0)),
                ('allowed_quota', models.IntegerField(default=0)),
                ('dormitory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='room_characteristics', to='engine.Dormitory')),
            ],
        ),
        migrations.CreateModel(
            name='ActivityFacilityFilter',
            fields=[
                ('filter_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='engine.Filter')),
                ('is_dorm_activity_facility', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('engine.filter',),
        ),
        migrations.CreateModel(
            name='IntegralFilter',
            fields=[
                ('filter_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='engine.Filter')),
                ('number', models.IntegerField(default=0)),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('engine.filter',),
        ),
        migrations.CreateModel(
            name='RadioFilter',
            fields=[
                ('filter_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='engine.Filter')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('engine.filter',),
        ),
        migrations.AddField(
            model_name='roomcharacteristics',
            name='filters',
            field=models.ManyToManyField(related_name='filters', to='engine.Filter'),
        ),
        migrations.AddField(
            model_name='filter',
            name='polymorphic_ctype',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_engine.filter_set+', to='contenttypes.ContentType'),
        ),
        migrations.AddField(
            model_name='option',
            name='radio_filter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='options', to='engine.RadioFilter'),
        ),
        migrations.AddField(
            model_name='dormitory',
            name='activities_facilities',
            field=models.ManyToManyField(related_name='activities_facilities', to='engine.ActivityFacilityFilter'),
        ),
    ]
