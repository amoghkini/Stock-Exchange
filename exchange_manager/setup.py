from setuptools import setup, find_packages
from version import VERSION


setup(
    name="exchange_manager",
    version=VERSION,
    description="Exchange Manager",
    author="Amogh Kini",
    packages=find_packages(),
    install_requires=[
        "redis",
    ],
    include_package_data=True,
    python_requires=">=3.12",  # Ensure compatibility with Python 3.12 and above
)
