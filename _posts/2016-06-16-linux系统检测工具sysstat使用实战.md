---
layout: post
title: Linux系统检测工具sysstat使用实战
date: 2016-06-16
categories: blog
tags: [技术]
description: sysstat是linux系统下的一个软件包，包含一组监测系统性能以及效率的工具，它的主要用途是观察服务负载，比如CPU和内存的占用率、网络的使用率以及磁盘写入和读取速度等。
---

用sysstat工具对某机顶盒系统进行性能分析，从cpu性能，内存，网络流量三个方面进行测试.
sysstat是linux系统下的一个软件包，包含一组监测系统性能以及效率的工具，它的主要用途是观察服务负载，比如CPU和内存的占用率、网络的使用率以及磁盘写入和读取速度等。

#### 参数和命令介绍：
 sar 的命令格式为：
 
sar  [ -A ] [ -b ] [ -B ] [ -c ] [ -d ] [ -i interval ] [ -p ] [ -q ]
     [ -r ] [ -R ] [ -t ] [ -u ] [ -v ] [ -V ] [ -w ] [ -W ] [ -y ]
     [ -n { DEV | EDEV | NFS | NFSD | SOCK | ALL } ]
     [ -x { pid | SELF | ALL } ] [ -X { pid | SELF | ALL } ] 
     [ -I { irq | SUM | ALL | XALL } ] [ -P { cpu | ALL } ]
     [ -o [ filename ] | -f [ filename ] ]
     [ -s [ hh:mm:ss ] ] [ -e [ hh:mm:ss ] ] 
     [ interval [ count ] ]

其中：
interval : 为取样时间间隔
count : 为输出次数，若省略此项，默认值为 1
常用选项：

    选项 说明
    -A 	等价于 -bBcdqrRuvwWy -I SUM -I XALL -n ALL -P ALL
    -b 	显示I/O和传送速率的统计信息
    -B 	输出内存页面的统计信息
    -c 	输出进程统计信息，每秒创建的进程数
    -d 	输出每一个块设备的活动信息
    -i interval 	指定间隔时长，单位为秒
    -p 	显示友好设备名字，以方便查看，也可以和-d 和-n 参数结合使用，比如 -dp 或-np
    -q 	输出进程队列长度和平均负载状态统计信息
    -r 	输出内存和交换空间的统计信息
    -R 	输出内存页面的统计信息
    -t 	读取 /var/log/sa/saDD 的数据时显示其中记录的原始时间，如果没有这个参数使用用户的本地时间
    -u 	输出CPU使用情况的统计信息
    -v 	输出inode、文件和其他内核表的统计信息
    -V 	输出版本号信息
    -w 	输出系统交换活动信息
    -W 	输出系统交换的统计信息
    -y 	输出TTY设备的活动信息
    -n {DEV|EDEV|NFS|NFSD|SOCK|ALL} 	分析输出网络设备状态统计信息。
    DEV 	报告网络设备的统计信息
    EDEV 	报告网络设备的错误统计信息
    NFS 	报告 NFS 客户端的活动统计信息
    NFSD 	报告 NFS 服务器的活动统计信息
    SOCK 	报告网络套接字（sockets）的使用统计信息
    ALL 	报告所有类型的网络活动统计信息
    -x {pid|SELF|ALL} 	输出指定进程的统计信息。
    pid 	用 pid 指定特定的进程
    SELF 	表示 sar 自身
    ALL 	表示所有进程
    -X {pid|SELF|ALL} 	输出指定进程的子进程的统计信息
    -I {irq|SUM|ALL|XALL} 	输出指定中断的统计信息。
    irq 	指定中断号
    SUM 	指定输出每秒接收到的中断总数
    ALL 	指定输出前16个中断
    XALL 	指定输出全部的中断信息
    -P {cpu|ALL} 	输出指定 CPU 的统计信息
    -o filename 	将输出信息保存到文件 filename
    -f filename 	从文件 filename 读取数据信息。filename 是使用-o 选项时生成的文件。
    -s hh:mm:ss 	指定输出统计数据的起始时间
    -e hh:mm:ss 	指定输出统计数据的截至时间，默认为18:00:00

1、输出CPU使用情况的统计信息

    # sar -u
    12:00:01 AM CPU     %user     %nice   %system   %iowait    %steal     %idle
    12:10:01 AM all      0.02      0.00      0.14      0.01      0.00     99.84
    12:20:01 AM all      0.02      0.00      0.12      0.01      0.00     99.86
    12:30:01 AM all      0.01      0.00      0.12      0.01      0.00     99.86
    Average:    all      0.03      0.00      0.13      0.01      0.00     99.84

