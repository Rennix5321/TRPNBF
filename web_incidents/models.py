"""Модели ORM ПР9. Не путать с консольными классами models/."""
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class IncidentUser(models.Model):
    name = models.CharField(max_length=150, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Executor(models.Model):
    name = models.CharField(max_length=150, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Incident(models.Model):
    STATUSES = [(s, s) for s in ("Новый", "В работе", "Решен", "Закрыт")]
    title = models.CharField(max_length=255)
    description = models.TextField()
    user = models.ForeignKey(IncidentUser, on_delete=models.PROTECT,
                             related_name="incidents")
    executor = models.ForeignKey(Executor, on_delete=models.SET_NULL,
                                 null=True, blank=True, related_name="incidents")
    priority = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(3)])
    status = models.CharField(max_length=20, choices=STATUSES)
    # В исходном JSON дата хранится строкой ISO; DateTimeField обеспечивает
    # корректную сортировку и работу с датами через ORM.
    created_at = models.DateTimeField()

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return f"#{self.pk}: {self.title}"
