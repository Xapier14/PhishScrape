import glob
import pathlib

htmls = glob.glob('failed_htmls/*.html')
for html in htmls:
    # delete
    pathlib.Path(html).unlink()

# create gitkeep
with open('failed_htmls/.gitkeep', 'w') as f:
    f.write('')
print('Done.')