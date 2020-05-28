# To add a new cell, type '#%%'
# To add a new markdown cell, type '#%% [markdown]'
#%% Change working directory from the workspace root to the ipynb file location. Turn this addition off with the DataScience.changeDirOnImportExport setting
# ms-python.python added
import os
try:
	os.chdir(os.path.join(os.getcwd(), 'github/mrtunguyen.github.io/_notebooks'))
	print(os.getcwd())
except:
	pass
#%%
from datetime import datetime
import re, os
from pathlib import Path
from typing import Tuple, Set

# Check for YYYY-MM-DD
_re_blog_date = re.compile(r'([12]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])-)')
# Check for leading dashses or numbers
_re_numdash = re.compile(r'(^[-\d]+)')

def rename_for_jekyll(nb_path: Path, warnings: Set[Tuple[str, str]]=None) -> str:
    """
    Return a Path's filename string appended with its modified time in YYYY-MM-DD format.
    """
    assert nb_path.exists(), f'{nb_path} could not be found.'

    # Checks if filename is compliant with Jekyll blog posts
    if _re_blog_date.match(nb_path.name): return nb_path.with_suffix('.md').name.replace(' ', '-')
    
    else:
        clean_name = _re_numdash.sub('', nb_path.with_suffix('.md').name).replace(' ', '-')

        # Gets the file's last modified time and and append YYYY-MM-DD- to the beginning of the filename
        mdate = os.path.getmtime(nb_path) - 86400 # subtract one day b/c dates in the future break Jekyll
        dtnm = datetime.fromtimestamp(mdate).strftime("%Y-%m-%d-") + clean_name
        assert _re_blog_date.match(dtnm), f'{dtnm} is not a valid name, filename must be pre-pended with YYYY-MM-DD-'
        # push this into a set b/c _nb2htmlfname gets called multiple times per conversion
        if warnings: warnings.add((nb_path, dtnm))
        return dtnm


#%%
from datetime import datetime
import re, os, logging
from nbdev import export2html
from nbdev.export2html import Config, Path, _re_digits, _to_html, _re_block_notes

warnings = set()
    
# Modify the naming process such that destination files get named properly for Jekyll _posts
def _nb2htmlfname(nb_path, dest=None): 
    fname = rename_for_jekyll(nb_path, warnings=warnings)
    if dest is None: dest = Config().doc_path
    return Path(dest)/fname


#%%
for original, new in warnings:
    print(f'{original} has been renamed to {new} to be complaint with Jekyll naming conventions.\n')
    
## apply monkey patches
export2html._nb2htmlfname = _nb2htmlfname


#%%
export2html.notebook2html(fname='./2020-05-20-Autoregressive-Generative-Models.ipynb', dest='../_posts/', template_file='../_action_files/fastpages.tpl')


#%%
fname = '2020-05-20-Autoregressive-Generative-Models.ipynb'
p = Path(fname)
files = list(p.parent.glob(p.name))


#%%
_nb2htmlfname(files[0], dest='.')


#%%



