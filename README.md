# chinese_number_recognition
没有参考网上资料，由自己独立完成以下部分，最后有部分实例，更多请参考test_by_sentence_result文件。

## 文件结构说明
**sentence_data.txt**：测使用例，里面有测试用的句子和一些单独的中文数字（包括混合形式）

**test_by_sentence_result**：数据测试出来的结果存储。

**chinese_number_translate.py**：里面是此次任务的各种functions。

**test_by_sentence.py**：用此文件测试句子。

**utils.py**：定义Number类，以及导入文件方法。

## 解决需求的思路说明
### 关于识别时的基本参数
基本参数包括单位和基本数字。他们是两个词典，对于单位来说，一共有六个单位，分别是个、十、百、千、万、亿，关于他们的映射值比如字符串“万”，映射到的值是10000。而基本数字是0-9的中文表达的字符串，它们映射到值本身。

### 识别句子（utf8编码）中的中文或数字表达
设置一个字符串num和一个数组nums，然后将当前的句子进行遍历，如果当前的字是单位或者数字（包括中文和阿拉伯数字）或者逗号的话，便将其加入到num中去，这个过程在一个while循环中，直到当前的index是最后一个或者不是一个数字的组成部分时，跳出这个循环。这时如果num的长度大于零，便记录信息并将其加入到nums数组中去，最后初始化num字符串。最后返回nums数组。这样就可以把需要的中文数字提取出来。

### 能够识别纯中文数字表达
首先需要对这个数字进行预处理，将其中的逗号“,”（为之后的混合形式进行处理）和“个”（如“一个亿”）这些没有语意的部分删除。

然后，遇到这个问题，我的想法是，第一，“零”是一个标志，在零之后和之前的部分都是一个完整的中文数字，比如一千零一十，一千和一十便是两个完整的部分。因此我们可以用“零”来切割这个中文数字，然后将各个部分代表的阿拉伯数字求出来，在相加即可，当然需要注意前一部分的单位大小。

第二，以最大单位为界限，对这个词再次进行切割，这个最大单位的前面部分一定是一个完整的中文数字，而之后的部分有三种情况。

情况1. 之后的部分只有一个数字，那这个数字的单位便是比最大单位小十倍的一个单位。例如一万一，最大单位是万，则一万是一个完整的单位，而一代表的是一千。

情况2. 二是之后的部分长度大于1，那么他一定代表了一个完整的数字例如一千一百一十，则一百一十一是一个完整的数字。

情况3. 三是之后的部分长度为零，我们直接取之前的部分求值即可，例如一万，一千，一百。

最后在对每个词进行切割，以最大单位为界限，算出之前的部分和之后的部分分别代表的值，再将其相加，这可以用递归实现，我们便可求得纯中文的阿拉布数字形式。

### 能够识别中英文混合的数字表达
识别中英文混合的数字表达形式。这个的话和之前的思路比较类似，因为阿拉伯数字之后是单位或者结尾。这样的话，我们在用最大单位进行切割的时候，只需要判断前后部分是否是阿拉伯数字，如果是的话，返回即可。

### 支持基本的阿拉伯数字的识别
在之前的步骤已经把逗号删掉了。如果只是阿拉伯数字，在算法中会首先判断是否是数字，如果是的话输出即可。

### 考虑单位从大到小识别
关于这点，我有一些自己的想法，但是仍需要进行确认。

我认为对于单位从小到大来说，我们需要从最大单位开始，检测此单位前后两个部分是否存在这种情况。考虑单位从大到小排列并不是一刀切，例如“三千三百万”，我们就不应该分成三千和三百万。而哪些情况会需要进行切割呢？我认为，当当前最大单位是亿、万、千、百时，他们的前面部分可能是需要进行切割的，而后面部分除了百（因为百后只有十，不会产生歧义）以外，其他进行检测，而其它单位十、个直接转换即可。这里面又分为两种情况：a. 对于亿、万来说，这两个单位之前的部分，如果只有一位数字，且长度为一，则是合法的，如果长度超过1且亿或万前一位是数字，且前面部分三百三、三千三这种情况，那么是需要进行切割的，如果是三十三则不需要。b. 对于千和百来说，他们当前数乘十，即会进位，这种现象带来的影响是，当千或百为最大单位时，他们的前面只允许单个数字的存在。

### 需求之外的情况：对于一零一（101）、二零一八（表示年份）这些数字的处理。
我的想法是，这存在一个语意和数字的问题，二零一八更倾向于是一个时间上的概念而不是存粹的数字，而一零一代表的可能是1、0、1三个数字，而组合起来的一百一十的这个数字概念和他本身的关系并不是很大。这类中文数字表达的意思更倾向于一个语意上的概念，而不是数字本身。故也就不存在二零一十八这种说法，换句话说，不存在一些结构不完整的中文数字，所以我的思路是如果没有任何单位的话，可以逐字转换（此思路已经在代码中实现，可参考测试用例结果）。

## 数据来源
1. 各种形式的中文数字测试用例，部分来源邮件，另外的是由我自己设计的。
2. 句子部分来源是腾讯公司公开的财务信息和广东省财务局的信息，这些信息可能会被我稍微修改，以及自己设计的一些信息。

## Python版本号
3.7.0

## 此程序可以处理的中文数字实例（更多情况请参考test_by_sentence_result文件）：
一：1

十一：11

一十一：11

一百一：110

五十零五：55

三百三十三：333

一千零一：1001

一千一：1100

一千二十：1020

三万三千三十三：33033

八十三万亿：83000000000000

三十三百：切割成三十、三百，转换成30，300

三百三亿三十三百：切割成三百、三亿三十、三百，转换成300，300000030，300

1百2：120

500万：5000000

5千500：5500

1,000,000：1000000

一个亿三千万：130000000

二零一八：2018

一零一：101

三三三三：3333
