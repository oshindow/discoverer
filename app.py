"""no zui 高校学者查询系统
视图函数模块的开发文档

Date: 2020/8/11
Authors: 王心童，刘今禹，李明泽，王一迈，罗沁鹤，陈寒露
"""

import json
import logging

from xpinyin import Pinyin
from flask_wtf import FlaskForm
from pypinyin import pinyin, Style
from flask import Flask, render_template, request, session
from wtforms import StringField, SubmitField, SelectField
from connect import InsertUser, ReadUser, ReadBJFU, Read
from draw import YearsData, JournalData, MapData

logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s (%(module)s:%(lineno)d) %(levelname)s: %(message)s",
        )
app = Flask(__name__)

# 加上这句解决flask_wtf 报错
app.config["SECRET_KEY"] = "123456"


class SearchForm(FlaskForm):
    """SearchForm 是一个继承自FlaskForm 的类

    它将表单中的字段都定义为类变量，类变量的值是相应字段类型的对象
    StringField 类表示属性为type="text" 的<input>元素
    SelectField 类表示<select>元素
    SubmitField 类表示属性为type="submit" 的<input>元素

    Author: 王心童
    """
    method = StringField('请输入')

    SearchMethod = SelectField('选择搜索方式', choices=[(0, '-请选择检索方式-'), (1, '研究方向'), (2, '院校'), (3, '专业'), (4, '姓名')], coerce=int)
    MajorInSchool = SelectField('选择专业', choices=[('default', '')])
    NameIndex = SelectField('选择索引', choices=[('default', '')])

    submit = SubmitField("搜索")


def NameOrder(lis):
    """将中文姓名转为拼音后按首字母排序

    :param lis:(list) 原始姓名列表
    :return: result:(list) 排序后的姓名列表

    Author: 李明泽
    """
    pin = Pinyin()
    result = []
    for item in lis:
        result.append((pin.get_pinyin(item), item))
    result.sort()
    for i in range(len(result)):
        result[i] = result[i][1]

    return result


@app.route('/login')
def login():
    """登录 & 注册页面

    Authors: 罗沁鹤，陈寒露
    """
    return render_template("login.html")


@app.route('/')
def Index():
    """ 网站主页

    Authors:罗沁鹤，陈寒露
    """
    form = SearchForm()
    return render_template("index.html", form=form)


@app.route('/Register', methods=['post'])
def Register():
    """ 注册操作

    后端获取前端input 的邮箱，昵称，密码，确认密码，机构和身份
    通过session 记住上下文会话传到主页面

    Authors: 王心童，陈寒露
    """
    email = request.values.get("email")
    nickname = request.values.get("nickname")
    password = request.values.get("password")
    password_con = request.values.get("password_con")
    institution = request.values.get("institution")
    identity = request.values.get("identity")

    while password_con != password:
        return render_template("login.html")

    password_exist = ReadUser(email)
    if len(password_exist.values) > 0:
        return render_template("login.html")

    if password == password_con:
        data = tuple([email, nickname, password, institution, identity])
        InsertUser(data)
        session["user"] = email
        print("session user set")
        form = SearchForm()
        return render_template("index_session.html", form=form)


@app.route('/registercheck', methods=['post'])
def Registercheck():
    email = request.values.get("email")
    password_exist = ReadUser(email)
    if len(password_exist.values) > 0:
        return "exit"
    else:
        return "pass"


@app.route('/Logout')
def Logout():
    session["user"] = None
    form = SearchForm()
    return render_template("index.html", form=form)


@app.route('/Login', methods=['post'])
def Login():
    """登录操作

    后端获取前端input 的邮箱和密码
    通过session 记住上下文会话传到主页面

    Authors: 王心童，陈寒露
    """
    email = request.values.get("email")
    password = request.values.get("password")

    password_con = ReadUser(email)

    if len(password_con.values) == 0:
        return render_template("login.html")

    while password_con.values[0] != password:
        return render_template("login.html")

    if password_con.values[0] == password:
        session["user"] = email
        form = SearchForm()
        return render_template("index_session.html", form=form)


@app.route('/logcheck', methods=['post'])
def Logcheck():
    email = request.values.get("email")
    password = request.values.get("password")

    password_exist = ReadUser(email)
    if len(password_exist.values) == 0:
        return "none"

    if password_exist.values[0] != password:
        return "nomatch"
    else:
        return "pass"


