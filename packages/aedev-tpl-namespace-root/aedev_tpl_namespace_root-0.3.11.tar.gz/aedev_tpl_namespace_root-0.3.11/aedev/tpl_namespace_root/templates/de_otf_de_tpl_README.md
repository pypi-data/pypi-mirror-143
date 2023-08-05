# __{namespace_name}__ {project_type} project

{project_desc}


## {namespace_name} namespace root package use-cases

this project is maintaining the portions (modules and sub-packages) of the {namespace_name} namespace to:

* bulk refactor multiple portions of this namespace simultaneously using the [grm children actions](
https://aedev.readthedocs.io/en/latest/man/git_repo_manager.html "git_repo_manager manual")
* update and deploy common outsourced files, optionally generated from templates
* merge docstrings of all portions into a single combined and cross-linked documentation
* publish documentation via Sphinx onto [ReadTheDocs]({docs_root} "{namespace_name} on RTD")

this {project_type} package is only needed for development tasks, so never add it to the installation requirements
file ({REQ_FILE_NAME}) of a project.

to ensure the update and deployment of outsourced files generated from the templates provided by this root package via
the [git repository manager tool](https://github.com/aedev-group/aedev_git_repo_manager), add this root package to the
development requirements file ({REQ_DEV_FILE_NAME}) of a portion project of this namespace.


## installation

to use this root package first clone it to your local machine and then install it as editable package with `pip`::

   cd projects-parent-folder
   git clone {repo_root}
   pip install -e {namespace_name}_{namespace_name}


## namespace portions

the following {len(portions_pypi_refs_md)} portions are currently included in this namespace:

{portions_pypi_refs_md}
