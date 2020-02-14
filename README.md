# fangfrisch

Copyright © 2020 Ralph Seichter

Fangfrisch (German for "freshly caught") is a sibling to the Clam Anti-Virus
freshclam utility.

## Usage

Display command arguments:
```shell
python -m fangfrisch --help
```

```
usage: __main__.py [-h] [-c CONF] [-f] {dumpconf,refresh}

positional arguments:
  {dumpconf,refresh}    Action to perform

optional arguments:
  -h, --help            show this help message and exit
  -c CONF, --conf CONF  Configuration file
  -f, --force           Force action (default: False)
```

*  **dumpconf**: Dump the effective configuration to stdout. This will include
both internal defaults and your own configuration.

*  **refresh**: Refresh the configured URLs). The `force` switch can be set to
force downloads regardless of local file age.

```shell
python -m fangfrisch --conf /path/to/my.conf refresh
```

The configuration file is mandatory and must contain a `db_url` entry. See
[here](https://docs.python.org/3.7/library/configparser.html) for a detailed
description of the supported configuration file syntax. Fangfrisch supports
extended interpolation syntax, as shown in the following example:

```
[DEFAULT]
db_url = sqlite:////var/lib/clamav/fangfrisch.sqlite
local_directory = /var/lib/clamav

[exampleprovider]
enabled = yes
integrity_check = sha256
# Maximum age (in minutes) of local files
max_age = 1440
prefix = https://example.tld/clamav-unofficial/
url_eggs = ${prefix}foo.ndb
url_spam = ${prefix}bar.ndb
```

Fangfrisch has internal default values for Sanesecurity which you can use simply
by enabling the `[sanesecurity]` config section, as shown in
[sample.conf](contrib/sample.conf). The resulting [effective
configuration](contrib/sample-dump.conf) can be displayed using the `dumpconf`
action.
