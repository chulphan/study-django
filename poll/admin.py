from django.contrib import admin
from poll.models import Question, Choice

# Register your models here.

# class QuestionAdmin(admin.ModelAdmin):
#     fields = ['pub_date', 'question_text']

# class QuestionAdmin(admin.ModelAdmin):
#     fieldsets = [
#         ('Question Statement', {'fields': ['question_text']}),
#         ('Date Information', {'fields': ['pub_date'], 'classes': ['collapse']})
#     ]

class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 2

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]

admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)