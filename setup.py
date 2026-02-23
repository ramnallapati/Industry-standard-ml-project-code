'''
The setup.py file is an essential part of packaging and distributing
python projects. It is used by setuptools (or distutils in older python versions) to define
the configuration of your project, such as its metadata,
dependencies,and more
'''

from setuptools import find_packages,setup
from typing import List

def get_requirements() -> List[str]:
  """
  This function will return list of requirements
  """
  requirement_list:List[str] = []
  try:
    with open('requirements.txt','r') as file:
      # read lines from the file
      lines = file.readlines()
      # process each line
      for line in lines:
        requirement = line.strip()
        # ignore empty lines and -e.
        if requirement and requirement != '-e.':
          requirement_list.append(requirement)
  except FileNotFoundError:
    print('requirements.txt file not found')
    

  return requirement_list


setup(
  # project name
  name = "NetworkSecurity",
  # package version
  version = "0.0.1",
  # author
  author = "Ram Nallapati",
  # author email
  author_email="ramnallapati741@gmail.com",
  # getting packages
  packages=find_packages(),
  # installing packages,
  install_requires=get_requirements()
)

# execution part

# print(get_requirements())
         