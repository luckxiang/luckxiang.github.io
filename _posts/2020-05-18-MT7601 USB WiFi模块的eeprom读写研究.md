---
layout: post
title: MT7601 USB WiFi模块的eeprom读写研究
date: 2020-05-18
categories: blog
tags: [技术]
description: 
---

####  0x00 前言

MT7601的驱动是台湾人写的，没有找到太多的参考资料，自己分析了一下。
![mt7601-eeprom调用流程.png](https://i.loli.net/2020/05/18/WnmSjAPL1kEliVx.png)

#### 0x01 入口分析
首先查看eeprom.c中的RtmpChipOpsEepromHook函数，里边定义了三个宏：

- RTMP_FLASH_SUPPORT
- RTMP_EFUSE_SUPPORT
- RTMP_USB_SUPPORT

表面WiFi模块的初始化数据可以通过flash，efuse和usb三种接口读取，毎类接口又实现了init，read，wirte三个回调。驱动代码中flash读写未实现，在RTMP_EFUSE_SUPPORT和RTMP_USB_SUPPORT同时开启的情况下，优先走的RTMP_EFUSE_SUPPORT分支。

实际测试中发现RTUSBWriteEEPROM16也是工作不正常的。所以基本可以判断RTMP_USB_SUPPORT分支实现是有问题的，不再深入研究，我们继续分析RTMP_EFUSE_SUPPORT分支。

#### 0x02 RTMP_EFUSE_SUPPORT分支

EFUSE的概念是一次性可编程存储器，不过代码里的逻辑和它的命名明显不对应，可能设计之初是想用于EFUSE器件，但是后来写代码的人放飞自我，走偏了。下面来看看它的实现。

- eFuse_init

  ​	初始化接口首先会调用eFuseGetFreeBlockCount检查eeprom里边是不是写了足够的数据，假如free block太多，驱动就认为eeprom有问题，他会接着调用eFuseLoadEEPROM去加载存放在文件系统中的eeprom数据。如果加载不成功，就会使用代码里默认的EFUSE_DEFAULT_BIN数据。加载进来的内存数据存放在`pAd->EEPROMImage`, 同时会设置`pAd->bFroceEEPROMBuffer=true`。

- rtmp_ee_efuse_read16&rtmp_ee_efuse_write16

    read和write接口根据`pAd->bFroceEEPROMBuffer`的条件，选择操作内存中的EEPROMImage数据还是直接通过USB操作eeprom模块，eFuseWrite还有一个block的逻辑，毎16个字节为一个block，假如这个block全为0xFF(空的block), 那么写操作会把block数据先清0再写。



#### 0x03 总结

在目前的驱动逻辑下，如果eeprom是空片，则用户只能操作内存数据，没有办法往eeprom中写入数据，只有eeprom中写入了足够的数据，用户才可以修改eeprom。eeprom数据可能会存在三个地方：

- eeprom芯片
- 文件系统中的eeprom文件数据
- 代码的初始化数组
