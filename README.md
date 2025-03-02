# pip-mark-installed

A utility tool to mark packages as installed in pip without actually installing them.

## Description

`pip-mark-installed` creates the necessary metadata files to make pip believe that a package is installed, without actually installing any of the package code. This is particularly useful for resolving conflicts between different package variants that share the same namespace (e.g., different OpenCV distributions, system installations of pytorch etc.).

## Installation

Grab the [pip-mark-installed.py](https://raw.githubusercontent.com/sitic/pip-mark-installed/main/pip-mark-installed.py) script or install it via pip:

```bash
pip install pip-mark-installed
```

## Usage

```bash
pip-mark-installed PACKAGE_SPEC [PACKAGE_SPEC ...]
```

Where `PACKAGE_SPEC` can be either:
- `PACKAGE_NAME` (uses a default future version)
- `PACKAGE_NAME==VERSION`

### Examples

Mark a package with default version:
```bash
pip-mark-installed.py opencv-python
```

Mark multiple packages with specific versions:
```bash
pip-mark-installed.py opencv-python-headless==4.5.1 opencv-contrib-python==4.5.1
```

Specify a custom site-packages directory:
```bash
pip-mark-installed.py --site-packages /path/to/site-packages some-package
```

## Common Use Cases

For example, OpenCV has several Python package variants that conflict with each other:
- `opencv-python` (standard build)
- `opencv-python-headless` (without GUI)
- `opencv-contrib-python` (with extra modules)
- `opencv-contrib-python-headless` (extra modules, no GUI)

Different dependencies might specify different variants, leading to accidental file overwrites and runtime errors. `pip-mark-installed` can help you resolve these conflicts by marking undesired packages as installed without actually installing them:

```bash
# First install the variant you actually want
pip install opencv-python-headless

# Then mark the conflicting package as installed
pip-mark-installed opencv-python
```

## How It Works

The script creates the necessary `.dist-info` directory structure and metadata files that pip uses to determine if a package is installed.

## License

MIT
