<h1>Welcome to MAAS's new command-line tool &amp; Python client library</h1>

_python-libmaas_ provides:

* A rich and stable Python client library for interacting with MAAS 2.0+
  servers. This can be used in a synchronous/blocking mode, or an
  asynchronous/non-blocking mode based on [asyncio][].

* A lower-level Python client library, auto-generated to match the MAAS
  server it's interacting with.

* A command-line tool for working with MAAS servers.

For MAAS _server_ documentation, visit
[docs.ubuntu.com](https://docs.ubuntu.com/maas/).

----

This is **ALPHA** software. We are converging on a finished product, but
until we release a beta all APIs could change.

----


## Installation

Either work from a branch:

```console
$ git clone https://github.com/maas/python-libmaas.git
$ cd python-libmaas
$ make
```

Or install with [pip](https://pip.pypa.io/) into a
[virtualenv](https://virtualenv.readthedocs.org/):

```console
$ virtualenv --python=python3.5 amc && source amc/bin/activate
$ pip install git+https://github.com/maas/python-libmaas.git
```

Or install from [PyPI](https://pypi.python.org/):

```console
$ virtualenv --python=python3.5 amc && source amc/bin/activate
$ pip install python-libmaas
```

**Note** that PyPI may lag the others.

This documentation assumes you're working from a branch or in a
virtualenv. In practice this means it will use partially qualified paths
like ``bin/maas`` instead of bare ``maas`` invocations. If you've
installed from PyPI the ``maas`` command will probably be installed on
your shell's ``PATH`` so you can invoke it as ``maas``.


## Command-line

```console
$ bin/maas profiles login --help
$ bin/maas profiles login exmpl \
>   http://example.com:5240/MAAS/ my_username
Password: …
$ bin/maas list
┌───┬────────────┬───────────┬───────┬────────┬────────┬─────────┐
│   │ Hostname   │ System ID │ #CPUs │ RAM    │ Status │ Power   │
├───┼────────────┼───────────┼───────┼────────┼────────┼─────────┤
│ m │ botswana   │ pncys4    │ 4     │ 8.0 GB │ Ready  │ Off     │
│ c │ namibia    │ xfaxgw    │ 4     │ 8.0 GB │ —      │ Error   │
│ C │ madagascar │ 4y3h7n    │ 4     │ 8.0 GB │ —      │ Unknown │
└───┴────────────┴───────────┴───────┴────────┴────────┴─────────┘
```

Tab-completion in ``bash`` and ``tcsh`` is supported too. For example,
in ``bash``:

```console
$ source <(bin/register-python-argcomplete --shell=bash bin/maas)
$ bin/maas <tab>
allocate  launch  list  list-files  list-tags  ...
```


## Client library

For a developer the simplest entry points into ``python-libmaas`` are
the ``connect`` and ``login`` functions in ``maas.client``. The former
connects to a MAAS server using a previously obtained API key, and the
latter logs-in to MAAS with your username and password. These returns a
``Client`` object that has convenient attributes for working with MAAS.

For example, this prints out all interfaces on all machines:

```python
from maas.client import login
client = login(
    "http://localhost:5240/MAAS/",
    username="my_user", password="my_pass",
)
tmpl = "{0.hostname} {1.name} {1.mac_address}"
for machine in client.machines.list():
    for interface in machine.interfaces:
        print(tmpl.format(machine, interface))
```

Learn more about the [client](client/index.md).


## Shell

There's an interactive shell. If a profile name is given or a default
profile has been set — see ``maas profiles --help`` — this places a
``Client`` instance in the default namespace (as ``client``) that you
can use interactively or in a script.

For the best experience install [IPython](https://ipython.org/) first.

```console
$ bin/maas shell
Welcome to the MAAS shell.
...
```

```pycon
>>> origin.Version.read()
<Version 2.2.0 beta2+bzr5717 [bridging-automatic-ubuntu ...]>
>>> dir(client)
[..., 'account', 'boot_resources', ...]
```

Scripts can also be run. For example, given the following ``script.py``:

```python
print("Machines:", len(client.machines.list()))
print("Devices:", len(client.devices.list()))
print("Racks:", len(client.rack_controllers.list()))
print("Regions:", len(client.region_controllers.list()))
```

the following will run it against the default profile:

```console
$ bin/maas shell script.py
Machines: 1
Devices: 0
Racks: 2
Regions: 1
```


## Development

It's easy to start hacking on _python-libmaas_:

```console
$ git clone git@github.com:maas/python-libmaas.git
$ cd python-libmaas
$ make develop
$ make test
```

Installing [IPython][] is generally a good idea too:

```console
$ bin/pip install -UI IPython
```

Pull requests are welcome but authors need to sign the [Canonical
contributor license agreement][CCLA] before those PRs can be merged.


### _bones_ & _viscera_

Digging around in the code and when using the primary client API, you
may find references to _bones_ and _viscera_. These libraries form the
base for the client API:

* [_bones_](bones/index.md) is a lower-level library that closely
  mirrors MAAS's Web API. Every MAAS server publishes a description of
  its Web API and _bones_ generates a convenient mechanism to interact
  with it.

* [_viscera_](viscera/index.md) is a higher-level library which makes
  heavy use of _bones_. MAAS's Web API is sometimes unfriendly or
  inconsistent, but _viscera_ presents a hand-crafted API that has been
  designed for developers rather than machines.


[asyncio]: https://docs.python.org/3/library/asyncio.html

[CCLA]: https://www.ubuntu.com/legal/contributors

[IPython]: https://ipython.org/
