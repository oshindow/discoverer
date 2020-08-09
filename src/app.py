import logging
import pandas as pd

from xpinyin import Pinyin
from flask_wtf import FlaskForm
from pypinyin import pinyin, Style
from wtforms.validators import Required
from flask import Flask, render_template, request, session
from wtforms import StringField, SubmitField, SelectField
from connect import connect_page, connect_user, CreateUser, InsertUser, ReadUser, ReadPaper, Read

logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s (%(module)s:%(lineno)d) %(levelname)s: %(message)s",
        )

app = Flask(__name__)
# 加上这句解决flask_wtf 报错
app.config["SECRET_KEY"] = "123456"


# SearchForm 是一个继承自FlaskForm 的类，将表单中的字段都定义为类变量，类变量的值是相应字段类型的对象
# StringField 类表示属性为type="text" 的<input>元素
# SelectField 类表示<select>元素
# SubmitField 类表示属性为type="submit" 的<input>元素
# 字段.label 用来渲染HTML
class SearchForm(FlaskForm):

    method = StringField('请输入')
    major = StringField('请输入专业')
    school = StringField('请输入学校')
    name = StringField('请输入姓名')
    field = StringField('请输入研究方向')

    SearchMethod = SelectField('选择搜索方式', choices=[(1, '研究方向'), (2, '院校'), (3, '专业'), (4, '姓名')], coerce=int)
    NameOrder = SelectField('选择排序方式', choices=[(1, '升序'), (2, '降序')], coerce=int)
    Major_in_School = SelectField('选择专业', choices=[('default', '')])
    NameIndex = SelectField('选择索引', choices=[('default', '')])

    submit = SubmitField("Send")


# 按拼音首字母排序
def NameOrder(lis):
    pin = Pinyin()
    result = []
    for item in lis:
        result.append((pin.get_pinyin(item), item))
    result.sort()
    for i in range(len(result)):
        result[i] = result[i][1]

    return result

# 登录 & 注册界面
@app.route('/login')
def login():
    return render_template("login.html")

# 网站主页
@app.route('/index')
def Index():
    form = SearchForm()
    return render_template("index.html", form=form)

# 注册操作
@app.route('/Register')
def Register():
    email = request.args.get("email")
    nickname = request.args.get("nickname")
    password = request.args.get("password")
    password_con = request.args.get("password_con")
    institution = request.args.get("institution")
    identity = request.args.get("identity")

    while password_con != password:
        return render_template("login.html")

    if password == password_con:
        data = tuple([email, nickname, password, institution, identity])
        InsertUser(data)
        session["user"] = email
        print("session user set")
        return render_template("index_session.html")

# 登录操作
@app.route('/Login')
def Login():
    email = request.args.get("email")
    password = request.args.get("password")

    password_con = ReadUser(email)

    while password_con != password:
        return render_template("login.html")

    if password_con == password:
        session["user"] = email
        return render_template("index_session.html")

