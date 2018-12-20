---
layout: post
title: gcc扩展__attribute__((constructor))详解和在.a库中的使用方法
date: 2016-09-04
categories: blog
tags: [技术]
description: 
---

gcc对c语言做了很多扩展，使得c语言的表现力得到了很大的增强，本文主要介绍一下constructor扩展，这个扩展和C＋＋的构造函数很像，它会在main函数之前由程序加载器自动调用，与之相对的是destructor，它会在main函数执行结束或者exit的时候自动调用，由于两个扩展是一对，destructor这里就不介绍了。ANSI C标准还引入了atexit函数，这个是在进程结束的时候自动调用。和destructor也比较相似。  
constructor扩展的用法如下     

```
void func() __attribute__((constructor));                              
```

他有如下规则
- 构造函数先于main函数而执行
- 不同构造函数如果在同一个文件中，则先出现的函数后执行
- 对于不同文件中的构造函数，编译命令中后出现的.c文件的构造函数先执行

利用constructor属性，我们可以定义一些宏来实现模块的自动注册机制。也就是说我们用宏自动构造注册函数，然后把注册函数赋予constructor属性，这样我们在添加新的模块的时候就不需要显示的调用注册函数来，只需要在模块文件内加上一个宏调用即可。例子如下：

```
#define INITIALIZER(f) \
   static void f(void) __attribute__((constructor)); \
   static void f(void)               

#define FAP_REGISTER(name)                                              \
  INITIALIZER(fap_register_ ## name) {                                  \
    fileaccess_register_entry(&fa_protocol_ ## name);			\
  }
```

然后我们只要在模块内调用`FAP_REGISTER(fs);`即可，这样做的好处是添加新的模块更加方便，代码维护也更简单，那么问题来了，假如我们现在有这样一套注册机制的模块，我们把它编译成.a库集成到现在的应用方案中，应用没有在任何地方调用我们的注册函数，编译出来的结果能正确自动调用注册函数吗？答案是可能会出问题，定义constructor属性的函数会放在elf文件的constructor区域，在链接的时候由于我们的注册函数没被调用，所以编译器很可能做优化，不去链接我们的注册函数，这样elf文件的constructor区域就没有我们的注册函数，自然注册函数就不会自动的调用了，解决办法就是在链接的时候强制把.a里所有的函数都链接到可执行文件中。我们使用-Wl,--whole-archive和 -Wl,--no-whole-archive这两个链接命令来做这件事情。--whole-archive 可以把在其后面出现的静态库包含的函数和变量输出到结果中，--no-whole-archive 则关掉这个特性。你不想把--whole-archive后边所有.a库的函数和变量都链接到输出结果的时候就需要用--no-whole-archive了，这里需要注意的是-wl，--whole-archive 和 --no-whole-archive 是ld专有的命令行参数，gcc 并不认识，要通gcc传递到 ld，需要在他们前面加 -Wl,例子如下:

```
gcc main.o  -lb.a -wl,--whole-archive -lmode_fs.a -wl, --no-whole-archive -lc.a -lz.a -o man 
```
