import inspect
from django import forms
from django.conf import settings
from django.template.loader import render_to_string
import json_logic


class JSONLogicWidget(forms.Textarea):
    class Media:
        js = (
            settings.STATIC_URL + 'jsonlogic/jsonlogic.js',
        )
        css = {
            'all': (settings.STATIC_URL + 'jsonlogic/jsonlogic.css',)
        }

    def __init__(self, attrs=None,
                 actions=None, variables=None, operators=None):
        super(JSONLogicWidget, self).__init__(attrs)
        self.actions = actions
        self.variables = variables
        self.operators = operators

    def render(self, name, value, attrs=None):
        known_binary = set(['-', '/'])
        textarea = super(JSONLogicWidget, self).render(name, value, attrs)

        if self.operators is not None:
            operator_names = self.operators
        else:
            operator_names = sorted(json_logic.operations.keys())

        operators = []
        for operator in operator_names:
            func = json_logic.operations[operator]

            if operator == 'var':
                continue

            try:
                arg_spec = inspect.getargspec(func)
            except TypeError:
                # Some functions (builtins, C extensions) can't be inspected.
                # We'll just assume 2 args for them for now.
                min_args = max_args = initial_args = 2
            else:
                assert arg_spec.keywords is None
                min_args = max_args = initial_args = len(arg_spec.args)
                if arg_spec.varargs:
                    max_args = None
                    if not initial_args:
                        initial_args = 2

                if arg_spec.defaults:
                    min_args -= len(arg_spec.defaults)
                    if operator not in known_binary:
                        initial_args = min_args

            operators.append({
                "operator": operator,
                "min_args": min_args,
                "max_args": max_args,
                "initial_args": '[' + ",".join(["null"] * initial_args) + ']',
            })

        return render_to_string(
            "jsonlogic/widget.html",
            {
                'operators': operators,
                'actions': self.actions,
                'variables': self.variables,
                'textarea': textarea,
            }
        )
