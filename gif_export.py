#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Inkscape extension to export objects as GIF
"""

import inkex
import tempfile
import subprocess
import os
from PIL import Image

class GifExport(inkex.Effect):
	def __init__(self):
		inkex.Effect.__init__(self)
		self.arg_parser.add_argument(
			'-f', '--folder',
			type=str,
			dest='folder',
			help='Folder name'
			)
		self.arg_parser.add_argument(
			'-n', '--name',
			type=str,
			dest='name',
			help='GIF name'
			)
		self.arg_parser.add_argument(
			'-r', '--reverse',
			type=bool,
			dest='reverse',
			help='Reverse the order of the objects'
			)
		self.arg_parser.add_argument(
			'-l', '--loop',
			type=int,
			dest='loop',
			help='Number of loops, use 0 for infinite'
			)
		self.arg_parser.add_argument(
			'-d', '--duration',
			type=int,
			dest='duration',
			help='Duration in ms'
			)

	def effect(self):
		inkex.errormsg(f'loop: {self.options.loop}, duration: {self.options.duration}')
		svg_fd, svg_tmpfile = tempfile.mkstemp(suffix='.svg')
		self.document.write(svg_tmpfile)

		if len(self.options.ids) < 2:
			inkex.errormsg('Too few objects selected')
			exit()

		frames = []
		for i, obj_id in enumerate(self.options.ids):
			png_fd, png_tmpfile = tempfile.mkstemp(suffix='.png')
			subprocess.run(['inkscape', '--vacuum-defs', f'--export-id={obj_id}', '--export-id-only', f'--export-filename={png_tmpfile}', svg_tmpfile])
			frames.append(Image.open(png_tmpfile))

		path = os.path.expanduser('~/Documents/Exports/') + self.options.folder + '/'
		if not os.path.exists(path):
			os.makedirs(path)
		filename = path + self.options.name
		if filename[-4:] != '.gif':
			filename += '.gif'
		if self.options.reverse:
			frames.reverse()
		frames[0].save(filename, append_images=frames[1:], save_all=True, duration=self.options.duration, loop=self.options.loop)
		inkex.errormsg('GIF exported')

if __name__ == '__main__':
	exporter = GifExport()
	exporter.run()
