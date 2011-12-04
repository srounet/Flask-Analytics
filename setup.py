"""
Flask-Analytics
-------------

Monitor users navigation history.
"""
from setuptools import setup

version='0.1'


setup(
    name='Flask-Analytics',
    version=version,
    license='BSD',
    author='Fabien Reboia',
    author_email='srounet@gmail.com',
    description='Monitor users navigation history',
    long_description=__doc__,
    py_modules=['flask_analytics'],
    zip_safe=False,
    platforms='any',
    install_requires=[
        'Flask'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
