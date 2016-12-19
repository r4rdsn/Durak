from setuptools import setup

setup(name='Durak',
      version='0.1',
      description='simple python powered game with AI opponent',
      url='https://github.com/r4rdsn/Durak',
      author='alfred richardsn',
      author_email='rchrdsn@protonmail.ch',
      license='MIT',
      packages=['game'],
      install_requires=[
          'kivy',     # GUI
          'pymsgbox'  # message box
      ],
      zip_safe=False)
