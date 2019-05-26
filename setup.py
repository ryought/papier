from setuptools import setup

setup(
        name="papier",
        version="0.0.1",
        install_requires=["iterfzf", "python-editor"],
        entry_points={
            "console_scripts": [
                "papier = papier.main:main"
                ]
            }
        )
