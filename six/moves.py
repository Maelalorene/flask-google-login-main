"""
Provide a minimal `six.moves` module exposing common moved modules used by
google libraries.

This implements:
- `http_client` -> the Python 3 `http.client` module
- `urllib` -> a module-like object with `request`, `parse`, and `error` submodules

The goal is to satisfy imports like `from six.moves import urllib` and
`from six.moves import http_client` without shipping the full `six` package.
"""

import types
import http.client as http_client
import urllib.request as _urllib_request
import urllib.parse as _urllib_parse
import urllib.error as _urllib_error
import builtins

# Build a simple module-like object for `urllib` with commonly used submodules
urllib = types.ModuleType("urllib")
urllib.request = _urllib_request
urllib.parse = _urllib_parse
urllib.error = _urllib_error

# Provide `input` as expected by some libraries (from six.moves import input)
# Map it to the Python 3 built-in input function
input = builtins.input

__all__ = ["http_client", "urllib", "input"]
