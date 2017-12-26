from setuptools import setup


setup(
    name='pypageobject',
    version='0.1.0',
    description='framework for creating page objects in python',
    long_description=open('README.rst').read(),
    author='bwalkowi',
    url='https://github.com/bwalkowi/pypageobject',
    packages=['pypageobject'],
    install_requires=['selenium>=3.0.0'],
    license='MIT',
    keywords='pageobject testing automation',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
    ]
)
