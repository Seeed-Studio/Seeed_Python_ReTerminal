from setuptools import setup, find_packages

setup(
    name='seeed-python-reterminal',
    version='0.1',
    description='seeed-python-reterminal',
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
