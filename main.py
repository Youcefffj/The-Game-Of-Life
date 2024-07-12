import subprocess,sys,os

chemin_absolu_main = os.path.abspath("menu.py")

chemin_python = os.path.abspath(sys.executable)

subprocess.run([chemin_python, chemin_absolu_main], check=True)