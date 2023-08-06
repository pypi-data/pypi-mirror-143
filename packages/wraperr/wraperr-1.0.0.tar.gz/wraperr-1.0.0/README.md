# WrapErr

The goal of WrapErr is to avoid contaminating main logic with try-catch blocks and the exception handling logic.

Without WrapErr, you have something like this:

```python
try:
    // do something
except Exception as e:
    // exception handling logic
```

With WrapErr, you would write something more like this:

```python
def error_handler(e: Exception):
    // exception handling logic

@wrap_error(error_handler)
def foo(*args, **kwargs):
    // do something
```

You can reuse the same error handling logic across multiple functions and methods:

```python
def error_handler(e: Exception):
    // exception handling logic

@wrap_error(error_handler)
def foo(*args, **kwargs):
    // do something

@wrap_error(error_handler):
def bar(*args, **kwargs):
    // do something else
```

You can also only handle exceptions of a specific type:

```python
def value_error_handler(e: ValueError):
    // exception handling logic

@wrap_error(error_handler, ValueError)
def foo(*args, **kwargs):
    // do something
```

And you can combine different error handlers that handle different exceptions:

```python
def value_error_handler(e: ValueError):
    // exception handling logic

def attribute_error_handler(e: AttributeError):
    // more exception handling logic

@wrap_error(value_error_handler, ValueError)
@wrap_error(attribute_error_handler, AttributeError)
def foo(*args, **kwargs):
    // do something
```
