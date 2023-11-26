from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='fiscal_calendar',
    version='0.2',
    license='MIT',
    description='Fiscal Retail Calendar - 4-5-4 week retail calendar',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Tony Hollaar',
    author_email='thollaar@gmail.com',
    url='https://github.com/tonyhollaar/fiscal_calendar',
    download_url='https://github.com/tonyhollaar/fiscal_calendar/archive/refs/tags/v0.2.tar.gz',
    packages=find_packages(),
    install_requires=[
        'pandas>=1.0.0',
        'numpy>=1.18.0',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)