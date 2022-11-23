import csv
l=[]
with open('sample.txt','r')  as f:
    s = f.readlines()
    # print(s)
    with open('data.csv', 'w', newline="") as d:
        writer = csv.writer(d)
        for data in s:
            l = data.split('\t')
            l[-1] = l[-1][:len(l[-1])-1]
            for i in range(0,len(l)-1,2):
                city,code = l[i],l[i+1]
                m = [city,code]
                writer.writerow(m)
