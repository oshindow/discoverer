# Discoverer
A University Scholar Discovery System

# Introduction

# Features

# Environment
* logging 
* pymysql
* pandas
* flask

# Useage
## 导入、连接数据库
```
### 导入网页/用户数据库

进入mysql数据库控制台，终端输入命令：

mysql -u root -p

### 创建数据库:  

create database database_name;
    
### 选择数据库：

use database_name;

### 导入数据库:  

source /path/to/database_name.sql

### 检查是否导入成功：

show tables;

### 连接数据库

更改`src/app.py`中的 `pymysql.connect()` 参数为本地参数
```
## Run
```
* 配置pycharm的解释器
* 创建flask server运行配置文件
* 运行`src/app.py`
* 从http://127.0.0.1:5000/index 进入网站
```
# Author
No Uzi
