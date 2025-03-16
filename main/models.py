from django.db import models

class Shipment(models.Model):
    BRANCH_CHOICES = (
        ('ATL', 'ATL'),
        ('CMU', 'CMU'),
        ('CON', 'CON'),
        ('DOR', 'DOR'),
        ('HEC', 'HEC'),
        ('HNL', 'HNL'),
        ('HOU', 'HOU'),
        ('ICS', 'ICS'),
        ('IMP', 'IMP'),
        ('JFK', 'JFK'),
        ('LAX', 'LAX'),
        ('LCL', 'LCL'),
        ('ORD', 'ORD'),
        ('PPG', 'PPG'),
    )

    CLAIM_RECEIVED_CHOICES = (
        ('YES', 'Yes'),
        ('NO', 'No'),
    )

    Claim_No = models.CharField(max_length=100, unique=True)  # Ensuring unique claim numbers
    Claiming_Client = models.CharField(max_length=100, blank=True, null=True)
    Branch = models.CharField(max_length=3, choices=BRANCH_CHOICES)
    Formal_Claim_Received = models.CharField(max_length=3, choices=CLAIM_RECEIVED_CHOICES, blank=True, null=True)
    Intend_Claim_Date = models.DateField(blank=True, null=True)
    Formal_Claim_Date_Received = models.DateField(blank=True, null=True)
    Claimed_Amount = models.DecimalField(max_digits=10, decimal_places=2)
    Closed_Date = models.DateField(blank=True, null=True)
    Amount_Paid_By_Carrier = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    Amount_Paid_By_Awa = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    Amount_Paid_By_Insurance = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f"Shipment No: {self.Claim_No}"
