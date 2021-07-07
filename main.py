class DjangoDefault:
  """
    Set up Django Default files
  """

  def config_settings(self, project_name):
    with open('{}/settings.py'.format(project_name), 'a') as settings:
      settings.write('\n\n')
      settings.write('''
# Django Graphene Boilerplate Configurations
import os

from django.apps import AppConfig

AppConfig.default = False

# This apps should replace the Django Default one
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'graphene_django',
    '%s.apps.example'
]

GRAPHENE = {
    "SCHEMA": "%s.schema.schema",
    "MIDDLEWARE": [
        "graphql_jwt.middleware.JSONWebTokenMiddleware",
        "graphene_django.debug.DjangoDebugMiddleware",
        'graphene_django_extras.ExtraGraphQLDirectiveMiddleware'
    ],
    "SCHEMA_INDENT": 2,
}

# Add settings for authentication with graphql_jwt
AUTHENTICATION_BACKENDS = [
    'graphql_jwt.backends.JSONWebTokenBackend',
    'django.contrib.auth.backends.ModelBackend',
]

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, '%s/static/')
]

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

CORS_ORIGIN_ALLOW_ALL = True

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'\n

      ''' % (project_name, project_name, project_name))


def main():
  print('*****************************************************************************')
  print('*****************************************************************************')
  print('********************* Graphene Django Extra Boilerplate *********************') 
  print('*****************************************************************************')
  print('*****************************************************************************')
  import os
  import sys 
  import subprocess

  args = sys.argv[1:]
  name_index = args.index("--name")
  default = DjangoDefault()


  if len(args[name_index]):
    if len(sys.argv[1:][name_index + 1]) > 0:
      # print("Initializing your directory...")
      # os.system('pwd/{}'.format(args[name_index+1]))
      print('Creating virtual environment')
      venv = subprocess.run(["python3", "-m", "venv", "./venv/"])

      if venv.returncode == 0:
        print('Activating the virtual environment...')
        # os.system("")
        print('Installing dependencies...')
        os.system('source venv/bin/activate')
        subprocess.call("source ./venv/bin/activate", shell=True, executable='/bin/bash')
        print('Initializing git repository...')
        subprocess.run(["git", "init"])
        print('Add virtual environment folder to ignored folders')
        subprocess.run(["touch", ".gitignore"])
        print('Installing Graphene Django Extras...')
        subprocess.run(["python3", "-m", "pip", "install", "django"])
        subprocess.run(["python3", "-m", "pip", "install", "graphene-django"])
        subprocess.run(["python3", "-m", "pip", "install", "graphene-django-extras"])
        subprocess.run(["python3", "-m", "pip", "install", "django-graphql-jwt"])
        subprocess.run(["python3", "-m", "pip", "install", "django-cors-headers"])
        subprocess.run(["python3", "-m", "pip", "install", "whitenoise"])
        print('Initializing Django default structure...')
        subprocess.run(["django-admin", "startproject", "{}".format(args[name_index+1]), "."])
        print('Migrating Django Default Migrations')
        os.system("python3 manage.py migrate")
        print('Creating apps folder to hold all django apps')
        os.system("mkdir {}/apps".format(args[name_index+1]))
        print("Initializing example app for graphql implementation...")
        subprocess.run(["django-admin", "startapp", "example"])
        print("Moving the example app to apps folder")
        os.system("mv example boilerplate/apps/example")
        print('Writing Example Model of the created example app...')
        
        with open('{}/apps/example/models.py'.format(args[name_index+1]), 'a') as model:
          model.write('''
class Example(models.Model):
  example = models.CharField(
    max_length=200, null=True, blank=True)
  created_at = models.DateField(
    auto_now_add=True)

  class Meta:
    ordering = ['created_at']

          ''')
        
        print('Initialize app schema folder...')
        os.system('mkdir {}/apps/example/schema'.format(args[name_index+1]))
        print('Initialize graphql schema folder structure...')
        os.system('mkdir {}/apps/example/schema/mutations'.format(args[name_index+1]))
        os.system('mkdir {}/apps/example/schema/queries'.format(args[name_index+1]))
        os.system('mkdir {}/apps/example/schema/types'.format(args[name_index+1]))

        print('Adding example query...')
        os.system('touch {}/apps/example/schema/types/example_types.py'.format(args[name_index+1]))

        with open('{}/apps/example/schema/types/example_types.py'.format(args[name_index+1]), 'a') as types:
          types.write('''
# Example types
from graphene_django_extras import DjangoObjectType, DjangoInputObjectType, \
  DjangoListObjectType
from ...models import Example


class ExampleType(DjangoObjectType):
  class Meta:
    model = Example
    description = " Example type "

  @classmethod
  def get_queryset(cls, queryset, info):
      return queryset

class ExampleInputType(DjangoInputObjectType):
  class Meta:
    model = Example
    description = " Example Input type "


class ExampleListType(DjangoListObjectType):
  class Meta:
    model = Example
    description = " Example list type "

          ''')

        print('Adding example query...')
        os.system('touch {}/apps/example/schema/queries/example.py'.format(args[name_index+1]))

        with open('{}/apps/example/schema/queries/example.py'.format(args[name_index+1]), 'w') as queries:
          queries.write('''
# Example queries
import graphene
from graphene_django_extras import DjangoListObjectField
from ..types.example_types import ExampleListType

class Query(graphene.ObjectType):
  examples = DjangoListObjectField(
    ExampleListType, description=' Example list data ')
          
          ''')

        print('Adding example mutation...')
        os.system('touch {}/apps/example/schema/mutations/example.py'.format(args[name_index+1]))

        with open('{}/apps/example/schema/mutations/example.py'.format(
          args[name_index+1]), 'w') as mutation:
          mutation.write('''
# Example mutation

import graphene
from ...models import Example as ExampleModel
from ..types.example_types import ExampleInputType, \
  ExampleType

class Example(graphene.Mutation):
  """
  Example Mutation

  Args:
      new_example (obj): example object
  """
  success = graphene.String()
  example = graphene.Field(ExampleType)

  class Arguments:
    new_example = graphene.Argument(ExampleInputType)

  def mutate(self, info, **kwargs):
    success = 'Example created successfully'

    example = kwargs.get('new_example')

    example_instance = ExampleModel(
      example=example['example']
    )

    example_instance.save()

    return Example(success=success, example=example_instance)


class Mutation(graphene.ObjectType):
  create_example = Example.Field()

          ''')
        
        # configure schema file
        print('Configuring graphql schema file...')
        os.system('touch {}/schema.py'.format(args[name_index+1]))
        
        with open('{}/schema.py'.format(args[name_index+1]), 'a') as schemas:
          schemas.write('''
# Schema configurations    
import graphene
import graphql_jwt
from graphene_django.debug import DjangoDebug
from graphene_django_extras import all_directives

from .apps.example.schema.mutations.example import Mutation as ExampleMutations
from .apps.example.schema.queries.example import Query as ExampleQueries



class Query(ExampleQueries):
    debug = graphene.Field(DjangoDebug, name='_debug')
    pass


class Mutation(ExampleMutations):
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


schema = graphene.Schema(
    mutation=Mutation, query=Query, directives=all_directives)

          ''')

        # configure urls to get schemas
        print('Configuring urls...')
        os.system('echo "" > {}/urls.py'.format(args[name_index+1]))

        with open('{}/urls.py'.format(args[name_index+1]), 'w') as urls:
          urls.write('''
"""boilerplate URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView

#urlpatterns = [
#    path('admin/', admin.site.urls),
#]

urlpatterns = [
  path('admin/', admin.site.urls),
  path('graphql/', csrf_exempt(GraphQLView.as_view(graphiql=True)))
]

          ''')


        # configure .gitignore
        print('Configuring .gitignore')
        with open('.gitignore', 'w') as gitignore:
            gitignore.write('''
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
pip-wheel-metadata/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
#  Usually these files are written by a python script from a template
#  before PyInstaller builds the exe, so as to inject date/other infos into it.
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/

# Translations
*.mo
*.pot

# Django stuff:
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal

# Scrapy stuff:
.scrapy

# Sphinx documentation
docs/_build/

# PyBuilder
target/

# Jupyter Notebook
.ipynb_checkpoints

# IPython
profile_default/
ipython_config.py

# pyenv
.python-version

# pipenv
#   According to pypa/pipenv#598, it is recommended to include Pipfile.lock in version control.
#   However, in case of collaboration, if having platform-specific dependencies or dependencies
#   having no cross-platform support, pipenv may install dependencies that don't work, or not
#   install all needed dependencies.
#Pipfile.lock

# PEP 582; used by e.g. github.com/David-OConnor/pyflow
__pypackages__/

# Celery stuff
celerybeat-schedule
celerybeat.pid

# SageMath parsed files
*.sage.py

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# mkdocs documentation
/site

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Pyre type checker
.pyre/

# others
static/
.editorconfig
.vscode/
\n\n       
            ''')
            gitignore.write("manage.py\n")
            gitignore.write("requirements.txt\n")

        project_name = '{}'.format(args[name_index+1])

        print('Configuring Django Settings...')
        default.config_settings(project_name)
        os.system('pip freeze > requirements.txt')
        os.system('python3 manage.py makemigrations')
        os.system('python3 manage.py migrate')
        os.system('python3 manage.py runserver')

main()