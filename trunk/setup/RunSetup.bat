rem ɾ�����ļ�
rd build /S /Q
rd dist /S /Q

rem ��setup.py���Ƶ��ϼ�Ŀ¼����Ϊpy2exeҪ��setup.py������ļ���ͬĿ¼��
copy setup.py ..\setup.py

rem ��ʼ���������py2exe��Ŀ¼���⣬Ҫ���ϼ�Ŀ¼ȥִ�У�Ȼ���ٻ���
cd ..
setup.py py2exe
cd setup

rem ɾ���ղŸ��Ƶ�setup.py�ļ���
del ..\setup.py

rem ������ļ��Ƶ���Ŀ¼�¡�
move ..\build build
move ..\dist dist

@pause
