from setuptools import setup

setup(
    name='pycraft',
    version='0.1',
    description='PyCraft',
    packages=['pycraft'],
    install_requires=[
        'pyglet',
        'noise'
    ],
    extras_require={
        'test': ['pytest', 'mock', 'coverage']
    },
    entry_points={
        'console_scripts': [
            'pycraft=pycraft.main:main'
        ]
    }
)
