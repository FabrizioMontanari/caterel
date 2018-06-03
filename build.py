import pathlib
import sass
import shutil


# clean up
print('Cleaning up destination folders...')
shutil.rmtree('static', ignore_errors=True)
shutil.rmtree('backend', ignore_errors=True)

# css compile
print('Compiling css...')
pathlib.Path('static/css').mkdir(parents=True, exist_ok=True) 
sass.compile(dirname=('src/sass', 'static/css'), output_style='compressed')

# static files copy
print('Copying static files...')
shutil.copytree('src/fonts', 'static/fonts')
shutil.copytree('src/img', 'static/img')
shutil.copytree('src/js', 'static/js')

# backend files copy
print('Copying bakend code...')
shutil.copytree('src/templates', 'backend/templates')
shutil.copy2('src/martini.py', 'backend')
shutil.copy2('src/zappa_settings.json', 'backend')

print('Build step completed.\n')