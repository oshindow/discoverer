import json
from connect import ReadBJFU


def YearsData(papers):
    """ 保存教授论文发表年份数据

    :param papers: (str) 教授论文信息字符串

    Author: 王心童
    """
    AllYears = []
    for paper in papers:
        date = paper.split('. ')[1]
        if len(date.split('-')) == 3:
            AllYears.append(date.split('-')[0])
        elif len(date.split('(')) == 2:
            AllYears.append(date.split('(')[0])

    years = set(AllYears)
    clean_years = {}
    for item in years:
        clean_years.update({item: AllYears.count(item)})

    years_list = list(clean_years.keys())

    for item in years_list:
        if len(item) > 4:
            clean_years.pop(item)
    if '' in clean_years:
        clean_years.pop('')
    clean_years = sorted(clean_years.items(), key=lambda e: e[0])

    # 将论文发表年份数据按键值对，存为json 文件
    years_list = []
    for year in clean_years:
        years = {}
        years['year'] = year[0]
        years['num'] = year[1]
        years_list.append(years)

    with open('C:\code\static\years.json', 'w', encoding='utf-8') as fid:
        json.dump(years_list, fid, ensure_ascii=False)


def JournalData(papers):
    """ 保存期刊和专利数据

    :param papers: (str) 教授论文信息字符串

    Author: 李明泽
    """

    # 期刊列表
    journal_list = []
    # 文章列表
    artical_list = []
    # 专利列表
    patent_list = []
    for i in range(len(papers)):
        if '[J]' in papers[i]:
            artical_list.append(papers[i])
        if '[P]' in papers[i]:
            patent_list.append(papers[i])

    # 将题目按专利和文章分类
    for i in range(len(artical_list)):
        # 从文章中分离出期刊
        journal_list.append(artical_list[i].split('\n')[1].split('.')[0])
    # 元素去除重复
    # journal_list = sorted(list(set(journal_list)))
    # 查期刊发表的频度
    journal_set = set(journal_list)
    journal = {}
    for item in journal_set:
        journal.update({item: journal_list.count(item)})
    journal.update({'中国专利': len(patent_list)})

    journal_sorted = sorted(journal.items(), key=lambda e: e[1], reverse=True)
    # 新增字典列表
    journal_dict = {}
    for i in range(min(len(journal_sorted), 10)):
        journal_dict[journal_sorted[i][0]] = journal_sorted[i][1]

    # 将期刊专利数据按键值对，存为json 文件
    with open('C:\code\static\journal.json', 'w', encoding='utf-8') as fid:
        json.dump(journal_dict, fid, ensure_ascii=False)


def MapData(rank, name, majors, friends):
    """ 保存图谱关系数据

    :param rank:(str) 教授的唯一专业
    :param name:(str) 教授的姓名
    :param majors:(list) 教授的多个专业
    :param friends:(str) 教授的合作学者

    Author: 李明泽
    """
    # 图谱关系 = ['合作', '专业相同', '专业相关']
    # author (friends)
    # ranking 相同则为专业相同学者peer_list(同行)(majors)
    # domain与 ranking 的差值为专业相关学者peer_related_list(猜你想找)

    # ranking 增加通配符查找同行
    ranking = '%' + rank + '%'

    # 基于ranking的同行列表, 定义专业相同学者
    peer_list = ReadBJFU(name=name, ranking=ranking, Peer=1)
    peer_list = sorted(list(set(peer_list)))  # peer_list元素去除重复

    tmp_list = []
    data_list = ReadBJFU(name=name, domain_list=majors, PeerRelated=1)
    for i in range(0, len(data_list)):
        for data in data_list[i]:
            tmp_list.append(data)
    tmp_list = sorted(list(set(tmp_list)))  # temp_list元素去除重复

    peer_related_list = []
    for i in range(len(tmp_list)):
        if tmp_list[i] not in peer_list:
            peer_related_list.append(tmp_list[i])  # 两表做差，生成peer_related_list列表

    map = {}
    map['partner_list'] = "".join(friends)
    map['peer_list'] = ";".join(peer_list)
    map['peer_related_list'] = ";".join(peer_related_list)

    with open('C:\code\static\map.json', 'w', encoding='utf-8') as fid:
        json.dump(map, fid, ensure_ascii=False)