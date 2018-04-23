from setuptools import setup

setup(
    name='briscas',
    packages=['briscas'],
    version='1.1',
    description='Library to model the briscas card game.',
    author='Bryan Collazo',
    author_email='bcollazo2010@gmail.com',
    license='MIT',
    url='https://github.com/bcollazo/briscas',
    download_url='https://github.com/bcollazo/briscas/archive/v1.1.zip',
    keywords=['briscas', 'card', 'game', 'terminal', 'naipes'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Topic :: Games/Entertainment',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    install_requires=[],
    entry_points={
        'console_scripts': ['briscas=briscas.main:main']
    }
)
