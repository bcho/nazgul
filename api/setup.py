from setuptools import setup, find_packages

setup(
    name='nazgul',
    version='0.0.1',
    packages=find_packages(exclude=['tests*']),
    zip_safe=False,
    install_requires=[
        'click==5.1',
    ],
    include_package_data=True
)
