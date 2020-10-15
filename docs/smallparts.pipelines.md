# smallparts.pipelines

> Wrappers for command line interface pipelines.  
> Source: [smallparts/pipelines.py](https://github.com/blackstream-x/smallparts/blob/master/smallparts/pipelines.py)

> Please note: You can also use this module to just run a single command,
> but in that case the
> [subprocess.run()](https://docs.python.org/3/library/subprocess.html#subprocess.run).
> function is simpler and more suitable.

## Module contents

### Constants

This module uses the standard library’s
[subprocess](https://docs.python.org/3/library/subprocess.html) module internally.
It defines the following "proxy" constants to eliminate the need for an expicit
import of subprocess just for accessing these special values:

smallparts.pipelines.**DEVNULL**

> [subprocess.DEVNULL](https://docs.python.org/3/library/subprocess.html#subprocess.DEVNULL)

smallparts.pipelines.**PIPE**

> [subprocess.PIPE](https://docs.python.org/3/library/subprocess.html#subprocess.PIPE)

smallparts.pipelines.**STDOUT**

> [subprocess.STDOUT](https://docs.python.org/3/library/subprocess.html#subprocess.STDOUT)

### Exceptions

#### smallparts.pipelines.**IllegalStateException**

This exception is raised if a pipeline object is started although it is currently
running or has finished.

### Classes

#### *class* smallparts.pipelines.**ProcessPipeline**(_\*commands, check=False, input=None, timeout=None, intermediate\_stderr=None, execute\_immediately=True, \*\*kwargs_)

Instances of this class implement a shell pipeline as proposed in the first example of
[Replacing shell pipeline](https://docs.python.org/3/library/subprocess.html#replacing-shell-pipeline).

_\*commands_ is a sequence of commands to be executed in the pipeline.  
Each command can be a sequence of command components or a string.  
All commands will be transformed to lists internally. For strings,
[shlex.split()](https://docs.python.org/3/library/shlex.html#shlex.split)
is used for this purpose.

* If _check_ is set to ```True```,
  a [subprocess.CalledProcessError](https://docs.python.org/3/library/subprocess.html#subprocess.CalledProcessError)
  is raised if the last command’s returncode is non-zero.
* If _input_ is not ```None```,
  it is sent to standard input **if there is only one command in the pipeline**.
* If _timeout_ is not ```None```,
  [subprocess.TimeoutExpired](https://docs.python.org/3/library/subprocess.html#subprocess.TimeoutExpired)
  is raised if the last command exceeds the specified timeout in seconds.
* if _intermediate\_stderr_ is set to **STDOUT**, standard error from any command but the last
  is redirected to the same command’s standard output stream (which is consumed by the next process’
  standard input). If set to **DEVNULL**, standard error is suppressed.
  **PIPE** does not make sense here.
  
**Pipelines are run immediately unless _execute\_immediately_ is set to ```False```!**,

_\*\*kwargs_ can be any keyword arguments accepted by [subprocess.Popen](https://docs.python.org/3/library/subprocess.html#subprocess.Popen),
plus _check_ (default: ```False```), _input_ and _timeout_ (noth defaulting to ```None```.  
Contrary to the subprocess.Popen constructor, the _stdout_ and _stderr_ arguments
default to **PIPE**.

##### Methods:

**.repeat**()

Returns a fresh copy of the current instance. That way, pipelines can be repeated.

**.execute**(_\*\*kwargs_):

Executes the pipeline and sets the instance’s **.result** attribute to a
[subprocess.CompletedProcess](https://docs.python.org/3/library/subprocess.html#subprocess.CompletedProcess)
instance matching the result of the last command in the pipeline.

_check_, _input_ and _timeout_ may be given as keyword arguments here to override the values from instantiation.

*classmethod:*  
**.run**(_\*commands, \*\*kwargs_)

Create an instance with the provoded arguments, run it and return the result
(i.e. the [subprocess.CompletedProcess](https://docs.python.org/3/library/subprocess.html#subprocess.CompletedProcess)
instance assingned to the instance’s **.result** attribute) directly.


#### *class* smallparts.pipelines.**ProcessChain**(_\*commands, check=False, input=None, timeout=None, intermediate\_stderr=None, execute\_immediately=True, \*\*kwargs_)

Instances of this class basically work the same way like **ProcessPipeline** instances,
but the single commands are run sequentially, and all results
([subprocess.CompletedProcess](https://docs.python.org/3/library/subprocess.html#subprocess.CompletedProcess)
instances) are collected in the **.all_results** attribute unique to this class.

Another significant difference  is that _input_ - if provided - is always sent
to standard input of the first command, regardless of how many commands there are in the pipeline.

The methods are the same as **ProcessPipeline** instance and class methods.


## Usage examples

```python
>>> from smallparts import pipelines
>>> echo_pipeline = pipelines.ProcessPipeline('echo "x"', ['tr', 'x', 'u'])
>>> echo_pipeline.result
CompletedProcess(args=['tr', 'x', 'u'], returncode=0, stdout=b'u\n', stderr=b'')
>>> 
>>> # Repeated execution causes an IllegalStateException:
>>> echo_pipeline.execute()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/home/rainer/projects/github/smallparts/smallparts/pipelines.py", line 163, in execute
    raise IllegalStateException('Please create a new instance'
smallparts.pipelines.IllegalStateException: Please create a new instance using the .repeat() method!
>>> 
>>> # Use the .repeat() method to "clone" the pipeline instead:
>>> echo_pipeline_2 = echo_pipeline.repeat()
>>> echo_pipeline_2.result
CompletedProcess(args=['tr', 'x', 'u'], returncode=0, stdout=b'u\n', stderr=b'')
>>> 
>>> echo_chain = pipelines.ProcessChain('echo "x"', ['tr', 'x', 'u'])
>>> echo_chain.result
CompletedProcess(args=['tr', 'x', 'u'], returncode=0, stdout=b'u\n', stderr=b'')
>>> 
```

----
[(smallparts docs home)](./)

