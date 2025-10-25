"""
Local shim that attempts to delegate to the real `six` installed in site-packages.

Some environments import packages from the project root first. If a small local
shim was previously created (or accidentally exists), this module will try to
load the system `six` implementation from site-packages and copy its public
attributes into this module's namespace so libraries like `google-auth` that
expect `six.add_metaclass` and `six.moves` will work.

If the real `six` cannot be found, the module still exposes a minimal
`moves` submodule (see `moves.py`) that provides `http_client` so code doing
`from six.moves import http_client` can still work.
"""

import importlib.machinery
import importlib.util
import os
import site

_real_six = None
# Look for a system-installed six (six.py) in site-packages paths
for p in site.getsitepackages() + [site.getusersitepackages()]:
	candidate = os.path.join(p, "six.py")
	if os.path.exists(candidate):
		loader = importlib.machinery.SourceFileLoader("_real_six", candidate)
		spec = importlib.util.spec_from_loader(loader.name, loader)
		module = importlib.util.module_from_spec(spec)
		loader.exec_module(module)
		_real_six = module
		break

if _real_six is not None:
	# copy public attributes from the real six into this module
	for name in dir(_real_six):
		if not name.startswith("__"):
			globals()[name] = getattr(_real_six, name)

# Ensure the local moves submodule is importable as `six.moves`
from . import moves  # noqa: E402

__all__ = ["moves"]
