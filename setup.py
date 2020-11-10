from setuptools import setup, find_packages

requires = [
    'flask',
    'flask-sqlalchemy',
    'psycopg2',
]

setup(
    name='DiscSpring',
    version='0.0',
    description='DiscSpringGrapher',
    author='Sean Doughty',
    author_email='sean.doughty@outlook.com',
    keywords='web flask',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires
)