输出项说明：
CPU 	all 表示统计信息为所有 CPU 的平均值。
%user 	显示在用户级别(application)运行使用 CPU 总时间的百分比。
%nice 	显示在用户级别，用于nice操作，所占用 CPU 总时间的百分比。
%system 	在核心级别(kernel)运行所使用 CPU 总时间的百分比。
%iowait 	显示用于等待I/O操作占用 CPU 总时间的百分比。
%steal 	管理程序(hypervisor)为另一个虚拟进程提供服务而等待虚拟 CPU 的百分比。
%idle 	显示 CPU 空闲时间占用 CPU 总时间的百分比。

> 若 %iowait 的值过高，表示硬盘存在I/O瓶颈 若 %idle 的值高但系统响应慢时，有可能是 CPU 等待分配内存，此时应加大内存容量 若 %idle 的值持续低于 10，则系统的 CPU 处理能力相对较低，表明系统中最需要解决的资源是CPU。

2、输出内存页面的统计信息

    # sar -B
    12:00:01 AM  pgpgin/s pgpgout/s   fault/s  majflt/s
    12:10:01 AM      0.00      4.17      9.74      0.00
    12:20:01 AM      0.00      2.71      2.24      0.00
    12:30:01 AM      0.00      2.69      2.25      0.00
    Average:         0.00      3.17      4.07      0.00

输出项说明：
pgpgin/s 	每秒钟从磁盘读入的系统页面的 KB 总数
pgpgout/s 	每秒钟向磁盘写出的系统页面的 KB 总数
fault/s 	系统每秒产生的页面失效(major + minor)数量
majflt/s 	系统每秒产生的页面失效(major)数量

 3、输出内存和交换空间的统计信息

    # sar -r
    12:00:01 AM kbmemfree kbmemused  %memused kbbuffers  kbcached kbswpfree kbswpused  %swpused  kbswpcad
    12:10:01 AM    262068    253408     49.16     43884    156456   1048568         0      0.00         0
    12:20:01 AM    261572    253904     49.26     44580    156448   1048568         0      0.00         0
    12:30:01 AM    260704    254772     49.42     45124    156472   1048568         0      0.00         0
    Average:       259551    255925     49.65     46453    156470   1048568         0      0.00         0

输出项说明：
kbmemfree 	可用的空闲内存数量，单位为 KB
kbmemused 	已使用的内存数量（不包含内核使用的内存），单位为 KB
%memused 	已使用内存的百分数
kbbuffers 	内核缓冲区（buffer）使用的内存数量，单位为 KB
kbcached 	内核高速缓存（cache）数据使用的内存数量，单位为 KB
kbswpfree 	可用的空闲交换空间数量，单位为 KB
kbswpused 	已使用的交换空间数量，单位为 KB
%swpused 	已使用交换空间的百分数
kbswpcad 	交换空间的高速缓存使用的内存数量

 4、 输出系统交换的统计信息

    # sar -W
    12:00:01 AM  pswpin/s pswpout/s
    12:10:01 AM      0.00      0.00
    12:20:01 AM      0.00      0.00
    12:30:01 AM      0.00      0.00
    Average:         0.00      0.00

输出项说明：
pswpin/s 	每秒系统换入的交换页面（swap page）数量
pswpout/s 	每秒系统换出的交换页面（swap page）数量

5、输出进程队列长度和平均负载状态统计信息

    # sar -q
    12:00:01 AM   runq-sz  plist-sz   ldavg-1   ldavg-5  ldavg-15
    12:10:01 AM         0        85      0.02      0.01      0.00
    12:20:01 AM         0        85      0.01      0.00      0.00
    12:30:01 AM         0        85      0.03      0.01      0.00
    Average:            0        85      0.01      0.00      0.00

输出项说明：
runq-sz 	运行队列的长度（等待运行的进程数）
plist-sz 	进程列表中进程（processes）和线程（threads）的数量
ldavg-1 	最后1分钟的系统平均负载（System load average）
ldavg-5 	过去5分钟的系统平均负载
ldavg-15 	过去15分钟的系统平均负载

 6、输出网络设备状态的统计信息

    # sar -n DEV
    12:00:01 AM     IFACE   rxpck/s   txpck/s   rxbyt/s   txbyt/s   rxcmp/s   txcmp/s  rxmcst/s
    12:10:01 AM      eth0      0.59      0.92     41.57    893.98      0.00      0.00      0.00
    12:20:01 AM      eth0      0.55      0.88     37.50    859.56      0.00      0.00      0.00
    12:30:01 AM      eth0      0.55      0.86     38.17    871.98      0.00      0.00      0.00
    Average:         eth0      0.29      0.42     21.05    379.29      0.00      0.00      0.00

输出项说明：
IFACE 	网络设备名
rxpck/s 	每秒接收的包总数
txpck/s 	每秒传输的包总数
rxbyt/s 	每秒接收的字节（byte）总数
txbyt/s 	每秒传输的字节（byte）总数
rxcmp/s 	每秒接收压缩包的总数
txcmp/s 	每秒传输压缩包的总数
rxmcst/s 	每秒接收的多播（multicast）包的总数

