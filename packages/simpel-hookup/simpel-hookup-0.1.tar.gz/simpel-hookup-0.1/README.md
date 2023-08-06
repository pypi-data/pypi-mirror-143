# 🚀 Simpel Hookup

Simpel function hook for Django.
Install :

```shell

pip install simpel-hookup

```

Simpel hookup secara otomatis akan mencari `hooks.py` di dalam setiap aplikasi Django yang terinstall dalam project.

## Registrasi hooks

```python
# app/hooks.py

import simpel_hookup as hookup

@hookup.register("PROCESS_TEXT_HOOKS", order=1)
def process_text_replace_space(text):
    text = text.replace(" ", "-")
    print(text)
    return text

@hookup.register("PROCESS_TEXT_HOOKS", order=2)
def process_text_replace_dash(text):
    text = text.replace("-", "_")
    print(text)
    return text

```

## Memanggil hook

```python

# app/views.py
from django.http.response import HttpResponse
import simpel_hookup as hookup

def index(request):
    text = "Lorem ipsum dolor sit amet"

    hook_funcs = hookup.get_hooks('PROCESS_TEXT_HOOKS')
    for func in hook_funcs:
        text = func(text)

    return HttpResponse(text)

```
