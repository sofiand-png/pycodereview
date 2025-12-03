
from setuptools import setup, find_packages

setup(
    name="crss-example-sensor-voting",
    version="1.0.0",
    description="CRSS Python Strict-A sensor voting reference implementation (v3)",
    package_dir={"": "src"},
    packages=find_packages(where="src"),  # crss_example_sensor_voting and subpackages
    python_requires=">=3.11,<3.13",
    install_requires=[],
    extras_require={"dev": ["pytest", "coverage"]},
)
