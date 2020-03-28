from __future__ import absolute_import
from __future__ import division
import sys
import os
import logging

from extract_answers.extract_answers import extract_answers
#from mod_interact import question_generation
from question_generation.mod_interact import question_generation
from question_answering.mod_run_squad import run_squad
#from combine_qa import combine_qa

import argparse
from builtins import range

import apache_beam as beam
from apache_beam.io import WriteToText



def from_pixel(x, y, n):
  """Converts a NxN pixel position to a (-1..1, -1..1) complex number."""
  return complex(2.0 * x / n - 1.0, 2.0 * y / n - 1.0)


def get_julia_set_point_color(element, c, n, max_iterations):
  """Given an pixel, convert it into a point in our julia set."""
  x, y = element
  z = from_pixel(x, y, n)
  for i in range(max_iterations):
    if z.real * z.real + z.imag * z.imag > 2.0:
      break
    z = z * z + c
  return x, y, i  # pylint: disable=undefined-loop-variable


def generate_julia_set_colors(pipeline, c, n, max_iterations):
  """Compute julia set coordinates for each point in our set."""
  def point_set(n):
    for x in range(n):
      for y in range(n):
        yield (x, y)

  julia_set_colors = (
      pipeline
      | 'add points' >> beam.Create(point_set(n))
      | beam.Map(get_julia_set_point_color, c, n, max_iterations))

  return julia_set_colors


def generate_julia_set_visualization(data, n, max_iterations):
  """Generate the pixel matrix for rendering the julia set as an image."""
  import numpy as np  # pylint: disable=wrong-import-order, wrong-import-position
  colors = []
  for r in range(0, 256, 16):
    for g in range(0, 256, 16):
      for b in range(0, 256, 16):
        colors.append((r, g, b))

  xy = np.zeros((n, n, 3), dtype=np.uint8)
  for x, y, iteration in data:
    xy[x, y] = colors[iteration * len(colors) // max_iterations]

  return xy


def save_julia_set_visualization(out_file, image_array):
  """Save the fractal image of our julia set as a png."""
  from matplotlib import pyplot as plt  # pylint: disable=wrong-import-order, wrong-import-position
  plt.imsave(out_file, image_array, format='png')

def directory_structure(test):
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
  logging.info("path exists {0}".format(os.path.exists(model_checkpoint1)))
  logging.info("path exists {0}".format(os.path.exists(model_checkpoint2)))
  return test



def run(argv=None):  # pylint: disable=missing-docstring
  parser = argparse.ArgumentParser()
  parser.add_argument(
      '--grid_size',
      dest='grid_size',
      default=1000,
      help='Size of the NxN matrix')
  parser.add_argument(
      '--coordinate_output',
      dest='coordinate_output',
      required=True,
      help='Output file to write the color coordinates of the image to.')
  parser.add_argument(
      '--image_output',
      dest='image_output',
      default=None,
      help='Output file to write the resulting image to.')
  known_args, pipeline_args = parser.parse_known_args(argv)

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
