from setuptools import setup, find_packages

with open("README.md", 'r', encoding='utf-8') as fh:
    long_description= fh.read()

setup(
    name='convbaspy',
    version='1.0.4',
    license='MIT',
    author="D Penilla",
    author_email='dpenillac@correo.usbcali.edu.co',
    packages=find_packages('src'),
    description='Convertidor de Bases IEEE754',
    long_description=long_description,
    long_description_content_type='text/markdown',
    scripts=['src/convbaspy.py'],
    package_dir={'': 'src'},
    url='https://github.com/etensor/baseconvpy',
    keywords='convertidor bases converter hex oct bin ieee754 32bit 64bit',
    install_requires=[
          'rich',
          'textual',
          'pyfiglet',
          'pyperclip'
      ],

)
