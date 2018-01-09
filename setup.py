import setuptools

with open('README.rst') as fp:
    long_description = fp.read()

setuptools.setup(
    name='moshez_middlefield_beamer',
    license='MIT',
    description="Middlefield Beamer: Build beamer presentations",
    long_description=long_description,
    use_incremental=True,
    setup_requires=['incremental'],
    author="Moshe Zadka",
    author_email="zadka.moshe@gmail.com",
    packages=setuptools.find_packages(where='src'),
    package_dir={"": "src"},
    install_requires=['middlefield'],
    entry_points=dict(
        gather=["gather=moshez_middlefield_beamer"],
    )
)
