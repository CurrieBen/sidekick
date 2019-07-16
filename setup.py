import setuptools

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name="side-kick",
    version="0.1.9",
    author="Ben Currie",
    author_email="benjamin.w.currie@gmail.com",
    description="A lightweight task runner for django with easy admin controls",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/CurrieBen/sidekick",
    license="MIT License",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
