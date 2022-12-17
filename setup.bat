@echo on
cd /d %~dp0
cd /d %~dp0\resources
call conda env create -f environment.yml
call conda activate Picf
pip install git+https://github.com/openai/CLIP.git
pip install --upgrade pillow
cd /d %~dp0\imagededup
call python setup.py install
rd /s /q imagededup.egg-info
rd /s /q build
rd /s /q dist
pause