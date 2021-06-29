def main():
  print('*****************************************************')
  print('************ Django Graphene Boilerplate ************')
  print('*****************************************************')
  import os
  import sys
  import subprocess

  args = sys.argv[1:]
  name_index = args.index("--name")


  if len(args[name_index]):
    if len(sys.argv[1:][name_index + 1]) > 0:
      print("Initializing your directory...")
      os.system('pwd/{}'.format(args[name_index+1]))
      print('Creating virtual environment')
      venv = subprocess.run(["python3", "-m", "venv", "./venv/"])



      if venv.returncode == 0:
        print('Activating the virtual environment...')
        os.system("source venv/bin/activate")
        print('Installing dependencies...')
        subprocess.run(["pip", "install", "django"])
        print('Initializing git repository...')
        subprocess.run(["git", "init"])
        print('Add virtual environment folder to ignored folders')
        subprocess.run(["touch", ".gitignore"])
        # os.system('echo venv/\n >> .gitignore')
        print('Initializing Django default structure...')
        subprocess.run(["django-admin", "startproject", "{}".format(args[name_index+1]), "."])
        print('Migrating Django Default Migrations')
        os.system("python3 manage.py migrate")
        # os.system("python3 manage.py runserver")
        # os.system("rm -rf django_graphene_boilerplate venv .gitignore manage.py db.sqlite3")

        with open('.gitignore', 'w') as gitignore:
            gitignore.write("venv/\n")
            gitignore.write("db.sqlite3\n")
            gitignore.write("manage.py\n")
            gitignore.write("django_graphene_boilerplate/\n")

        project_name = '{}'.format(args[name_index+1])

        with open('{}/settings.py'.format(project_name), 'a') as settings:
          print(settings)



main()