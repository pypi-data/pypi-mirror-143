echo on
chcp 65001
cd /d %~dp0
cd ..
set QPT_COLOR=False
set QPT_MODE=Debug
set PYTHONPATH=Python/Lib/site-packages;Python/Lib;Python
set PATH=Python/Lib/site-package;Python/Lib;Python;%PATH%
cls
"./Python/python.exe" -c "import sys;sys.path.append('./Python');sys.path.append('./Python/Lib');sys.path.append('./Python/Lib/site-packages');sys.path.append('./Python/Scripts');import qpt.run as run"
pause
