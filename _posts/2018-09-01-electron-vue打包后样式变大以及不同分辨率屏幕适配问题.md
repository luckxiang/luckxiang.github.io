---
layout: post
title: electron-vue打包后样式变大以及不同分辨率屏幕适配问题
date: 2018-09-01
categories: blog
tags: [技术]
description: 
---
#### 背景
公司产品中的桌面程序部分,我选用的是electron-vue的技术方案,最近功能开发完了,npm run build 打包之后发现界面的样式和npm run dev调试时候样式不一样,整体偏大一些,装到另一台电脑,发现差别更大了,怀疑是屏幕分辨率适配的问题,试了一下,果然如此,解决方案很简单,先读取电脑屏幕的系统分辨率,然后做一下缩放适配,这样在不同的电脑上显示效果都一样了.

#### 处理方案
在man.js中引入如下代码

```
var devInnerHeight = 1080.0 // 开发时的InnerHeight
var devDevicePixelRatio = 1.0// 开发时的devicepixelratio
var devScaleFactor = 1.3 // 开发时的ScaleFactor
var scaleFactor = require('electron').screen.getPrimaryDisplay().scaleFactor
var zoomFactor = (window.innerHeight / devInnerHeight) * (window.devicePixelRatio / devDevicePixelRatio) * (devScaleFactor / scaleFactor)
require('electron').webFrame.setZoomFactor(zoomFactor)
```

简单解释一下, zoomFactor就是缩放比例了,你把devInnerHeight设置成你开发时设置的electron窗体分辨率,(比如我用的1920 * 1080),然后调节devScaleFactor达到自己想要的效果即可
