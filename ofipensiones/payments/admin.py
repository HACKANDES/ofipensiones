from django.contrib import admin

from .models import (
    Grade,
    GradeTerm,
    Institution,
    OfipensionesLog,
    Student,
    TermPayment,
)

admin.site.register(Institution)
admin.site.register(Grade)
admin.site.register(GradeTerm)
admin.site.register(Student)
admin.site.register(TermPayment)
admin.site.register(OfipensionesLog)
