# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nemesis',
 'nemesis.resources',
 'nemesis.resources.elasticsearch',
 'nemesis.schemas',
 'nemesis.schemas.elasticsearch',
 'nemesis.scripts',
 'nemesis.templates',
 'nemesis.tests',
 'nemesis.tests.resources.elasticsearch']

package_data = \
{'': ['*']}

install_requires = \
['Click>=7.1,<7.2',
 'dacite>=1.6.0,<2.0.0',
 'deepdiff>=5.6.0,<6.0.0',
 'elasticsearch>=7.15.2,<8.0.0',
 'marshmallow>=3.14.1,<4.0.0',
 'python-dateutil>=2.8.2,<3.0.0',
 'pytz>=2021.3,<2022.0',
 'requests>=2.26.0,<3.0.0',
 'rich>=10.14.0,<11.0.0',
 'sphinx-rtd-theme>=1.0.0,<2.0.0']

extras_require = \
{':extra == "docs"': ['Sphinx>=4.4.0,<5.0.0']}

entry_points = \
{'console_scripts': ['nemesis = nemesis.scripts.nemesis:cli']}

setup_kwargs = {
    'name': 'nemesis',
    'version': '0.0.9',
    'description': 'Tool for managing Elasticsearch resources as code',
    'long_description': '# Nemesis ![tests-badge](https://github.com/fxdgear/nemesis/actions/workflows/python-app.yml/badge.svg)\n\nNemesis is a python library to manage Elasticsearch resources as code. Nemesis operates\na lot more like Pulumi than terraform. Each resource that nemesis supports is an actual\npython object which can be used like any other python object.\n\nElasticsearch resources can be crafted as Python objects.\nElasticsearch resources can be fetched from the Elasticsearch cluster and diffed against local versions.\nDeployments can happen if a remote resource doesn\'t exist.\nDeployments can happen if a local_resource is registered with force=True, to force updating of the\nresource even if it hasn\'t changed.\n\nCreating new resources is not trivial at this point in time.\nIt\'s difficult because, to create the resource you first need to define the dataclass and all the attributes on that class.\nNext you would need to define the Schema for that resource, then you would need to define all the CRUD method for that resource.\nThere\'s no automated way to do this. But would be nice to create a code generator to scan the Elasticsearch repo and pull out the various resources and their types so they can be created in Nemesis.\n\nPull requests for new resources added to nemesis would be greatly appriciated!\n\n## Getting started.\n\n### Installation\nFirst to get started you must install `nemesis`:\n\n```\npip install nemesis\n```\n\n### Creating your first nemesis project\n\nFirst create the directory you want to put your nemesis project into:\n\n```\n$ mkdir my_first_project\n$ cd my_first_project\n$ nemesis new\n```\n\n### The __nemesis__.py file\n\nAfter you run the `nemesis new` command a newly created __nemesis__.py file will exist. This file has some example code in it to help you get started.\n\n1. instantiate the `Nemesis` object as the variable `n`.\n2. using the `nemesis.resources.elasticsearch.*` modules create your ES resources\n3. `register` those resources with the `Nemesis` client. `n.register(my_resource_name)`\n\n### Help\n\nRunning the `--help` flag will give you help on any command or subcommand.\n\n```\n> nemesis --help\nUsage: nemesis [OPTIONS] COMMAND1 [ARGS]... [COMMAND2 [ARGS]...]...\n\n  Nemesis CLI\n\nOptions:\n  --help  Show this message and exit.\n\nCommands:\n  launch   Deploy resources to Elasticsearch\n  new      Create a new nemesis deployment\n  preview  Preview the resources to deployed\n```\n\n\n### Preview\n\nRun `nemesis preview` to see what will be deployed to Elasticsearch.\n\nThis will render a diff to tell you what\'s going to be created or changed.\n\n### Launch\n\nRun `nemesis launch` to deploy your changes.\n\nThis will actually ship your resources to Elasticsearch\n\n---\n\n# Additional features\n\n## Pre/Post deploy hooks.\nnemesis supports pre and post deploy hooks. This is useful in various situations:\n\n1. You are creating an ingest pipeline and you want to run some tests to ensure your pipeline works before the pipeline is deployed.\nYou can write a function to call `resource.simulate` on  your pipeline resource.\n2. You have a transform you want to "reset". You can define a "predeploy" function to "stop" the current transform,\n  delete the current dest index, and then recreate the dest index. then define a "postdeploy" function which will start the transform\n3. Watchers can be "simulated" using the "execute" api. This unfortunatly only works on watchers that exist already, but you can deploy the watcher and then write a post-deploy\ntest that will ensure your watcher works as expected.\n4. Your imagination is the limit on things you might want to do before and/or after something has been deployed\n\n---\n\n# Diffing elasticsearch resources\n\nNemesis supports deep diffing of resources with a succinct mode and verbose mode.\n\nExample of a "succinct" diff:\n\n```\n> nemesis launch -y\nHello Nemesis!\n                             Preview resources to be deployed\n┏━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┓\n┃ Resource         ┃ Name                             ┃  Action   ┃                 Diff ┃\n┡━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━┩\n│ IndexTemplate    │ index_template_billing_aggregate │  create   │ + [\'index_patterns\'] │\n│                  │                                  │           │       + [\'template\'] │\n│                  │                                  │           │        + [\'version\'] │\n├──────────────────┼──────────────────────────────────┼───────────┼──────────────────────┤\n│ IngestPipeline   │ total_cost                       │  create   │             + [\'id\'] │\n│                  │                                  │           │     + [\'processors\'] │\n│                  │                                  │           │    + [\'description\'] │\n│                  │                                  │           │        + [\'version\'] │\n├──────────────────┼──────────────────────────────────┼───────────┼──────────────────────┤\n│ Transform        │ total_cost_2021_12               │  create   │         + [\'source\'] │\n│                  │                                  │           │           + [\'dest\'] │\n│                  │                                  │           │             + [\'id\'] │\n│                  │                                  │           │          + [\'pivot\'] │\n│                  │                                  │           │    + [\'description\'] │\n│                  │                                  │           │      + \'frequency\'] │\n├──────────────────┼──────────────────────────────────┼───────────┼──────────────────────┤\n│ LogstashPipeline │ test_logstash_pipeline           │  update   │  ~ [\'last_modified\'] │\n├──────────────────┼──────────────────────────────────┼───────────┼──────────────────────┤\n│ Role             │ test-role                        │ unchanged │                      │\n├──────────────────┼──────────────────────────────────┼───────────┼──────────────────────┤\n│ RoleMapping      │ test_role_mapping                │ unchanged │                      │\n├──────────────────┼──────────────────────────────────┼───────────┼──────────────────────┤\n│ Watch            │ test-watch                       │ unchanged │                      │\n└──────────────────┴──────────────────────────────────┴───────────┴──────────────────────┘\n\nResources:\n        Creating: 3\n        Updating: 1\n        Unchanged: 3\n```\n\nAnd an example of a verbose diff:\n```\n> nemesis launch -v\nHello Nemesis!\n────────────────────────────────────────────────────────────────────────────────────────────────────────\n Preview IndexTemplate(index_template_billing_aggregate)\n┏━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓\n┃ Field               ┃ Value                           ┃\n┡━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩\n│ [\'index_patterns\']  │ + [                             │\n│                     │   "billing_aggregate_*"         │\n│                     │ ]                               │\n│ [\'template\']        │ + {                             │\n│                     │   "settings": {                 │\n│                     │     "index": {                  │\n│                     │       "number_of_shards": "1",  │\n│                     │       "number_of_replicas": "1" │\n│                     │     }                           │\n│                     │   },                            │\n│                     │   "mappings": {                 │\n│                     │     "_source": {                │\n│                     │       "enabled": true           │\n│                     │     },                          │\n│                     │     "properties": {             │\n│                     │       "@timestamp": {           │\n│                     │         "type": "date"          │\n│                     │       },                        │\n│                     │       "@version": {             │\n│                     │         "type": "text"          │\n│                     │       },                        │\n│                     │       "cloud_provider": {       │\n│                     │         "type": "keyword"       │\n│                     │       },                        │\n│                     │       "sum_total": {            │\n│                     │         "type": "float"         │\n│                     │       },                        │\n│                     │       "team_name": {            │\n│                     │         "type": "keyword"       │\n│                     │       }                         │\n│                     │     }                           │\n│                     │   }                             │\n│                     │ }                               │\n│ [\'version\']         │ + 3                             │\n└─────────────────────┴─────────────────────────────────┘\n```\n',
    'author': 'Nick Lang',
    'author_email': 'nick@nicklang.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/fxdgear/nemesis',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
