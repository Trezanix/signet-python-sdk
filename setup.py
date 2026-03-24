from setuptools import setup, find_packages

setup(
    name="signet-sdk",
    version="1.0.0",
    description="Official Python SDK for Signet Licensing Platform by Trezanix.",
    long_description=open("README.md").read() if open("README.md") else "",
    long_description_content_type="text/markdown",
    author="Trezanix",
    url="https://github.com/trezanix/signet-python-sdk",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.0",
        "ecdsa>=0.18.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Security :: Cryptography",
    ],
    python_requires='>=3.7',
)