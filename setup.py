from setuptools import setup, find_packages

setup(
    name="batch_processor",
    version="0.1.0",
    description="A simple Python library for asynchronous batch processing.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Tiago Araujo",
    author_email="tybbi96@hotmail.com",
    url="https://github.com/seuusuario/batch_processor",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=["asyncio"],
    include_package_data=True,
)
