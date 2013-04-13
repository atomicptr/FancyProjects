FancyProjects
=============

A Sublime Text plug-in which allows you to create any kind of project from your own custom templates.

Installation
------------

### Package Control:

1. Install [Package Control](http://wbond.net/sublime_packages/package_control)
1. From within Package Control look for "Fancy Projects" and install it.

### Manual:

1. Clone or download this repository
1. Create a folder "FancyProjects", put the files you downloaded earlier into this folder
1. Move the folder "FancyProjects" into your Sublime Text packages folder. If you're not sure where your Packages folder is, use the menu shortcut `Preferences/Browse Packages…`

Usage
-----

1. Invoke the Quick Panel (usually CMD/Ctrl+Shift+P)
1. Enter "create" (Which should show you the following option: "Fancy Projects: Create new project")
1. Select a project template
1. and select a new name for it
1. Done! There should be a new project folder in your "Project folder directory" (Default: HOME_FOLDER/Projects, you can change this! Instructions below)

Configuration
-------------

### Open your FancyProjects settings

There are multiple ways to do this:
* Via menu: `Project -> FancyProject: Preferences -> Preferences - User`
* Via quick panel: Enter into your quick panel "Fancy Projects Settings - User"

**Remember**: This is JSON so use the curly brackets! :P

### Project template directory

Add to your settings file:

    {
		"project_template_directory": "path/to/templates"
    }

The default path is: `${packages}/FancyProjects/templates`

### User project directory

Add to your settings file:

    {
	    "user_project_directory": "path/to/project/folder"
    }

**Note**: You can use ${home} to get your home directory!

The default path is `${home}/Projects`

### Use Sublime project format

If you set this to true your new project folder will be like this:

	NewProject/
		NewProject/
			stuff...
		NewProject.sublime-project

If this setting is false your new project folder will look like this:

	NewProject/
		stuff…

Add to your settings file:

    {
	    "use_sublime_project_format": false
    }

The default setting is `true`

### Use counter if project folder already exists

If this option is set to false Sublime Text will print an error message if you want to create a project folder which already exists. To prevent this, this option will add a counter to the name of your project.

Add to your settings file:

    {
	    "use_counter_if_project_folder_already_exists": false
    }

The default setting is `true`


Create new templates
--------------------

### Open template folder

To create a new template open your template folder. You can access your template folder via quick panel ("Fancy Projects: Open template folder") or via menu (`Projects -> Fancy Projects: Open template folder`)

### A template structure

Now lets look at the structure of a template:

	name.fancyproj/
		contents/
			stuff...
		fancyproj.json

**name.fancyproj/**: This is the template container
**contents/**: You need to store all project-related stuff in this folder
**fancyproj.json**: This file contains project specific settings

### The fancyproj.json file

	{
		"name": "Foo project",
		"description": "This is an example project.",
		"default_project_name": "FoobarProject",

		"settings": {
			"tab_size": 8,
			"translate_tabs_to_spaces": true
		},

		"build_systems": [
			{
				"name": "List files",
				"cmd": "ls"
			}
		]
	}

* **name**: The name of your project template
* **description**: A description what this project is
* **default_project_name**: The default name for a new project
* **settings**: You can set project-specific settings here. (For more information look at this site: [Settings](http://www.sublimetext.com/docs/2/settings.html))
* **build_systems**: You can add several project-related build systems. (For more information look at this site: [Build Systems](http://docs.sublimetext.info/en/latest/file_processing/build_systems.html))

Licence
-------

FancyProjects is licenced under the terms of the MIT license, which means you have without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software. [For more information please read this](http://opensource.org/licenses/MIT)

Questions?
-----------------

If there are any questions feel free to contact me via [mail](mailto:ikasoki@gmail.com) or [Twitter](https://twitter.com/Kasoki)
