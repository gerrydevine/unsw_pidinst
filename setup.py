from setuptools import setup, find_packages

setup(
    name='unsw_pidinst',
    version='1.0',
    packages=find_packages(),
    package_data={
        'unsw_pidinst': ['web/templates/*.html']
    },
    install_requires = [
        'pygithub',
        'pandas',
        'python-dotenv'
    ]
)