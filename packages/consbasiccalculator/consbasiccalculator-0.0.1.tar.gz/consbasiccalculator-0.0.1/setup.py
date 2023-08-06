from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='consbasiccalculator',
  version='0.0.1',
  description='A very basic calculator produced for practice',
  long_description=open('README.md').read() + '\n\n' + open('CHANGELOG.md').read(),
  url='',  
  author='Conor ORegan',
  author_email='battlekill770@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='calculator', 
  packages=find_packages(),
  install_requires=[''] 
)