from distutils.core import setup

from typekit._version import __version__ as version

setup(
    name = 'typekit',
    packages = ['typekit'],
    version = version,
    license='MIT',
    description = 'Python wrapper for Typekit Developer API',
    author = 'Suchan Lee',
    author_email = 'lee.suchan@gmail.com',
    url = 'https://github.com/suchanlee/typekit-python',
    download_url = 'https://github.com/suchanlee/typekit-python/tarball/{}'.format(version),
    keywords = ['typekit', 'typekit-python', 'typekit python'],
    install_requires=[
        'requests>=0.14.0',
    ],
)