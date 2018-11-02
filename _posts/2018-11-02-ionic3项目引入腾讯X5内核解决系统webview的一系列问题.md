---
layout: post
title: ionic3项目引入腾讯X5内核解决系统webview的一系列问题
date: 2018-11-02
categories: blog
tags: [技术]
description: 
---

### 系统webview的问题
虽然安卓系统4.x之后已经切换到了chromium内核,但是依旧存在性能低下,不同版本页面渲染效果不一致的问题,特别是我们的设备属于定制系统,系统版本为5.1,在该版本上,存在一个严重的内存泄露的问题,如果高频的分配变量,则内存回收会出现问题,拷机发现约20个小时会泄露800M,由于我们的设备需要监测传感器每秒的数据变化,该问题会直接影响我们设备的稳定性,如果无法解决,整个方案必须推倒重来.我首先想到的是切换到Crosswalk,性能和效果都很满意,但是运行一段时间之后程序会死机.还好后来发现了腾讯的X5内核,引入之后测试了一个周,性能表现很稳定.开心!!!!


### 接入方法

接入很简单,有人已经写好了插件  
```
ionic cordova plugin add cordova-plugin-x5-webview    

cordova build android
```

### 判断X5内核是否启动
可以通过浏览器的userAgent来判断x5内核是否启用     
```
     getBrowserKernel(){
        let ua = navigator.userAgent;
        let key = "TBS/";
        let start = ua.indexOf(key);
        this.browserKernel = "系统内核";
        if (start !== -1) {
            start = start + key.length;
            this.browserKernel = "X5内核:" + ua.substr(start, ua.indexOf(" ", start) - start);
        }
    }

```

### X5内核无法启动怎么办?
X5内核优先采用共享模式,如果没有的话会去下载,如果实在启动不了,说明系统中可能没有X5内核,开发板连接wifi,安装开发组提供的TBSdemo APK,通过这个apk去安装X5内核.然后重新安装应用并启动试试.
