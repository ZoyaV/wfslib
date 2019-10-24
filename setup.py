from setuptools import setup, find_packages  # type: ignore

setup(
    name='wfslib',
    description='Tool for processing WFS data',
    # long_description=long_description,
    # version=wfslib.__version__,
    version='1.0',
    author="Zoya Volovikova, Polina Konetskaya",
    license=license,
    classifiers=[
        'Programming Language :: Python :: 3.7',
    ],
    keywords='wfs',
    packages=find_packages(exclude=['docs', 'tests']),
    python_requires='>=3.7',
)
