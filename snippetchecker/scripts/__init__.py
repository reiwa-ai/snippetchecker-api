__all__ = ['initial']
import os
import initial
if not os.path.isfile(os.path.join(os.path.expanduser("~"),".snippetchecker")):
    initial.initialrun()
