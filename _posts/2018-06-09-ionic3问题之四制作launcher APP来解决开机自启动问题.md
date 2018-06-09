---
layout: post
title: ionic3问题之四制作launcher APP来解决开机自启动问题
date: 2018-06-09
categories: blog
tags: [技术]
description: 
---

这几天为了解决ionic的自启动问题,茶饭不思,寝食难安.终于搞定了.问题背景如下:

#### 问题
原来的Android定制系统是4.4.2,自启动只需要弄个autostart插件就可以了,但是4.4.2有个致命问题,运行不够流畅,即使改了浏览器内核之后效果也满足不了要求,于是我把系统升级到了6.0.1.流畅性倒是大大提高了,然而自启动不能用了.这几天把autostart插件代码和Android广播相关的知识看了好几遍,也做了很多尝试,任然没有解决问题.个人比较怀疑这个是不是系统的bug了.

#### 曲线救国之路
想靠debug插件代码没走通,结果发现了launcher APP,之前没有系统的学习过Android,居然没发现这个对我来说非常好的特性,开机直接运行APP,连桌面都不用加载了.避免客户进行一些奇怪的操作.简直完美.真所谓"山穷水尽疑无路,柳暗花明又一村".直接修改'./platforms/android/AndroidManifest.xml',添加两行配置
```
<intent-filter android:label="@string/launcher_name">
    <action android:name="android.intent.action.MAIN" />
    <category android:name="android.intent.category.LAUNCHER" />
    <category android:name="android.intent.category.HOME" /> //新增配置, 设置该组件为Home Activity
    <category android:name="android.intent.category.DEFAULT" /> //新增配置, Android系统中默认的执行方式，按照普通Activity的执行方式执行。表示所有intent都可以激活它
</intent-filter>

```
加上上边最后两行配置以后,重新编译运行程序,设置程序为默认 launcher,重启.