@app.route('/Find')
def Find():
    """主页查找功能

    1.按研究领域查找，调用Find_by_Field(field)，返回searchprolist.html
    2.按院校查找，调用Find_by_School(field)，返回searchprolist_multi.html
    3.按专业查找，直接读取数据库，返回searchprolist_major.html
    4.按姓名查找，直接读取数据库，返回person.html

    Author: 王心童
    """
    form = SearchForm(request.args)
    method = form.method.data

    if form.SearchMethod.data == 1:

        names, school, award, majors = Find_by_Field(method)

        return render_template("searchprolist.html",
                               names=names, award=award,
                               school=school, majors=majors
                               )

    elif form.SearchMethod.data == 2:

        names, country, majors, form = Find_by_School(school=method)

        return render_template("searchprolist_multi.html", form=form,
                               names=names, country=country,
                               school=method, majors=majors
                               )

    elif form.SearchMethod.data == 3:
        method_all = '%' + method + '%'

        names, country, school, _, majors, _, _, _ = Read(major=method_all)

        form = SearchForm()
        IndexList = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
                     'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

        form.NameIndex.choices = [(index, index) for index in IndexList]
        return render_template("searchprolist_major.html", form=form,
                               names=names, country=country,
                               school=school, majors=majors,
                               major=method
                               )

    elif form.SearchMethod.data == 4:

        name, country, school, award, majors, papers, friends, summary = Read(name=method)

        if len(name) == 0:
            return render_template("noneperson.html")

        else:
            papers = papers[0].split(';')
            friends = friends[0].split(';')
            majors = majors[0].split(';')

            # 在合作学者字符串中添加分号，方便前端在js中分割字符串，添加人名到合作学者
            for i in range(len(friends)):
                friends[i] = friends[i] + ";"

            if method == '李永乐':
                picture = "../static/propictures/luoyouqing.png"
            elif method == '母义明':
                picture = "../static/propictures/muyiming.png"
            elif method == '季加孚':
                picture = "../static/propictures/jijiafu.png"
            else:
                picture = "../static/propictures/default.jpg"

            return render_template("person.html", picture=picture,
                                    name=" ".join(name[0]), country=" ".join(country[0]),
                                    school=" ".join(school[0]), award=" ".join(award[0]),
                                    majors=majors, papers=papers,
                                    friends=friends, summary=summary[0]
                                    )

    else:
        return render_template("index.html", form=form)


@app.route('/Find_by_Field')
def Find_by_Field(field):
    """ 按研究领域查找

    研究领域查找仅限于chinese 数据库中的bjfu 表
    :param field:(str) 研究领域. 供主页查找函数Find 中的院校查找调用
    Author: 李明泽
    """
    field = '%' + '%'.join(field) + '%'

    name, school, award, majors = ReadBJFU(field=field)

    '''
    majors = ";".join(majors).split(";")
    majors = list(filter(None, majors))
    
    with open('d:/discoverer/src/static/majors.json', 'w',  encoding='utf-8') as fid:
        json.dump(majors, fid, ensure_ascii=False)

    
    author_list = ";".join(authors).split(";")

    author_list = list(set(author_list))  # aythor_list元素去除重复
    
    for i in range(len(author_list)):  # aythor_list每个元素去除空格
        author_list[i] = author_list[i].replace(" ", "")
    author_list.remove('')  # 删除author_list中的空元素
    '''
    # 按拼音首字母排序
    # author_list = NameOrder(author_list)
    return name, school, award, majors


@app.route('/Find_by_Author')
def Find_by_Author():
    """ 按姓名查找，区别于Find_by_Name，仅限bjfu 表

    在按院校查找后，点击姓名进入教授主页(bjfu)

    Author: 王心童，刘今禹，李明泽，王一迈
    """
    name = request.args.get("fname")

    award, school, field, majors, rank, author, title, journal, book, project, summary = ReadBJFU(name=name)

    majors = majors.strip(';').split(';')
    papers = title.split(';')
    friends = author.split(';')

    # 去除学校末尾的分号
    school = " ".join(school).split(' ')
    school.remove(';')
    school = "".join(school)
    # 在合作学者字符串中添加分号，方便前端在js中分割字符串，添加人名到合作学者
    for i in range(len(friends)):
        friends[i] = friends[i] + ";"

    YearsData(papers)
    JournalData(papers)
    MapData(rank, name, majors, friends)

    if name == "骆有庆":
        picture = "../static/propictures/luoyouqing.png"
    elif name == "吴保国":
        picture = "../static/propictures/wubaoguo.png"
    elif name == "沈国舫":
        picture = "../static/propictures/shenguofnag.png"
    elif name == "孟兆祯":
        picture = "../static/propictures/mengzhaozhen.png"
    elif name == '温亚利':
        picture = "../static/propictures/wenyali.png"
    elif name == "潘会堂":
        picture = "../static/propictures/panhuitang.png"
    else:
        picture = "../static/propictures/default.jpg"

    return render_template("person.html", picture=picture,
                           name=name, award=award, field=field,
                           majors=majors, rank=rank, papers=papers,
                           friends=friends, book=book, project=project,
                           summary=summary, journal=journal, school=school,
                           )


