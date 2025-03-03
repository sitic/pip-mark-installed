#!/usr/bin/env python3
"""
Tool to mark packages as installed in pip without actually installing them.
Useful e.g. for resolving conflicts between different OpenCV variants that share the same namespace.

Usage:
    pip-mark-installed.py PACKAGE_SPEC [PACKAGE_SPEC ...]

Where PACKAGE_SPEC can be either:
    - PACKAGE_NAME (uses default version 9999.99.99)
    or
    - PACKAGE_NAME==VERSION

Examples:
    pip-mark-installed some-package
    pip-mark-installed some-package==1.0.0 another-package==2.0.0
"""

import site
import re
import argparse
from pathlib import Path


def get_site_packages_path():
    """Return the site-packages directory for the current Python environment."""
    return site.getsitepackages()[0]


def create_dist_info(package_name, version, site_packages):
    """Create the necessary dist-info directory and files to mark a package as installed."""
    normalized_name = re.sub(r"[-.]+", "_", package_name).lower()
    site_packages = Path(site_packages)

    existing_installs = list(site_packages.glob(f"{normalized_name}-*"))
    if existing_installs:
        raise FileExistsError(
            f"Package {package_name} is already installed. Please uninstall first."
        )

    dist_info_name = f"{normalized_name}-{version}.dist-info"
    dist_info_path = site_packages / dist_info_name
    dist_info_path.mkdir(parents=True)

    metadata = f"""\
Metadata-Version: 2.1
Name: {package_name}
Version: {version}
Summary: Dummy package for dependency resolution
"""

    (dist_info_path / "METADATA").write_text(metadata)
    (dist_info_path / "INSTALLER").write_text("pip-mark-installed")
    (dist_info_path / "REQUESTED").write_text("")

    record_file = []
    for f in ["METADATA", "INSTALLER", "RECORD", "REQUESTED"]:
        record_file.append(f"{dist_info_name}/{f},,")
    (dist_info_path / "RECORD").write_text("\n".join(record_file))

    # print(f"Created {dist_info_name} in {site_packages}.")
    print(f"Marked {package_name} {version} as installed.")


def parse_package_spec(package_spec):
    """Parse a package specification into name and version."""
    if "==" in package_spec:
        package_name, version = package_spec.split("==", 1)
        return package_name, version
    else:
        return package_spec, "9999.99.99"  # Default version


def main():
    examples = """
Examples:
    pip-mark-installed some-package
    pip-mark-installed some-package==1.0.0 another-package==2.0.0
"""

    parser = argparse.ArgumentParser(
        description="Mark packages as installed by creating metadata files.",
        epilog=examples,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "package_specs",
        nargs="*",
        help="Package specifications in the format PACKAGE_NAME or PACKAGE_NAME==VERSION",
    )
    parser.add_argument(
        "--site-packages", help="Path to the site-packages directory (optional)."
    )
    args = parser.parse_args()

    if not args.package_specs:
        parser.print_help()
        return

    if args.site_packages:
        site_packages_path = Path(args.site_packages)
    else:
        site_packages_path = Path(get_site_packages_path())
    print(f"Using Python environment at: {site_packages_path}")

    for package_spec in args.package_specs:
        package_name, version = parse_package_spec(package_spec)
        try:
            create_dist_info(package_name, version, site_packages_path)
        except FileExistsError as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
