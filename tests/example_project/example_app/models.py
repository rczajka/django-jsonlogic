from django.db import models


class ExampleModel(models.Model):
    """We'll register this model for editing in admin."""
    logic = models.TextField()


class ExampleSubModel(models.Model):
    """We'll use this model as an inline in admin."""
    example = models.ForeignKey(ExampleModel)
    logic = models.TextField()
