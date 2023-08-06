# autodidaqt-common

<div align="center">

[![Build status](https://github.com/chstan/autodidaqt-common/workflows/build/badge.svg?branch=master&event=push)](https://github.com/chstan/autodidaqt-common/actions?query=workflow%3Abuild)
[![Python Version](https://img.shields.io/pypi/pyversions/autodidaqt-common.svg)](https://pypi.org/project/autodidaqt-common/)

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License](https://img.shields.io/github/license/chstan/autodidaqt-common)](https://github.com/chstan/autodidaqt-common/blob/master/LICENSE)

Analyis-side bridge for autodiDAQt.

</div>

## Installation

```bash
pip install -U autodidaqt-common
```

or install with `Poetry`

```bash
poetry add autodidaqt-common
```

## Building and releasing

Building a new version of the application contains steps:

- Bump the version of your package `poetry version <version>`. You can pass the new version explicitly, or a rule such as `major`, `minor`, or `patch`. For more details, refer to the [Semantic Versions](https://semver.org/) standard.
- Make a commit to `GitHub`.
- Create a `GitHub release`.
- Publish `poetry publish --build`
