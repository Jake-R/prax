from setuptools import setup

setup(
    name='prax',
    version='0.1.4',
    packages=['prax'],
    url='https://github.com/Jake-R/prax',
    license='MIT',
    author='robie',
    author_email='jacob.robie@gmail.com',
    description='A data conversion utility',
    entry_points={
        'console_scripts': [
            'prax = prax.praxcmd:main'
        ]
    },
    install_requires=['future', 'funcsigs', 'pwntools'],#, 'pwntools==0.0.0;python_version>"2"'],
    #setup_requires=['pytest-runner',],
    #tests_require=['pytest', 'hypothesis',],
)