# 主查找函数
@app.route('/Find')
def Find():
    form = SearchForm(request.args)
    method = form.method.data

    if form.SearchMethod.data == 1:

        name, school, award, domain = Find_by_Field(method)

        return render_template("searchprolist.html",
                               names=name, awards=award,  # country数据库缺少信息，不过基本都是中国人\(^ 0^)/
                               university=school,  # university和majors在‘authordata’，
                               majors=domain)

    elif form.SearchMethod.data == 2:

        length, names, country, uni, majors, major_list, form = Find_by_School(university=method)

        return render_template("searchprolist_multi.html", form=form,
                               length=length, names=names, country=country,
                               university=uni,
                               majors=majors, majorlist=major_list, length2=len(major_list))

    elif form.SearchMethod.data == 3:
        method_all = '%' + method + '%'

        length, names, country, university, awards, majors, papers, friends, info = Read(majors=method_all)

        form = SearchForm()
        form.NameIndex.choices = [(index, index) for index in ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']]
        return render_template("searchprolist_major.html", form=form,
                               length=length, names=names, country=country,
                               university=university,
                               majors=majors, major=method)

    elif form.SearchMethod.data == 4:

        length, name, country, university, awards, majors, papers, friends, info = Read(name=method)
        if length == 0:
            return render_template("noneperson.html")
        else:
            papers = papers[0].split(';')
            friends = friends[0].split(';')
            majors = majors[0].split(';')

            return render_template("person.html",
                                    name=" ".join(name), country=" ".join(country),
                                    university=" ".join(university), awards=" ".join(awards),
                                    majors=majors, papers=papers,
                                    friends=friends, info=info
                                    )

    else:
        return render_template("index_session.html", form=form)

# 按研究领域查找
@app.route('/Find_by_Field')
def Find_by_Field(field):
    """

    :param field:
    :return:
    """
    field = '%' + '%'.join(field) + '%'

    name, school, award, domain = ReadPaper(field=field)
    '''
    author_list = ";".join(authors).split(";")

    author_list = list(set(author_list))  # aythor_list元素去除重复
    
    for i in range(len(author_list)):  # aythor_list每个元素去除空格
        author_list[i] = author_list[i].replace(" ", "")
    author_list.remove('')  # 删除author_list中的空元素
    '''
    # 按拼音首字母排序
    # author_list = NameOrder(author_list)
    return name, school, award, domain


@app.route('/Find_by_Author')
def Find_by_Author():
    name = request.args.get("fname")

    award, school, field, domain, rank, author, title, journal, book, project, summary = ReadPaper(name=name)

    domains = domain.strip(';').split(';')
    papers = title.split(';')
    friends = author.split(';')

    return render_template("person.html",
                           name=name, award=award, field=field, domains=domains,rank=rank,
                           papers=papers, friends=friends, book=book,
                           project=project, summary=summary,
                           journal=journal, university=school,
                           majors=domain
                           )


@app.route('/Find_by_School')
def Find_by_School(university):
    """
    # Find by college on the main page, called in Find:
# Search for a school to return to the list of professors in the school, select a major at the top of the search results, and you can refresh the list to the list of professors in that school
    :param university:
    :return: professor list
    """
    university_all = '%' + university + '%'

    length, names, country, uni, awards, majors, _, _, _ = Read(university=university_all)

    # 去除majors 中的空值
    majors_all = ";".join(majors).split(";")
    majors_all = list(filter(None, majors_all))

    major_list = []
    for major in majors_all:
        if major not in major_list:
            major_list.append(major)

    form = SearchForm()
    form.Major_in_School.choices = [(major_list[i], major_list[i]) for i in range(0, len(major_list))]

    return length, names, country, university, majors, major_list, form


@app.route('/Find_by_MaS')
def Find_by_MaS():
    """
    The secondary search of the major of the school:
    Remember the values of the two variables `College` and `Professional` while performing the secondary search.
    `School` will pretend to be a submit button, value={{university}}, and still get the value of the name attribute by request.args.get().
    The value of `Professional` is obtained through the SelectFiled class
    :return: professor list
    """
    # 获取`院校`的值，添加通配符
    university = request.args.get("fname")
    university_all = '%' + university + '%'

    # 获取`专业`的值，添加通配符
    form = SearchForm(request.args)
    major = form.Major_in_School.data
    major_all = '%' + major + '%'

    length, names, country, uni, awards, majors, papers, friends, info = Read(university=university_all, majors=major_all, multi=1)

    majors_all = ';'.join(majors).split(';')
    majors_all = list(filter(None, majors_all))
    major_list = []
    for major in majors_all:
        if major not in major_list:
            major_list.append(major)

    form = SearchForm()
    form.Major_in_School.choices = [(major_list[i], major_list[i]) for i in range(0, len(major_list))]

    return render_template("searchprolist_multi.html", form=form,
                           length=length, names=names, country=country,
                           university=university,
                           majors=majors)


@app.route('/Find_by_Major')
def Find_by_Major():
    """
    Search by `Professional`:
    Search for `professional`-return to the list of professors of the profession, and sort them according to the relevance of the profession.
    Professor's name can be quickly searched through the pinyin initials index.
    When getting the pinyin first word index, you need to remember the professional value.
    `Professional` will pretend to be a submit button, value={{major}}, and still get the value of the name attribute through request.args.get().
    :return: professor list
    """
    # 获取`专业`的值，添加通配符
    major = request.args.get("fname")
    major_all = '%' + major + '%'

    # 获取`拼音首字母索引`的值
    form = SearchForm(request.args)
    index = form.NameIndex.data

    length, names, country, university, awards, majors, papers, friends, info = Read(majors=major_all)

    if index:
        IndexName = []
        IndexCountry = []
        IndexUniversity = []
        IndexMajors = []

        count = 0
        for name in names:
            first_char = " ".join(name).split(' ')[0]
            if pinyin(first_char, style=Style.FIRST_LETTER)[0][0] == index.lower():
                IndexName.append(name)
                IndexCountry.append(country[count])
                IndexUniversity.append(university[count])
                IndexMajors.append(majors[count])

            count += 1

        # 相关度排序
        IndexOrigin = []
        for i in range(0, len(IndexName)):
            data = {}
            data['IndexName'] = IndexName[i]
            data['IndexCountry'] = IndexCountry[i]
            data['IndexUniversity'] = IndexUniversity[i]
            data['IndexMajors'] = IndexMajors[i]
            data['IndexMajorsRelated'] = len(IndexMajors[i])
            IndexOrigin.append(data)

        IndexRelated = sorted(IndexOrigin, key=lambda e: e.__getitem__('IndexMajorsRelated'))

        IndexRelatedName = []
        IndexRelatedCountry = []
        IndexRelatedUniversity = []
        IndexRelatedMajors = []

        for i in range(0, len(IndexRelated)):
            IndexRelatedName.append(IndexRelated[i]['IndexName'])
            IndexRelatedCountry.append(IndexRelated[i]['IndexCountry'])
            IndexRelatedUniversity.append(IndexRelated[i]['IndexUniversity'])
            IndexRelatedMajors.append(IndexRelated[i]['IndexMajors'])

        # if form.NameOrder.data:
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
                                length=len(IndexName), names=IndexRelatedName, country=IndexRelatedCountry,
                                university=IndexRelatedUniversity,
                                majors=IndexRelatedMajors, major=major)
    else:
        form = SearchForm()
        form.NameIndex.choices = [(index, index) for index in
                                  ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
                                   'R',
                                   'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']]

        return render_template("searchprolist_major.html", form=form,
                               length=length, names=names, country=country,
                               university=university,
                               majors=majors, major=major)

@app.route('/Find_by_Name')
def Find_by_Name():
    """
    Search by `name`:
    The search by name here, especially the search by name appended to other search result lists.
    The `name` in the result list will be disguised as a submit button, value={{name}}, and the value of the name attribute is still obtained by request.args.get().
    The search by name of the homepage is defined and called in the Find() view function, and the value of the name field is obtained by form.name.data.
    return professor mainpage
    """
    name = request.args.get("fname")
    length, name, country, university, awards, majors, papers, friends, info = Read(name=name)
    if length == 0:
        return render_template("noneperson.html")
    else:
        papers = papers[0].split(';')
        friends = friends[0].split(';')
        majors = majors[0].split(';')

        return render_template("person_jin.html",
                                name=" ".join(name), country=" ".join(country),
                                university=" ".join(university), awards=" ".join(awards),
                                majors=majors, papers=papers,
                                friends=friends, info=info
                                )


if __name__ == '__main__':

    app.run(debug=True)

