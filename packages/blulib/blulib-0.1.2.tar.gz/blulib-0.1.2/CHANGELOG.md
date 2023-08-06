# Changelog

All notable changes to this project will be documented in this file

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.1]

### Fixed

- If a field is not a string but should be read as a string (and later converted).
  If that field is missing rather than using the default value it would crash [#3](https://github.com/Senth/blulib/issues/3)

## [0.1.0]

### Added

- Config parser to easily parse ini/cfg files into objects.
