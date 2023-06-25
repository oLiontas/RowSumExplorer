import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='rowSumExplorer',
    version='1.0',
    author='Leonidas Dosas',
    author_email='liontas76@gmail.com',
    description='Testing installation of Package',
    long_description=long_description,
    long_description_content_type="text/markdown",
    donwload_url='https://github.com/oLiontas/RowSumExplorer/archive/refs/tags/v1.0.tar.gz',
    url='https://github.com/oLiontas/RowSumExplorer/code',
    project_urls = {
        ""
    },
    license='MIT',
    packages=['code'],
    install_requires=['pandas','openpyxl','itertools'],
)
