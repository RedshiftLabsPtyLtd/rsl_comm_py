import json
import setuptools
from os import environ


with open("README.md", "r") as fh:
    long_description = fh.read()

with open("VERSION", "r") as fh:
    version_info = json.load(fh)

version_major = '0' if not version_info.get('VERSION_MAJOR') else version_info['VERSION_MAJOR']
version_minor = '0' if not version_info.get('VERSION_MINOR') else version_info['VERSION_MINOR']
pipeline_number = '0' if not environ.get('GITHUB_RUN_NUMBER') else environ['GITHUB_RUN_NUMBER']

setuptools.setup(
    name="rsl_comm_py",
    version=f"{version_major}.{version_minor}.{pipeline_number}",
    author="Redshift Labs Pty Ltd, Dr. Konstantin Selyunin",
    author_email="selyunin.k.v@gmail.com",
    license="MIT",
    description="Redshift Labs Pty Ltd RSL Communication Python Driver",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/RedshiftLabsPtyLtd/rsl_comm_py",
    packages=["rsl_comm_py"],
    requires=["pyserial"],
    install_requires=["pyserial"],
    package_dir={'rsl_comm_py': 'rsl_comm_py'},
    package_data={"rsl_comm_py": ['rsl_xml_svd/RSL-SVD.xsd',
                                  'rsl_xml_svd/*.svd',
                                  'rsl_xml_svd/rsl_svd_parser.py',
                                  'templates/*.jinja2',
                                  'examples/*.py']},
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX",
    ],
)
