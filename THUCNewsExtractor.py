#导出数据到单一的文件中，并切分为训练集、测试集
import os
import sys
import argparse
import math
import random
import json
from threading import Thread

def extract_text(clazz_dir,files):
    sentences=[]
    file_num = 0
    print('start ',clazz)
    for file_name in files:
        df = open(clazz_dir+'/'+file_name,'r',encoding='utf-8')
        sentence=""
        for line in df.readlines():
            sentence +=line

        sentences.append(json.dumps({"text":sentence},ensure_ascii=False))
        df.close()
        if file_num%1000==0:
            print(file_name)
        file_num+=1
        # if file_num>1000:
        #     break
    
    total_count_of_class = len(sentences)
    ## create test set
    output_dir = outdir+clazz
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    test_set = open(output_dir+'/test_set','a',encoding='utf-8')
    for times in range(int(total_count_of_class*0.3)):
        index = random.randint(0,total_count_of_class-times-1)
        test_set.write(sentences[index]+'\n')
        # print(sentences[index],len(sentences))
        sentences.pop(index)
    test_set.close()

    train_set=open(output_dir+'/train_set','a',encoding='utf-8')
    for sentence in sentences:
        train_set.write(sentence+'\n')
    train_set.close()

    print('finish ',clazz)

def main():
    parser = argparse.ArgumentParser(prog=os.path.basename(sys.argv[0]),
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description=__doc__)
    parser.add_argument("input", help="where is THUCNews")
    parser.add_argument("-o","--output",
        help="directory for generate train set and test set")

    args = parser.parse_args()

    rootdir = args.input
    outdir = args.output
    
    if not os.path.exists(rootdir):
        print(rootdir," not exist")
        return

    directories = os.listdir(rootdir)
    last_char = rootdir[len(rootdir)-1]
    if last_char!='/' or last_char!='\\':
        rootdir += '/'

    outdir = os.path.abspath(outdir)+'/'
    if not os.path.exists(outdir):
        os.makedirs(outdir)

    #按类别读取文件，将每个文件的内容输出为一行，然后70%作为训练集，30%作为测试集，保存到指定目录
    for clazz in directories:
        clazz_dir = rootdir+clazz
        files = os.listdir(clazz_dir)
        thread = Thread(target=extract_text,args=(clazz_dir,files))
        thread.start()
        # extract_text(clazz_dir,files)
        
if __name__ == '__main__':
    main()