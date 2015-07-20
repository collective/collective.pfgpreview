from setuptools import setup, find_packages
import os

version = '1.2.dev0'

setup(name='collective.pfgpreview',
      version=version,
      description="Preview page for PloneFormGen",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read() + "\n" +
                       open(os.path.join("docs", "CONTRIBUTORS.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='plone ploneformgen preview',
      author='Roman Kozlovskyi (kroman0)',
      author_email='krzroman@gmail.com',
      url='http://pypi.python.org/pypi/collective.pfgpreview',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'Products.PloneFormGen',
          'archetypes.schemaextender',
      ],
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
