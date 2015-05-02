#!/usr/bin/python

def license():

    print '\n\tCoded by Oussama ELGOUMRI (c) 2014\n\tv1.0\n'


import os
import zipfile
import json
import time
import re


class ProcessImage(object):

    def __init__(self, fileHandler):
        self.fileHandler = fileHandler
        self.Run()


    def Run(self):

        # get all the images name from the current directory
        self.file = open(self.fileHandler.filename)
        data = json.load(self.file)

        for file in os.listdir('.'):
            ext = file.split('.')[-1]

            if re.match(r'(jpg|png|jpeg)', ext, re.I):

                # add the new content to memory
                data['content'].append({
                        'path': file,
                        'title': file.split('.')[0].replace('_', ' '),
                        'description': ''
                    })
                self.file.close()

        # save the content to the file
        self.file.close()
        self.file = open(self.fileHandler.filename, 'w')
        json.dump(data, self.file)



class ProcessVideo(object):

    def __init__(self, fileHandler):
        self.fileHandler = fileHandler
        self.Run()


    def Run(self):

        # get the information required for the new content
        self.video_url = raw_input('\nvideo url > ')
        self.video_id = self.GetVideoId()
        self.iframe = '<iframe width="155" height="134" src="//www.youtube.com/embed/' + self.video_id + '?rel=0&amp;controls=0&amp;showinfo=0" frameborder="0" allowfullscreen></iframe>'

        self.video_title = raw_input('video title > ')
        self.video_description = raw_input('video description > ')

        # add the new content to memory
        self.file = open(self.fileHandler.filename)
        data = json.load(self.file)
        data['content'].append({
                'path': self.iframe,
                'title': self.video_title,
                'description': self.video_description
            })

        # save the new content to the file
        self.file.close()
        self.file = open(self.fileHandler.filename, 'w')
        json.dump(data, self.file)


    def GetVideoId(self):

        # extract the id from an ordinary youtube url
        video_id = self.video_url.split('=')[1]

        # does the url combined with any other get request? if so ..
        if video_id.find('&') is not -1:
            video_id = video_id.split('&')[0]

        return video_id



class FileHandler(object):

    def __init__(self, filename):

        # get the filename
        self.filename = filename

        if self.IsFileExists():

            # open the file then extract the content type from it
            self.file = open(self.filename)
            data = json.load(self.file)
            self.content_type = data['type']

            # remove the file
            if self.content_type == 'image':

                self.file.close()
                os.remove(self.filename)

                # initialize the json file by the very basic template
                self.file = open(self.filename, 'w')
                data = {'type': self.content_type, 'content':[]}
                json.dump(data, self.file)

            else:
                self.Backup()

            self.file.close()

        else:

            # create a new file, then initialize it with the basic template
            self.file = open(self.filename, 'w')
            self.Initialize()
            self.file.close()


    def Initialize(self):

        # get the content type from the user
        content_type = raw_input(
                        '\nthe content type is: \n' +
                        '  [1] image\n' +
                        '  [2] video\n\n' +
                        '  >>> ')

        # add the content type to the locals
        if content_type == '1':
            self.content_type = 'image'
        elif content_type == '2':
            self.content_type = 'video'

        # initialize the json file by the very basic template
        data = {'type': self.content_type, 'content':[]}
        json.dump(data, self.file)


    def Backup(self):

        # prepare the file to be zipped out
        dst = self.filename[:self.filename.rfind('.')] + time.strftime('%Y-%m-%d_%H:%M:%S') + '.json'
        with zipfile.ZipFile('content_bak.zip', 'a') as handler_bak:
            handler_bak.write(self.filename, dst)
        

    def IsFileExists(self):

        # check the file existance and report back properly
        if os.path.exists(self.filename):
            return True
        else:
            return False


def main():

    filename = 'content.json'

    fileHandler = FileHandler(filename)

    # process the file
    if fileHandler.content_type == 'image':
        process = ProcessImage(fileHandler)

    elif fileHandler.content_type == 'video':
        process = ProcessVideo(fileHandler)


    while(True):
        again = raw_input('\ncontinue (y/n) > ')

        if again == 'y' or again == 'Y' or again == '':
            process.Run()

        else:
            break

if __name__ == '__main__':
    license()
    main()
