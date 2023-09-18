from setuptools import setup, find_packages

setup(
    name="epub2audio",
    version="1.0",
    packages=find_packages(),
    install_requires=[
        "TTS",
        "ebooklib",
        "beautifulsoup4",
        "torch",
    ],
)
