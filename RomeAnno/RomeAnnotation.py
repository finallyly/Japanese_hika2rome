#coding=utf8
#########################################################################
#   Copyright (C) 2016 All rights reserved.
# 
#   文件名称：RomeAnnotation.py
#   创 建 者：unicodeproject
#   创建日期：2016年11月29日
#   描    述：
#
#   备    注：将日语假名注音转成罗马音
#   用最短路径分词方法将假名系列作切分，如シャギ 可分成 シ、ャ、ギ 或者シャ、ギ
#   注意促音的处理
#########################################################################
#!/usr/bin/python
# please add your code here!
__Author__="finallyly"
import sys;
reload(sys);
sys.setdefaultencoding('utf8');
class RomeAnnotator:
    def __init__(self):
        self.wordict={};
    def loadWordList(self,pathname):
        fid = open(pathname,"r");
        while True:
            line = fid.readline();
            if (len(line)==0):
                break;
            line = line.replace("\n","");
            col = line.split("\t");
            col[0].strip();
            col[1].strip();
            col[2].strip();
            if self.wordict.has_key(col[0]):
                self.wordict[col[0]].append((col[1],int(col[2])));
            else:
                self.wordict[col[0]]=[];
                self.wordict[col[0]].append((col[1],int(col[2])));
        for m in self.wordict.keys():
            sum = 0; 
            for i in range(0,len(self.wordict[m])):
                sum+=float(self.wordict[m][i][1]);
            for i in range(0,len(self.wordict[m])):
                val=self.wordict[m][i][1]/sum;
                self.wordict[m][i]=(self.wordict[m][i][0],val);
        #for m in self.wordict.keys():
            #for i in range(0,len(self.wordict[m])):
                #print m, self.wordict[m][i][0],self.wordict[m][i][1];
    def DynamicShortestPathSegment(self,sentence):
        usentence = unicode(sentence,"UTF-8");
        #跟据词典情况构建词图
        uindex = [];
        for i in range(0,len(usentence)+1):
            uindex.append([]);
        pos = 0; 
        while pos<=len(usentence)-1:
            j=pos+1;
            while j <=len(usentence):
                upiece=usentence[pos:j];
                utf8counterpart=upiece.encode("UTF-8");
                #unicode原子自动存在词图
                if j-pos == 1:
                    uindex[pos].append(j);
                else:
                    if self.wordict.has_key(utf8counterpart):
                        uindex[pos].append(j);
                j+=1;
            pos+=1;
        uindex[pos].append(-1);
        #利用uindex二维数组，以及动态规划算法查找最短路径
        cost  = 1;
        max_cost = 10000;
        pos = len(usentence);
        #保存层图的最小耗费；
        #保存层图最小耗费对应的回退路径
        ulen=[];
        ucost=[];
        for i in range(0,len(usentence)+1):
            ucost.append(max_cost);
            ulen.append(i+1);
        while pos>=0:
            ucost[pos] = max_cost;
            for m in uindex[pos]:
                temp = cost+ucost[m];
                if (temp < ucost[pos]):
                    ucost[pos] = temp;
                    ulen[pos] = m;
                if (m==-1):
                    #尾巴节点
                    ucost[pos]=0;
                    ulen[pos]=-1;
            pos-=1;
        pos = 0;
        seg=[];
        while pos<len(usentence):
            temp=usentence[pos:ulen[pos]].encode("UTF-8");
            seg.append(temp);
            pos=ulen[pos];
        return seg;
    def AnnotateByWordSegmentor(self,sentence):
        seg = self.DynamicShortestPathSegment(sentence);
        length=[];
        now=[];
        eflag = 0;
        for i in range(0,len(seg)):
            if (not self.wordict.has_key(seg[i])):
                eflag = 1;
                break;
            else:
              count=len(self.wordict[seg[i]]);
              length.append(count);
              now.append(-1);
        if eflag == 1:
            return None;
        pos = 0;
        now[pos]=-1;
        finalresult = [];
        while pos != -1:
             now[pos]+=1;
             if now[pos] < length[pos]:
                if pos==len(seg)-1:
                    score = 1.0;
                    mystr="";
                    #促音时用于保留第二候选,即吞掉促音xtu的注音方式,
                    #即：きっさてん 注音成ki'xtu'ssa'te'nn和ki'ssa'te'nn都可以
                    mystr2="";
                    #用flag标注促音
                    for i in range(0,len(seg)):
                        flag=0;
                        if i >0 and seg[i]!="ー" and (seg[i-1]=="っ"or seg[i-1]=="ッ"):
                            flag=1;
                        if flag == 0:
                            if mystr=="":
                                mystr+=self.wordict[seg[i]][now[i]][0];
                            else:
                                mystr+="'";
                                mystr+=self.wordict[seg[i]][now[i]][0];
                                if mystr2!="":
                                    mystr2+="'";
                                    mystr2+=self.wordict[seg[i]][now[i]][0];
                        else:
                            if mystr=="":
                                mystr+=(self.wordict[seg[i]][now[i]][0][0:1]+self.wordict[seg[i]][now[i]][0]);
                            else:
                                mystr2=mystr;
                                subcol=mystr2.split("'");
                                mystr2="'".join(subcol[:-1]);
                                mystr+="'";
                                mystr2+="'";
                                mystr2+=(self.wordict[seg[i]][now[i]][0][0:1]+self.wordict[seg[i]][now[i]][0]);
                                mystr+=(self.wordict[seg[i]][now[i]][0][0:1]+self.wordict[seg[i]][now[i]][0]);
                        score*=self.wordict[seg[i]][now[i]][1];
                    finalresult.append((mystr,score));
                    if mystr2!="":
                        finalresult.append((mystr2,score));
                else:
                    pos+=1;
             else:
                 now[pos]=-1;
                 pos-=1;
        return finalresult;
