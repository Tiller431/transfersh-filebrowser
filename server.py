from bottle import Bottle, run, static_file
import os
from pathlib import Path
from os import listdir
from os.path import isfile, join


datadir = "data"
app = Bottle()


def sorted_ls(path):
    mtime = lambda f: os.stat(os.path.join(path, f)).st_mtime
    return list(sorted(os.listdir(path), key=mtime))


@app.route('/')
def main():
  response = """<!DOCTYPE html>
  <html>
  <body>
    <div>"""

  folders = []
  cwd = os.getcwd()
  sortedFolders = sorted_ls(datadir)[::-1]
  for folder in sortedFolders:
    folderpath = cwd + "/" + datadir + "/" + folder
    files = os.listdir(folderpath)
    response += "<div><a href=\"/download/{fo}/{fi}\">/{fo}/{fi}</a></div>\n".format(fo=folder, fi=files[0])

  response += """  </div>
  </body>
  </html>"""
  return response

@app.route("/download/<folder>/<file>")
def download(folder, file):
  return static_file(file, root=datadir + "/" + folder)


run(app, host='localhost', port=8080)