class DjangoDefault:
  """
    Set up Django Default files
  """

  def config_settings(self, project_name):
    with open('{}/settings.py'.format(project_name), 'a') as settings:
      settings.write('\n')
      settings.write('# Django Graphene Boilerplate Configurations\n')
      settings.write('import os\n\n')
      settings.write('''

# This apps should replace the Django Default ones on top 

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'graphene_django',
]

GRAPHENE = {
    "SCHEMA": "%s.schema.schema",
    "MIDDLEWARE": [
        "graphql_jwt.middleware.JSONWebTokenMiddleware",
        "graphene_django.debug.DjangoDebugMiddleware",
        'graphene_django_extras.ExtraGraphQLDirectiveMiddleware'
    ],
    "SCHEMA_INDENT": 4,
}

# Add settings for authentication with graphql_jwt
AUTHENTICATION_BACKENDS = [
    'graphql_jwt.backends.JSONWebTokenBackend',
    'django.contrib.auth.backends.ModelBackend',
]

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, '%s/static/')
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

CORS_ORIGIN_ALLOW_ALL = True

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

      ''' % (project_name, project_name))
      settings.write('\n')


  def config_schema(self, project_name):
    with open('{}/schema.py'.format(project_name), 'a') as schema:
      schema.write('\n')


def main():
  print('*****************************************************************************')
  print('*****************************************************************************')
  print('************************ Django Graphene Boilerplate ************************')
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
      print("Initializing your directory...")
      os.system('pwd/{}'.format(args[name_index+1]))
      print('Creating virtual environment')
      venv = subprocess.run(["python3", "-m", "venv", "./venv/"])



      if venv.returncode == 0:
        print('Activating the virtual environment...')
        # os.system("")
        print('Installing dependencies...')
        subprocess.call("source venv/bin/activate", shell=True, executable='/bin/bash')
        subprocess.run(["pip", "install", "django"])
        print('Initializing git repository...')
        subprocess.run(["git", "init"])
        print('Add virtual environment folder to ignored folders')
        subprocess.run(["touch", ".gitignore"])
        print('Initializing Django default structure...')
        subprocess.run(["django-admin", "startproject", "{}".format(args[name_index+1]), "."])
        print('Migrating Django Default Migrations')
        os.system("python3 manage.py migrate")
        print('Installing Graphene Django Extras...')
        subprocess.run(["pip", "install", "graphene-django-extras"])
        subprocess.run(["pip", "install", "django-graphql-jwt"])
        subprocess.run(["pip", "install", "django-cors-headers"])

        # configure .gitignore
        print('Configuring .gitignore')
        with open('.gitignore', 'w') as gitignore:
            gitignore.write("venv/\n")
            gitignore.write("db.sqlite3\n")
            gitignore.write("manage.py\n")
            gitignore.write("django_graphene_boilerplate/\n")

        project_name = '{}'.format(args[name_index+1])

        print('Configuring Django Settings...')
        default.config_settings(project_name)






main()