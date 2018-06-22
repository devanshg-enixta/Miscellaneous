import difflib
import pysrt
import os,subprocess
import shutil
path = os.getcwd()
def update_srt(filename,x,flag):
    if os.path.exists(os.path.dirname(path+"/static/static/videos_text/"+filename.split('.txt')[0]+"/")):
        shutil.rmtree(path+"/static/static/videos_text/"+filename.split('.txt')[0]+"/")
        os.makedirs(os.path.dirname(path+"/static/static/videos_text/"+filename.split('.txt')[0]+"/"))
    else:
        os.makedirs(os.path.dirname(path+"/static/static/videos_text/"+filename.split('.txt')[0]+"/"))

    x=x.replace("  "," ").replace('  ',' ').replace('\r','').replace('\\nn','').replace('\\n','').replace('\\','').replace('\n','').replace('&nbsp;','')
    d = difflib.Differ()
    srt_file=filename.split('.txt')[0]+'.srt'
    subs = pysrt.open(path+"/static/static/videos_text/"+srt_file, encoding='iso-8859-1')
    f= open(path+"/static/static/videos_text/"+filename,"r+")
    y=str(f.readlines())
    y = y.replace("  "," ").replace('  ',' ').replace('\r','').replace('\\nn','').replace('\\n','').replace('\\','').replace('\n','').replace('&nbsp;','')
    y=y[2:len(y)-2].lower()
    x=x.lower()
    y=y.split(' ')
    t=x
    x = x.split(' ')
    i=0
    omit={}
    add ={}
    result1 = list(d.compare(y, x))
    result = list(d.compare(x, y))
    result1 =  [v for v in result1 if v[0] != '?']
    result =  [v for v in result if v[0] != '?']

    omit_word=[]
    add_word=[]
    for l in range(0,len(result1)):
        #print i,result1[l]
        if result1[l][0] == '-' and len(result1[l])>2:
            omit['line_no'] = i
            omit['word'] = result1[l][2:len(result1[l])]
            if l+1<len(result1):
                if result1[l+1][0] == '+' or result1[l-1][0] == '+' and l>0:
                    omit['flag'] = 1
                    if result1[l-1][0] == '+' and result1[l+1][0] == '-' :
                        i=i+1
                if result1[l+1][0] == '+' and result1[l-1][0] == '-' and l>0:
                    i=i-1
                else:
                    omit['flag'] = 0 
            omit_word.append(omit.copy())
        if result1[l][0] == '+' and len(result1[l])>2:
            add['line_no'] = i
            add['word'] = result1[l][2:len(result1[l])]
            add['flag'] = 0
            add_word.append(add.copy())
        if l+1<len(result1):
            if result1[l][0] == '-' and result1[l+1][0] != '-':
                i=i-1
        i=i+1
    for l in range(0,len(omit_word)):
        for k in range(0,len(add_word)):
            if add_word[k]['line_no'] == omit_word[l]['line_no']:
                omit_word[l]['flag'] = 1
                add_word[k]['flag'] = 1

  #  print omit_word
   # print "###############"
   # print add_word
    cnt=0
    pl_s=0
    pl_e=0
    for j in range(0,len(subs)):
        txt = subs[j].text.lower().replace("  "," ").replace('  ',' ').replace('\n',"").replace('\r','').replace('&nbsp;','')
        q=txt.split(' ')
        pl_s=pl_e
        pl_e = pl_e+len(q)
        print (txt,"---------------------->",pl_s,pl_e)


        for z in range(0,len(add_word)):
            if add_word[z]['flag'] == 0 and pl_s<=add_word[z]['line_no']<pl_e:
                pos = add_word[z]['line_no'] - pl_s
                q = txt.split(' ')
                q.insert(pos,add_word[z]['word'])
                txt = " ".join(q)
                subs[j].text = txt.replace("  "," ").replace('  ',' ').replace('\n',"").replace('\r','')
                pl_e = pl_e+1
        for i in range(0,len(omit_word)):
            if pl_s<=omit_word[i]['line_no'] <pl_e:
                if omit_word[i]['flag'] == 1:
                    #print omit_word[i]['word']
                    for z in range(0,len(add_word)):
                        if add_word[z]['line_no'] == omit_word[i]['line_no']:
                            #print omit_word[i]
                            if q:
                                try:
                                  #  print txt,pl_s,pl_e,omit_word[i]['word'],omit_word[i]['line_no']
                                    #q.remove(omit_word[i]['word'])
                                    pos = add_word[z]['line_no'] - pl_s
                                    #print pos,"######%%%%%%%%%%%%"
                                    q.pop(pos)
                                    q.insert(pos,add_word[z]['word'])
                                    txt = " ".join(q)
                                    txt=txt.replace("  "," ").replace('  ',' ').replace('\n',"").replace('\r','').replace('&nbsp;','')
                                    subs[j].text = txt
                                    add_word[z]['flag'] = 2
                                    omit_word[i]['flag'] = 2
                                    #print txt
                                    #print omit_word[i]['word'],add_word[z]['word'],omit_word[i]['line_no'],add_word[z]['line_no']
                                except:
                                    #txt=txt.replace(omit_word[i]['word'],add_word[z]['word'])
                                    pass
                               # print txt,pl_s,pl_e,omit_word[i]['word'],omit_word[i]['line_no'],omit_word[i]['flag']

                                

                elif omit_word[i]['flag'] == 0:
                   # print q
                    try:
                        if not q:
                            txt = ""
                        else:
                            q.remove(omit_word[i]['word'])
                            txt = " ".join(q)
                            pl_e = pl_e-1
                            omit_word[i]['flag'] = 2
                    except:
                        pass
                    subs[j].text = txt.replace("  "," ").replace('  ',' ').replace('\n',"").replace('\r','').replace('&nbsp;','')

        
        print (txt,"---------------------->",pl_s,pl_e)
        pl_s=pl_e
    subs.save(path+"/static/static/videos_text/"+srt_file, encoding='iso-8859-1')
#    subs.save(path+"/static/static/videos_text/""+filename.split('.txt')[0]+"/"+srt_file, encoding='iso-8859-1')
    try:
        os.remove(path+"/static/static/videos_text/"+srt_file.split('.')[0].strip()+".vtt")
        print (path+"/static/static/videos_text/"+filename.split('.txt')[0]+"/"+srt_file.split('.')[0].strip()+".vtt")
        os.remove(path+"/static/static/videos_text/"+filename.split('.txt')[0]+"/"+srt_file.split('.')[0].strip()+".vtt")
    except:
        pass
    final = open(path+"/static/static/videos_text/"+filename,'w+')
    print>>final,t
    command = "ffmpeg -i "+  path+"/static/static/videos_text/"+srt_file+" "+path+"/static/static/videos_text/"+srt_file.split('.')[0].strip()+".vtt"
    subprocess.call(command, shell=True)
    command = "ffmpeg -i "+  path+"/static/static/videos_text/"+srt_file+" "+path+"/static/static/videos_text/"+filename.split('.txt')[0]+"/"+srt_file.split('.')[0].strip()+str(flag)+".vtt"
    subprocess.call(command, shell=True)

