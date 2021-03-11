from setuptools import find_packages, setup

setup(
    name='Dcoya Challenge',
    author="Itai Dotan",
    packages=find_packages(),
    zip_safe=False,
    install_requires=[
        'flask',
        'PyJWT',
        'requests',
    ],
    extras_require={"test": ["pytest"]},
)
