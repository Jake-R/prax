from distutils.core import setup

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
            'prax = prax.praxidike:main'
        ]
    },
    install_requires=['grako', 'future']
)
