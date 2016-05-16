#!/usr/bin/env python3.5
# coding=utf-8
import time
import os

title = input('Creat new blog post\nPlease enter blog post title:')
tags = input('Please enter tags:')
ISOTIMEFORMAT = '%Y-%m-%d'
date = time.strftime(ISOTIMEFORMAT, time.localtime(time.time()))
filename = '_posts/%s-%s.md' % (date,title)
with open(filename, 'w') as f:
    f.write('---\n')
    f.write('layout: post\n')
    f.write('title: %s\n' % title)
    f.write('date: %s\n' % date)
    f.write('categories: blog\n')
    f.write('tags: [%s]\n' % tags)
    f.write('description: \n')
    f.write('---\n\n\n')
sys = 'vi  "%s"' % filename
os.system(sys)
