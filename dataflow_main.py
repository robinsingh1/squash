from __future__ import absolute_import
import os
"""A Julia set computing workflow: https://en.wikipedia.org/wiki/Julia_set.

This example has in the juliaset/ folder all the code needed to execute the
workflow. It is organized in this way so that it can be packaged as a Python
package and later installed in the VM workers executing the job. The root
directory for the example contains just a "driver" script to launch the job
and the setup.py file needed to create a package.

The advantages for organizing the code is that large projects will naturally
evolve beyond just one module and you will have to make sure the additional
modules are present in the worker.

In Python Dataflow, using the --setup_file option when submitting a job, will
trigger creating a source distribution (as if running python setup.py sdist) and
then staging the resulting tarball in the staging area. The workers, upon
startup, will install the tarball.

Below is a complete command line for running the juliaset workflow remotely as
an example:

python juliaset_main.py \
  --job_name juliaset-$USER \
  --project YOUR-PROJECT \
  --runner DataflowRunner \
  --setup_file ./setup.py \
  --staging_location gs://YOUR-BUCKET/juliaset/staging \
  --temp_location gs://YOUR-BUCKET/juliaset/temp \
  --coordinate_output gs://YOUR-BUCKET/juliaset/out \
  --grid_size 20

"""
from extract_answers.extract_answers import extract_answers
#from mod_interact import question_generation
from question_generation.mod_interact import question_generation
from question_answering.mod_run_squad import run_squad
#from combine_qa import combine_qa

import argparse
from builtins import range

import apache_beam as beam
from apache_beam.io import WriteToText

# pytype: skip-file


import logging
import os

#from apache_beam.examples.complete.juliaset.juliaset import juliaset
#from juliaset import run

def directory_structure(test):
  import os
  import subprocess
  ls = subprocess.check_output(["ls"])
  ls1 = subprocess.check_output(["/usr/local/lib/python3.5/site-packages/dataflow_worker"])
  ls2 = subprocess.check_output(["/usr/local/lib/python3.5/site-packages/"])
  ls3 = subprocess.check_output(["/usr/local/lib/python3.5/"])
  ls4 = subprocess.check_output(["/home/"])
  dir_path = os.path.dirname(os.path.realpath(__file__))

  SAVED_MODEL_DIR="gpt2_corefs_question_generation"
  model_checkpoint1 = os.path.join(dir_path, SAVED_MODEL_DIR)
  SAVED_MODEL_DIR="question_generation/gpt2_corefs_question_generation"
  model_checkpoint2 = os.path.join(dir_path, SAVED_MODEL_DIR)
  print(dir_path)
  print(model_checkpoint1)
  print(model_checkpoint2)
  logging.info(dir_path)
  logging.info(model_checkpoint1)
  logging.info(model_checkpoint2)
  logging.info(ls1)
  logging.info(ls2)
  logging.info(ls3)
  logging.info(ls4)
  logging.info("path exists {0}".format(os.path.exists(model_checkpoint1)))
  logging.info("path exists {0}".format(os.path.exists(model_checkpoint2)))
  logging.info(ls)
  return test

if __name__ == '__main__':
  logging.getLogger().setLevel(logging.INFO)
  parser = argparse.ArgumentParser()
  known_args, pipeline_args = parser.parse_known_args()
  # download and run fule
  with beam.Pipeline(argv=pipeline_args) as p:
      """
			lines = p | "Create" >> beam.Create(["cat dog", "snake cat", "dog cat cat"])
      counts = (
        lines 
        | "Squash" >> beam.Map()
        #| "Wrie" >> beam.write()
      )
      """
      data = [{"input_text": "Upon graduation, he declared for the 1996 NBA draft and was selected by the Charlotte Hornets with the 13th overall pick", "key": "test_123", "timestamp": "2020-03-14 22:00:54.296257", "settings": {"top_p": 0.9, "gen_frac": 0.5, "spec_frac": 0.8}}]
      #lines = p | "Create" >> beam.Create(["cat dog", "snake cat", "dog cat cat"])
      lines = p | "Create" >> beam.Create(data)
      GCS_BUCKET = "gs://ds-playground/squash-dataflow/"
      counts = (
          lines 
          #| "Extract Answers" >> beam.Map(extract_answers)
      #    | "Generated Questions" >> beam.Map(question_generation)
          | "Test Path" >> beam.Map(directory_structure)
          #| "Generated Answers" >> beam.Map(run_squad)
          #| "Write to GCS" >> beam.io.WriteToText(GCS_BUCKET)
          | beam.Map(print)
      )
