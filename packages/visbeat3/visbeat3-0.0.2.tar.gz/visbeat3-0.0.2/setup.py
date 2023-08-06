import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
  name="visbeat3",
  version="0.0.2",
  author="Haofan Wang",
  author_email="haofanwang.ai@gmail.com",
  description="Code for 'Visual Rhythm and Beat' SIGGRAPH 2018",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/haofanwang/visbeat3",
  packages=setuptools.find_packages(),
  install_requires=[
        'numpy',
        'scipy',
        'bs4',
        'librosa',
        'imageio',
        'requests',
        'moviepy',
        'termcolor',
        'youtube-dl',
        'matplotlib',
    ],
  scripts=['bin/dancefer'],
  classifiers=[
  "Programming Language :: Python :: 3",
  "License :: OSI Approved :: Apache Software License",
  "Operating System :: OS Independent",
  ],
)
