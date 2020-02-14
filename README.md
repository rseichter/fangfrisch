# Fangfrisch

Copyright © 2020 Ralph Seichter

Fangfrisch (German for "freshly caught") is a sibling to the Clam Anti-Virus
freshclam utility. It allows downloading virus definition files that are not
official ClamAV canon, e.g. from [Sanesecurity](https://sanesecurity.com).

## Update strategy

Fangfrisch is expected to run periodically, for example using `cron`. Download
attempts are recorded in a database which is accessed via
[SQLAlchemy](https://docs.sqlalchemy.org/en/13/core/engines.html#supported-databases),
and new attempts are only made after the defined age threshold is reached.
Additionally, Fangfrisch will check digests first (if available), and only
download virus definitions when their recorded digest changes, minimising
transfer volumes.

## Usage

You can display command line arguments as follows:
```shell
python -m fangfrisch --help
```

```
usage: __main__.py [-h] [-c CONF] [-f] {dumpconf,initdb,refresh}

positional arguments:
  {dumpconf,initdb,refresh}
                        Action to perform

optional arguments:
  -h, --help            show this help message and exit
  -c CONF, --conf CONF  Configuration file
  -f, --force           Force action (default: False)
```

*   **dumpconf**: Dump the effective configuration to stdout. This will include
both internal defaults and your own configuration.

*   **initdb**: Create the database structure. This needs to be run only once,
before the first refresh.

*   **refresh**: Refresh the configured URLs). The `force` switch can be set to
force downloads regardless of local file age.

Fangfrisch should never be run as `root`, but as your local ClamAV user
(typically `clamav`). An example crontab looks like this:

```
# minute hour day-of-month month day-of-week user command
*/30 * * * * clamav python -m fangfrisch --conf /etc/fangfrisch.conf refresh
```

## Configuration

A [configuration file](contrib/sample.conf) is mandatory and must contain a
`db_url` entry. See
[here](https://docs.python.org/3.7/library/configparser.html) for a detailed
description of the supported configuration file syntax with extended
interpolation, and
[here](https://docs.sqlalchemy.org/en/13/core/engines.html#supported-databases)
for SQLAlchemy's DB URL syntax.

Internal default values for Sanesecurity can be used by enabling the
`[sanesecurity]` config section. The resulting [effective
configuration](contrib/sample-dump.conf) can be displayed using the `dumpconf`
action.

You can add your own sections for additional virus definition providers:
```
[exampleprovider]
enabled = yes
integrity_check = md5
max_age = 1234
prefix = http://example.tld/clamav/
url_eggs = ${prefix}eggs.ndb
url_spam = ${prefix}spam.hdb
```

Fangfrisch will process only enabled sections, downloading files defined in
lines with the prefix `url_`. Note that `max_age` is specified in minutes.
`integrity_check` determines the expected filename for digests, e.g.
`http://example.tld/clamav/eggs.ndb.md5`.
