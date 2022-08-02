#!/usr/bin/env python
"""This package contains GRR client templates."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import glob
import os
import re
import shutil

import configparser
from setuptools import setup
from setuptools.command.sdist import sdist

THIS_DIRECTORY = os.path.dirname(os.path.realpath(__file__))

# If you run setup.py from the root GRR dir you get very different results since
# setuptools uses the MANIFEST.in from the root dir.  Make sure we are in the
# package dir.
os.chdir(THIS_DIRECTORY)


def get_config():
  """Get INI parser with version.ini data."""
  ini_path = os.path.join(THIS_DIRECTORY, "version.ini")
  if not os.path.exists(ini_path):
    ini_path = os.path.join(THIS_DIRECTORY, "../../../version.ini")
    if not os.path.exists(ini_path):
      raise RuntimeError("Couldn't find version.ini")

  config = configparser.SafeConfigParser()
  config.read(ini_path)
  return config


VERSION = get_config()


class Sdist(sdist):
  """Make a sdist release."""

  REQUIRED_TEMPLATES = [
      "GRR_maj.minor_amd64.exe.zip",
      "grr_maj.minor_amd64.deb.zip",
      "grr_maj.minor_amd64.xar.zip",
      "grr_maj.minor_amd64.rpm.zip",
  ]

  def CheckTemplates(self, base_dir, version):
    """Verify we have at least one template that matches maj.minor version."""
    major_minor = ".".join(version.split(".")[:2])
    templates = glob.glob(os.path.join(base_dir, f"templates/*{major_minor}*.zip"))
    required_templates = {
        x.replace("maj.minor", major_minor)
        for x in self.REQUIRED_TEMPLATES
    }

    # Client templates have an extra version digit, e.g. 3.1.0.0
    templates_present = {
        re.sub(f"_{major_minor}[^_]+_", f"_{major_minor}_", os.path.basename(x))
        for x in templates
    }

    if difference := required_templates - templates_present:
      raise RuntimeError(f"Missing templates {difference}")

  def run(self):
    base_dir = os.getcwd()
    self.CheckTemplates(base_dir, setup_args["version"])
    sdist.run(self)
    print("To upload a release, run upload.sh [version]")

  def make_release_tree(self, base_dir, files):
    sdist.make_release_tree(self, base_dir, files)
    sdist_version_ini = os.path.join(base_dir, "version.ini")
    if os.path.exists(sdist_version_ini):
      os.unlink(sdist_version_ini)
    shutil.copy(
        os.path.join(THIS_DIRECTORY, "../../../version.ini"), sdist_version_ini)


def find_data_files(source, prefix=None):
  result = []
  for directory, _, files in os.walk(source):
    files = [os.path.join(directory, x) for x in files]
    if prefix:
      result.append((os.path.join(prefix, directory), files))
    else:
      result.append((directory, files))

  return result


if "VIRTUAL_ENV" not in os.environ:
  print("*****************************************************")
  print("  WARNING: You are not installing in a virtual")
  print("  environment. This configuration is not supported!!!")
  print("  Expect breakage.")
  print("*****************************************************")

setup_args = dict(
    name="grr-response-templates",
    version=VERSION.get("Version", "packageversion"),
    description="GRR Rapid Response client templates",
    long_description=("This PyPi package is just a placeholder. The package"
                      " itself is too large to distribute on PyPi so it is "
                      "available from google cloud storage. See"
                      " https://github.com/google/grr-doc/blob/master/"
                      "installfrompip.adoc for installation instructions."),
    license="Apache License, Version 2.0",
    url="https://github.com/google/grr",
    data_files=(find_data_files("templates", prefix="grr-response-templates") +
                ["version.ini"]),
    cmdclass={
        "sdist": Sdist,
    },
)

setup(**setup_args)
