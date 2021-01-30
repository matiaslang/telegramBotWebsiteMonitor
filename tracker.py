import smtplib
import bs4
import requests
import time
import difflib


def getInitialPage(siteurl, siteid):
    url = siteurl
    source = requests.get(siteurl, headers={
                          'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:32.0) Gecko/20100101 Firefox/32.0', }).text
    soup = bs4.BeautifulSoup(source, 'html.parser')
    event_string = str(soup.find('div', id=siteid))
    return event_string


def check(wclass):
    time.sleep(5)
    print('Checking site\n' + wclass.url)
    source = requests.get(wclass.url, headers={
                          'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:32.0) Gecko/20100101 Firefox/32.0', }).text
    soup = bs4.BeautifulSoup(source, 'html.parser')
    event_string_new = str(soup.find('div', id=wclass.id))
    # If the html of the form has changed trigger the email!
    if wclass.oldString != event_string_new:
        sm = difflib.SequenceMatcher(None, wclass.oldString, event_string_new)
        print(show_diff(sm))
        print("YAY, puppiees! :)")
        return True
    else:
        print("No puppies yet :(")
        return False


def show_diff(seqm):
    """Unify operations between two compared strings
seqm is a difflib.SequenceMatcher instance whose a & b are strings"""
    output = []
    for opcode, a0, a1, b0, b1 in seqm.get_opcodes():
        if opcode == 'equal':
            output.append(seqm.a[a0:a1])
        elif opcode == 'insert':
            output.append("<ins>" + seqm.b[b0:b1] + "</ins>")
        elif opcode == 'delete':
            output.append("<del>" + seqm.a[a0:a1] + "</del>")
        elif opcode == 'replace':
            pass
        else:
            raise RuntimeError
    return ''.join(output)
