# 🚀 Simpel Numerators

Simpel Numerators track autonumber style inner_id for model record
This repository contains a [Numerator](https://gitlab.com/simpel-projects/simpel-numerators) model utils to create nice formatted Inner ID.

## Installation

```shell
pip install simpel-numerators

```

## Usage

```python

from django.db import models
from simpel_numerators.models import NumeratorMixin

class Product(NumeratorMixin):
    doc_prefix = 'PD'
    name = models.CharField(max_length=100)

```

## Usage with Polymorphic

install django-polymorphic

```shell

pip install django-polymorphic

```

### Using Parent Model doc_prefix

```python
from django.db import models
from polymorphic.models import PolymorphicModel
from simpel_numerators.models import NumeratorMixin, NumeratorReset

class Product(NumeratorMixin):
    doc_prefix = 'PD'
    parent_prefix = True
    parent_model = 'Parent2'
    name = models.CharField(max_length=100)

class Inventory(Product):
    pass

class Asset(Product)
    pass
```

### Using Child Model doc prefix

```python

class Product(NumeratorMixin):
    name = models.CharField(max_length=100)

class Inventory(Product):
    doc_prefix = 'INV'

class Asset(Product)
    doc_prefix = 'AST'

```
