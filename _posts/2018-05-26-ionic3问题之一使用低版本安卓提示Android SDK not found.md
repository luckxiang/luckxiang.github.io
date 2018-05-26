---
layout: post
title: ionic3问题之一配置低版本安卓提示Android SDK not found
date: 2018-05-26
categories: blog
tags: [技术]
description: 
---

### 问题描述
需要Android上开发一些东西,原生开发效率太低,维护也麻烦,最后选了ionic3来作为开发方案.环境配置如下:
```
Ionic Framework: 3.9.2
Ionic App Scripts: 3.1.9
Angular Core: 5.2.10
Angular Compiler CLI: 5.2.10
Node: 8.10.0
Cordova:8.0.0

```
系统默认安装的安卓版本是7.0.0,在该版本上运行编译都正常,我想降低到5.0.0,然后提示
```
> cordova run android
(node:7421) UnhandledPromiseRejectionWarning: CordovaError: Android SDK not found. Make sure that it is installed. If it is not at the default location, set the ANDROID_HOME environment variable.
    at /home/luckyxiang/Workspace/github/ionic-conference-app/platforms/android/cordova/lib/check_reqs.js:45:27
```

### 解决方法
要解决这个问题有两个东西需要注意:
一个是去Android studio的 'SDK Manager'配置里边下载相关的API版本库.      
另外一个是对于5.0.0的版本,我的tools工具的版本(27.2.9)太高了,虽然我安装了对应版本的API库,但还是会提示Android SDK not found,下载[tools_r25.2.3](https://dl.google.com/android/repository/tools_r25.2.3-linux.zip),然后替换SDK目录下的tools即可.


