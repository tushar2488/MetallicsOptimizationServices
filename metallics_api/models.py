from django.db import models

class Chemical(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=250, unique=True, blank=False, null=False)

    class Meta:
        db_table = 'chemical'

    def __str__(self):
        return self.name


class Commodity(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=250, unique=True, blank=False, null=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    inventory = models.DecimalField(max_digits=10, decimal_places=2,blank=True)

    class Meta:
        db_table = "commodity"

    def __str__(self):
        return self.name


class Composition(models.Model):
    id = models.AutoField(primary_key=True)
    commodity = models.ForeignKey(Commodity, on_delete=models.CASCADE)
    element = models.ForeignKey(Chemical, on_delete=models.CASCADE)
    percentage = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = "composition"

    def __str__(self):
        return self.commodity.name + " - " + self.element.name + " - " + str(self.percentage) + "%"
