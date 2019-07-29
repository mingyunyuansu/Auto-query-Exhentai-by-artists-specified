import requests
import webbrowser
import time
import json
from bs4 import BeautifulSoup


headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'
}


#Prepare cookies, used in requests.get() below
cookies_f = open('ecookies.txt', 'r')
cookies_copy = eval(cookies_f.read())
cookies_f.close()


cookies = {}
for each_item in cookies_copy:
    cookies[each_item['name']] = each_item['value']


url = 'https://e-hentai.org/'

#template of url
url1 = r'https://e-hentai.org/?f_cats=1017&f_search='
#url2 = r'&f_apply=Apply+Filter'


artists = ['tiramisu', 'kimura neito', 'somejima', 'ichinose', 'pochi-goya', '由浦', 'kazakura', 'jitaku vacation', 'windarteam', 'kuronomiki', 'Nanahara Fuyuki', 'Oohira Sunset',
           'bifidus', 'bang-you', 'lorica', 'sugarbt', 'muneshiro', 'pyon-kti', 'nosebleed', 'komagata', 'ringoya', 'shinozuka yuuji', 'morikawa', 'ma-kurou', 'kyockcho', 'navier haruka', 'akigami satoru', 'shoot the moon', 'Yakitate Jamaica (Aomushi)', 'Neet', 'Brio', '八', '小島', '月野', '鬼月', '靴下', '瓜皮', '黑锅', '直人', '丧尸', 'doumou', 'kaiki', 'kobayashi youkoh',
           '武田', 'okayusan', 'ken-1', 'tonnosuke', 'shioroku', 'meme50', 'type-g', 'kemokomoya', 'ahegao', 'shiina kazuki', 'karasu', 'cyclone', 'kenja time', 'Nasi-pasuya', 'Muchakai', 'PIANIISHIMO', 'gokuburi', 'banana koubou', 'yukiusagi', 'taira issui', 'arakure', 'E-musu', 'gessyu', 'kurowa', 'Funabori Nariaki', 'Orutoro', 'chin']
    

def req_by_name(name):
    #get method, loaded by get()
    payload = {'f_doujinshi': '1',
           'f_manga': '1',
           'f_artistcg': '0',
           'f_gamecg': '0',
           'f_western': '0',
           'f_non-h': '0',
           'f_imageset': '0',
           'f_cosplay': '0',
           'f_asianporn': '0',
           'f_misc': '0',
           'f_search': None,
           'f_apply': 'Apply+Filter'}
    payload['f_search'] = name
    #r = requests.get(url, cookies=cookies, headers=headers, params=payload)
    r = requests.get(url, headers=headers, cookies=cookies, params=payload)
    print(name)
    return r.text

def main_process():

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
        soup = BeautifulSoup(html_text, features='lxml')
        collection = []
        for each in soup.find_all(class_='gl4t glname glink'):    
            collection.append(each.get_text())
        new[each_name] = collection
        # Since the e-hentai forbides some content available on the ex-hentai, we now have to verify is this item availble on the e-hentai
        if not new[each_name]:
            continue
        if each_name not in old.keys() or old[each_name][0] != new[each_name][0]:
            webbrowser.open(url1+each_name, new=2)
            cnt += 1
            print('\t---changed to', new[each_name][0])

    js = json.dumps(new)
    f = open('old.txt', 'w')
    f.write(js)
    f.close()
    #routine for gmgard
    webbrowser.open('https://gmgard.com', new=2)
    print('\n\n\n***Finished***\n', cnt, 'changed.')

def main():
    start_time = time.clock() #Timing
    retry_times = 0
    '''
    while True:
        try:
            main_process()
            break
        except requests.RequestException as err:
            print('\n\n\n***', err, '***\n\n\n')
            print('restart')
            retry_times += 1
            if retry_times >= 10:
                break
        except BaseException as unk_err:
            print('Unknow error, quit', unk_err, time.clock()-start_time)
            break
        finally:
            print(time.clock()-start_time)
            print('Retried', retry_times, 'times')
    '''
    main_process()
    print(time.clock()-start_time)

if __name__=='__main__':
    main()

'''
#Initialize(or reset) the old.txt by json
js = json.dumps(new)
f = open('old.txt', 'w')
f.write(js)
f.close()
'''

