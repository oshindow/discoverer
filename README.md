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
## Import & Connect database
```
### 导入网页/用户数据库

终端输入命令,进入mysql数据库控制台：

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

更改`src/connect.py`中的 `pymysql.connect()` 参数为本地参数
```
## Run
```
* 配置pycharm的解释器
* 创建flask server运行配置文件
* 运行`src/app.py`
* 从http://127.0.0.1:5000/index 进入网站
```
# Author
Xintong Wang, Jinyu Liu, Qinhe Luo, Hanlu Chen, Mingze Li, Yimai Wang  

Mathematice and Applied Mathematics  
College of Science, Beijing Forestry University
