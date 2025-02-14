from PIL import Image
import requests
import os 
import json
import datetime

def get_images(): 
    # do stuff to get images here
    print('get images')
    #&until=0 < Add for cursor value
    cursor = ''
    run = True
    while run:
        if (cursor == ''):
            url = 'https://public.api.bsky.app/xrpc/app.bsky.feed.searchPosts?sort=latest&limit=100&q=p4a2025&until='# + str(cursor)
        else:
            url = 'https://public.api.bsky.app/xrpc/app.bsky.feed.searchPosts?sort=latest&limit=100&q=p4a2025&until=' + str(cursor)
        response = requests.get(url)
        pos = -1
        if 'posts' not in response.json():
            run = False
        else:
            for x in response.json()['posts']:
                pos += 1
                avatar = x['author']['avatar']
                # this will also serve as the file name 👇🏻
                handle = './avatars/'+x['author']['handle']+'.jpg'
                image = requests.get(avatar).content
                with open(handle, 'wb') as handler:
                    handler.write(image)
                #last element
                if pos == len(response.json()['posts']) -1:
                    cursor = x['record']['createdAt']
            print(cursor)
            if len(response.json()['posts']) < 100:
                run = False
        # disable once ready to loop forever 👇🏻
        # run = False

def count_pixels(): 
    # do stuff to count quantities here
    print('get counts')
    lpurp = 0 #E1DBFF
    dpurp = 0 #938AE3
    green = 0 #D3FF6A
    other = 0 #NA
    directory = os.fsencode('./avatars/')

    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        im = Image.open('./avatars/'+filename)
        pix = im.load()
        hexcode = '#%02x%02x%02x' % pix[60, 350]
        if (hexcode == '#e1dbff'):
            lpurp += 1
        elif (hexcode == '#d3ff6a'):
            green += 1
        elif (hexcode == '#938ae3'):
            dpurp += 1
        else:
            other += 1
    print('light purple:',lpurp)
    print('dark purple:',dpurp)
    print('lime:',green)
    print('other:',other)
    updatedAt = datetime.datetime.now()
    d = {
        'lightPurple': lpurp,
        'darkPurple': dpurp,
        'lime': green,
        'other': other,
        'updatedAt': str(updatedAt.year) + '-' + str(updatedAt.month) + '-' + str(updatedAt.day) + ' '+ str(updatedAt.hour)+':' + str(updatedAt.minute)
    }
    with open('data.json', 'w') as file: 
        json.dump(d, file)


# def test():
#     filename = 'andincorporated.bsky.social.jpg'
#     im = Image.open('./avatars/'+filename)
#     pix = im.load()
#     hexcode = '#%02x%02x%02x' % pix[60, 350]
#     print(hexcode)

get_images()
count_pixels()
# test()