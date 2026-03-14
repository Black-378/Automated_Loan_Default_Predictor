from django.contrib import admin
from .models import LoanApplication

@admin.register(LoanApplication)
class LoanApplicationAdmin(admin.ModelAdmin):
    # What columns to show in the admin list
    list_display = ('user', 'applied_on', 'principal', 'prediction_result', 'probability_score')
    
    # Add filters to quickly find rejected loans
    list_filter = ('prediction_result', 'education')
    
    # Allow searching by username
    search_fields = ('user__username',)
    
    # Make the AI score read-only so managers can't fake the data
    readonly_fields = ('applied_on', 'probability_score')