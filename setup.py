from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="phoenix-core",
    version="0.1.0",
    author="Marco Olivier",
    author_email="marco.olivier@phoenix-compute.dev",
    description="High-performance GPU compute library with hardware abstraction",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/marco-olivier/phoenix-core",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Topic :: Scientific/Engineering :: Physics",
    ],
    python_requires=">=3.9",
    install_requires=[
        "numpy>=1.21.0",
        "pybind11>=2.10.0",
    ],
    extras_require={
        "hip": ["hip-python>=5.7"],
        "cuda": ["cupy-cuda12x>=12.0"],
        "vulkan": ["vulkan>=1.3"],
        "dev": ["pytest", "pytest-benchmark", "black", "mypy"],
    },
)
