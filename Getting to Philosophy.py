import urllib.request
import time

# starting url input and opening its source code as string
site_url = input('please enter the starting site(please add a space to the end of the link): ')
site_html = str(urllib.request.urlopen(site_url).read())

# processing of the new pages
# title --> page title, visited --> pages visited
home_url = 'https://en.wikipedia.org'
visited = []
title = ''
while title != 'Philosophy':
    site_html = site_html[site_html.find('<p>') - 1:]

    # take only the wanted parts of the html file
    total_page = ''
    timeout = 5
    while site_html.find('<p>') and timeout != 0:
        total_page += site_html[site_html.find('<p>'): site_html.find('</p>')]
        site_html = site_html[site_html.find('</p>') + 1:]
        timeout -= 1

    # ignore anything inside parentheses
    parentheses_counter = 0
    while total_page.find('(') < total_page.find('href="') and total_page.find('(') != -1:
        parentheses_counter += 1
        total_page = total_page[total_page.find('(') + 2:]
        while parentheses_counter != 0:
            if total_page.find('(') < total_page.find(')') and total_page.find('(') != -1:
                parentheses_counter += 1
                total_page = total_page[total_page.find('(') + 2:]
            else:
                parentheses_counter -= 1
                total_page = total_page[total_page.find(')') + 1:]

    # get the api and title of the next page
    first_reference = total_page[total_page.find('href="') + 6:]
    while first_reference[0] != '/':
        first_reference = first_reference[first_reference.find('href="') + 6:]
    new_url = home_url + first_reference[:first_reference.find('"')]
    to_get_title = first_reference[first_reference.find('title="') + 7:]
    title = to_get_title[:to_get_title.find('"')]

    # search for a loop
    try:
        visited.index(title)
        print('we entered a loop')
        break
    except:
        visited.append(title)

    print(title)
    site_html = str(urllib.request.urlopen(new_url).read())
    time.sleep(0.5)

