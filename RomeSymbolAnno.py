#coding=utf8
#########################################################################
#   Copyright (C) 2016 All rights reserved.
# 
#   文件名称：test.py
#   创 建 者：unicodeproject
#   创建日期：2016年11月29日
#   描    述：
#
#   备    注：
#
#########################################################################
#!/usr/bin/python
# please add your code here!
import sys;
import re;
reload(sys);
sys.setdefaultencoding('utf8');
from  RomeAnno import RomeAnnotation;
def Process(infilename,ofilename,errfile):
    annoworker=RomeAnnotation.RomeAnnotator();
    annoworker.loadWordList("RomeAnno/jprome.txt");
    p=re.compile(",");
    fid = open(infilename,"r");
    fout = open(ofilename,"w");
    ferr = open(errfile,"w");
    linecount=0;
    while True:
        line = fid.readline();
        if (len(line)==0):
            break;
        line = line.replace("\n","");
        col = line.split("\t");
        linecount+=1;
        if (0==linecount%10):
            sys.stderr.write("%d\n"%linecount);
        #假名#词条#权重
        col[1] = col[1].replace("'","");
        annoresult = annoworker.AnnotateByWordSegmentor(col[1]);
        if annoresult==None:
            ferr.write("%s\n"%line);
            continue;
        for m in annoresult:
            val=m[1]*float(col[2]);
            fout.write("%s\t%s\t%f\n"%(col[0],m[0],val));
    fid.close();
    fout.close();
    ferr.close();

if __name__=="__main__":
    if (len(sys.argv)!=4):
        sys.stderr.write("program [IN] [OUT] [ERR]\n");
        sys.exit(1);
    #Process(sys.argv[1],sys.argv[2],sys.argv[3]);

    annoworker=RomeAnnotation.RomeAnnotator();
    annoworker.loadWordList("RomeAnno/jprome.txt");
    #seg=annoworker.DynamicShortestPathSegment("ようごしゅう");
    #for m in seg:
    #    print m;
    anno=annoworker.AnnotateByWordSegmentor("きっさてん");
    for m in anno:
        print m;
    anno=annoworker.AnnotateByWordSegmentor("さっしゅ");
    for m in anno:
        print m;
    anno=annoworker.AnnotateByWordSegmentor("ふつう");
    for m in anno:
        print m;
