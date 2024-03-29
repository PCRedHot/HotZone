# Generated by Django 3.1.2 on 2020-10-29 19:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Case',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('case_number', models.IntegerField()),
                ('date_confirmed', models.DateField()),
                ('is_local', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Disease',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('disease_name', models.CharField(max_length=20)),
                ('virus', models.CharField(max_length=20)),
                ('max_infectious_period', models.IntegerField()),
                ('curr_case_number', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('patient_name', models.CharField(max_length=100)),
                ('identify_number', models.CharField(max_length=20)),
                ('date_of_birth', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=100, null=True)),
                ('x_coor', models.IntegerField()),
                ('y_coor', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='CasePlace',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_from', models.DateField()),
                ('date_to', models.DateField()),
                ('category', models.CharField(choices=[('Residence', 'Residence'), ('Workplace', 'Workplace'), ('Visit', 'Visit')], default='Visit', max_length=9)),
                ('case', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotzoneData.case')),
                ('place', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotzoneData.place')),
            ],
        ),
        migrations.AddField(
            model_name='case',
            name='disease',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotzoneData.disease'),
        ),
        migrations.AddField(
            model_name='case',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotzoneData.patient'),
        ),
    ]
