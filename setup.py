import os
from setuptools import setup


# Compile the list of packages available, because distutils doesn't have
# an easy way to do this.
packages, data_files = [], []
root_dir = os.path.dirname(__file__)
if root_dir:
    os.chdir(root_dir)

for dir_path, dir_names, file_names in os.walk('quran'):
    # Ignore dir_names that start with '.'
    for i, dir_name in enumerate(dir_names):
        if dir_name.startswith('.'): del dir_names[i]
    if '__init__.py' in file_names:
        pkg = dir_path.replace(os.path.sep, '.')
        if os.path.altsep:
            pkg = pkg.replace(os.path.altsep, '.')
        packages.append(pkg)
    elif file_names:
        prefix = dir_path[6:] # Strip "quran/" or "quran\"
        for f in file_names:
            data_files.append(os.path.join(prefix, f))


# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "django-quran",
    version = "0.1",
    author = "Idris Mokhtarzada",
    description ="Quranic models and helpers for use in Django projects",
    license = "BSD",
    keywords = "django quran islam arabic",
    url = "http://github.com/idris/django-quran",
    package_dir={'quran': 'quran'},
    packages=packages,
    package_data={'quran': data_files},
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Framework :: Django",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
    ], requires=['django']
)