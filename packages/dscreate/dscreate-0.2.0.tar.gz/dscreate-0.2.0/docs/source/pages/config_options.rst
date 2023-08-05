


Application.log_datefmt : Unicode
    Default: ``'%Y-%m-%d %H:%M:%S'``

    The date format used by logging formatters for %(asctime)s

Application.log_format : Unicode
    Default: ``'[%(name)s]%(highlevel)s %(message)s'``

    The Logging format template

Application.log_level : any of ``0``|``10``|``20``|``30``|``40``|``50``|``'DEBUG'``|``'INFO'``|``'WARN'``|``'ERROR'``|``'CRITICAL'``
    Default: ``30``

    Set the log level by value or name.

Application.show_config : Bool
    Default: ``False``

    Instead of starting the Application, dump configuration to stdout

Application.show_config_json : Bool
    Default: ``False``

    Instead of starting the Application, dump configuration to stdout (as JSON)

DsCreate.app_dir : Unicode
    Default: ``''``

    No description

DsCreate.classes : List
    Default: ``[]``

    No description

DsCreate.config_file : Unicode
    Default: ``''``

    No description

DsCreate.config_file_name : Unicode
    Default: ``'dscreate_config.py'``

    Specify a config file to load.

DsCreate.dsconfig : Unicode
    Default: ``''``

    No description

DsCreate.inline : Bool
    Default: ``False``

    No description

DsCreate.log_datefmt : Unicode
    Default: ``'%Y-%m-%d %H:%M:%S'``

    The date format used by logging formatters for %(asctime)s

DsCreate.log_format : Unicode
    Default: ``'[%(name)s]%(highlevel)s %(message)s'``

    The Logging format template

DsCreate.log_level : Int
    Default: ``50``

    No description

DsCreate.show_config : Bool
    Default: ``False``

    Instead of starting the Application, dump configuration to stdout

DsCreate.show_config_json : Bool
    Default: ``False``

    Instead of starting the Application, dump configuration to stdout (as JSON)

DsCreate.system_config_path : Unicode
    Default: ``''``

    No description

DsPipeline.branches : List
    Default: ``[]``

    No description

DsPipeline.steps : List
    Default: ``[]``

    No description

CollectCurriculum.edit_branch : Unicode
    Default: ``'curriculum'``

    No description

CollectCurriculum.edit_file : Unicode
    Default: ``'index.ipynb'``

    No description

BaseController.branches : List
    Default: ``['curriculum', 'master', 'solution']``

    No description

BaseController.enabled : Bool
    Default: ``False``

    No description

CheckoutController.branches : List
    Default: ``['curriculum', 'master', 'solution']``

    No description

CheckoutController.enabled : Bool
    Default: ``False``

    No description

CheckoutController.printout : Unicode
    Default: ``''``

    No description

CommitController.branches : List
    Default: ``['curriculum', 'master', 'solution']``

    No description

CommitController.commit_msg : Unicode
    Default: ``''``

    No description

CommitController.count : Int
    Default: ``0``

    No description

CommitController.enabled : Bool
    Default: ``False``

    No description

PushController.branches : List
    Default: ``['curriculum', 'master', 'solution']``

    No description

PushController.enabled : Bool
    Default: ``False``

    No description

PushController.remote : Unicode
    Default: ``''``

    No description

CheckoutEditBranch.branches : List
    Default: ``['curriculum', 'master', 'solution']``

    No description

CheckoutEditBranch.enabled : Bool
    Default: ``False``

    No description

BaseConverter.enabled : Bool
    Default: ``True``

    No description

BaseConverter.exporter_class : Type
    Default: ``'nbconvert.exporters.notebook.NotebookExporter'``

    No description

BaseConverter.output : Unicode
    Default: ``'index'``

    No description

BaseConverter.preprocessors : List
    Default: ``[]``

    No description

BaseConverter.solution_dir : Unicode
    Default: ``'/Users/joel/Documents/scripts/dscreate/docs/.solution_files'``

    No description

MasterConverter.enabled : Bool
    Default: ``True``

    No description

MasterConverter.exporter_class : Type
    Default: ``'nbconvert.exporters.notebook.NotebookExporter'``

    No description

