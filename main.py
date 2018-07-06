import re
from htmlGetter import *


def tydeni(html):
    out = re.findall('[tT][ýÝ][dD]([^ˇ]*)', html)
    prep = ""
    while True:
        prep = out[0]
        if len(out) > 0:
            out = re.findall('[tT][ýÝ][dD][eE][nN]([^ˇ]*)', out[0])
            check = 1
            if len(out) > 0:
                check = re.findall('[úÚ][tT][eE][rR][ýÝ]', out[0])
            if not len(out) > 0 or len(check) == 0:
                return prep
        else:
            break
    return prep


def denni(html):
    out = re.findall('[dD][eE][nN]([^ˇ]*)', html)
    prep = ""
    while True:
        prep = out[0]
        if len(out) > 0:
            out = re.findall('[dD][eE][nN]([^ˇ]*)', out[0])
            check = 1
            if len(out) > 0:
                check = re.findall('[úÚ][tT][eE][rR][ýÝ]', out[0])
            if not len(out) > 0 or len(check) == 0:
                return prep
        else:
            break
    return prep


def obed(html):
    out = re.findall('[oO][bB][ěĚ][dD][oO][vV]([^ˇ]*)', html)
    prep = ""
    while True:
        prep = out[0]
        if len(out) > 0:
            out = re.findall('[oO][bB][ěĚ][dD][oO][vV]([^ˇ]*)', out[0])
            check = 1
            if len(out) > 0:
                check = re.findall('[úÚ][tT][eE][rR][ýÝ]', out[0])
            if not len(out) > 0 or len(check) == 0:
                return prep
        else:
            break
    return prep


def poledni(html):
    out = re.findall('[pP][oO][lL][eE][dD][nN][íÍ]([^ˇ]*)', html)
    prep = ""
    while True:
        prep = out[0]
        if len(out) > 0:
            out = re.findall('[pP][oO][lL][eE][dD]([^ˇ]*)', out[0])
            check = 1
            if len(out) > 0:
                check = re.findall('[úÚ][tT][eE][rR][ýÝ]', out[0])
            if not len(out) > 0 or len(check) == 0:
                return prep
        else:
            break
    return prep


def prepareInput(html):
    prep = html
    if 'Týdenní' in html:
        prep = tydeni(html)
    if 'Polední' in html:
        prep = poledni(html)
    if 'Denní' in html or 'DENNÍ' in html:
        prep = denni(html)
        # print(prep)
    return prep


def findBestMonday(html):
    out = re.findall('[pP][oO][nN][dD][ěĚ][lL][iIíÍ]([^ˇ]*)', html)
    prep = ""
    while True:
        prep = out[0]
        if len(out) > 0:
            out = re.findall('[pP][oO][nN][dD][ěĚ][lL][iIíÍ]([^ˇ]*)', out[0])
            if not len(out) > 0:
                return prep
        else:
            break
    return prep


def readInput():
    f = open("lastrada.html", encoding='utf-8')
    # f = open("naknofliku.html", encoding='utf-8')
    # f = open("velorex.html", encoding='utf-8')
    # f = open("faust.html", encoding='utf-8')
    # f = open("sokec.html", encoding='utf-8')

    return f.read()


def matchPrint(match):
    length = 0
    for x in match:
        stripped = (re.sub('<[^<]+?>', '', x))
        stripped = stripped.split('\n')
        for c in stripped:
            length += 1
            c = c.replace("&nbsp", "").replace(";", "")
            if len(c) < 10:
                continue
            print("<p>" + c.strip(whitespace) + "</p>")
            # if 'Kč' in c:
            #     onePrice += 1
            #     match_kc = re.findall('\d+[^ˇ]*(?=[kK][čČ])', c)
            # zjistit kolik je radku s jidlem
            # pokavad je onePrice pocet jak radku tak je cena tam
            # pokud ne je nekde na zacatk ua jeji potreba vytahnout
    return length


def matchPrintSpecific(match, menuLength):
    for x in match:
        stripped = (re.sub('<[^<]+?>', '', x))
        stripped = stripped.split('\n')
        for c in stripped:
            menuLength -= 1
            if menuLength == 0:
                break

            c = c.replace("&nbsp", "").replace(";", "")
            if len(c) < 10:
                continue
            print("<p>" + c.strip(whitespace) + "</p>")

if __name__ == "__main__":
    load = load_data('urls.csv')
    # os.system("pause")
    for link in load:
        menu_link = find_menicko_link(link[0])
        resInput = give_me_data(menu_link)
        # resInput = readInput()
        prematch = prepareInput(resInput)
        onePrice = 0
        whitespace = "\r\n\t"
        nazev = link[1]
        url = menu_link
        print("<h2>" + nazev + " - <a href='" + url + "'>" + url + "</a></h2>")
        menuLength = 0

        print("<h3>Pondělí:</h3>")
        match = re.findall(
            '[pP][oO][nN][dD][ěĚ][lL][iIíÍ][^ˇ]*(?=[úÚ][tT][eE][rR][ýÝ])', prematch)
        menuLength = matchPrint(match)

        print("<h3>Úterý:</h3>")
        match = re.findall(
            '[úÚ][tT][eE][rR][ýÝ][^ˇ]*(?=[sS][tT][řŘ][eE][dD][aA])', prematch)
        matchPrintSpecific(match, menuLength)

        print("<h3>Středa:</h3>")
        match = re.findall(
            '[sS][tT][řŘ][eE][dD][aA][^ˇ]*(?=[čČ][tT][vV][rR][tT][eE][kK])', prematch)
        # testm = re.findall(
        #     '[sS][tT][řŘ][eE][dD][aA][^ˇ]*(?=[čČ][tT][vV][rR][tT][eE][kK])', prematch)
        # print(testm)
        # exit(1)
        matchPrintSpecific(match, menuLength)

        print("<h3>Čtvrtek:</h3>")
        match = re.findall(
            '[čČ][tT][vV][rR][tT][eE][kK][^ˇ]*(?=[pP][áÁaA][tT][eE][kK])', prematch)
        matchPrintSpecific(match, menuLength)

        print("<h3>Pátek:</h3>")
        match = re.findall(
            '[pP][áÁaA][tT][eE][kK][^ˇ]*', prematch)
        matchPrintSpecific(match, menuLength)
        # exit(1)
