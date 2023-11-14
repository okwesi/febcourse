from django.db import models

class Attendee(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    tag_number = models.CharField(max_length=20)
    telephone = models.CharField(max_length=15)
    area = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    local_assembly = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_contact_info(self):
        return f"Phone: {self.telephone}, Area: {self.area}, District: {self.district}"

    def is_high_amount(self):
        return self.amount > 1000

    def format_amount(self):
        return "${:.2f}".format(self.amount)
