# -*- coding: utf-8 -*-

"""

smallparts.cli

Command line interface (subprocess) wrapper

"""


import shlex
import subprocess

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


class ProcessPipeline():

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

    # States
    states = namespaces.Namespace(
        ready=0,
        running=1,
        finished=2)
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

    def __init__(self, *commands, **kwargs):
        """Prepare subprocess(es)"""
        # Store arguments for the .repeat() method
        self.__commands = []
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
                self.__commands.append(appendable_command)
            #
        #
        if not self.__commands:
            raise ValueError('Please provide at least one command.')
        #
        self.__kwargs = kwargs
        self.__repeatable = namespaces.Namespace(
            commands=commands,
            kwargs=kwargs.copy())
        self.__arguments = namespaces.Namespace(
            input=None,
            intermediate_stderr=self.__kwargs.pop(
                'intermediate_stderr', None),
            timeout=self.__kwargs.pop('timeout', None))
        self.__state = self.states.ready
        #
        if len(self.__commands) == 1:
            self.__arguments.input = self.__kwargs.pop('input', None)
            self.__kwargs['stdin'] = PIPE
        else:
            self.__kwargs['stdin'] = None
        #
        self.result = namespaces.Namespace(
            returncode=None,
            stderr=None,
            stdout=None)
        if self.__kwargs.pop('run_immediately', True):
            self.run()
        #

    def repeat(self):
        """Create an instance with the same parameters as the current one"""
        return self.__class__(*self.__repeatable.commands,
                              **self.__repeatable.kwargs)

    def __get_process_arguments(self):
        """Return a dict containing a fully usable arguments set
        for subprocess.Popen()
        """
        arguments = dict(self.defaults)
        arguments.update(self.__kwargs)
        return arguments

    def run(self):
        """Start the subprocess(es) and set the result"""
        if self.__state != self.states.ready:
            raise IllegalStateException('Please create a new instance'
                                        ' using the .repeat() method!')
        #
        self.__state = self.states.running
        processes = []
        process_arguments = self.__get_process_arguments()
        number_of_commands = len(self.__commands)
        last_command_index = number_of_commands - 1
        for current_index in range(number_of_commands):
            current_arguments = namespaces.Namespace(process_arguments)
            if current_index > 0:
                current_arguments.stdin = processes[current_index - 1].stdout
            #
            if current_index < last_command_index:
                current_arguments.stdout = PIPE
                current_arguments.stderr = self.__arguments.intermediate_stderr
            #
            try:
                current_process = subprocess.Popen(
                    self.__commands[current_index],
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
                self.__state = self.states.finished
                raise
            #
            processes.append(current_process)
        #
        # Close stdout to allow processes to receive SIGPIPE, see
        # <https://docs.python.org/3.6/library/
        #  subprocess.html#replacing-shell-pipeline>
        for current_index in range(last_command_index):
            processes[current_index].stdout.close()
        #
        # Communicate with the last process in the pipeline
        stdout, stderr = processes[last_command_index].communicate(
            input=self.__arguments.input,
            timeout=self.__arguments.timeout)
        self.result = namespaces.Namespace(
            stdout=stdout,
            stderr=stderr,
            returncode=processes[last_command_index].returncode)
        # processes cleanup; avoid ResourceWarnings
        for current_index in range(last_command_index):
            processes[current_index].wait()
        #
        self.__state = self.states.finished


# vim:fileencoding=utf-8 autoindent ts=4 sw=4 sts=4 expandtab:
