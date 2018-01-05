from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name             = 'fmu2aadl',
      version          = '0.1',
      description      = 'FMU2AADL converter',
      long_description = readme(),
      packages         = ['fmu2aadl'],
      entry_points     = {
          'console_scripts' : ['fmu2aadl=fmu2aadl.command_line:main'],
      },
      include_package_data = True,
      zip_safe = False
)
