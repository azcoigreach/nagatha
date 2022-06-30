from setuptools import setup

setup(
    name="nagatha-core",
    version="1.0",
    packages=["core", "core.commands"],
    include_package_data=True,
    install_requires=[
        "click",
        "requests",
        ],
    entry_points="""
        [console_scripts]
        nagatha=core.cli:cli
    """,
)
