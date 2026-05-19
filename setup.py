"""
Setup script for life-planning-coach skill.
"""

from setuptools import setup

setup(
    name="life-planning-coach",
    version="0.10.1",
    description="Evidence-based life planning coach for Claude",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/azagreev/life-planning-coach",
    classifiers=[
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.9",
)
