import os, glob
from toaster.plugin import Plugin


class ConverterProvider(object):
    __metaclass__ = Plugin


# specify that we want to import all of the modules in this package
__all__ = [ os.path.basename(f)[:-3] for f in glob.glob(os.path.dirname(__file__) + '/*.py')]