MasterConverter.output : Unicode
    Default: ``'index'``

    No description

MasterConverter.preprocessors : List
    Default: ``[<class 'dscreate.pipeline.preprocessors.ClearOutput.ClearOut...``

    No description

MasterConverter.solution_dir : Unicode
    Default: ``'/Users/joel/Documents/scripts/dscreate/docs/.solution_files'``

    No description

ReleaseConverter.enabled : Bool
    Default: ``True``

    No description

ReleaseConverter.exporter_class : Type
    Default: ``'nbconvert.exporters.markdown.MarkdownExporter'``

    No description

ReleaseConverter.notebook_path : Unicode
    Default: ``'index.ipynb'``

    No description

ReleaseConverter.output : Unicode
    Default: ``'README'``

    No description

ReleaseConverter.preprocessors : List
    Default: ``[]``

    No description

ReleaseConverter.solution_dir : Unicode
    Default: ``'/Users/joel/Documents/scripts/dscreate/docs/.solution_files'``

    No description

SolutionConverter.enabled : Bool
    Default: ``True``

    No description

SolutionConverter.exporter_class : Type
    Default: ``'nbconvert.exporters.notebook.NotebookExporter'``

    No description

SolutionConverter.output : Unicode
    Default: ``'index'``

    No description

SolutionConverter.preprocessors : List
    Default: ``[<class 'dscreate.pipeline.preprocessors.ClearOutput.ClearOut...``

    No description

SolutionConverter.solution_dir : Unicode
    Default: ``'/Users/joel/Documents/scripts/dscreate/docs/.solution_files'``

    No description

ReadmeConverter.enabled : Bool
    Default: ``True``

    No description

ReadmeConverter.exporter_class : Type
    Default: ``'nbconvert.exporters.markdown.MarkdownExporter'``

    No description

ReadmeConverter.notebook_path : Unicode
    Default: ``''``

    No description

ReadmeConverter.output : Unicode
    Default: ``'README'``

    No description

ReadmeConverter.preprocessors : List
    Default: ``[]``

    No description

ReadmeConverter.solution_dir : Unicode
    Default: ``'/Users/joel/Documents/scripts/dscreate/docs/.solution_files'``

    No description

SourceConverter.enabled : Bool
    Default: ``True``

    No description

SourceConverter.exporter_class : Type
    Default: ``'nbconvert.exporters.markdown.MarkdownExporter'``

    No description

SourceConverter.notebook_path : Unicode
    Default: ``''``

    No description

SourceConverter.output : Unicode
    Default: ``'README'``

    No description

SourceConverter.preprocessors : List
    Default: ``[]``

    No description

SourceConverter.solution_dir : Unicode
    Default: ``'/Users/joel/Documents/scripts/dscreate/docs/.solution_files'``

    No description

MergeConverter.enabled : Bool
    Default: ``True``

    No description

MergeConverter.exporter_class : Type
    Default: ``'nbconvert.exporters.notebook.NotebookExporter'``

    No description

MergeConverter.old : Bool
    Default: ``False``

    No description

MergeConverter.output : Unicode
    Default: ``'curriculum'``

    No description

MergeConverter.preprocessors : List
    Default: ``[<class 'dscreate.pipeline.preprocessors.SortCells.SortCells'>]``

    No description

MergeConverter.solution_dir : Unicode
    Default: ``'/Users/joel/Documents/scripts/dscreate/docs/.solution_files'``

    No description

NbConvertBase.default_language : Unicode
    Default: ``'ipython'``

    Deprecated default highlight language as of 5.0, please use language_info metadata instead

NbConvertBase.display_data_priority : List
    Default: ``['text/html', 'application/pdf', 'text/latex', 'image/svg+xml...``


    An ordered list of preferred output type, the first
    encountered will usually be used when converting discarding
    the others.


Preprocessor.default_language : Unicode
    Default: ``'ipython'``

    Deprecated default highlight language as of 5.0, please use language_info metadata instead

Preprocessor.display_data_priority : List
    Default: ``['text/html', 'application/pdf', 'text/latex', 'image/svg+xml...``


    An ordered list of preferred output type, the first
    encountered will usually be used when converting discarding
    the others.


Preprocessor.enabled : Bool
    Default: ``False``

    No description

DsCreatePreprocessor.default_language : Unicode
    Default: ``'ipython'``

    Deprecated default highlight language as of 5.0, please use language_info metadata instead

DsCreatePreprocessor.display_data_priority : List
    Default: ``['text/html', 'application/pdf', 'text/latex', 'image/svg+xml...``


    An ordered list of preferred output type, the first
    encountered will usually be used when converting discarding
    the others.


DsCreatePreprocessor.enabled : Bool
    Default: ``True``

    Whether to use this preprocessor when running dscreate

AddCellIndex.default_language : Unicode
    Default: ``'ipython'``

    Deprecated default highlight language as of 5.0, please use language_info metadata instead

AddCellIndex.display_data_priority : List
    Default: ``['text/html', 'application/pdf', 'text/latex', 'image/svg+xml...``


    An ordered list of preferred output type, the first
    encountered will usually be used when converting discarding
    the others.


AddCellIndex.enabled : Bool
    Default: ``True``

    Whether to use this preprocessor when running dscreate

AddCellIndex.solution_tags : Set
    Default: ``{'#==SOLUTION==', '#__SOLUTION__', '==SOLUTION==', '__SOLUTIO...``

    Tags indicating which cells are to be removed

RemoveSolutionCells.code_tags : Set
    Default: ``{'#==SOLUTION==', '#__SOLUTION__'}``

    Tags indicating which cells are to be removed

RemoveSolutionCells.default_language : Unicode
    Default: ``'ipython'``

    Deprecated default highlight language as of 5.0, please use language_info metadata instead

RemoveSolutionCells.display_data_priority : List
    Default: ``['text/html', 'application/pdf', 'text/latex', 'image/svg+xml...``


    An ordered list of preferred output type, the first
    encountered will usually be used when converting discarding
    the others.


RemoveSolutionCells.enabled : Bool
    Default: ``True``

    Whether to use this preprocessor when running dscreate

RemoveSolutionCells.markdown_tags : Set
    Default: ``{'==SOLUTION==', '__SOLUTION__'}``

    No description

RemoveLessonCells.default_language : Unicode
    Default: ``'ipython'``

    Deprecated default highlight language as of 5.0, please use language_info metadata instead

RemoveLessonCells.display_data_priority : List
    Default: ``['text/html', 'application/pdf', 'text/latex', 'image/svg+xml...``


    An ordered list of preferred output type, the first
    encountered will usually be used when converting discarding
    the others.


RemoveLessonCells.enabled : Bool
    Default: ``True``

    Whether to use this preprocessor when running dscreate

RemoveLessonCells.solution_tags : Set
    Default: ``{'#==SOLUTION==', '#__SOLUTION__', '==SOLUTION==', '__SOLUTIO...``

    Tags indicating which cells are to be removed

SortCells.default_language : Unicode
    Default: ``'ipython'``

    Deprecated default highlight language as of 5.0, please use language_info metadata instead

SortCells.display_data_priority : List
    Default: ``['text/html', 'application/pdf', 'text/latex', 'image/svg+xml...``


    An ordered list of preferred output type, the first
    encountered will usually be used when converting discarding
    the others.


SortCells.enabled : Bool
    Default: ``True``

    Whether to use this preprocessor when running dscreate

ClearOutputPreprocessor.default_language : Unicode
    Default: ``'ipython'``

    Deprecated default highlight language as of 5.0, please use language_info metadata instead

ClearOutputPreprocessor.display_data_priority : List
    Default: ``['text/html', 'application/pdf', 'text/latex', 'image/svg+xml...``


    An ordered list of preferred output type, the first
    encountered will usually be used when converting discarding
    the others.


ClearOutputPreprocessor.enabled : Bool
    Default: ``False``

    No description

ClearOutputPreprocessor.remove_metadata_fields : Set
    Default: ``{'collapsed', 'scrolled'}``

    No description

ClearOutput.default_language : Unicode
    Default: ``'ipython'``

    Deprecated default highlight language as of 5.0, please use language_info metadata instead

ClearOutput.display_data_priority : List
    Default: ``['text/html', 'application/pdf', 'text/latex', 'image/svg+xml...``


    An ordered list of preferred output type, the first
    encountered will usually be used when converting discarding
    the others.


ClearOutput.enabled : Bool
    Default: ``True``

    Whether to use this preprocessor when running dscreate

ClearOutput.remove_metadata_fields : Set
    Default: ``{'collapsed', 'scrolled'}``

    No description

NotebookClient.allow_error_names : List
    Default: ``[]``


    List of error names which won't stop the execution. Use this if the
    ``allow_errors`` option it too general and you want to allow only
    specific kinds of errors.


NotebookClient.allow_errors : Bool
    Default: ``False``


    If ``False`` (default), when a cell raises an error the
    execution is stopped and a `CellExecutionError`
    is raised, except if the error name is in
    ``allow_error_names``.
    If ``True``, execution errors are ignored and the execution
    is continued until the end of the notebook. Output from
    exceptions is included in the cell output in both cases.


NotebookClient.display_data_priority : List
    Default: ``['text/html', 'application/pdf', 'text/latex', 'image/svg+xml...``


    An ordered list of preferred output type, the first
    encountered will usually be used when converting discarding
    the others.


NotebookClient.extra_arguments : List
    Default: ``[]``

    No description

NotebookClient.force_raise_errors : Bool
    Default: ``False``


    If False (default), errors from executing the notebook can be
    allowed with a ``raises-exception`` tag on a single cell, or the
    ``allow_errors`` or ``allow_error_names`` configurable options for
    all cells. An allowed error will be recorded in notebook output, and
    execution will continue. If an error occurs when it is not
    explicitly allowed, a `CellExecutionError` will be raised.
    If True, `CellExecutionError` will be raised for any error that occurs
    while executing the notebook. This overrides the ``allow_errors``
    and ``allow_error_names`` options and the ``raises-exception`` cell
    tag.


NotebookClient.interrupt_on_timeout : Bool
    Default: ``False``


    If execution of a cell times out, interrupt the kernel and
    continue executing other cells rather than throwing an error and
    stopping.


NotebookClient.iopub_timeout : Int
    Default: ``4``


    The time to wait (in seconds) for IOPub output. This generally
    doesn't need to be set, but on some slow networks (such as CI
    systems) the default timeout might not be long enough to get all
    messages.


NotebookClient.ipython_hist_file : Unicode
    Default: ``':memory:'``

    Path to file to use for SQLite history database for an IPython kernel.

            The specific value ``:memory:`` (including the colon
            at both end but not the back ticks), avoids creating a history file. Otherwise, IPython
            will create a history file for each kernel.

            When running kernels simultaneously (e.g. via multiprocessing) saving history a single
            SQLite file can result in database errors, so using ``:memory:`` is recommended in
            non-interactive contexts.


NotebookClient.kernel_manager_class : Type
    Default: ``'builtins.object'``

    The kernel manager class to use.

NotebookClient.kernel_name : Unicode
    Default: ``''``


    Name of kernel to use to execute the cells.
    If not set, use the kernel_spec embedded in the notebook.


NotebookClient.raise_on_iopub_timeout : Bool
    Default: ``False``


    If ``False`` (default), then the kernel will continue waiting for
    iopub messages until it receives a kernel idle message, or until a
    timeout occurs, at which point the currently executing cell will be
    skipped. If ``True``, then an error will be raised after the first
    timeout. This option generally does not need to be used, but may be
    useful in contexts where there is the possibility of executing
    notebooks with memory-consuming infinite loops.


NotebookClient.record_timing : Bool
    Default: ``True``


    If ``True`` (default), then the execution timings of each cell will
    be stored in the metadata of the notebook.


NotebookClient.shell_timeout_interval : Int
    Default: ``5``


    The time to wait (in seconds) for Shell output before retrying.
    This generally doesn't need to be set, but if one needs to check
    for dead kernels at a faster rate this can help.


NotebookClient.shutdown_kernel : any of ``'graceful'``|``'immediate'``
    Default: ``'graceful'``


    If ``graceful`` (default), then the kernel is given time to clean
    up after executing all cells, e.g., to execute its ``atexit`` hooks.
    If ``immediate``, then the kernel is signaled to immediately
    terminate.


NotebookClient.startup_timeout : Int
    Default: ``60``


    The time to wait (in seconds) for the kernel to start.
    If kernel startup takes longer, a RuntimeError is
    raised.


NotebookClient.store_widget_state : Bool
    Default: ``True``


    If ``True`` (default), then the state of the Jupyter widgets created
    at the kernel will be stored in the metadata of the notebook.


NotebookClient.timeout : Int
    Default: ``None``


    The time to wait (in seconds) for output from executions.
    If a cell execution takes longer, a TimeoutError is raised.

    ``None`` or ``-1`` will disable the timeout. If ``timeout_func`` is set,
    it overrides ``timeout``.


NotebookClient.timeout_func : Any
    Default: ``None``


    A callable which, when given the cell source as input,
    returns the time to wait (in seconds) for output from cell
    executions. If a cell execution takes longer, a TimeoutError
    is raised.

    Returning ``None`` or ``-1`` will disable the timeout for the cell.
    Not setting ``timeout_func`` will cause the client to
    default to using the ``timeout`` trait for all cells. The
    ``timeout_func`` trait overrides ``timeout`` if it is not ``None``.


ExecutePreprocessor.allow_error_names : List
    Default: ``[]``


    List of error names which won't stop the execution. Use this if the
    ``allow_errors`` option it too general and you want to allow only
    specific kinds of errors.


ExecutePreprocessor.allow_errors : Bool
    Default: ``False``


    If ``False`` (default), when a cell raises an error the
    execution is stopped and a `CellExecutionError`
    is raised, except if the error name is in
    ``allow_error_names``.
    If ``True``, execution errors are ignored and the execution
    is continued until the end of the notebook. Output from
    exceptions is included in the cell output in both cases.


ExecutePreprocessor.default_language : Unicode
    Default: ``'ipython'``

    Deprecated default highlight language as of 5.0, please use language_info metadata instead

ExecutePreprocessor.display_data_priority : List
    Default: ``['text/html', 'application/pdf', 'text/latex', 'image/svg+xml...``


    An ordered list of preferred output type, the first
    encountered will usually be used when converting discarding
    the others.


ExecutePreprocessor.enabled : Bool
    Default: ``False``

    No description

ExecutePreprocessor.extra_arguments : List
    Default: ``[]``

    No description

ExecutePreprocessor.force_raise_errors : Bool
    Default: ``False``


    If False (default), errors from executing the notebook can be
    allowed with a ``raises-exception`` tag on a single cell, or the
    ``allow_errors`` or ``allow_error_names`` configurable options for
    all cells. An allowed error will be recorded in notebook output, and
    execution will continue. If an error occurs when it is not
    explicitly allowed, a `CellExecutionError` will be raised.
    If True, `CellExecutionError` will be raised for any error that occurs
    while executing the notebook. This overrides the ``allow_errors``
    and ``allow_error_names`` options and the ``raises-exception`` cell
    tag.


ExecutePreprocessor.interrupt_on_timeout : Bool
    Default: ``False``


    If execution of a cell times out, interrupt the kernel and
    continue executing other cells rather than throwing an error and
    stopping.


ExecutePreprocessor.iopub_timeout : Int
    Default: ``4``


    The time to wait (in seconds) for IOPub output. This generally
    doesn't need to be set, but on some slow networks (such as CI
    systems) the default timeout might not be long enough to get all
    messages.


ExecutePreprocessor.ipython_hist_file : Unicode
    Default: ``':memory:'``

    Path to file to use for SQLite history database for an IPython kernel.

            The specific value ``:memory:`` (including the colon
            at both end but not the back ticks), avoids creating a history file. Otherwise, IPython
            will create a history file for each kernel.

            When running kernels simultaneously (e.g. via multiprocessing) saving history a single
            SQLite file can result in database errors, so using ``:memory:`` is recommended in
            non-interactive contexts.


ExecutePreprocessor.kernel_manager_class : Type
    Default: ``'builtins.object'``

    The kernel manager class to use.

ExecutePreprocessor.kernel_name : Unicode
    Default: ``''``


    Name of kernel to use to execute the cells.
    If not set, use the kernel_spec embedded in the notebook.


ExecutePreprocessor.raise_on_iopub_timeout : Bool
    Default: ``False``


    If ``False`` (default), then the kernel will continue waiting for
    iopub messages until it receives a kernel idle message, or until a
    timeout occurs, at which point the currently executing cell will be
    skipped. If ``True``, then an error will be raised after the first
    timeout. This option generally does not need to be used, but may be
    useful in contexts where there is the possibility of executing
    notebooks with memory-consuming infinite loops.


ExecutePreprocessor.record_timing : Bool
    Default: ``True``


    If ``True`` (default), then the execution timings of each cell will
    be stored in the metadata of the notebook.


ExecutePreprocessor.shell_timeout_interval : Int
    Default: ``5``


    The time to wait (in seconds) for Shell output before retrying.
    This generally doesn't need to be set, but if one needs to check
    for dead kernels at a faster rate this can help.


ExecutePreprocessor.shutdown_kernel : any of ``'graceful'``|``'immediate'``
    Default: ``'graceful'``


    If ``graceful`` (default), then the kernel is given time to clean
    up after executing all cells, e.g., to execute its ``atexit`` hooks.
    If ``immediate``, then the kernel is signaled to immediately
    terminate.


ExecutePreprocessor.startup_timeout : Int
    Default: ``60``


    The time to wait (in seconds) for the kernel to start.
    If kernel startup takes longer, a RuntimeError is
    raised.


ExecutePreprocessor.store_widget_state : Bool
    Default: ``True``


    If ``True`` (default), then the state of the Jupyter widgets created
    at the kernel will be stored in the metadata of the notebook.


ExecutePreprocessor.timeout : Int
    Default: ``None``


    The time to wait (in seconds) for output from executions.
    If a cell execution takes longer, a TimeoutError is raised.

    ``None`` or ``-1`` will disable the timeout. If ``timeout_func`` is set,
    it overrides ``timeout``.


ExecutePreprocessor.timeout_func : Any
    Default: ``None``


    A callable which, when given the cell source as input,
    returns the time to wait (in seconds) for output from cell
    executions. If a cell execution takes longer, a TimeoutError
    is raised.

    Returning ``None`` or ``-1`` will disable the timeout for the cell.
    Not setting ``timeout_func`` will cause the client to
    default to using the ``timeout`` trait for all cells. The
    ``timeout_func`` trait overrides ``timeout`` if it is not ``None``.


ExecuteCells.allow_error_names : List
    Default: ``[]``


    List of error names which won't stop the execution. Use this if the
    ``allow_errors`` option it too general and you want to allow only
    specific kinds of errors.


ExecuteCells.allow_errors : Bool
    Default: ``False``


    If ``False`` (default), when a cell raises an error the
    execution is stopped and a `CellExecutionError`
    is raised, except if the error name is in
    ``allow_error_names``.
    If ``True``, execution errors are ignored and the execution
    is continued until the end of the notebook. Output from
    exceptions is included in the cell output in both cases.


ExecuteCells.default_language : Unicode
    Default: ``'ipython'``

    Deprecated default highlight language as of 5.0, please use language_info metadata instead

ExecuteCells.display_data_priority : List
    Default: ``['text/html', 'application/pdf', 'text/latex', 'image/svg+xml...``


    An ordered list of preferred output type, the first
    encountered will usually be used when converting discarding
    the others.


ExecuteCells.enabled : Bool
    Default: ``True``

    Whether to use this preprocessor when running dscreate

ExecuteCells.extra_arguments : List
    Default: ``[]``

    No description

ExecuteCells.force_raise_errors : Bool
    Default: ``False``


    If False (default), errors from executing the notebook can be
    allowed with a ``raises-exception`` tag on a single cell, or the
    ``allow_errors`` or ``allow_error_names`` configurable options for
    all cells. An allowed error will be recorded in notebook output, and
    execution will continue. If an error occurs when it is not
    explicitly allowed, a `CellExecutionError` will be raised.
    If True, `CellExecutionError` will be raised for any error that occurs
    while executing the notebook. This overrides the ``allow_errors``
    and ``allow_error_names`` options and the ``raises-exception`` cell
    tag.


ExecuteCells.interrupt_on_timeout : Bool
    Default: ``False``


    If execution of a cell times out, interrupt the kernel and
    continue executing other cells rather than throwing an error and
    stopping.


ExecuteCells.iopub_timeout : Int
    Default: ``4``


    The time to wait (in seconds) for IOPub output. This generally
    doesn't need to be set, but on some slow networks (such as CI
    systems) the default timeout might not be long enough to get all
    messages.


ExecuteCells.ipython_hist_file : Unicode
    Default: ``':memory:'``

    Path to file to use for SQLite history database for an IPython kernel.

            The specific value ``:memory:`` (including the colon
            at both end but not the back ticks), avoids creating a history file. Otherwise, IPython
            will create a history file for each kernel.

            When running kernels simultaneously (e.g. via multiprocessing) saving history a single
            SQLite file can result in database errors, so using ``:memory:`` is recommended in
            non-interactive contexts.


ExecuteCells.kernel_manager_class : Type
    Default: ``'builtins.object'``

    The kernel manager class to use.

ExecuteCells.kernel_name : Unicode
    Default: ``''``


    Name of kernel to use to execute the cells.
    If not set, use the kernel_spec embedded in the notebook.


ExecuteCells.raise_on_iopub_timeout : Bool
    Default: ``False``


    If ``False`` (default), then the kernel will continue waiting for
    iopub messages until it receives a kernel idle message, or until a
    timeout occurs, at which point the currently executing cell will be
    skipped. If ``True``, then an error will be raised after the first
    timeout. This option generally does not need to be used, but may be
    useful in contexts where there is the possibility of executing
    notebooks with memory-consuming infinite loops.


ExecuteCells.record_timing : Bool
    Default: ``True``


    If ``True`` (default), then the execution timings of each cell will
    be stored in the metadata of the notebook.


ExecuteCells.shell_timeout_interval : Int
    Default: ``5``


    The time to wait (in seconds) for Shell output before retrying.
    This generally doesn't need to be set, but if one needs to check
    for dead kernels at a faster rate this can help.


ExecuteCells.shutdown_kernel : any of ``'graceful'``|``'immediate'``
    Default: ``'graceful'``


    If ``graceful`` (default), then the kernel is given time to clean
    up after executing all cells, e.g., to execute its ``atexit`` hooks.
    If ``immediate``, then the kernel is signaled to immediately
    terminate.


ExecuteCells.startup_timeout : Int
    Default: ``60``


    The time to wait (in seconds) for the kernel to start.
    If kernel startup takes longer, a RuntimeError is
    raised.


ExecuteCells.store_widget_state : Bool
    Default: ``True``


    If ``True`` (default), then the state of the Jupyter widgets created
    at the kernel will be stored in the metadata of the notebook.


ExecuteCells.timeout : Int
    Default: ``None``


    The time to wait (in seconds) for output from executions.
    If a cell execution takes longer, a TimeoutError is raised.

    ``None`` or ``-1`` will disable the timeout. If ``timeout_func`` is set,
    it overrides ``timeout``.


ExecuteCells.timeout_func : Any
    Default: ``None``


    A callable which, when given the cell source as input,
    returns the time to wait (in seconds) for output from cell
    executions. If a cell execution takes longer, a TimeoutError
    is raised.

    Returning ``None`` or ``-1`` will disable the timeout for the cell.
    Not setting ``timeout_func`` will cause the client to
    default to using the ``timeout`` trait for all cells. The
    ``timeout_func`` trait overrides ``timeout`` if it is not ``None``.


AddLanguage.default_language : Unicode
    Default: ``'ipython'``

    Deprecated default highlight language as of 5.0, please use language_info metadata instead

AddLanguage.display_data_priority : List
    Default: ``['text/html', 'application/pdf', 'text/latex', 'image/svg+xml...``


    An ordered list of preferred output type, the first
    encountered will usually be used when converting discarding
    the others.


AddLanguage.enabled : Bool
    Default: ``True``

    Whether to use this preprocessor when running dscreate

AddLanguage.language : Unicode
    Default: ``'python'``

    No description
