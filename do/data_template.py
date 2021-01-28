import random

from faker import Faker
fake = Faker(['it_IT', 'en_US', 'ja_JP', 'zh_CN',
              'en_CA', 'en_PH', 'en_TH', 'uk_UA'])
# fake = Faker(['zh_CN'])


'''faker伪数据库支持方法'''
TEMPLATES = {
    'Id NO.': 'INT',
    'First Name': 'VARCHAR(50)',  # 名
    'Last Name': 'VARCHAR(50)',  # 姓
    'Email Address': 'VARCHAR(150)',  # 邮箱
    'Gender': 'VARCHAR(50)',  # 性别
    'IP Address V4': 'VARCHAR(150)',  # 随机IP4地址
    # "地理信息伪数据"
    'City': 'VARCHAR(500)',  # 城市
    'Country': 'VARCHAR(500)',  # 国家
    'Country Code': 'VARCHAR(50)',  # 国家编码
    # 'Area'district: 'VARCHAR(100)', # 仅支持中国
    'Latitude': 'VARCHAR(150)',  # 地理坐标：纬度
    'Longitude': 'VARCHAR(150)',  # 地理坐标：经度
    'Postcode': 'VARCHAR(150)',  # 邮编
    # 'Province'province: 'VARCHAR(100)',  # 台湾，美国没有
    'Address': 'VARCHAR(500)',  # 详细地址
    'Street Address': 'VARCHAR(500)',  # 街道地址
    'Street Name': 'VARCHAR(200)',  # 街道名
    'Street Suffix': 'VARCHAR(200)',  # 街、路
    'Building NO.': 'VARCHAR(200)',  # 楼牌号 eg：'B座'

    # "基础信息伪数据"
    'SSN': 'VARCHAR(100)',  # SSN号
    'Service Business': 'VARCHAR(500)',  # 随机公司服务行业
    'Company Name': 'VARCHAR(500)',  # 随机公司名
    'Card Info': 'VARCHAR(500)',  # 生成完整信用卡信息
    'Card NO.': 'VARCHAR(150)',  # 生成信用卡号
    'Card Type': 'VARCHAR(100)',  # 信用卡类型
    'Card Security Code': 'VARCHAR(100)',  # 信用卡安全码
    'Job': 'VARCHAR(200)',  # 职位


    'First Name(Female)': 'VARCHAR(50)',  # 女性 名
    'First Name(Male)': 'VARCHAR(50)',  # 男性 名
    'Last Name(Female)': 'VARCHAR(50)',  # 女性
    'Last Name(Male)': 'VARCHAR(50)',  # 男性
    'Full Name': 'VARCHAR(100)',  # 随机生成全名
    'Male Name': 'VARCHAR(100)',  # 男性全名
    'Female Name': 'VARCHAR(100)',  # 女性全名
    'ISDN NO.': 'VARCHAR(100)',  # 移动台国际用户识别码，即移动用户的ISDN号码
    'Phone NO.': 'VARCHAR(100)',  # 随机生成电话号
    'NO. Segment(Phone)': 'VARCHAR(100)',  # 随机生成手机号段如'139'

    # "网络基础信息伪数据"
    'Domain Name': 'VARCHAR(200)',  # 生成域名

    'IP Address V6': 'VARCHAR(100)',  # 随机IP6地址
    'MAC Address': 'VARCHAR(100)',  # 随机MAC地址
    'URI Address': 'VARCHAR(500)',  # 随机URI地址
    'URL Address': 'VARCHAR(500)',  # 随机URL地址
    'User Name': 'VARCHAR(100)',  # 随机用户名

    # "浏览器信息伪数据"
    'User Agent': 'VARCHAR(500)',  # 随机user_agent信息

    # "文件信息伪数据"
    'File Type': 'VARCHAR(50)',  # 随机文件扩展名如'avi'，'txt'
    'File Name': 'VARCHAR(100)',  # 随机文件名（包含扩展名，不包含路径）
    'File Path': 'VARCHAR(200)',  # 随机文件路径（包含文件名，扩展名）
    'Mime Type': 'VARCHAR(100)',  # 随机mime Type
}

