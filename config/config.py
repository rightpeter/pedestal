#encoding=utf-8
ENV_DICT = {}

db_config = 'mysql://ssdutnews:ssdutnewsplayswell@127.0.0.1/ssdutnews'

UPDATE_INTERVAL = 15 # seconds

RENREN_EMAIL = 'pedestal_peter@163.com'
RENREN_PW = 'pedestaldlut'

HOME_PAGE = "http://tucao.pedestal.cn"
local_page = "210.30.97.149"
ali_page = "115.28.2.165"

mail_poster = {}
mail_poster['163'] = {}
mail_poster['163']['host'] = "smtp.163.com"
mail_poster['163']['user'] = "pedestal_peter"
mail_poster['163']['pass'] = "pedestaldlut"
mail_poster['163']['postfix'] = "163.com"
mail_poster['qq'] = {}
mail_poster['qq']['host'] = "smtp.qq.com"
mail_poster['qq']['user'] = "pedestal_scott"
mail_poster['qq']['pass'] = "pedestaldlut"
mail_poster['qq']['postfix'] = "qq.com"

re_email = r'^([[a-zA-Z0-9]+[_|\_|\.]?]*[a-zA-Z0-9]+)@([[a-zA-Z0-9]+[_|\_|\.]?]*[a-zA-Z0-9]+)\.[a-zA-Z]{2,4}$'
        
avatar_path = '/home/rightpeter/github/ssdutnews/static/images/avatar/'

