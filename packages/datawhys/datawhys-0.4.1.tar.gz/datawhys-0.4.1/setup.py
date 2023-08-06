import distutils.cmd
import os
import re
import sys

from setuptools import find_packages, setup

ROOT = os.path.dirname(__file__)

SEMVER_REGEX = r"(?P<semver>(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)(?:-(?P<prerelease>(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+(?P<buildmetadata>[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?)"  # noqa: E501
VERSION_RE = re.compile(r'__version__ = "' + SEMVER_REGEX + r'"')


def get_version():
    init = open(os.path.join(ROOT, "datawhys", "__init__.py")).read()
    return VERSION_RE.search(init).group("semver")


class VerifyVersionCommand(distutils.cmd.Command):
    """Custom command to verify that the git tag matches our version"""

    description = "verify that the git tag matches our version"

    user_options = [
        ("git-tag=", None, "Tag to verify"),
        ("git-branch=", None, "Branch to verify"),
    ]

    def initialize_options(self):
        """Set default values for options."""
        # Each user option must be listed here with their default value.
        self.git_tag = os.getenv("CIRCLE_TAG")
        self.git_branch = os.getenv("CIRCLE_BRANCH")

    def finalize_options(self):
        pass

    def run(self):
        git_version = self.git_tag

        if git_version is None:
            branch = self.git_branch or "NO TAG/RELEASE BRANCH"
            _, _, git_version = branch.partition("release/")

        print(git_version)
        version = get_version()

        if git_version != version:
            info = "Git tag: {0} does not match the version of this app: {1}".format(
                git_version, version
            )
            sys.exit(info)


setup(
    name="datawhys",
    version=get_version(),
    description="DataWhys API wrapper",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="DataWhys",
    url="https://bitbucket.org/mondobrain/datawhys-python",
    project_urls={
        "DataWhys homepage": "https://datawhys.ai",
        "DataWhys source": "https://bitbucket.org/mondobrain/datawhys-python",
    },
    packages=find_packages(exclude=["tests*"], include=["datawhys", "datawhys.*"]),
    package_data={"datawhys": ["examples/*.md", "datasets/data/*.csv"]},
    include_package_data=True,
    license="MIT License",
    classifiers=[
        # How mature is this project?
        "Development Status :: 3 - Alpha",
        # Intended audience
        "Intended Audience :: Developers",
        "Topic :: Software Development",
        "Topic :: Scientific/Engineering",
        # Language of project
        "Natural Language :: English",
        # License
        "License :: OSI Approved :: MIT License",
        # Versions supported
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        # Operating systems
        "Operating System :: OS Independent",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        "Operating System :: Unix",
        "Operating System :: MacOS",
    ],
    platforms="any",
    python_requires=">=3.6",
    install_requires=[
        "networkx ~= 2.5",
        "numpy ~= 1.18",
        "pandas ~= 1.0",
        "pyarrow ~= 3.0.0",
        "requests ~= 2.7",
        "scikit-learn ~= 0.22.1",
    ],
    # extras_require={
    # "nlp": ["solver @ git+https://bitbucket.org/mondobrain/indigo@70569bb"]
    # },
    extras_require={
        "sci": ["umap-learn ~= 0.5.1"],
        "viz": ["graphviz ~= 0.14.2", "pygraphviz ~= 1.6"],
    },
    cmdclass={"verify": VerifyVersionCommand},
)
