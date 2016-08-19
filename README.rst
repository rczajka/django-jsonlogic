django-jsonlogic
===============

This package provides a Django form widget for editing logic in
JSONLogic format in a form.

Usage:
------

* Add `jsonlogic_widget` to your INSTALLED_APPS.
* Use `jsonlogic_widget.JSONLogicWidget` in a form, e.g. by using
  ModelAdmin.formfield_overrides for Django admin.
  See `tests/example_project` for an example.

Known issues:
-------------

In Django 1.8, the widget won't work in dynamically added rows in inline
formsets.  This is because the JavaScript event on adding a row was only
added in Django 1.9.
