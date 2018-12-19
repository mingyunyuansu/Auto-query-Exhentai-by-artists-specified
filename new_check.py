import requests
import webbrowser
import time
import json
from bs4 import BeautifulSoup

#Timing, make sure no problem
start_time = time.clock()

#Prepare cookies, used in requests.get() below
cookis_f = open('cookie.txt', 'r')
cookies_copy = eval(cookis_f.read())
cookis_f.close()

cookies = {}
for each_item in cookies_copy:
    cookies[each_item['name']] = each_item['value']

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'
}


url = 'https://exhentai.org/'

#template of url
url1 = r'https://exhentai.org/?f_doujinshi=1&f_manga=1&f_artistcg=1&f_gamecg=1&f_western=1&f_non-h=1&f_imageset=1&f_cosplay=1&f_asianporn=1&f_misc=1&f_search='
url2 = r'&f_apply=Apply+Filter'


artists = ['tiramisu', 'kimura neito', 'somejima', 'ichinose', 'pochi-goya', '由浦', 'kazakura', 'jitaku vacation', 'windarteam', 'Nekokaburi', 'yontarou', 'Oohira Sunset',
           'bifidus', 'bang-you', 'lorica', 'sugarbt', 'muneshiro', 'pyon-kti', 'nosebleed', 'komagata', 'ringoya', 'shinozuka yuuji', 'morikawa', 'ma-kurou', 'kyockcho', 'navier haruka', 'akigami satoru', 'shoot the moon', 'Yakitate Jamaica (Aomushi)', 'Neet', 'Brio', '八', '小島', '月野', '鬼月', '靴下', '瓜皮', '黑锅', '直人', '丧尸', 'doumou', 'kaiki', 'kobayashi youkoh',
           '武田', 'okayusan', 'ken-1', 'tonnosuke', 'shioroku', 'meme50', 'type-g', 'kemokomoya', 'ahegao', 'shiina kazuki', 'karasu', 'cyclone', 'kenja time', 'Nasi-pasuya', 'Muchakai', 'PIANIISHIMO', 'gokuburi', 'banana koubou', 'yukiusagi', 'taira issui', 'arakure', 'E-musu', 'gessyu', 'kurowa', 'Funabori Nariaki']

def req_by_name(name):
    #get method, loaded by get()
    payload = {'f_doujinshi': '1',
           'f_manga': '1',
           'f_artistcg': '1',
           'f_gamecg': '1',
           'f_western': '1',
           'f_non-h': '1',
           'f_imageset': '1',
           'f_cosplay': '1',
           'f_asianporn': '1',
           'f_misc': '1',
           'f_search': None,
           'f_apply': 'Apply+Filter'}
    payload['f_search'] = name
    r = requests.get(url, cookies=cookies, headers=headers, params=payload)
    print(name)
    return r.text

old = {} #A dict, artist:[manga's names]
new = {}

#Read from old.txt which contains old data to be compared
file = open('old.txt', 'r') 
js = file.read()
old = json.loads(js)   
file.close()

cnt = 0 #counting for altered object
for each_name in artists:
    html_text = req_by_name(each_name)
    soup = BeautifulSoup(html_text)
    collection = []
    for each in soup.find_all(class_='id2'):
        collection.append(each.a.get_text())
    new[each_name] = collection
    if each_name not in old.keys() or old[each_name][0] != new[each_name][0]:
        webbrowser.open(url1+each_name+url2)
        cnt += 1
        print('----------------------changed from', old[each_name][0], 'to', new[each_name][0])

js = json.dumps(new)
f = open('old.txt', 'w')
f.write(js)
f.close()
#routine for gmgard
webbrowser.open_new('https://gmgard.com')
print('OK', cnt, 'changed.')
print('duration', time.clock()-start_time)



'''
Initialize(or reset) the old.txt by json
js = json.dumps(new)
f = open('old.txt', 'w')
f.write(js)
f.close()
'''

