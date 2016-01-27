#!/usr/bin/python
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
import sqlite3

from os import path
from PIL import Image
from sys import argv
from wordcloud import WordCloud, STOPWORDS

def main(save_files = False, db_filename = '../output/database.sqlite'):
    conn = sqlite3.connect(db_filename)
    c = conn.cursor()

    # Retrieve papers
    c.execute('''SELECT *
                 FROM Papers''')

    paper_content = c.fetchall()
    conn.close()

    titles = ''

    for pc in paper_content:
        titles += pc[1]

    # A Marvin Minsky mask
    mask = np.array(Image.open("../files/minsky_mask.png"))

    wc = WordCloud(background_color="white", max_words=2000, mask=mask, stopwords=STOPWORDS.copy())
    # Generate word cloud
    wc.generate(titles)
    
    if (save_files):
        # Store to file
        wc.to_file("../files/title_cloud.png")
    
    # Show word cloud
    plt.imshow(wc)
    plt.axis("off")
    # Show mask
#    plt.figure()
#    plt.imshow(mask, cmap=plt.cm.gray)
#    plt.axis("off")
    plt.show()

if __name__ == '__main__':
    if ('--help' in argv) or ('-h' in argv):
        print("Explores the papers submitted to NIPS 2015.")
        print("Usage: %s -s [database_filename]" % argv[0])
        print("Option -s: Save plots in ../files")
        print("Option [database_filename]: Supply a database other than '../output/database.sqlite'")
    else:
        kwargs = {}
        if len(argv) > 1:
            if ('-s' == argv[1]):
                kwargs['save_files'] = True
        if len(argv) > 2:
            kwargs['db_filename'] = argv[2]
        main(**kwargs)
