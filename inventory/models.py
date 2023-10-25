from django.db import models


# Create your models here.
class Inventory(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(
        max_length=100, default="Suffolk Coins Inventory Item", blank=True, null=True
    )
    file = models.FileField(
        upload_to="inventory_files", default="inventory_files/blank.pdf"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Inventories"
