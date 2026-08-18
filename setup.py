from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in bfarm/__init__.py
from bfarm import __version__ as version

setup(
	name="bfarm",
	version=version,
	description="Bfarm Agriculture Customization",
	author="Beeyond",
	author_email="contact@beeyond.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
