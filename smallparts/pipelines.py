# -*- coding: utf-8 -*-

"""

smallparts.pipelines

Command line interface (subprocess) pipelines wrapper

"""


import shlex
import subprocess
import warnings

from smallparts import namespaces


# "Proxy" subprocess constants

DEVNULL = subprocess.DEVNULL
PIPE = subprocess.PIPE
STDOUT = subprocess.STDOUT


#
# Exceptions
#


class IllegalStateException(Exception):

    """Raised when a ProcessPipeline is run twice"""

    ...


#
# Classes
#


class _AbstractPipeline():

    """Wrapper for a subprocess.Popen() object
    also storing the result

    Supports keyword arguments for the subprocess.Popen() objects as defined in
    https://docs.python.org/3.6/library/subprocess.html#popen-constructor
    with the exception of the deprecated preexec_fn argument.
    Default values are the same as documented there, except stderr and stdout
    (both defaulting to subprocess.PIPE).

    Additional keyword arguments:
        run_immediately (default: False)
        intermediate_stderr (default: None)
        input (default: None)
        timeout (default: None)
    """

    defaults = dict(
        bufsize=-1,
        executable=None,
        stdin=None,
        stdout=PIPE,
        stderr=PIPE,
        close_fds=True,
        shell=False,
        cwd=None,
        env=None,
        universal_newlines=False,
        startupinfo=None,
        creationflags=0,
        restore_signals=True,
        start_new_session=False,
        pass_fds=(),
        encoding=None,
        errors=None)
    states = namespaces.Namespace(
        ready=0,
        running=1,
        finished=2)
    supported_intermediate_stderr = (None, DEVNULL, STDOUT)

    def __init__(self, *commands, **kwargs):
        """Prepare subprocess(es)"""
        # Store arguments for the .repeat() method
        self.__repeatable = namespaces.Namespace(
            commands=commands,
            kwargs=kwargs.copy())
        # Build the actual commands list from the provided
        # (non-keyword) arguments
        self.commands = []
        for single_command in commands:
            if isinstance(single_command, str):
                appendable_command = shlex.split(single_command)
            else:
                try:
                    appendable_command = list(single_command)
                except TypeError as type_error:
                    raise ValueError(
                        'Invalid command: {0!r}'.format(
                            single_command)) from type_error
                #
            #
            if appendable_command:
                self.commands.append(appendable_command)
            #
        #
        if not self.commands:
            raise ValueError('Please provide at least one command.')
        #
        check = kwargs.pop('check', False)
        execute_immediately = kwargs.pop('execute_immediately', True)
        input_ = kwargs.pop('input', None)
        intermediate_stderr = kwargs.pop('intermediate_stderr', None)
        if intermediate_stderr not in self.supported_intermediate_stderr:
            warnings.warn(
                'Supported values for intermediate_stderr:'
                ' None, DEVNULL or STDOUT. {0!r} has been ignored and'
                ' substituted by None.'.format(intermediate_stderr))
            intermediate_stderr = None
        #
        timeout = kwargs.pop('timeout', None)
        self.call_arguments = namespaces.Namespace(
            check=check,
            input=input_,
            intermediate_stderr=intermediate_stderr,
            timeout=timeout)
        #
        if input_:
            kwargs['stdin'] = PIPE
        else:
            kwargs['stdin'] = None
        #
        self.current_state = self.states.ready
        self.process_arguments = dict(self.defaults)
        self.process_arguments.update(kwargs)
        self.result = None
        if execute_immediately:
            self.execute()
        #

    def repeat(self):
        """Create an instance with the same parameters as the current one"""
        return self.__class__(*self.__repeatable.commands,
                              **self.__repeatable.kwargs)

    def _execution_implementation(self):
        """Override this method in child classes with the implementation
        of the pipeline call: Start the subprocess(es) and set the result
        """
        raise NotImplementedError

    def execute(self, **kwargs):
        """Check if self.state is ready, set self.state to running
        or raise an exception.
        Update self.call_arguments from the keyword arguments
        check, input, and timeout (each if provided)
        Execute the concrete implementation of
        """
        if self.current_state != self.states.ready:
            raise IllegalStateException('Please create a new instance'
                                        ' using the .repeat() method!')
        #
        self.current_state = self.states.running
        for item in ('check', 'input', 'timeout'):
            try:
                self.call_arguments[item] = kwargs[item]
            except KeyError:
                continue
            #
        #
        self._execution_implementation()

    @classmethod
    def run(cls, *commands, **kwargs):
        """Create an instance, run it immediately and return its result"""
        kwargs['execute_immediately'] = True
        pipeline = cls(*commands, **kwargs)
        return pipeline.result