@app.route('/year')
def Year():
    """ 接受前端JQuery 请求读取json文件返回到前端

    :return data_years:(dict) 论文发表年份为key,数量为value
    Author: 王心童
    """
    with open('C:\code\static\years.json', 'r', encoding='utf-8') as fid:
        content = fid.read()
        data = json.loads(content)

    data_years = {}
    for item in data:
        year = item['year']
        num = item['num']
        data_years[year] = num

    return data_years


@app.route('/map')
def Map():
    """ 接受前端JQuery 请求读取json文件返回到前端

    :return data:(dict) key为三种关系，value为三种关系对应的人

    Author: 刘今禹
    """
    with open('C:\code\static\map.json', 'r', encoding='utf-8') as fid:
        content = fid.read()
        data = json.loads(content)

    return data


@app.route('/journal')
def Journal():
    """ 接受前端JQuery 请求读取json文件返回到前端

    :return data:(dict) dict 的元素也为dict，key 为期刊，value 为数量
    Author: 李明泽
    """
    with open('C:\code\static\journal.json', 'r', encoding="utf8") as fid:
        content = fid.read()
        data = json.loads(content)

    return data


@app.route('/Find_by_School')
def Find_by_School(school):
    """按院校查找

    查找于chinese 数据库的sprint1 表
    搜索学校以返回到该学校的教授列表
    在搜索结果顶部选择一个专业，可以将列表刷新为该校该专业的教授列表

    :param school:(str) 院校名称. 供主页查找函数Find 中的院校查找调用
    Authors: 王一迈，刘今禹
    """
    school_all = '%' + school + '%'

    names, country, _, _, majors, _, _, _ = Read(school=school_all)

    # 将抽取的院校专业形成list，动态添加到SelectField 类对象MajorInSchool中
    majors_all = ";".join(majors).split(";")
    majors_all = list(filter(None, majors_all))

    majors_list = []
    for major in majors_all:
        if major not in majors_list:
            majors_list.append(major)

    form = SearchForm()
    form.MajorInSchool.choices = [(majors_list[i], majors_list[i]) for i in range(0, len(majors_list))]

    return names, country, majors, form


@app.route('/Find_by_MaS')
def Find_by_MaS():
    """ 再按院校搜索后的专业搜索

    在执行二级搜索时，需要记住两个变量，院校和专业的值.
    院校将假装为"提交"按钮，value = {{university}}，并仍通过request.args.get() 获得name 属性的值.
    专业的值通过SelectFiled 类获得

    Authors: 王一迈，刘今禹
    """
    # 获取`院校`的值，添加通配符
    school = request.args.get("fname")
    school_all = '%' + school + '%'

    # 获取`专业`的值，添加通配符
    form = SearchForm(request.args)
    major = form.MajorInSchool.data
    major_all = '%' + major + '%'

    names, country, _, award, majors, _, _, _ = Read(school=school_all, majors=major_all, multi=1)

    # 将抽取的院校专业形成list，动态添加到SelectField 类对象MajorInSchool中
    majors_all = ';'.join(majors).split(';')
    majors_all = list(filter(None, majors_all))

    majors_list = []
    for major in majors_all:
        if major not in majors_list:
            majors_list.append(major)

    form = SearchForm()
    form.MajorInSchool.choices = [(majors_list[i], majors_list[i]) for i in range(0, len(majors_list))]

    return render_template("searchprolist_multi.html", form=form,
                           names=names, country=country,
                           school=school, majors=majors
                           )


