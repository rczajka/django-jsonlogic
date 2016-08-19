from django.contrib import admin
from django.db import models
from jsonlogic_widget import JSONLogicWidget
from .models import ExampleModel, ExampleSubModel


class ExampleSubModelInline(admin.StackedInline):
    """Using the widget here for all TextFields."""
    model = ExampleSubModel
    extra = 1
    formfield_overrides = {
        models.TextField: {'widget': JSONLogicWidget},
    }


class ExampleModelAdmin(admin.ModelAdmin):
    """Defining actions, variables and a subset of operators."""
    formfield_overrides = {
        models.TextField: {'widget': JSONLogicWidget(
            actions=["Fail"],
            variables=["some.var"],
            operators=["!", "if", "<"]
        )},
    }
    inlines = [
        ExampleSubModelInline
    ]


admin.site.register(ExampleModel, ExampleModelAdmin)
