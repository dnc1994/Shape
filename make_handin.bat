mkdir submit
mkdir submit\src
mkdir submit\src\puzzy
mkdir submit\data_sample
mkdir submit\data_sample\cg\
mkdir submit\data_sample\sketch\

copy src\*.py submit\src\
copy src\puzzy\*.py submit\src\puzzy\
copy src\rule_base.txt submit\src\
copy data\sample\cg\* submit\data_sample\cg\
copy data\sample\sketch\* submit\data_sample\sketch\
copy report\report.pdf submit\AI-PJ-Report-ZhangLinghao.pdf
copy README.md submit\

rename submit AI-PJ-ZhangLinghao

pause
