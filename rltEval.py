#coding=utf-8
from __future__ import division
import os, re

GS_DIR = 'D:\\SIBS\\work\\ZQ\evaluation\\GS\\'
TEST_DIR = 'D:\\SIBS\\work\\ZQ\\evaluation\\test\\part1'
OUT_FILE = 'D:\\SIBS\\work\\ZQ\\evaluation\\tt.csv', 'w+'

def readRecord(recDir):
    f = open(recDir)
    recList = []
    for line in f:
        recList.append(line)
    return recList

def findGS(gs_dir, prefix):
    gs_rec_dir = ''
    for p, d, f in os.walk(gs_dir):
        for ff in f:
            if ff.startswith(prefix):
                gs_rec_dir = os.path.join(p, ff)
    return gs_rec_dir

def findPos(record):
    start = re.search(ur"pos=\"(\w+):", record).group(1)
    end = re.search(ur":(\w+)\"", record).group(1)
    return start, end

def evaluation(std, rlt):
    model_name =  model_stat_str =  model_stat_lap =  item_len = []
    index = -1
    for item in std:
        temp = re.search(ur"model=\"(\w+)\"", item)
        if temp:
            if temp.group(1) not in model_name:
                model_name.append(temp.group(1))
        else:
            print 'ERROR @' + item
    for i in model_name:
        model_stat_str.append(0)
        model_stat_lap.append(0)
        item_len.append(0)
    for item in model_name:
        index += 1
        count = 0
        for i in std:
            if re.search(ur"model=\"(\w+)\"", i).group(1) == item:
                count += 1
                i = i.replace(' ', '')
                start_pos1, end_pos1 = findPos(i)
                for j in rlt:
                    j = j.replace(' ', '')
                    if re.search(ur"model=\"(\w+)\"", j).group(1) != item:
                        continue
                    start_pos2, end_pos2 = findPos(j)
                    if i == j:
                        model_stat_str[index] += 1
                        model_stat_lap[index] += 1
                    elif (start_pos1 >= start_pos2)&(end_pos1 <= end_pos2):
                        model_stat_lap[index] += 1
        item_len[index] = count
    for i in range(len(model_name)):
        if model_stat_lap[i] > item_len[i]:
            model_stat_lap[i] = item_len[i]
    return model_name, item_len, model_stat_str, model_stat_lap, len(std)


def main():
    D1 = D2 = N = S = Fscore1 = Fscore2 = 0
    with open(OUT_FILE,'w') as f:
        for parent, dirnames, filenames in os.walk(TEST_DIR):
            for filename in filenames:
                rlt_dir = os.path.join(parent, filename)
                gs_rec_dir = findGS(GS_DIR, filename[0:6])
                model_out = readRecord(rlt_dir)
                golden_std = readRecord(gs_rec_dir)
                print filename
                name, item_len, strict, lap, lengs = evaluation(golden_std, model_out)
                N += len(model_out)
                S += lengs
                D1 += sum(strict)
                D2 += sum(lap)
                ind = 0
                for i in name:
                    result = [i , str(item_len[ind]) , str(strict[ind]) , str(lap[ind])]
                    f.write(','.join(result))
                    f.write('\n')
                    ind += 1
        IP1 = D1/N
        IP2 = D2/N
        IR1 = D1/S
        IR2 = D2/S
        Fscore1 = (2*IP1*IR1)/(IP1 + IR1)
        Fscore2 = (2*IP2*IR2)/(IP2 + IR2)
        #print IP1,IR1,Fscore1,IP2,IR2,Fscore2

if __name__ == '__main__':
    main()
