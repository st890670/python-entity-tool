# Auto convert database column to Java Entity class tool

## Warning
這個小工具只是為了在資達工作上加速開發而已，並不是完善的工具。

## TL;DR
這個python專案用psycopg2連接資料庫，並將欄位資訊轉為Java的Entity產出。變數型態跟繼承類別可能會有誤，請轉出後再檢查。
  
## Modify config (Required!)

- `config.ini`修改資料庫連線資訊及必要的資訊
```
host=db url
port=db port
database=db name
user=db role
password=role password

package_path=template class package path
table_name=convert table name
```

## How to startup

- 安裝python
```
python execute.py
```
