from distutils.core import setup

setup(
    name='prax',
    version='0.1.3',
    packages=['prax'],
    url='https://github.com/Jake-R/prax',
    license='MIT',
    author='robie',
    author_email='jacob.robie@gmail.com',
    description='A data conversion utility',
    entry_points={
        'console_scripts': [
            'prax = prax.main:main'
        ]
    },
    install_requires=['grako', 'future']
)
