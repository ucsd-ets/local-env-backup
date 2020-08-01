from setuptools import setup, find_packages

setup(
    name='env-backup',
    version='0.0.2',
    description='Backup your .local python environment',
    url='http://github.com/ucsd-ets/local-env-backup',
    author='Yuxin Zou',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'pytest',
        'timeout_decorator'
    ],
    entry_points = {
        'console_scripts': ['env-backup=env_backup.command_line:main'],
    },
    scripts=['bin/env-activate', 'bin/env-deactivate']
)
