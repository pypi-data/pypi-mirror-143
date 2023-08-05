"""
Handles paradigm generation.
"""

import string
from .manager import *
from . import settings

from hfst_optimized_lookup import TransducerFile


def default_paradigm_manager() -> ParadigmManager:
    """
    Returns the ParadigmManager instance that loads layouts and FST from the res
    (resource) directory for the crk/eng language pair (itwêwina).

    Affected by:
      - MORPHODICT_PARADIGM_SIZE_ORDER
    """

    # Directory with paradigm layouts to load
    layout_dir = settings.get_layouts_dir()

    generator = strict_generator()

    if hasattr(settings, "MORPHODICT_PARADIGM_SIZES"):
        return ParadigmManagerWithExplicitSizes(
            layout_dir,
            generator,
            ordered_sizes=settings.MORPHODICT_PARADIGM_SIZES,
        )
    else:
        return ParadigmManager(layout_dir, generator)

def strict_generator():
    path = settings.get_fst_filepath()
    print(path, "pathhhh")
    try:
        return TransducerFile(path)
    except Exception as error:
        print("\\" + str(error).split(":")[0] + "\\")
        if (str(error).split(":")[0] == 'Transducer not found'):
            raise Exception(str(error).split(":")[0] + f' in \"{path}\"')
        else:
            raise Exception(str(error))
