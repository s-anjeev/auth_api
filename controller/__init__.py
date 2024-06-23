# __all__=["user_controller", "product_controller"]

import os
import glob

__all__ = [os.path.basename(f)[:-3] for f in glob.glob(os.path.join(os.path.dirname(__file__), "*.py")) if os.path.isfile(f) and not f.endswith('__init__.py')]

