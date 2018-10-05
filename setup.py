from setuptools import setup

setup(name='mlecon',
      version='0.1.4',
      description='Machine Learning for Economic Modeling',
      url='',
      author='Victor Duarte',
      author_email='victorduarte2112@gmail.com',
      license='',
      package_dir={'': '.'},
      package_data={'':
                    ['mlecon_compiled.cpython-36m-darwin.so', 'mlecon_compiled.cpython-36m-x86_64-linux-gnu.so']},
      install_requires=[
          'tensorflow>=1.6',
          'progressbar2',
          'mpld3'
      ],
      packages=['mlecon'],
      zip_safe=False)