@app.route('/Find_by_Major')
def Find_by_Major():
    """按专业搜索，供在教授主页中跳转用

    搜索专业返回该专业的教授列表，并根据该专业的相关性对其进行排序.
    可以通过拼音首字母索引快速搜索教授的姓名.
    获取拼音首字母索引时，需要记住其专业价值.
    专业将伪装成一个"提交"按钮，value = {{major}}，仍然可以通过request.args.get() 获得name 属性的值.

    Author: 王心童，王一迈
    """
    # 获取`专业`的值，添加通配符
    major = request.args.get("fname")
    major_all = '%' + major + '%'

    # 获取`拼音首字母索引`的值
    form = SearchForm(request.args)
    index = form.NameIndex.data

    names, country, school, award, majors, _, _, _ = Read(major=major_all)

    if index:
        IndexNames = []
        IndexCountry = []
        IndexSchool = []
        IndexMajors = []

        count = 0
        for name in names:
            first_char = " ".join(name).split(' ')[0]
            if pinyin(first_char, style=Style.FIRST_LETTER)[0][0] == index.lower():
                IndexNames.append(name)
                IndexCountry.append(country[count])
                IndexSchool.append(school[count])
                IndexMajors.append(majors[count])

            count += 1

        # 相关度排序
        IndexOrigin = []
        for i in range(0, len(IndexNames)):
            data = {}
            data['IndexName'] = IndexNames[i]
            data['IndexCountry'] = IndexCountry[i]
            data['IndexSchool'] = IndexSchool[i]
            data['IndexMajors'] = IndexMajors[i]
            data['IndexMajorsRelated'] = len(IndexMajors[i])
            IndexOrigin.append(data)

        IndexRelated = sorted(IndexOrigin, key=lambda e: e.__getitem__('IndexMajorsRelated'))

        RelatedNames = []
        RelatedCountry = []
        RelatedSchool = []
        RelatedMajors = []

        for i in range(0, len(IndexRelated)):
            RelatedNames.append(IndexRelated[i]['IndexName'])
            RelatedCountry.append(IndexRelated[i]['IndexCountry'])
            RelatedSchool.append(IndexRelated[i]['IndexSchool'])
            RelatedMajors.append(IndexRelated[i]['IndexMajors'])

    #     人名按升序降序排序，意义不大，注释掉
    #     if form.NameOrder.data:
    #     if form.NameOrder.data == 1:
    #        return render_template("searchprolist_option.html", OrderForm=form,
    #                                length=length, names=names, country=country,
    #                                university=university,
    #                                majors=majors)
    #     else:
    #         names = names.tolist()[::-1]
    #         country = country.tolist()[::-1]
    # 3        university = university.tolist()[::-1]
    #         majors = majors.tolist()[::-1]
    #   return render_template("searchprolist_option.html", OrderForm=form,
    #                            length=length, names=names, country=country,
    #                            university=university,
    #                            majors=majors)

        form = SearchForm()
        form.NameIndex.choices = [(index, index) for index in
                              ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
                               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']]

        return render_template("searchprolist_major.html", form=form,
                                names=RelatedNames, country=RelatedCountry,
                                school=RelatedSchool, majors=RelatedMajors,
                                major=major)

    # 起始页没有指定index
    else:
        form = SearchForm()
        form.NameIndex.choices = [(index, index) for index in
                                  ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
                                   'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']]

        return render_template("searchprolist_major.html", form=form,
                               names=names, country=country,
                               school=school, majors=majors,
                               major=major)


@app.route('/Find_by_Name')
def Find_by_Name():
    """按姓名搜索

    此处按名称搜索，特别指在搜索结果列表中的按姓名搜索.
    结果列表中的姓名将被伪装成一个"提交"按钮，value = {{姓名}}，而名称属性的值仍由request.args.get()获得.
    按主页名称搜索是在Find() 视图函数中定义和调用的，而名称字段的值是通过form.name.data获得的.

    Author: 王心童
    """
    name = request.args.get("fname")
    name, country, school, awards, majors, papers, friends, summary = Read(name=name)
    # 查无此人
    if len(name) == 0:
        return render_template("noneperson.html")
    else:
        papers = papers[0].split(';')
        friends = friends[0].split(';')
        majors = majors[0].split(';')

        # 在合作学者字符串中添加分号，方便前端在js中分割字符串，添加人名到合作学者
        for i in range(len(friends)):
            friends[i] = friends[i] + ";"

        if name == '李永乐':
            picture = "../static/propictures/luoyouqing.png"
        elif name == '母义明':
            picture = "../static/propictures/muyiming.png"
        elif name == '季加孚':
            picture = "../static/propictures/jijiafu.png"
        else:
            picture = "../static/propictures/default.jpg"

        return render_template("person.html", picture=picture,
                                name=" ".join(name), country=" ".join(country),
                                school=" ".join(school), awards=" ".join(awards),
                                majors=majors, papers=papers,
                                friends=friends, summary=summary
                                )


if __name__ == '__main__':

    app.run()