#### 部分测试数据
该部分测试数据为测试中的一部分且都是统计出来的平均值，更多数据请参考测试数据附件。
CPU相关数据
播放前：

    [root@luckxiang /]# sar -u -q 3 100 
    Linux 2.6.27.55 (luckxiang)        01/01/15        _csky_  (1 CPU)
    Average:        CPU     %user     %nice   %system   %iowait    %steal     %idle
    Average:        all      0.96      0.00      7.96      0.00      0.00     91.08
    
    Average:      runq-sz  plist-sz   ldavg-1   ldavg-5  ldavg-15   blocked
    Average:            2        79      1.37      1.30      1.25         0

播放中：

    [root@luckxiang /]# sar -u -q 3 100 
    Linux 2.6.27.55 (luckxiang)        01/01/15        _csky_  (1 CPU)
     Average:        CPU     %user     %nice   %system   %iowait    %steal     %idle
    Average:        all      4.74      0.00     18.43      0.00      0.00     76.83
    
    Average:      runq-sz  plist-sz   ldavg-1   ldavg-5  ldavg-15   blocked
    Average:            3        86      1.30      1.30      1.25         0


内存相关数据：
播放前：

    [root@luckxiang /]# sar -r -B -W 3 100 
    Linux 2.6.27.55 (luckxiang)        01/01/15        _csky_  (1 CPU)
    
    Average:     pswpin/s pswpout/s
    Average:         0.00      0.00
    
    Average:     pgpgin/s pgpgout/s   fault/s  majflt/s  pgfree/s pgscank/s pgscand/s pgsteal/s    %vmeff
    Average:         0.00      0.00    553.47      0.00    155.36      0.00      0.00      0.00      0.00
    
    Average:    kbmemfree kbmemused  %memused kbbuffers  kbcached  kbcommit   %commit  kbactive   kbinact   kbdirty
    Average:        26609     39071     59.49      5904     13360    264302    402.41      9918     15368         0

播放中：

    [root@luckxiang /]# sar -r -B -W 3 100 
    Linux 2.6.27.55 (luckxiang)        01/01/15        _csky_  (1 CPU)
    Average:     pswpin/s pswpout/s
    Average:         0.00      0.00
    
    Average:     pgpgin/s pgpgout/s   fault/s  majflt/s  pgfree/s pgscank/s pgscand/s pgsteal/s    %vmeff
    Average:         0.00      0.00    549.03      0.00    181.96      0.00      0.00      0.00      0.00
    
    Average:    kbmemfree kbmemused  %memused kbbuffers  kbcached  kbcommit   %commit  kbactive   kbinact   kbdirty
    Average:        21805     43875     66.80      5904     13360    293345    446.63     14403     15368         0

流量相关数据：
   

    客户提供的测试链接
    [root@luckxiang /]# sar -n DEV 2 100 |grep -E 'ra0|IFACE'
    Average:        IFACE   rxpck/s   txpck/s    rxkB/s    txkB/s   rxcmp/s   txcmp/s  rxmcst/s   %ifutil
    Average:          ra0    174.68     43.86    194.59      3.68      0.00      0.00      0.00      0.00
    云端链接：
    [root@luckxiang /]# sar -n DEV 2 100 |grep -E 'ra0|IFACE'
    Average:        IFACE   rxpck/s   txpck/s    rxkB/s    txkB/s   rxcmp/s   txcmp/s  rxmcst/s   %ifutil
    Average:          ra0    128.38     65.23     89.67      6.65      0.00      0.00      0.00      0.00
    有线连接：
    Average:        IFACE   rxpck/s   txpck/s    rxkB/s    txkB/s   rxcmp/s   txcmp/s  rxmcst/s   %ifutil
    Average:         eth0    129.17     41.48    178.44      2.67      0.00      0.00      0.00      0.00



在测试2中，我观察了内存，CPU和流量数据，不同的播放源，对CPU的消耗是不一样的，内存也有充足的剩余空间，播放普通视频CPU空闲时间百分比比较高，播放M3U8视频CPU空闲时间百分比基本为0。补充测试了连接有线的情况，结果差别很大，最大能到1M多，慢的时候和wifi差不多，在有线网速很快的情况下，播放M3U8格式的凤凰视频的时候，也多次出现了缓冲的情况。而播放普通视频则没有出现缓冲。

根据测试分析如下：
是否CPU在播放M3U8格式视频的时候处理能力不够。M3U8格式视频播放的时候，基本上都是隔4，5秒才会下载一次数据，样机也基本上是隔4,5秒取一次数据，我觉得可以关注下M3U8格式视频的解析过程，是不是这个地方解析的时候存在瓶颈，解析太慢导致缓存耗尽，还是说多线程下载过程中影响了当前播放下载线程的速度，所以需要确认两个点，一个是客户测试用的是什么连接，一个是M3U8处理流程是怎么样子的。

