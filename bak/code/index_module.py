# -*- coding: utf-8 -*-
"""
Created on Sat Dec  5 23:31:22 2015

@author: bitjoy.net
"""

from os import listdir
import xml.etree.ElementTree as ET
import jieba
import sqlite3
import configparser

class Doc:
    docid = 0
    date_time = ''
    tf = 0
    ld = 0
    def __init__(self, docid, tf, ld):
        self.docid = docid
        self.tf = tf
        self.ld = ld
    def __repr__(self):
        return(str(self.docid) + '\t' + str(self.tf) + '\t' + str(self.ld))
    def __str__(self):
        return(str(self.docid) + '\t' + str(self.tf) + '\t' + str(self.ld))

class IndexModule:
    stop_words = set()
    postings_lists = {}
    
    config_path = ''
    config_encoding = ''
    
    def __init__(self, config_path, config_encoding):
        self.config_path = config_path
        self.config_encoding = config_encoding
        config = configparser.ConfigParser()
        config.read(config_path, config_encoding)
        f = open(config['DEFAULT']['stop_words_path'], encoding = config['DEFAULT']['stop_words_encoding'])
        words = f.read()
        self.stop_words = set(words.split('\n'))

    def is_number(self, s):
        try:
            float(s)
            return True
        except ValueError:
            return False
        
    def clean_list(self, seg_list):
        cleaned_dict = {}
        n = 0
        for i in seg_list:
            i = i.strip().lower()
            if i != '' and not self.is_number(i) and i not in self.stop_words:
                n = n + 1
                if i in cleaned_dict:
                    cleaned_dict[i] = cleaned_dict[i] + 1
                else:
                    cleaned_dict[i] = 1
        return n, cleaned_dict
    
    # def write_postings_to_db(self, db_path):
    #
    #
    #
    
    def construct_postings_lists(self):
        config = configparser.ConfigParser()
        config.read(self.config_path, self.config_encoding)

        db_path = config['DEFAULT']['db_path']
        conn = sqlite3.connect(db_path)
        c = conn.cursor()

        c.execute('''DROP TABLE IF EXISTS postings''')
        c.execute('''CREATE TABLE postings
                             (term TEXT PRIMARY KEY, df INTEGER, folder INTEGER, docs TEXT)''')

        for folder_i in range(1, 11):
            files = listdir(config['DEFAULT']['doc_dir_path'] + '{}'.format(folder_i))
            AVG_L = 0
            for i in files:
                print(config['DEFAULT']['doc_dir_path'] + '{}/'.format(folder_i) + '{}'.format(i))
                root = ET.parse(config['DEFAULT']['doc_dir_path'] + '{}/'.format(folder_i) + i).getroot()
                title = root.find('title').text
                body = root.find('body').text
                docid = int(root.find('id').text)
                # date_time = root.find('datetime').text


                try:
                    seg_list = jieba.lcut(title + '。' + body, cut_all=False)
                    ld, cleaned_dict = self.clean_list(seg_list)

                    AVG_L = AVG_L + ld

                    for key, value in cleaned_dict.items():
                        d = Doc(docid, value, ld)
                        if key in self.postings_lists:
                            self.postings_lists[key][0] = self.postings_lists[key][0] + 1  # df++
                            self.postings_lists[key][1].append(d)
                        else:
                            self.postings_lists[key] = [1, [d]]  # [df, [Doc]]
                except TypeError as e:
                    print(i)

            if (len(files) > 0):
                AVG_L = AVG_L / len(files)
                config.set('DEFAULT', 'N', str(len(files)))
                config.set('DEFAULT', 'avg_l', str(AVG_L))
                with open(self.config_path, 'w', encoding = self.config_encoding) as configfile:
                    config.write(configfile)
                for key, value in self.postings_lists.items():
                    doc_list = '\n'.join(map(str, value[1]))
                    c.execute("INSERT INTO postings VALUES (?, ?, ?, ?)", (key, value[0], folder_i, doc_list))
        conn.commit()
        conn.close()

if __name__ == "__main__":
    im = IndexModule('../config.ini', 'utf-8')
    im.construct_postings_lists()
