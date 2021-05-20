from setuptools import setup, find_packages

with open('README.md') as f:
    long_description = f.read()

setup(
    name='seeed-python-reterminal',
    version='0.2',
    description='seeed-python-reterminal',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT License',
    url='https://github.com/Seeed-Studio/Seeed_Python_ReTerminal',
    author='Takashi Matsuoka (matsujirushi)',
    author_email='matsujirushi@live.jp',
    classifiers=[
        "Programming Language :: Python :: 3.8",
    ],
    install_requires=[
        "evdev"
    ],
    packages=find_packages(
        exclude=[
            "samples",
            "samples.*",
        ]
    ),
)
