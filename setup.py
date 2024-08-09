import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='eurlparser',
    version='0.0.2',
    author='Vladislav Tislenko',
    author_email='keklick1337@gmail.com',
    description='A powerful URL parser with detailed analysis.',
    keywords='url, parser, url-parser, enhanced-url-parser',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/keklick1337/eurlparser',
    project_urls={
        'Documentation': 'https://github.com/keklick1337/eurlparser',
        'Bug Reports': 'https://github.com/keklick1337/eurlparser/issues',
        'Source Code': 'https://github.com/keklick1337/eurlparser',
    },
    package_dir={'': 'src'},
    packages=setuptools.find_packages(where='src'),
    classifiers=[
        'Development Status :: 4 - Beta',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3 :: Only',

        'License :: OSI Approved :: MIT License',

        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    extras_require={
        'dev': ['check-manifest'],
    },
)
