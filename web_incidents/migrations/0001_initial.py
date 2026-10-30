# Начальная миграция ORM-моделей ПР9.
from django.db import migrations, models
import django.db.models.deletion
import django.core.validators


class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(name="IncidentUser", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("name", models.CharField(max_length=150, unique=True)),
        ], options={"ordering": ["name"]}),
        migrations.CreateModel(name="Executor", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("name", models.CharField(max_length=150, unique=True)),
        ], options={"ordering": ["name"]}),
        migrations.CreateModel(name="Incident", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("title", models.CharField(max_length=255)),
            ("description", models.TextField()),
            ("priority", models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(3)])),
            ("status", models.CharField(choices=[("Новый", "Новый"), ("В работе", "В работе"), ("Решен", "Решен"), ("Закрыт", "Закрыт")], max_length=20)),
            ("created_at", models.DateTimeField()),
            ("user", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="incidents", to="web_incidents.incidentuser")),
            ("executor", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="incidents", to="web_incidents.executor")),
        ], options={"ordering": ["id"]}),
    ]
