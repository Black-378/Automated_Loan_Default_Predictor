from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings
from django.contrib import messages
from .forms import LoanApplicationForm
from .models import LoanApplication
from django import forms
import joblib
import numpy as np
import os


# Load ML Model and Scaler
MODEL_PATH = os.path.join(settings.BASE_DIR, 'loans', 'loan_model.pkl')
SCALER_PATH = os.path.join(settings.BASE_DIR, 'loans', 'scaler.pkl')

model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)


# Register View
def register(request):

    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('login')

    else:
        form = UserCreationForm()

    return render(request, 'registration/register.html', {'form': form})


# Dashboard View
@login_required
def dashboard(request):
    
    user_loans = LoanApplication.objects.filter(
        user=request.user
    ).order_by('-applied_on')

    return render(request, 'loans/dashboard.html', {'loans': user_loans})


# Apply Loan View
@login_required
def apply_loan(request):

    if request.method == 'POST':

        form = LoanApplicationForm(request.POST)

        if form.is_valid():
            
            loan = form.save(commit=False)
            loan.user = request.user

            # Encode Gender
            gender_val = 1 if loan.gender == 'female' else 0

            # Encode Education (must match MODEL training)
            is_bachelor = 1 if loan.education == 'Bechalor' else 0
            is_hs = 1 if loan.education == 'High School or Below' else 0
            is_college = 1 if loan.education == 'college' else 0

            # Model Input Order
            input_data = np.array([[
                loan.principal,
                loan.terms,
                loan.age,
                gender_val,
                loan.terms,
                0,
                is_bachelor,
                is_hs,
                is_college
            ]])

            # Scale
            input_scaled = scaler.transform(input_data)

            # Predict
            prediction = model.predict(input_scaled)
            probability = model.predict_proba(input_scaled)[0][1]

            # Save Prediction
            loan.prediction_result = "Approved" if prediction[0] == 1 else "Rejected"
            loan.probability_score = round(probability * 100, 2)

            loan.save()
            messages.success(request, f"Your application has been processed by our AI engine!")
            return redirect('dashboard')

    else:
        form = LoanApplicationForm()

    return render(request, 'loans/apply.html', {'form': form})