class ProcessChain(_AbstractPipeline):

    """Pseudo pipeline using sequential subprocesses with subprocess.run()
    """

    def __init__(self, *commands, **kwargs):
        """Initialize the super class"""
        self.all_results = []
        super().__init__(*commands, **kwargs)

    def _execution_implementation(self):
        """Start the subprocess(es) and set the result"""
        self.all_results.clear()
        last_command_index = len(self.commands) - 1
        for current_index, current_command in enumerate(self.commands):
            current_arguments = namespaces.Namespace(self.process_arguments)
            if current_index > 0:
                current_input = self.all_results[current_index - 1].stdout
            else:
                current_input = self.call_arguments.input
            #
            if current_index < last_command_index:
                current_arguments.stdout = PIPE
                current_arguments.stderr = \
                    self.call_arguments.intermediate_stderr
            #
            self.all_results.append(
                subprocess.run(
                    current_command,
                    input=current_input,
                    check=self.call_arguments.check,
                    timeout=self.call_arguments.timeout,
                    bufsize=current_arguments.bufsize,
                    executable=current_arguments.executable,
                    stdout=current_arguments.stdout,
                    stderr=current_arguments.stderr,
                    close_fds=current_arguments.close_fds,
                    shell=current_arguments.shell,
                    cwd=current_arguments.cwd,
                    env=current_arguments.env,
                    universal_newlines=current_arguments.universal_newlines,
                    startupinfo=current_arguments.startupinfo,
                    creationflags=current_arguments.creationflags,
                    restore_signals=current_arguments.restore_signals,
                    start_new_session=current_arguments.start_new_session,
                    pass_fds=current_arguments.pass_fds,
                    encoding=current_arguments.encoding,
                    errors=current_arguments.errors))
            #
        #
        self.current_state = self.states.finished
        self.result = self.all_results[last_command_index]


class ProcessPipeline(_AbstractPipeline):

    """Pipeline using parallel subprocesses as described in
    https://docs.python.org/3/library/subprocess.html#replacing-shell-pipeline
    """

    def _execution_implementation(self):
        """Start the subprocess(es) and set the result"""
        processes = []
        last_command_index = len(self.commands) - 1
        if last_command_index > 0:
            # We communicate() only with the last process in the pipeline.
            # If there is more than one process, input is ignored,
            # and a warning is issued.
            if self.call_arguments.input is not None:
                warnings.warn(
                    'Input {0.call_arguments.input!r} has been ignored.'
                    ' Use the ProcessChain class to avoid this.'.format(self))
            self.call_arguments.input = None
            self.process_arguments['stdin'] = None
        #
        for current_index, current_command in enumerate(self.commands):
            current_arguments = namespaces.Namespace(self.process_arguments)
            if current_index > 0:
                current_arguments.stdin = processes[current_index - 1].stdout
            #
            if current_index < last_command_index:
                current_arguments.stdout = PIPE
                current_arguments.stderr = \
                    self.call_arguments.intermediate_stderr
            #
            try:
                current_process = subprocess.Popen(
                    current_command,
                    bufsize=current_arguments.bufsize,
                    executable=current_arguments.executable,
                    stdin=current_arguments.stdin,
                    stdout=current_arguments.stdout,
                    stderr=current_arguments.stderr,
                    close_fds=current_arguments.close_fds,
                    shell=current_arguments.shell,
                    cwd=current_arguments.cwd,
                    env=current_arguments.env,
                    universal_newlines=current_arguments.universal_newlines,
                    startupinfo=current_arguments.startupinfo,
                    creationflags=current_arguments.creationflags,
                    restore_signals=current_arguments.restore_signals,
                    start_new_session=current_arguments.start_new_session,
                    pass_fds=current_arguments.pass_fds,
                    encoding=current_arguments.encoding,
                    errors=current_arguments.errors)
            except (OSError, ValueError):
                self.current_state = self.states.finished
                raise
            #
            processes.append(current_process)
        #
        # Close stdout to allow processes to receive SIGPIPE.
        for current_index in range(last_command_index):
            processes[current_index].stdout.close()
        #
        # Communicate with the last process in the pipeline.
        # Mimick subprocess.run() behaviour as in
        # https://github.com/python/cpython/blob/3.6/Lib/subprocess.py#L424
        last_process = processes[last_command_index]
        try:
            stdout, stderr = last_process.communicate(
                input=self.call_arguments.input,
                timeout=self.call_arguments.timeout)
        except subprocess.TimeoutExpired as timeout_expired:
            last_process.kill()
            stdout, stderr = last_process.communicate()
            raise subprocess.TimeoutExpired(
                last_process.args,
                self.call_arguments.timeout,
                output=stdout,
                stderr=stderr) from timeout_expired
        #
        returncode = last_process.poll()
        if self.call_arguments.check and returncode:
            raise subprocess.CalledProcessError(
                returncode,
                last_process.args,
                output=stdout,
                stderr=stderr)
        #
        self.result = subprocess.CompletedProcess(
            last_process.args,
            returncode,
            stdout=stdout,
            stderr=stderr)
        # processes cleanup; avoid ResourceWarnings
        for current_index in range(last_command_index):
            processes[current_index].wait()
        #
        self.current_state = self.states.finished


# vim:fileencoding=utf-8 autoindent ts=4 sw=4 sts=4 expandtab:
