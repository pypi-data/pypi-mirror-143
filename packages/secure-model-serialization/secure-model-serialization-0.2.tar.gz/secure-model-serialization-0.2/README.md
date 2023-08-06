# Secure-Model-Serialization
Python model serialization library.


# Quick Install

Tagged versions of `secure-model-serialization` are published to Ripple's internal artifactory PYPI
server, which can be used by adding the following to `~/.config/pip/pip.conf`

```
[global]
index-url = https://artifactory.ops.ripple.com/artifactory/api/pypi/ripple-pypi/simple
```
Then install by running

```
pip install secure-model-serialization==0.1.0
```

## Quick Installation Setup

Sometimes when the `~/.pip/` doesn't exist, create it with the following steps:
1. `cd $HOME`
2. `mkdir .pip`
3. `cd .pip`
4. `touch pip.conf`
5. `vim ~/.pip/pip.conf` and then proceed to _quick install_ mentioned above.