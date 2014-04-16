from setuptools import setup, find_packages

version = '0.0.1'

setup(name="helga-ugrep",
      version=version,
      description=('user activity tracker for helga'),
      classifiers=['Development Status :: 1 - Beta',
                   'Environment :: IRC',
                   'Intended Audience :: Twisted Developers, IRC Bot Developers',
                   'License :: OSI Approved :: MIT License',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Topic :: Software Development :: Libraries :: Python Modules',
                   'Topic :: IRC Bots'],
      keywords='irc bot ugrep',
      author='alfredo deza',
      author_email='contact@deza.pe',
      url='https://github.com/alfredodeza/helga-ugrep',
      license='MIT',
      packages=find_packages(),
      entry_points = dict(
          helga_plugins = [
              'ugrep = ugrep:ugrep',
          ],
      ),
)
