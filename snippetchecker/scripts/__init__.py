__all__ = ['initial']
import os
from .initial import initialrun
if not os.path.isfile(os.path.join(os.path.expanduser("~"),".snippetchecker")):
    initial.initialrun()
