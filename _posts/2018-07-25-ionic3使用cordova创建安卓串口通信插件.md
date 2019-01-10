---
layout: post
title: ionic3使用cordova创建安卓串口通信插件
date: 2018-07-25
categories: blog
tags: [技术]
description: 
---

#### 创建cordova插件工程
首先安装plugman工具，然后用该工具创建一个插件工程
```
npm install -g plugman
plugman create --name SerialPortPlugin --plugin_id com.plugin.SerialPortPlugin --plugin_version 1.0.0
```
然后在src目录下创建android文件夹用来存放java代码，js则放在www中，plugin已经帮我们创建了js文件。plugin.xml是我们的配置文件，我们需要把包含的java文件引入其中，否则安装插件时java文件会被忽略,具体配置参数见源码。         
java和js的对应关系很简单，在js里边应用exec接口，然后在java里边创建一个继承自CordovaPlugin的类，然后在execute函数中处理响应。js函数有success和error两个回调函数，java则通过callbackContext.success和CallbackContext.error返回回调执行结果。下边是对应的接口设计代码。
```
var exec = require('cordova/exec');


var SerialPort = {

    openSerialPort: function (settings, success, error) {
        exec(success, error, "SerialPortPlugin", "openSerialPort", [settings]);
    },
    closeSerialPort: function (success, error) {
        exec(success, error, "SerialPortPlugin", "closeSerialPort", []);
    },
    writeSerialData: function (data, success, error) {
        exec(success, error, "SerialPortPlugin", "writeSerialData", [data]);
    },
    sendDataAndWaitResponse: function (data, success, error) {
        exec(success, error, "SerialPortPlugin", "sendDataAndWaitResponse", [data]);
    },
    readSerialData: function (success, error) {
        exec(success, error, "SerialPortPlugin", "readSerialData", []);
    }

};

module.exports = SerialPort;
```

```
public class SerialPortPlugin extends CordovaPlugin {
    private SerialPort serialPort;
    private InputStream inputStream;
    private OutputStream outputStream;
    private ReadDataThread readThread;

    @Override
    public boolean execute(String action, JSONArray args, CallbackContext callbackContext) throws JSONException {
        if (action.equals("openSerialPort")) {
            String message = args.getString(0);
            this.openSerialPort(message, callbackContext);
            return true;
        }
        else if (action.equals("writeSerialData")) {
            String message = args.getString(0);
            this.writeSerialData(message, callbackContext);
            return true;
        }
        else if (action.equals("readSerialData")) {
            this.readSerialData(callbackContext);
            return true;
        }
        else if (action.equals("sendDataAndWaitResponse")) {
            String message = args.getString(0);
            this.sendDataAndWaitResponse(message, callbackContext);
            return true;
        }
        else if (action.equals("closeSerialPort")) {
            this.closeSerialPort(callbackContext);
            return true;
        }

        return false;
    }
}
```

#### 设计思路
怎么创建一个插件我们了解了，下边就是串口插件怎么设计，串口是一个驱动设备，我们数据流程是从js=>java=>android=>serial dev,由于安卓没有提供串口驱动操作接口，java=>android=>serial dev,这个环节需要用JNI来实现，即先用c/c++编写串口操作接口，然后用JNI封装成java接口，JNI这里不展开介绍，相关代码为工程里边的libs so库和SerialPort.java代码。        
数据流打通了，接下来就是我们的接口怎么定义，一般来说串口只需要有open， write和read，close就可以了，但是需要注意，通信协议一般都是发送一帧数据，然后等待应答，由于js是采用回调的方式获取插件的返回数据，那么在应用层read和write会变成两个异步操作。这样会导致发送一帧数据没收到应答又发送一帧数据的情况。所以针对这种问题，必须要在java层把这两个过程封装在一起，即发送一帧数据之后收到应答才返回结果。代码中的sendDataAndWaitResponse接口提供了这个功能。          
我们在前边讲了数据的流程和接口的定义，但是还有一个重要的问题没有解决，就是数据应该以何种形式传递，单片机一般采用16进制，而js字符串更容易操作。通信协议通常按定义好的数据一帧一帧传递，同时串口对数据传输效率没那么高的要求，从便于处理的角度，我们把数据都序列化成hex string。如0x12a3序列化成"12a3",FormatUtil.java中提供了函数来处理字符串和16进制数据的互相转换。          
流程和数据都处理好了，接下来就是系统相关的一些细节问题，由于read接口没数据的时候会导致阻塞，js又是单线程执行，一旦阻塞程序直接卡死，因此read必须实现为非阻塞模式且有超时机制，刚开始写这个插件的时候对java的NIO不熟悉，我自己写了一个读线程来实现非阻塞读。读取的过程中，假如数据帧比较长，会发生数据一次read读不完的情况，必须要判断数据帧的长度，然后循环读取，保证数据帧的完整性。          
思路介绍就到这里，总的来说cordova串口插件编写还是很简单的，不需要太多的专业知识即可完成，具体源码可以查看我的github[https://github.com/luckxiang/cordova-plugin-serial-port](https://github.com/luckxiang/cordova-plugin-serial-port)
