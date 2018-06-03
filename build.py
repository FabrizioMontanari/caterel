import pathlib
import sass
import sys
import shutil


verbose = '--verbose' in sys.argv[1:]
def verbose_log(message):
    if verbose:
        print(message)


print('Building project...', end='\n' if verbose else '')

# clean up
verbose_log('    Cleaning up destination folders...')
shutil.rmtree('static', ignore_errors=True)
shutil.rmtree('backend', ignore_errors=True)

# css compile
verbose_log('    Compiling css...')
pathlib.Path('static/css').mkdir(parents=True, exist_ok=True) 
sass.compile(dirname=('src/sass', 'static/css'), output_style='compressed')

# static files copy
verbose_log('    Copying static files...')
shutil.copytree('src/fonts', 'static/fonts')
shutil.copytree('src/img', 'static/img')
shutil.copytree('src/js', 'static/js')

# backend files copy
verbose_log('    Copying bakend code...')
shutil.copytree('src/templates', 'backend/templates')
shutil.copy2('src/martini.py', 'backend')
shutil.copy2('src/zappa_settings.json', 'backend')

print('Done')