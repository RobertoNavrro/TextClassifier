from setuptools import setup, find_packages

with open("requirements.txt") as req:
    """Creates set of all unique requirements,
     for general usage and development"""
    requirements = set(line.strip() for line in req)
    requirements = list(requirements)

setup(
    name='Restaurant Assistant',
    version='0.3',
    packages=find_packages(),
    package_data={'': ['*.csv', '*.dat']},
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'restaurant_assistant = restaurant_assistant.__main__:main'
        ]
    }
)
