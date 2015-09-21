# -*- coding: utf-8 -*-
from setuptools import setup

__author__ = 'viruzzz-kun'
__version__ = '0.1'


if __name__ == '__main__':
    setup(
        name="bouser_simargl",
        version=__version__,
        description="Notification service for Bouser",
        long_description='',
        author=__author__,
        author_email="viruzzz.soft@gmail.com",
        license='ISC',
        url="http://github.com/hitsl/bouser_simargl",
        packages=[
            "bouser_simargl",
            "bouser_simargl.clients",
        ],
        zip_safe=False,
        package_data={},
        install_requires=[
            'bouser',
        ],
        extras_require={
            'DB': ['bouser_db'],
        },
        classifiers=[
            "Development Status :: 3 - Alpha",
            "Environment :: Plugins",
            "Programming Language :: Python",
        ])

