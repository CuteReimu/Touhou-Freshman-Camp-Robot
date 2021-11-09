from setuptools import setup, find_packages

setup(
    name="Touhou Freshman Camp Robot",
    version="1.0",
    author="CuteReimu",
    description="A QQ Chat robot of Touhou Freshman Camp",
    packages=find_packages(),
    install_requires=['flask', 'gevent', 'requests', 'rsa']
)
