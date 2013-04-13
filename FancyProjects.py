# Copyright (C) 2013 Christopher "Kasoki" Kaster
#
# This file is part of "FancyProjects". <http://github.com/Kasoki/FancyProjects>
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, 
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
# PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
import sublime
import sublime_plugin
import os
import json
from fancyprojects.project_structure import ProjectStructure
from shutil import copytree

# This command creates a new project
class FancyProjectsCreateNewProjectCommand(sublime_plugin.WindowCommand):
	def run(self):
		# load all settings
		settings = sublime.load_settings("FancyProjects.sublime-settings")
		self.template_path = settings.get("project_template_directory")
		self.user_project_path = settings.get("user_project_directory")
		self.use_sublime_project_format = settings.get("use_sublime_project_format")
		self.use_counter_if_project_folder_already_exists = settings.get("use_counter_if_project_folder_already_exists")

		# insert packages path
		self.template_path = self.template_path.replace("${packages}", sublime.packages_path())
		self.template_path = self.template_path.replace("${home}", os.path.expanduser("~"))

		# insert home path
		self.user_project_path = self.user_project_path.replace("${packages}", sublime.packages_path())
		self.user_project_path = self.user_project_path.replace("${home}", os.path.expanduser("~"))

		# get the content of the template folder
		template_folder_content = os.listdir(self.template_path)

		template_folder_items = []

		# get .fancyproj files
		for item in template_folder_content:
			if item.split(".")[-1] == "fancyproj":
				template_folder_items.append(item)


		# create instances of ProjectStructure from the .fancyproj file list
		self.project_structures = []

		for template_item in template_folder_items:
			if not os.path.exists(os.path.join(self.template_path, template_item, "fancyproj.json")):
				sublime.error_message("ERROR: %s is invalid" % template_item)
				return

			json_object = json.load(open("%s/%s/fancyproj.json" % (self.template_path, template_item)))
			project_structure = ProjectStructure(os.path.join(self.template_path, template_item), json_object)

			self.project_structures.append(project_structure)

		# create a list with all templates
		self.quickpanel_template_list = []

		for project_template in self.project_structures:
			self.quickpanel_template_list.append(project_template.to_quickpanel_item())

		self.window.show_quick_panel(self.quickpanel_template_list, self.on_picked_template)

	def on_picked_template(self, picked_item_index):
		# picked_item_index is -1 if the user cancels their action
		if picked_item_index < 0:
			return

		self.picked_project_structure = self.project_structures[picked_item_index]

		self.window.show_input_panel("Enter Project Name: ", self.picked_project_structure.default_project_name,
			self.on_picked_project_name, None, self.on_cancel)

	def on_picked_project_name(self, new_project_name):
		self.create_project(self.picked_project_structure, new_project_name)

	def on_cancel(self):
		return

	def create_project(self, project_structure, new_project_name):
		# if the user wants to use the sublime project format, the project file should be a directory below
		# the actual project
		project_subfolder = ""

		if self.use_sublime_project_format:
			project_subfolder = new_project_name

		# define the paths, which are used for copy
		source = os.path.join(project_structure.path, "contents")
		self.project_folder = os.path.join(self.user_project_path, new_project_name)
		destination = os.path.join(self.user_project_path, new_project_name, project_subfolder)

		# decide how the files should be copied
		if os.path.exists(self.project_folder) and not self.use_counter_if_project_folder_already_exists:
			sublime.error_message("Project %s already exists!" % new_project_name)
		elif os.path.exists(self.project_folder) and self.use_counter_if_project_folder_already_exists:
			counter = 2

			solution_found = False

			while not solution_found:
				new_project_name_with_counter = "%s%s" % (new_project_name, counter)

				if self.use_sublime_project_format:
					project_subfolder = new_project_name_with_counter
					
				self.project_folder = os.path.join(self.user_project_path, new_project_name_with_counter)
				destination = os.path.join(self.user_project_path, new_project_name_with_counter, project_subfolder)

				if os.path.exists(self.project_folder):
					counter += 1
				else:
					self.copy_folder(source, destination, new_project_name_with_counter)
					solution_found = True
		else:
			self.copy_folder(source, destination, new_project_name)

	def copy_folder(self, source, destination, project_name):
		copytree(source, destination)

		if self.use_sublime_project_format:
			self.create_project_file(project_name)

	def create_project_file(self, project_name):
		f = open(os.path.join(self.project_folder, "%s.sublime-project" % project_name), "w+")

		settings = ""

		for item in self.picked_project_structure.settings:
			value = self.picked_project_structure.settings[item]
			settings += "\"%s\": %s," % (item, "\"%s\"" % value if isinstance(value, str) else value)

		if settings.endswith(","):
			settings = settings[:-1]

		build_systems = ""

		for bsystem in self.picked_project_structure.build_systems:
			build_systems += "{"

			for item in bsystem:
				value = bsystem[item]
				print value, type(value)
				build_systems += "\"%s\": %s," % (item, "\"%s\"" % value if isinstance(value, unicode) or isinstance(value, str) else value)

			if build_systems.endswith(","):
				build_systems = build_systems[:-1]

			build_systems += "},"

		if build_systems.endswith(","):
			build_systems = build_systems[:-1]

		f.write("{\"folders\":[{\"path\":\"%s\"}], \"settings\":{%s}, \"build_systems\":[%s]}" % (project_name, settings, build_systems))
		f.close()

# This command opens the template folder
class FancyProjectsOpenTemplateFolderCommand(sublime_plugin.WindowCommand):
	def run(self):
		settings = sublime.load_settings("FancyProjects.sublime-settings")
		self.template_path = settings.get("project_template_directory")
		self.window.run_command("open_dir", {"dir": self.template_path})