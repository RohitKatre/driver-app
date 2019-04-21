# Generated by Django 2.2 on 2019-04-17 06:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20190416_0928'),
    ]

    operations = [
        migrations.RenameField(
            model_name='combinevericle',
            old_name='acctual_days_past_due',
            new_name='actual_days_past_due',
        ),
        migrations.RenameField(
            model_name='combinevericle',
            old_name='contract_data',
            new_name='contract_date',
        ),
        migrations.AlterField(
            model_name='borrowerfinace',
            name='account_status',
            field=models.CharField(choices=[('R', 'Recurrent'), ('P', 'OpenRecurrent'), ('O', 'TestRecurrent')], max_length=2),
        ),
        migrations.AlterField(
            model_name='combinevericle',
            name='account_status',
            field=models.CharField(choices=[('R', 'Recurrent'), ('P', 'OpenRecurrent'), ('O', 'TestRecurrent')], max_length=2),
        ),
        migrations.AlterField(
            model_name='driver',
            name='repo_agent_id',
            field=models.CharField(blank=True, max_length=20, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='driver',
            name='signature',
            field=models.ImageField(upload_to='signature/17-04-2019-06-04'),
        ),
    ]
