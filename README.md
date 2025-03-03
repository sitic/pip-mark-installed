# pip-mark-installed

A utility tool to mark packages as installed for pip or [uv](https://github.com/astral-sh/uv) without actually installing them.

## Description

`pip-mark-installed` creates the necessary metadata files to make pip believe that a package is installed, without actually installing any of the package code. This is particularly useful for resolving conflicts between different package variants that share the same namespace (e.g. GPU vs CPU, GUI vs headless variants) or when you want to prevent pip from installing certain packages that you have already managed through other means.

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
- `PACKAGE_NAME` (uses a default version of 9999.99.99)
- `PACKAGE_NAME==VERSION`

### Examples

Mark a package as installed:
```bash
pip-mark-installed opencv-python
```

Mark multiple packages with specific versions:
```bash
pip-mark-installed opencv-python==4.5.1 opencv-contrib-python==4.5.1
```

Specify a custom site-packages directory:
```bash
pip-mark-installed --site-packages /path/to/site-packages some-package
```

## Common Use Cases

This tool helps address situations where pip's dependency resolution doesn't behave as desired:

1.  **Conflicting Package Variants:** When multiple packages offer the same functionality but under identical import names, conflicts can arise.  A common example is the various OpenCV packages (e.g., `opencv-python`, `opencv-contrib-python`, `opencv-python-headless`).  These all install to the `cv2` namespace. You might want the `opencv-contrib-python` version, but `pip` might try to install `opencv-python` due to a dependency in another package.  `pip-mark-installed` allows you to install *your* preferred version and then "trick" `pip` into thinking the others are already present, preventing unwanted installations.

    ```bash
    # Install the variant you actually want:
    pip install opencv-contrib-python

    # Mark conflicting variants as "installed" to prevent pip from installing them:
    pip-mark-installed opencv-python opencv-python-headless opencv-python-headless
    ```

2. **Optional or broken dependencies**: Sometimes, a package might list an optional dependency that you *don't* want installed, or a dependency known to cause issues in your specific environment. For instance, a package might list PyQt5 as a dependency, but you want to use PySide6. If these are not strictly necessary, or if you've already managed them outside of pip, you can use `pip-mark-installed` to satisfy the dependency check without actually installing the packages.
    ```bash
    # Mark PyQt5 as installed, to prevent a dependency from installing them.
    pip-mark-installed PyQt5
    ```

3. **System-level installations**: When a package exists at system level but you want to prevent pip from installing conflicting versions in your environment.

    Example for resolving OpenCV variants conflict:
    ```bash
    # Install the variant you want
    pip install opencv-python-headless

    # Mark the conflicting package as installed
    pip-mark-installed opencv-python
    ```

## How It Works

The script creates the necessary `.dist-info` directory structure and metadata files that pip uses to determine if a package is installed.

## License

MIT
