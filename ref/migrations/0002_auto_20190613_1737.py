# Generated by Django 2.2.2 on 2019-06-13 15:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ref', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='consultant',
            name='company',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='ref.Subsidiary', verbose_name='Subsidiary'),
        ),
        migrations.AlterField(
            model_name='subsidiary',
            name='responsible',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='ref.Consultant'),
        ),
    ]