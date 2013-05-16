from setuptools import setup, find_packages
import sys, os

version = '0.1.1'

setup(name='redisconf',
      version=version,
      description="Basic module to store environment configuration on redis",
      long_description="""\
Basic module to store environment configuration on redis""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='config configuration redis python',
      author='Bruno Gomes Fran\xc3\xa7a',
      author_email='bgfranca@gmail.com',
      url='https://github.com/brunogfranca/redisconf',
      license='',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
