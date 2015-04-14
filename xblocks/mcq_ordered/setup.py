"""Setup for mcq_ordered XBlock."""

import os
from setuptools import setup


def package_data(pkg, roots):
    """Generic function to find package_data.

    All of the files under each of the `roots` will be declared as package
    data for package `pkg`.

    """
    data = []
    for root in roots:
        for dirname, _, files in os.walk(os.path.join(pkg, root)):
            for fname in files:
                data.append(os.path.relpath(os.path.join(dirname, fname), pkg))

    return {pkg: data}


setup(
    name='mcq_ordered-xblock',
    version='0.1',
    description='mcq_ordered XBlock',   # TODO: write a better description.
    packages=[
        'mcq_ordered',
    ],
    install_requires=[
        'XBlock',
    ],
    entry_points={
        'xblock.v1': [
            'mcq_ordered = mcq_ordered:MCQOrderedXBlock',
        ]
    },
    package_data=package_data("mcq_ordered", ["static", "public"]),
)
