import numpy as np

from qm.pb.general_messages_pb2 import (
    Message_LEVEL_ERROR,
    Message_LEVEL_INFO,
    Message_LEVEL_WARNING,
)
from qm.logger import logger, INFO, WARN, ERROR


def fix_object_data_type(obj):
    if isinstance(obj, np.floating):
        return obj.item()
    else:
        return obj


_level_map = {
    Message_LEVEL_ERROR: ERROR,
    Message_LEVEL_WARNING: WARN,
    Message_LEVEL_INFO: INFO,
}


def _set_compiler_options(request, **kwargs):
    request.highLevelProgram.compilerOptions.optimizeMergeCodeExecution = (
        kwargs.get("optimize_merge_code_execution") is not False
    )
    request.highLevelProgram.compilerOptions.optimizeWriteReadCommands = (
        kwargs.get("optimize_read_write_commands") is True
    )
    request.highLevelProgram.compilerOptions.strict = (
        kwargs.get("strict", False) is True
    )

    # handle deprecated skip_optimizations (backwards compatible for future flags)
    skip_optimizations = kwargs.get("skip_optimizations", None)
    if skip_optimizations is None:
        pass
    elif type(skip_optimizations) is tuple:
        optimization_to_skip = []
        for opt in skip_optimizations:
            if type(opt) is str:
                request.highLevelProgram.compilerOptions.skipOptimizations.append(opt)
                optimization_to_skip.append(opt)
        logger.info("Skipping optimizations: " + ",".join(optimization_to_skip))
    else:
        logger.warn("skip_optimizations must be a tuple of strings")

    # handle deprecated extra_optimizations (backwards compatible for future flags)
    extra_optimizations = kwargs.get("extra_optimizations", None)
    if extra_optimizations is None:
        pass
    elif type(extra_optimizations) is tuple:
        optimization_to_add = []
        for opt in extra_optimizations:
            if type(opt) is str:
                request.highLevelProgram.compilerOptions.skipOptimizations.append(
                    "!" + opt
                )
                optimization_to_add.append(opt)
        logger.info("extra optimizations: " + ",".join(optimization_to_add))
    else:
        logger.warn("extra_optimizations must be a tuple of strings")

    try:
        flags_arg = kwargs.get("flags", [])
        flags = [opt for opt in flags_arg if type(opt) is str]
    except TypeError:
        flags = []
    for opt in flags:
        request.highLevelProgram.compilerOptions.flags.append(opt)
    logger.info("Flags: " + ",".join(flags))
