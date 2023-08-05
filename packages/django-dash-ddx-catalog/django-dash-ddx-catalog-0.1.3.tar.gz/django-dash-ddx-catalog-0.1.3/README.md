# django-dash-ddx-catalog

[![GitHub Actions](https://github.com/pikhovkin/django-dash-ddx-catalog/workflows/build/badge.svg)](https://github.com/pikhovkin/django-dash-ddx-catalog/actions)
[![PyPI](https://img.shields.io/pypi/v/django-dash-ddx-catalog.svg)](https://pypi.org/project/django-dash-ddx-catalog/)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/django-dash-ddx-catalog.svg)
[![framework - Django](https://img.shields.io/badge/framework-Django-0C3C26.svg)](https://www.djangoproject.com/)
![PyPI - Django Version](https://img.shields.io/pypi/djversions/django-dash-ddx-catalog.svg)
[![PyPI - License](https://img.shields.io/pypi/l/django-dash-ddx-catalog)](./LICENSE)

Auxiliary Django forms for semi-automatic CRUD for [dash-devextreme](https://github.com/pikhovkin/dash-devextreme) components

### Installation

```bash
$ pip install django-dash-ddx-catalog
```

### Usage

```python
from dash_ddx_catalog.forms import DashDDXForm, DashDDXModelForm

from django import forms

from .models import MyModel


class SimpleForm(DashDDXForm):
    name = forms.CharField(label='Label name', max_length=255)
    ...


class SimpleModelForm(DashDDXModelForm):
    name = forms.CharField(label='Label name', max_length=255)
    ...
    
    class Meta:
        model = MyModel
```

### License

MIT
