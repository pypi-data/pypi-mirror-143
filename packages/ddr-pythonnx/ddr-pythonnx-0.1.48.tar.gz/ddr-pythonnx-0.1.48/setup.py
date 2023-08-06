import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ddr-pythonnx", # DDR-Python runtime for NX-OS
    version="0.1.48", #Update the version number here
    author="Peter Van Horne",
    author_email="petervh@cisco.com",
    description="Distributed Device Reasoning (DDR) NX-OS runtime",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://wwwin-github.cisco.com/petervh/ddr-pythonnx",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
                     ],
    python_requires='>=3.6',
    py_modules=['ddrlibnx', 'genie_parsers_nx'],
    )
