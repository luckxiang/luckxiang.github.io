---
layout: post
title: C语言跳坑之0x00:char和unsigned char
date: 2016-05-16
categories: blog
tags: [技术]
description: 
---

在c语言中，char是一个有点特殊的变量，变量有signed和unsigned之分，一般情况下signed变量我们在书写的时候都省略掉了signed，编译器会自动识别为signed，但是char型变量却不一定，它是signed还是unsigned是由编译器决定的，通常编译器会有一个选项开关来决定它是有符号数还是无符号数。这就导致我们直接用char型变量会带来很大的安全隐患，原因如下：  
首先在内存中，signed char与unsigned char没有什么不同，都是一个字节，唯一的区别是，signed char的最高位为符号位，因此signed char能表示-128~127, unsigned char没有符号位，因此能表示0~255。在读写文件和网络数据流的时候，signed char和unsigned char，读取结果都一样，如果把它们赋值给int，unsigned int，long等其他数据类型时，假如最高位是符号位且值为1，则系统会对signed char进行扩展，在前边补上1，而如果符号位是0或者为unsigned char，则不会扩展。在这种情况下，当最高位为0时，两者结果一致，最高位为1时，两者运行结果不一致。由此可见，使用char型变量时一定要十分小心。  
判断编译器的默认char符号代码

```
#include <stdio.h>
int main(void)
{
    char c = -1;
    if(c < 200){
        printf("signed char\n");
    }
    else
    {
        printf("unsigned char\n");
    }
    return 0;
}
```

关于char还有一个特殊的语言就是char *，它在C/C++中有专门的语义，既不同于signed char *，也不同于unsigned char *，专门用于指以'\0'为结束的字符串
C语言是弱类型还没什么，如果在C++中，你可以试一试，用

```
char *p = "abcd";
```

是可以通过编译的,  
但如果用

```
signed char *p = "abcd";
unsigned char *pp = "abcd";
```

都是不能通过编译的。

