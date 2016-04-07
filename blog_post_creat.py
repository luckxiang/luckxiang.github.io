#!/usr/bin/env python3.5
# coding=utf-8
import time
print('creat new blog post')
print('enter blog post title:')
title=input()
print('enter tags:')
tags=input()
ISOTIMEFORMAT='%Y-%m-%d'
date=time.strftime(ISOTIMEFORMAT, time.localtime(time.time()))
filename='_posts/%s-%s.md' % (date,title)
with open(filename, 'w') as f:
    f.write('---\n')
    f.write('layout: post\n')
    f.write('title: %s\n' % title)
    f.write('date: %s\n' % date)
    f.write('categories: blog\n')
    f.write('tags: [%s]\n' % tags)
    f.write('description: \n')
    f.write('---\n')
    f.write('\n')

