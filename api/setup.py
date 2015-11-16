from setuptools import setup, find_packages

setup(
    name='nazgul',
    version='0.0.1',
    packages=find_packages(exclude=['tests*']),
    zip_safe=False,
    install_requires=[
        'flask==0.10.1',
        'flask-sqlalchemy==2.1',
        'arrow==0.7.0',
        'click==5.1',
    ],
    include_package_data=True,

    entry_points={
        'console_scripts': [
            'nazgul-cli=nazgul.cli:main'
        ]
    }
)
