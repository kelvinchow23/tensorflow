from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import csv
import json
import os
import random

KELVIN = True
LABEL_NAME = "gesture"
DATA_NAME = "accel_ms2_xyz"
DATA_SUPP_NAME = "gyro_ms2_xyz"
#folders = ["wing", "ring", "slope"]
folders = ["training-data"]
#names = [
#    "hyw", "shiyun", "tangsy", "dengyl", "zhangxy", "pengxl", "liucx",
#    "jiangyh", "xunkai"
#]


def prepare_original_data(folder, idx, data, file_to_read):  # pylint: disable=redefined-outer-name
  """Read collected data from files."""
  if folder == "training-data":
    with open(file_to_read, "r") as f:
      lines = csv.reader(f)
      data_new = {}
      data_new[LABEL_NAME] = "a"
      data_new[DATA_NAME] = []
      data_new[DATA_SUPP_NAME] = []

      for idx, line in enumerate(lines):  # pylint: disable=unused-variable,redefined-outer-name
        if len(line[0]) != 1 and data_new[DATA_NAME]:
          data.append(data_new)
          data_new = {}
          data_new[LABEL_NAME] = line[0][13]
          data_new[DATA_NAME] = []
          data_new[DATA_SUPP_NAME] = []
          #data_new["name"] = line[0][13]
        elif len(line) == 11 and len(line[0]) == 1:
          #print("line: %s and length: %d" % (line[0], len(line[0])))
          data_new[DATA_NAME].append([float(i) for i in line[2:5]])
          data_new[DATA_SUPP_NAME].append([float(i) for i in line[5:8]])
      data.append(data_new)

  elif folder == "training-flourish":
    with open(file_to_read, "r") as f:
      lines = csv.reader(f)
      for idx, line in enumerate(lines):  # pylint: disable=unused-variable,redefined-outer-name
        data_new = {}
        if len(line[2]) == 1:
          data_new[LABEL_NAME] = line[2]
          data_new[DATA_NAME] = []
          parse_data = line[4].split('\n')
          for x, entry in enumerate(parse_data):
            separated_line = entry.split(',')
            data_new[DATA_NAME].append([float(i) for i in separated_line[1:4]])
          data.append(data_new)

  else:
    with open(file_to_read, "r") as f:
      lines = csv.reader(f)
      data_new = {}
      data_new[LABEL_NAME] = folder
      data_new[DATA_NAME] = []
      data_new["name"] = "negative%d" % (idx + 1)
      for idx, line in enumerate(lines):
        if len(line) == 3 and line[2] != "-":
          if len(data_new[DATA_NAME]) == 120:
            data.append(data_new)
            data_new = {}
            data_new[LABEL_NAME] = folder
            data_new[DATA_NAME] = []
            data_new["name"] = "negative%d" % (idx + 1)
          else:
            data_new[DATA_NAME].append([float(i) for i in line[0:3]])
      data.append(data_new)


def generate_negative_data(data):  # pylint: disable=redefined-outer-name
  """Generate negative data labeled as 'negative6~8'."""
  # Big movement -> around straight line
  for i in range(100):
    if i > 80:
      dic = {DATA_NAME: [], LABEL_NAME: "negative", "name": "negative8"}
    elif i > 60:
      dic = {DATA_NAME: [], LABEL_NAME: "negative", "name": "negative7"}
    else:
      dic = {DATA_NAME: [], LABEL_NAME: "negative", "name": "negative6"}
    start_x = (random.random() - 0.5) * 2000
    start_y = (random.random() - 0.5) * 2000
    start_z = (random.random() - 0.5) * 2000
    x_increase = (random.random() - 0.5) * 10
    y_increase = (random.random() - 0.5) * 10
    z_increase = (random.random() - 0.5) * 10
    for j in range(128):
      dic[DATA_NAME].append([
          start_x + j * x_increase + (random.random() - 0.5) * 6,
          start_y + j * y_increase + (random.random() - 0.5) * 6,
          start_z + j * z_increase + (random.random() - 0.5) * 6
      ])
    data.append(dic)
  # Random
  for i in range(100):
    if i > 80:
      dic = {DATA_NAME: [], LABEL_NAME: "negative", "name": "negative8"}
    elif i > 60:
      dic = {DATA_NAME: [], LABEL_NAME: "negative", "name": "negative7"}
    else:
      dic = {DATA_NAME: [], LABEL_NAME: "negative", "name": "negative6"}
    for j in range(128):
      dic[DATA_NAME].append([(random.random() - 0.5) * 1000,
                             (random.random() - 0.5) * 1000,
                             (random.random() - 0.5) * 1000])
    data.append(dic)
  # Stay still
  for i in range(100):
    if i > 80:
      dic = {DATA_NAME: [], LABEL_NAME: "negative", "name": "negative8"}
    elif i > 60:
      dic = {DATA_NAME: [], LABEL_NAME: "negative", "name": "negative7"}
    else:
      dic = {DATA_NAME: [], LABEL_NAME: "negative", "name": "negative6"}
    start_x = (random.random() - 0.5) * 2000
    start_y = (random.random() - 0.5) * 2000
    start_z = (random.random() - 0.5) * 2000
    for j in range(128):
      dic[DATA_NAME].append([
          start_x + (random.random() - 0.5) * 40,
          start_y + (random.random() - 0.5) * 40,
          start_z + (random.random() - 0.5) * 40
      ])
    data.append(dic)


# Write data to file
def write_data(data_to_write, path):
  with open(path, "w") as f:
    for idx, item in enumerate(data_to_write):  # pylint: disable=unused-variable,redefined-outer-name
      dic = json.dumps(item, ensure_ascii=False)
      f.write(dic)
      f.write("\n")


if __name__ == "__main__":
  data = []  # pylint: disable=redefined-outer-name
  for idx1, folder in enumerate(folders):
    directories = os.listdir("./%s/" % folder)
    for idx2, file in enumerate(directories):
      prepare_original_data(folder, idx2, data, "./%s/%s" % (folder,file))
  for idx in range(5):
    prepare_original_data("negative", idx, data,
                          "./negative/output_negative_%d.txt" % (idx + 1))
  generate_negative_data(data)
  print("data_length: " + str(len(data)))
  if not os.path.exists("./data"):
    os.makedirs("./data")
  write_data(data, "./data/complete_data")
