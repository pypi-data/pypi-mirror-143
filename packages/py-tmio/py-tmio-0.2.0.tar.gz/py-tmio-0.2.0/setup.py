from setuptools import setup

requirements = ["python-dotenv", "aiohttp", "redis"]

version = "v0.2.0"

readme = ""
with open("README.md") as f:
    readme = f.read()

packages = [
    "trackmania",
    "trackmania.structures",
    "trackmania.managers",
    "trackmania.util",
]

setup(
    name="py-tmio",
    author="Deepesh Nimma",
    url="https://github.com/NottCurious/py-tmio",
    project_urls={
        "Documentation": "https://py-trackmaniaio.rtfd.io/",
        "Issue Tracker": "https://github.com/NottCurious/py-tmio/issues",
    },
    version=version,
    license="MIT",
    description="Trackmania.io API Wrapper",
    long_description=readme,
    long_description_content_type="text/markdown",
    include_package_data=True,
    install_requires=requirements,
    python_requires=">=3.10",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=packages,
)
