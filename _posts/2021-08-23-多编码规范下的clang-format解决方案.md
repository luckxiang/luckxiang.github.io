---
layout: post
title: 多编码规范下的clang-format解决方案
date: 2021-08-23
categories: blog
tags: [技术]
description: 
---

## 0x00 需求场景
在嵌入式日常开发中，我们经常会遇到多编码规范的场景，比如团队A和团队B采用了不同的编码规范，内核代码和应用代码采用不同的编码规范，三方库A和三方库B采用了不同的编码规范。如果我们的工作涉及到以上场景，开发团队对代码的质量又有所追求，
那么编码规范的切换将是一个痛苦的问题。根据我的经验，我整理了如下需求：

- 开发者应该把精力放在开发工作上，采用自己习惯的编码规范工作，通过工具统一格式化代码，并把格式化排版引入开发流程中。
- 格式化排版工具要支持只针对修改补丁进行格式化，避免在维护代码的时候引入过多无关的修改。
- 格式化排版工具要容易集成，可以适配多种常见的编辑器。
- 格式化排版工具的配置要具有可读性，方便针对不同项目进行修改和维护。
- 可以在代码中灵活的禁用格式化，解决部分屎山代码格式化后变得更糟糕的问题。

## 0x01 clang-format介绍
根据上述需求，对比了网上多种格式化排版工具，我最终选择了clang-format工具。
[官网地址：https://clang.llvm.org/docs/ClangFormat.html](https://clang.llvm.org/docs/ClangFormat.html)

> ClangFormat describes a set of tools that are built on top of LibFormat. It can support your workflow in a variety of ways including a standalone tool and editor integrations.

ClangFormat描述了一组构建在[LibFormat](https://clang.llvm.org/docs/LibFormat.html)之上的 [工具](https://clang.llvm.org/docs/LibFormat.html)。它可以通过多种方式支持您的工作流程，包括独立工具和编辑器集成。

```shell
$ clang-format -help
OVERVIEW: A tool to format C/C++/Java/JavaScript/JSON/Objective-C/Protobuf/C# code.

If no arguments are specified, it formats the code from standard input
and writes the result to the standard output.
If <file>s are given, it reformats the files. If -i is specified
together with <file>s, the files are edited in-place. Otherwise, the
result is written to the standard output.

USAGE: clang-format [options] [<file> ...]

OPTIONS:

Clang-format options:

  --Werror                   - If set, changes formatting warnings to errors
  --Wno-error=<value>        - If set don't error out on the specified warning type.
    =unknown                 -   If set, unknown format options are only warned about.
                                 This can be used to enable formatting, even if the
                                 configuration contains unknown (newer) options.
                                 Use with caution, as this might lead to dramatically
                                 differing format depending on an option being
                                 supported or not.
  --assume-filename=<string> - Override filename used to determine the language.
                               When reading from stdin, clang-format assumes this
                               filename to determine the language.
  --cursor=<uint>            - The position of the cursor when invoking
                               clang-format from an editor integration
  --dry-run                  - If set, do not actually make the formatting changes
  --dump-config              - Dump configuration options to stdout and exit.
                               Can be used with -style option.
  --fallback-style=<string>  - The name of the predefined style used as a
                               fallback in case clang-format is invoked with
                               -style=file, but can not find the .clang-format
                               file to use.
                               Use -fallback-style=none to skip formatting.
  --ferror-limit=<uint>      - Set the maximum number of clang-format errors to
                               emit before stopping (0 = no limit). Used only
                               with --dry-run or -n
  -i                         - Inplace edit <file>s, if specified.
  --length=<uint>            - Format a range of this length (in bytes).
                               Multiple ranges can be formatted by specifying
                               several -offset and -length pairs.
                               When only a single -offset is specified without
                               -length, clang-format will format up to the end
                               of the file.
                               Can only be used with one input file.
  --lines=<string>           - <start line>:<end line> - format a range of
                               lines (both 1-based).
                               Multiple ranges can be formatted by specifying
                               several -lines arguments.
                               Can't be used with -offset and -length.
                               Can only be used with one input file.
  -n                         - Alias for --dry-run
  --offset=<uint>            - Format a range starting at this byte offset.
                               Multiple ranges can be formatted by specifying
                               several -offset and -length pairs.
                               Can only be used with one input file.
  --output-replacements-xml  - Output replacements as XML.
  --sort-includes            - If set, overrides the include sorting behavior
                               determined by the SortIncludes style flag
  --style=<string>           - Coding style, currently supports:
                                 LLVM, Google, Chromium, Mozilla, WebKit.
                               Use -style=file to load style configuration from
                               .clang-format file located in one of the parent
                               directories of the source file (or current
                               directory for stdin).
                               Use -style="{key: value, ...}" to set specific
                               parameters, e.g.:
                                 -style="{BasedOnStyle: llvm, IndentWidth: 8}"
  --verbose                  - If set, shows the list of processed files

Generic Options:

  --help                     - Display available options (--help-hidden for more)
  --help-list                - Display list of available options (--help-list-hidden for more)
  --version                  - Display the version of this program
```

通过指定`--style=file`，我们可以修改一个`.clang-format`文件来指定我们的编码排版规范，可用的样式选项在[Clang-Format 样式选项](https://clang.llvm.org/docs/ClangFormatStyleOptions.html)中描述。此外，官网还描述了多种编辑器的集成方法以及补丁格式化排版方法，在此不再赘述。

## 0x02 clang-format安装

### Windows：

去官网https://llvm.org/builds/下载相应的版本，点击安装即可。

### mac:

```shell
brew install clang-format
```

### ubuntu

方法一：

```shell
sudo apt-get install clang-format
```

方法二:

方法一安装的版本由于镜像源的原因，有可能版本会比较低，让人觉得不舒服，那么可以采用方法二来做：

- 打开网站https://apt.llvm.org/，可以发现提供了一个自动更新的脚本，我们把它下载下来：


  ```
  wget https://apt.llvm.org/llvm.sh
  chmod +x llvm.sh
  ```

- 脚本主要是根据不同的操作系统版本，去添加软件源。假如我们不需要安装完整的llvm，打开脚本，把最后一行apt-get install安装软件的命令注释掉。

  ```shell
  # apt-get install -y clang-$LLVM_VERSION lldb-$LLVM_VERSION lld-$LLVM_VERSION clangd-$LLVM_VERSION
  ```

- 执行脚本

  ```shell
  sudo ./llvm.sh
  ```

- 查询高版本的软件并安装

  ```
  apt search clang-format
  ```

  > ➜  Downloads apt search clang-format
  > 正在排序... 完成
  > 全文搜索... 完成  
  > arcanist-clang-format-linter/bionic,bionic 0.git20161021-2 all
  >   clang-format linter for Arcanist
  >
  > clang-format/bionic-updates 1:6.0-41~exp5~ubuntu1 amd64
  >   Tool to format C/C++/Obj-C code
  >
  > clang-format-10/bionic-updates,bionic-security 1:10.0.0-4ubuntu1~18.04.2 amd64
  >   Tool to format C/C++/Obj-C code
  >
  > clang-format-13/未知,now 1:13.0.0~++20210822101306+23ba3732246a-1~exp1~20210822082112.56 amd64 

比如我这里查询的最高版本是clang-format-13，直接安装这个版本并做一个软连接方便使用。

```shell
sudo apt-get install clang-format-13
sudo ln -s /usr/bin/clang-format-13 /usr/bin/clang-format
sudo ln -s /usr/bin/clang-format-diff-13 /usr/bin/clang-format-diff
```



## 0x03 clang-format使用

- 各个项目的编码规范制定人员完成`.clang-format`的编辑，并放入项目的顶层目录。
- 检查老代码，可以根据自己项目情况，（这里要特别小心评估代码大范围变动的影响）把格式强制刷一遍，或者只是对一些格式化后无法对齐的代码禁用格式化，`clang-format off`,`clang-format on`。
- 如果要求强制检测提交补丁的编码排版格式，则可以让管理员在服务端做一个pre-check，不符合规范的代码不允许提交。

- 开发人员安装clang-format工具，并把工具集成到版本管理工具中，官网有命令可以参考。我采用的集成方式如下，在.gitconfig中添加如下命令：

  ```
  clang-format-cached = !git diff -U0 --no-color --relative --cached | clang-format-diff -p1 -i && git status
  clang-format-head = !git diff -U0 --no-color --relative HEAD^ | clang-format-diff -p1 -i && git status
  
  ```

- `git clang-format-cached` 命令对暂存区的修改补丁进行格式化，而 `git clang-format-head`则对commit提交进行格式化。我喜欢手动格式化以后检查再提交，开发人员可以根据自己的需求修改执行命令。

  **tips**: `clang-format`可以根据文件路径路径，自动从位于输入文件的最近父目录中的文件往前搜索`.clang-format`配置，因此只需要在相关项目的顶层目录放置一份配置即可。如果有子项目，则只需要在子项目中放置一份配置即可覆盖父项目的配置。

## 0x04 附录：部分样式选项中文翻译

这里偷懒放一份别人做的`LLVM .clang-format`样式翻译，可以参考一下：

```shell
---
# 语言: None, Cpp, Java, JavaScript, ObjC, Proto, TableGen, TextProto
Language:   Cpp
# BasedOnStyle: LLVM
# 访问说明符(public、private等)的偏移
AccessModifierOffset:   -4
# 开括号(开圆括号、开尖括号、开方括号)后的对齐: Align, DontAlign, AlwaysBreak(总是在开括号后换行)
AlignAfterOpenBracket:  Align
# 连续赋值时，对齐所有等号
AlignConsecutiveAssignments:    true
# 连续声明时，对齐所有声明的变量名
AlignConsecutiveDeclarations:   true
# 左对齐逃脱换行(使用反斜杠换行)的反斜杠
AlignEscapedNewlinesLeft:   true
# 水平对齐二元和三元表达式的操作数
AlignOperands:  true
# 对齐连续的尾随的注释
AlignTrailingComments:  true
# 允许函数声明的所有参数在放在下一行
AllowAllParametersOfDeclarationOnNextLine:  true
# 允许短的块放在同一行
AllowShortBlocksOnASingleLine:  false
# 允许短的case标签放在同一行
AllowShortCaseLabelsOnASingleLine:  false
# 允许短的函数放在同一行: None, InlineOnly(定义在类中), Empty(空函数), Inline(定义在类中，空函数), All
AllowShortFunctionsOnASingleLine:   Empty
# 允许短的if语句保持在同一行
AllowShortIfStatementsOnASingleLine:    false
# 允许短的循环保持在同一行
AllowShortLoopsOnASingleLine:   false
# 总是在定义返回类型后换行(deprecated)
AlwaysBreakAfterDefinitionReturnType:   None
# 总是在返回类型后换行: None, All, TopLevel(顶级函数，不包括在类中的函数), 
#   AllDefinitions(所有的定义，不包括声明), TopLevelDefinitions(所有的顶级函数的定义)
AlwaysBreakAfterReturnType: None
# 总是在多行string字面量前换行
AlwaysBreakBeforeMultilineStrings:  false
# 总是在template声明后换行
AlwaysBreakTemplateDeclarations:    false
# false表示函数实参要么都在同一行，要么都各自一行
BinPackArguments:   true
# false表示所有形参要么都在同一行，要么都各自一行
BinPackParameters:  true
# 大括号换行，只有当BreakBeforeBraces设置为Custom时才有效
BraceWrapping:   
  # class定义后面
  AfterClass:   false
  # 控制语句后面
  AfterControlStatement:    false
  # enum定义后面
  AfterEnum:    false
  # 函数定义后面
  AfterFunction:    false
  # 命名空间定义后面
  AfterNamespace:   false
  # ObjC定义后面
  AfterObjCDeclaration: false
  # struct定义后面
  AfterStruct:  false
  # union定义后面
  AfterUnion:   false
  # catch之前
  BeforeCatch:  true
  # else之前
  BeforeElse:   true
  # 缩进大括号
  IndentBraces: false
# 在二元运算符前换行: None(在操作符后换行), NonAssignment(在非赋值的操作符前换行), All(在操作符前换行)
BreakBeforeBinaryOperators: NonAssignment
# 在大括号前换行: Attach(始终将大括号附加到周围的上下文), Linux(除函数、命名空间和类定义，与Attach类似), 
#   Mozilla(除枚举、函数、记录定义，与Attach类似), Stroustrup(除函数定义、catch、else，与Attach类似), 
#   Allman(总是在大括号前换行), GNU(总是在大括号前换行，并对于控制语句的大括号增加额外的缩进), WebKit(在函数前换行), Custom
#   注：这里认为语句块也属于函数
BreakBeforeBraces:  Custom
# 在三元运算符前换行
BreakBeforeTernaryOperators:    true
# 在构造函数的初始化列表的逗号前换行
BreakConstructorInitializersBeforeComma:    false
# 每行字符的限制，0表示没有限制
ColumnLimit:    200
# 描述具有特殊意义的注释的正则表达式，它不应该被分割为多行或以其它方式改变
CommentPragmas: '^ IWYU pragma:'
# 构造函数的初始化列表要么都在同一行，要么都各自一行
ConstructorInitializerAllOnOneLineOrOnePerLine: false
# 构造函数的初始化列表的缩进宽度
ConstructorInitializerIndentWidth:  4
# 延续的行的缩进宽度
ContinuationIndentWidth:    4
# 去除C++11的列表初始化的大括号{后和}前的空格
Cpp11BracedListStyle:   false
# 继承最常用的指针和引用的对齐方式
DerivePointerAlignment: false
# 关闭格式化
DisableFormat:  false
# 自动检测函数的调用和定义是否被格式为每行一个参数(Experimental)
ExperimentalAutoDetectBinPacking:   false
# 需要被解读为foreach循环而不是函数调用的宏
ForEachMacros:  [ foreach, Q_FOREACH, BOOST_FOREACH ]
# 对#include进行排序，匹配了某正则表达式的#include拥有对应的优先级，匹配不到的则默认优先级为INT_MAX(优先级越小排序越靠前)，
#   可以定义负数优先级从而保证某些#include永远在最前面
IncludeCategories: 
  - Regex:  '^"(llvm|llvm-c|clang|clang-c)/'
    Priority:   2
  - Regex:  '^(<|"(gtest|isl|json)/)'
    Priority:   3
  - Regex:  '.*'
    Priority:   1
# 缩进case标签
IndentCaseLabels:   false
# 缩进宽度
IndentWidth:    4
# 函数返回类型换行时，缩进函数声明或函数定义的函数名
IndentWrappedFunctionNames: false
# 保留在块开始处的空行
KeepEmptyLinesAtTheStartOfBlocks:   true
# 开始一个块的宏的正则表达式
MacroBlockBegin:    ''
# 结束一个块的宏的正则表达式
MacroBlockEnd:  ''
# 连续空行的最大数量
MaxEmptyLinesToKeep:    1
# 命名空间的缩进: None, Inner(缩进嵌套的命名空间中的内容), All
NamespaceIndentation:   Inner
# 使用ObjC块时缩进宽度
ObjCBlockIndentWidth:   4
# 在ObjC的@property后添加一个空格
ObjCSpaceAfterProperty: false
# 在ObjC的protocol列表前添加一个空格
ObjCSpaceBeforeProtocolList:    true
# 在call(后对函数调用换行的penalty
PenaltyBreakBeforeFirstCallParameter:   19
# 在一个注释中引入换行的penalty
PenaltyBreakComment:    300
# 第一次在<<前换行的penalty
PenaltyBreakFirstLessLess:  120
# 在一个字符串字面量中引入换行的penalty
PenaltyBreakString: 1000
# 对于每个在行字符数限制之外的字符的penalty
PenaltyExcessCharacter: 1000000
# 将函数的返回类型放到它自己的行的penalty
PenaltyReturnTypeOnItsOwnLine:  60
# 指针和引用的对齐: Left, Right, Middle
PointerAlignment:   Left
# 允许重新排版注释
ReflowComments: true
# 允许排序#include
SortIncludes:   true
# 在C风格类型转换后添加空格
SpaceAfterCStyleCast:   false
# 在赋值运算符之前添加空格
SpaceBeforeAssignmentOperators: true
# 开圆括号之前添加一个空格: Never, ControlStatements, Always
SpaceBeforeParens:  ControlStatements
# 在空的圆括号中添加空格
SpaceInEmptyParentheses:    false
# 在尾随的评论前添加的空格数(只适用于//)
SpacesBeforeTrailingComments:   2
# 在尖括号的<后和>前添加空格
SpacesInAngles: true
# 在容器(ObjC和JavaScript的数组和字典等)字面量中添加空格
SpacesInContainerLiterals:  true
# 在C风格类型转换的括号中添加空格
SpacesInCStyleCastParentheses:  true
# 在圆括号的(后和)前添加空格
SpacesInParentheses:    true
# 在方括号的[后和]前添加空格，lamda表达式和未指明大小的数组的声明不受影响
SpacesInSquareBrackets: true
# 标准: Cpp03, Cpp11, Auto
Standard:   Cpp11
# tab宽度
TabWidth:   4
# 使用tab字符: Never, ForIndentation, ForContinuationAndIndentation, Always
UseTab: Never
...
```
