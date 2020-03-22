=========
Changelog
=========

Release 1.1.0 (work in progress)

- Clean up previously downloaded files when the local path changes.
  This can happen when the user introduces or modifies a `filename_xyz` config entry.
  Suggested by Amish.

- Clean up previously downloaded files when a provider section is disabled.
  Suggested by Amish.

- Introduce the *dumpmappings* action.
  This allows passing URL-to-filepath mappings recorded in the database to utilities like `awk` without accessing the DB directly.

Release 1.0.1 (2020-02-27)

- Add two disabled data sources which are only available with a paid subscription to SecuriteInfo default configuration.
  Suggested by Arnaud Jacques.

- Reduce default SecuriteInfo interval to one hour. Suggested by Arnaud Jacques.

Release 1.0.0 (2020-02-21)

- First stable release.
