---
layout: post
title: windows下Qt开发的入门指南
date: 2018-04-12
categories: blog
tags: [技术]
description: 
---

项目需要在windows上开发一些桌面软件，考虑了webUI和Qt，python等方案，由于软件对安全的要求比较高，且后续可能要考虑跨平台，虽然我很想尝试一下webUI，为了项目稳定，最终还是决定用Qt，入门指南不包含怎么开发Qt程序，只是简单介绍一下一个完整Qt程序需要关注的东西。


### 开发环境
习惯了linux开发环境，windows刚开始用起来总有一点别扭，毕竟六七年没有碰过了。Qt自带了qtcreater，不过windows下还是Visual Studio强大，因此IDE选择vs2017，先安装Qt，再把vs2017和Qt关联起来，为了兼容32位系统，我选择编译生成32位的Qt程序。

### 给程序添加ICO
完整的程序必须要有ICO，注意程序运行起来的图标和exe文件显示的图标都要添加，程序运行起来的图标需要在解决方案资源管理器的qrc文件中添加ico文件，然后在程序中添加如下代码：    
```
	setWindowTitle(tr("日历浏览器"));
	setWindowIcon(QIcon(":/QtGuiApplication1/TestIco"));
```
exe的图标直接在项目里边添加一个ico资源，添加成功后会在资源管理器里边出现相应的rc文件，当然你也可以自己编写rc文件再add进去，不过这样还用IDE干嘛呢。

### 程序打包发布
一般来说我们的程序都是动态编译的，静态编译配置比较麻烦而且容易出错，最简单的方法就是把一堆文件直接打包成一个可执行程序，如果想安装到用户系统也可以做成一个安装包，安装包这里先不说，下边提供把一堆文件打包成一个可执行程序的方法。工具为 windeployqt.exe 和Enigma Virtual Box
- windeployqt.exe 这个程序是Qt安装的时候自带的，你需要添加一下环境变量，这样可以直接到vs编译生成的qt程序目录下，执行 `windeployqt.exe xxx.exe`，然后所以依赖的库都会被拷贝过来，注意有些库可能是多余的，需要自己裁剪一下。弄好之后点击程序，看看能不能执行。
- Enigma Virtual Box 打包程序，用这个就可以把一堆文件打包成一个可执行程序
