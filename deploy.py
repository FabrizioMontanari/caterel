import pathlib
import sass
import shutil


# clean up
shutil.rmtree('static', ignore_errors=True)
shutil.rmtree('backend', ignore_errors=True)


# css
pathlib.Path('static/css').mkdir(parents=True, exist_ok=True) 
sass.compile(dirname=('src/sass', 'static/css'), output_style='compressed')


# static files
shutil.copytree('src/fonts', 'static/fonts')
shutil.copytree('src/img', 'static/img')
shutil.copytree('src/js', 'static/js')


# backend files
shutil.copytree('src/templates', 'backend/templates')
shutil.copy2('src/martini.py', 'backend')
shutil.copy2('src/zappa_settings.json', 'backend')