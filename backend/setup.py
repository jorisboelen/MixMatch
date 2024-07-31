from setuptools import find_packages, setup

with open('requirements.txt') as requirements_file:
    requirements = requirements_file.readlines()

setup(
    name='mixmatch',
    version='0.0.1',
    python_requires='>=3.10',
    install_requires=requirements,
    include_package_data=True,
    packages=find_packages(include=['mixmatch', 'mixmatch.*']),

    entry_points={
        'console_scripts': [
            'mixmatch = mixmatch.__main__:main'
        ]
    }
)
