rem 删除旧文件
rd build /S /Q
rd dist /S /Q

rem 将setup.py复制到上级目录，因为py2exe要求setup.py与程序文件在同目录。
copy setup.py ..\setup.py

rem 开始打包。由于py2exe的目录问题，要到上级目录去执行，然后再回来
cd ..
setup.py py2exe
cd setup

rem 删除刚才复制的setup.py文件。
del ..\setup.py

rem 将输出文件移到此目录下。
move ..\build build
move ..\dist dist

@pause
