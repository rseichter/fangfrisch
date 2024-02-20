=========
Changelog
=========

Release 1.8.1 (TBA)

- Python unit tests requiring network connections are now disabled by default to facilitate sandboxed
  testing. Set environment variable `NETWORK_TESTS=1` to enable these tests.

Release 1.8.0 (2024-02-14)

- Sanesecurity (https://sanesecurity.com) provider default configuration overhaul. Switch to a less
  congested mirror site, add/remove several signature URLs.

- Modernise Python build re PEP 517 (https://peps.python.org/pep-0517/).

Release 1.7.0 (2024-02-03)

- Support user-defined connection timeouts.

Release 1.6.1 (2023-02-21)

- Require SQLAlchemy version 1.4 or higher. Version 1.3 is no longer maintained by the SQLAlchemy developers.

Release 1.6.0 (2023-02-18)

- Use Python context management protocol to improve SQLAlchemy session handling, in particular to more reliably
  release resources like database connections.

Release 1.5.0 (2021-10-12)

- When running external commands, Fangfrisch now catches all types of exceptions, not only those in the
  subprocess exception hierarchy. This allows refresh operations to continue if one of them raised
  an exception. Previous versions exited whenever one of the external commands failed.

Release 1.4.0 (2021-02-12)

- Allow the use of `url_xyz = disabled` in addition to empty values to disable URLs.

- Remove `url_doppelstern*` and `url_crdfam_clamav` from Sanesecurity's provider section because the related
  signatures are no longer maintained and/or no longer distributed by Sanesecurity.

Release 1.3.0 (2020-11-14)

- URL configuration entries can be individually disabled by setting them to an empty value.

- Disable discontinued "scamnailer" URL (see http://www.scamnailer.info for more information).

Release 1.2.0 (2020-03-29)

- In addition to console (i.e. stdout/stderr) logging, Fangfrisch now supports syslog.
  See the documentation for configuration options `log_method` et al for details.

Release 1.1.0 (2020-03-23)

If you are upgrading from a previous release, you need to either delete all existing database tables or create a new
DB, followed by running `fangfrisch initdb`.

- Clean up previously downloaded files when their local path changes.
  This can happen when `filename_xyz` entries are added or modified.
  Suggested by @amishmm.

- When a provider section is disabled, clean up associated virus signature files.
  This feature can optionally be disabled using the new `cleanup` configuration parameter.
  Suggested by @amishmm.

- Running `fangfrisch --force initdb` will attempt to drop existing tables.

- Introduce the *dumpmappings* action.
  This allows passing URL-to-filepath mappings recorded in the database to utilities like `awk` without accessing the
  DB directly.

Release 1.0.1 (2020-02-27)

- Add two disabled data sources which are only available with a paid subscription to SecuriteInfo default configuration.
  Suggested by Arnaud Jacques.

- Reduce default SecuriteInfo interval to one hour. Suggested by Arnaud Jacques.

Release 1.0.0 (2020-02-21)

- First stable release.
