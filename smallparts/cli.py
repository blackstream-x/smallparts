# -*- coding: utf-8 -*-

"""

smallparts.cli

Command line interface (subprocess) wrapper

"""


import shlex
import subprocess

# from smallparts import constants
from smallparts import namespaces

# "Proxy" subprocess constants

DEVNULL = subprocess.DEVNULL
PIPE = subprocess.PIPE
STDOUT = subprocess.STDOUT

#
# Exceptions
#


class IllegalStateException(Exception):

    """Raised when a Subprocess is run twice"""

    ...


#
# Classes
#


class Subprocess():

    """Wrapper for a subprocess.Popen() object
    also storing the result
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
        universal_newlines=None,
        startupinfo=None,
        creationflags=0,
        restore_signals=True,
        start_new_session=False,
        pass_fds=(),
        encoding=None,
        errors=None,
        text=None)

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
        self.__parameters = namespaces.Namespace(
            input=None,
            intermediate_stderr=self.__kwargs.pop(
                'intermediate_stderr', None),
            timeout=self.__kwargs.pop('timeout', None))
        self.__state = self.states.ready
        #
        if len(self.__commands) == 1:
            self.__parameters.input = self.__kwargs.pop('input', None)
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

    def __get_process_parameters(self):
        """Return a dict containing a fully usable parameters set
        for subprocess.Popen()
        """
        parameters = self.defaults.copy()
        parameters.update(self.__kwargs)
        return parameters

    def run(self):
        """Start the subprocess(es) and set the result"""
        if self.__state != self.states.ready:
            raise IllegalStateException('Please create a new instance'
                                        ' using the .repeat() method!')
        #
        self.__state = self.states.running
        processes = []
        number_of_commands = len(self.__commands)
        last_command_index = number_of_commands - 1
        for current_index in range(number_of_commands):
            cpp = namespaces.Namespace(self.__get_process_parameters())
            if current_index > 0:
                cpp.stdin = processes[current_index - 1].stdout
            #
            if current_index < last_command_index:
                cpp.stdout = PIPE
                cpp.stderr = self.__parameters.intermediate_stderr
            #
            try:
                current_process = subprocess.Popen(
                    self.__commands[current_index],
                    bufsize=cpp.bufsize,
                    executable=cpp.executable,
                    stdin=cpp.stdin,
                    stdout=cpp.stdout,
                    stderr=cpp.stderr,
                    close_fds=cpp.close_fds,
                    shell=cpp.shell,
                    cwd=cpp.cwd,
                    env=cpp.env,
                    universal_newlines=cpp.universal_newlines,
                    startupinfo=cpp.startupinfo,
                    creationflags=cpp.creationflags,
                    restore_signals=cpp.restore_signals,
                    start_new_session=cpp.start_new_session,
                    pass_fds=cpp.pass_fds,
                    encoding=cpp.encoding,
                    errors=cpp.errors,
                    text=cpp.text)
            except (OSError, ValueError):
                self.__state = self.states.finished
                raise
            #
            processes.append(current_process)
        #
        # Close stdout to allow processes to receive SIGPIPE, see
        # https://docs.python.org/3/library/subprocess.html#replacing-shell-pipeline
        for current_index in range(last_command_index):
            processes[current_index].stdout.close()
        #
        # Communicate with the last process in the pipeline
        stdout, stderr = processes[last_command_index].communicate(
            input=self.__parameters.input,
            timeout=self.__parameters.timeout)
        self.result = namespaces.Namespace(
            stdout=stdout,
            stderr=stderr,
            returncode=processes[last_command_index].returncode)
        # processes cleanup; avoid ResourceWarnings
        for current_index in range(last_command_index):
            processes[current_index].wait()
        #


# vim:fileencoding=utf-8 autoindent ts=4 sw=4 sts=4 expandtab:
