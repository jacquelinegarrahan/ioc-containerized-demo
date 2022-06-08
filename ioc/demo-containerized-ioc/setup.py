from setuptools import setup, find_packages
from os import path

cur_dir = path.abspath(path.dirname(__file__))

# parse requirements
with open(path.join(cur_dir, "requirements.txt"), "r") as f:
    requirements = f.read().split()

setup(
    name="demo-containerized-ioc",
    version=0.0,
    packages=find_packages(),
    author="SLAC National Accelerator Laboratory",
    author_email="jgarra@slac.stanford.edu",
    license="SLAC Open",
    install_requires=requirements,
    include_package_data=True,
    python_requires=">=3.8",
    #entry_points={
    #    "console_scripts": [
    #        "render-from-template=lume_epics.commands.render_from_template:render_from_template",
    #        "serve-from-template=lume_epics.commands.serve_from_template:serve_from_template",
    #    ]
    #},
)
