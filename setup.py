from setuptools import setup


with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="threads_py", 
    version="0.1",
    packages=["threads_py"],
    package_dir={"threads_py": "."},
    install_requires=requirements,
)