'''调用生成数据方法'''
def data_generator(field):
    if field == 'Id NO.':
        return fake.random_int()
    if field == 'First Name':
        return fake.first_name()
    if field == 'Last Name':
        return fake.last_name()
    if field == 'Email Address':
        return fake.email()
    if field == 'Gender':
        return random.choice(['Female', 'Male', 'Non-binary'])
    if field == 'IP Address V4':
        return fake.ipv4()

    if field == 'City':
        return fake.city(),  # 城市
    if field == 'Country':
        return fake.country(),  # 国家
    if field == 'Country Code':
        return fake.country_code(),  # 国家编码
    # 'Area': fake.district(), # 仅支持中国
    if field == 'Latitude':
        return fake.latitude(),  # 地理坐标：纬度
    if field == 'Longitude':
        return fake.longitude(),  # 地理坐标：经度
    if field == 'Postcode':
        return fake.postcode(),  # 邮编
    # 'Province': return fake.province(),  # 台湾，美国没有
    if field == 'Address':
        return fake.address(),  # 详细地址
    if field == 'Street Address':
        return fake.street_address(),  # 街道地址
    if field == 'Street Name':
        return fake.street_name(),  # 街道名
    if field == 'Street Suffix':
        return fake.street_suffix(),  # 街、路
    if field == 'Building NO.':
        return fake.building_number(),  # 楼牌号 eg：'B座'

    # "基础信息伪数据"
    if field == 'SSN':
        return fake.ssn(),  # SSN号
    if field == 'Service Business':
        return fake.bs(),  # 随机公司服务行业
    if field == 'Company Name':
        return fake.company(),  # 随机公司名
    if field == 'Card Info':
        return fake.credit_card_full(),  # 生成完整信用卡信息
    if field == 'Card NO.':
        return fake.credit_card_number(card_type=None),  # 生成信用卡号
    if field == 'Card Type':
        return fake.credit_card_provider(),  # 信用卡类型
    if field == 'Card Security Code':
        return fake.credit_card_security_code(),  # 信用卡安全码
    if field == 'Job':
        return fake.job(),  # 职位

    if field == 'First Name(Female)':
        return fake.first_name_female(),  # 女性 名
    if field == 'First Name(Male)':
        return fake.first_name_male(),  # 男性 名
    if field == 'Last Name(Female)':
        return fake.last_name_female(),  # 女性
    if field == 'Last Name(Male)':
        return fake.last_name_male(),  # 男性
    if field == 'Full Name':
        return fake.name(),  # 随机生成全名
    if field == 'Male Name':
        return fake.name_male(),  # 男性全名
    if field == 'Female Name':
        return fake.name_female(),  # 女性全名
    if field == 'ISDN NO.':
        return fake.msisdn(),  # 移动台国际用户识别码，即移动用户的ISDN号码
    if field == 'Phone NO.':
        return fake.phone_number(),  # 随机生成电话号
    if field == 'NO. Segment(Phone)':
        return fake.phonenumber_prefix(),  # 随机生成手机号段如'139'

    # "网络基础信息伪数据"
    if field == 'Domain Name':
        return fake.domain_name(),  # 生成域名

    if field == 'IP Address V6':
        return fake.ipv6(),  # 随机IP6地址
    if field == 'MAC Address':
        return fake.mac_address(),  # 随机MAC地址
    if field == 'URI Address':
        return fake.uri(),  # 随机URI地址
    if field == 'URL Address':
        return fake.url(),  # 随机URL地址
    if field == 'User Name':
        return fake.user_name(),  # 随机用户名

    # "浏览器信息伪数据"
    if field == 'User Agent':
        return fake.user_agent(),  # 随机user_agent信息

    # "文件信息伪数据"
    if field == 'File Type':
        return fake.file_extension(),  # 随机文件扩展名如'avi'，'txt'
    if field == 'File Name':
        return fake.file_name(),  # 随机文件名（包含扩展名，不包含路径）
    if field == 'File Path':
        return fake.file_path(),  # 随机文件路径（包含文件名，扩展名）
    if field == 'Mime Type':
        return fake.mime_type(),  # 随机mime Type
