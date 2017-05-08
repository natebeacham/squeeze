## squeeze

Squeeze is a simple drop-in Django asset pipeliner

### Installation

Add squeeze to your project (and add `'squeeze'` to your INSTALLED_APPS). From there, you can define a `SQUEEZE` object in your project's settings file the defines any static media packages used.

```python
SQUEEZE = {
    'packages': {
        'public': (
            "css/normalize.css",
            "css/foundation.min.css",
            "css/app.sass",
            "js/jquery.js",
            "js/underscore.js",
            "js/backbone.js",
            "js/app.js",
        ),

        'admin': (
            'css/admin.scss',
            'js/admin.js',
        ),
    }
}
```

You will also need to add the following to your urlpatterns:

```python
  url(r'^media/', include('squeeze.urls')),
```

### Usage

To embed a defined package into your template, you can use the included templatetag:

```html
{% load squeeze %}
{% render_package 'public' %}
```
