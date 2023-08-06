from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="swagger-coverage",
    version="2.2.4",
    author="Jamal Zeinalov",
    author_email="jamal.zeynalov@gmail.com",
    description='Python adapter for "swagger-coverage" tool',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JamalZeynalov/swagger-coverage-py",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "requests>=2.25.1",
        "Faker>=6.0.0",
        "setuptools>=53.0.0",
        "PyYAML",
        "python-dotenv~=0.16.0",
        "rootpath~=0.1.1",

    ],
    python_requires=">=3.6",
    include_package_data=True,
)
