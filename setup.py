from setuptools import setup
setup(
    name='notify',
    version='0.0.1',
    entry_points={
        'console_scripts': [
            'notify=notify:run'
        ]
    }
)