import os,re,sys,random
from time import sleep
try:
     from colorama import init,Fore
     import requests
     import urllib3
     urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
     from bs4 import BeautifulSoup as bs
except ImportError:
     exit("[!] Module not installed\n[+] Using : pip install -r requirements.txt to installing module")
init(autoreset=True)
W = Fore.WHITE
G = Fore.GREEN
C = Fore.CYAN
Y = Fore.YELLOW
R = Fore.RED
LW = "\033[1;97m"
rgb=random.choice([G,C,Y])
result_song=[]



#MainCode
def clear():
    os.system("clear")

def banner():
    clear()
    print(f"""
                  {LW}MIDI DOWNLOADER
             {rgb}https://github.com/AinxBOT{W}""")
    print(f"{R}－"*27)


def parse_input(pilih):
    items = pilih.split(',')
    result = []
    for item in items:
        if '-' in item:
            start, end = item.split('-')
            result.extend(range(int(start), int(end)+1))
        else:
            result.append(int(item))
    return sorted(set(result))


def search_music(query):
    req=requests.get("https://www.hamienet.com",verify=False).text
    i=re.findall(r'form action="/index.iva" method="GET"><input type="hidden" name="i" value="(.*?)">',req)[0]
    search=requests.get(f"http://www.hamienet.com/index.iva?i={i}&cat_id=midi&query={query}",verify=False).text
    if "Search returns no results." in str(search):
       print(f"{R}[!]{W} Music not found")
       sleep(5)
       os.system("python midi.py")
    else:
        results=bs(search,"html.parser").find_all("div", class_="linklist_lc")
        for result in results:
            link=result.find("a",class_="song")
            artist = ""
            for i, item in enumerate(result.contents):
                if item.name == "br" and i + 1 < len(result.contents):
                   artist = result.contents[i + 1].strip()
                   break
            result_song.append(link["href"]+"|"+link.text+" - "+artist)
    return result_song

def download_music(url, filename):
    try:
        req = requests.get(url, verify=False).text
        soup = bs(req, "html.parser")

        a_tag = soup.find("a", href=lambda x: x and x.endswith(".mid"))
        if not a_tag:
            print(f"{R}[!]{W} MIDI file not found in:{rgb} {url}")
            return

        mid_link = "https://www.hamienet.com" + a_tag["href"]
        r = requests.get(mid_link, verify=False)
        if "audio/midi" not in r.headers.get("Content-Type", ""):
            print(f"{R}[!]{W} Failed to download:{rgb} {filename} {R}(Invalid content)")
            return

        folder = "/sdcard/midi"
        os.makedirs(folder, exist_ok=True)
        path = os.path.join(folder, filename)

        with open(path, "wb") as f:
            f.write(r.content)
            for i in list('/|/-•'):
                print(f"\r{G}[*]{W} Download : {rgb}{i}", end=" ")
                sleep(1)
        print(f"\r{G}[√]{W} Download : ✅")
        print(f"\r{G}[√]{W} File tersimpan di :{rgb} {path}")
    except Exception as e:
        exit(f"{R}[!]{W} Error downloading {rgb}{filename}{W}: {R}{e}")

if __name__=="__main__":
    banner()
    judul=input(f"{rgb}[?]{W} Title of music : {rgb}")
    print(f"{R}－"*27)
    try:
         music = search_music(judul)
         for i, song in enumerate(music):
             num = f"{i+1:02}" if i+1 < 10 else str(i+1)
             print(f'{rgb}{num}). {W}{song.split("|")[1]}')
         print(f"{rgb}00).{W} Exit")
         print(f"{R}－"*27)
         print(f"{rgb}[INFO]{W} Choose tracks to download:")
         print(f"{rgb}>>>{W}       [1]       - Single track")
         print(f"{rgb}>>>{W}       [1,2,4]   - Custom multiple")
         print(f"{rgb}>>>{W}       [2-5]     - Range selection")
         pilih = input(f"{rgb}[?]{W} >>> {rgb}").strip()
         print(f"{R}－"*27)
         if pilih in ["00", "0"]:
            exit(f"{R}[!] {W}Program finished")
         indexes = [i-1 for i in parse_input(pilih)]
         for idx in indexes:
             href, title = music[idx].split("|")
             url = "https://www.hamienet.com" + href
             filename = title.replace(" ", "_") + ".mid"
             print(f"{G}[↓]{W} Downloading {rgb}{title}")
             download_music(url, filename)
         print(f"\n{G}[✓] {W}All downloads finished.")
         print(f"{R}－"*27)
         input(f"{W}[  {rgb}Press Enter To Back  {W}]")
         os.system("python midi.py")
    except Exception as e:
         exit(f"{R}[!]{W} Program stopped : {rgb}{e}")
