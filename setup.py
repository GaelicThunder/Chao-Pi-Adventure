#!/usr/bin/env python3
"""Setup script for Chao-Pi-Adventure"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_file = Path(__file__).parent / "README_NEW.md"
long_description = readme_file.read_text() if readme_file.exists() else ""

setup(
    name="chao-pi-adventure",
    version="2.0.0",
    description="A Tamagotchi-like game based on Chao Adventure for Raspberry Pi",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="GaelicThunder",
    url="https://github.com/GaelicThunder/Chao-Pi-Adventure",
    packages=find_packages(exclude=["tests", "tests.*"]),
    install_requires=[
        "Pillow>=9.0.0",
        "luma.core>=2.3.0",
        "luma.oled>=3.8.0",
        "timeloop>=1.0.2",
    ],
    extras_require={
        "raspberry-pi": [
            "RPi.GPIO>=0.7.1",
            "smbus>=1.1.post2",
            "pybluez>=0.23",
        ],
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=3.0.0",
            "black>=22.0.0",
            "flake8>=4.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "chao-pi-adventure=main:main",
        ],
    },
    python_requires=">=3.7",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: POSIX :: Linux",
        "Topic :: Games/Entertainment :: Simulation",
    ],
)
