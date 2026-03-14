from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class LoanApplication(models.Model):
    # Link the loan to a specific logged-in user
    # This creates the "Login" connection. Only the person who logged in can see their own loan details.
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # Financial Details
    principal = models.IntegerField(default=1000)
    terms = models.IntegerField(help_text="Loan term in days")

    # Personal Details
    age = models.IntegerField()
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female')])
    education = models.CharField(max_length=50, choices=[
        ('High School or Below', 'High School or Below'),
        ('Bachelor', 'Bachelor'),
        ('college', 'College'),
        ('Master or Above', 'Master or Above')
    ])

    # System timestamps (Auto-filled)
    applied_on = models.DateTimeField(auto_now_add=True)

    # The Result (To be filled by our AI Model)
    prediction_result = models.CharField(max_length=20, blank=True, null=True)
    probability_score = models.FloatField(blank=True, null=True)

    def __str__(self):
        return f"Loan {self.id} - {self.user.username}"