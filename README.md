# de-zip   
Python脚本  
对经过伪加密的zip文件进行处理  

原理:  
加密标志位在`general purpose bit flag`中，从后向前数，第一个bit为1，表示有加密  
查找zip的加密标志位，将其置为0即可  

```
4.3.7  Local file header:

    local file header signature     4 bytes  (0x04034b50)
    version needed to extract       2 bytes
    general purpose bit flag        2 bytes


4.3.12  Central directory structure:

    [central directory header 1]
    .
    .
    . 
    [central directory header n]
    [digital signature] 

    File header:

    central file header signature   4 bytes  (0x02014b50)
    version made by                 2 bytes
    version needed to extract       2 bytes
    general purpose bit flag        2 bytes


4.4.4 general purpose bit flag: (2 bytes)

    Bit 0: If set, indicates that the file is encrypted.
```

参考资料:  
https://pkware.cachefly.net/webdocs/APPNOTE/APPNOTE-6.2.0.txt  