def malljd_generatedictionarylist(number):
    list=[]
    with open('D://malljd1//information'+number+'.txt','r') as fetch:
        for line in set(fetch.readlines()):
            ziduanlist=line.split('|')

            dict={}

            if ziduanlist[3]!='':
                dict['sku']=ziduanlist[3]
            else:
                continue

            if ziduanlist[0]!='':
                dict['name']=ziduanlist[0]
            else:
                dict['name']=''

            if ziduanlist[2]!='':
                if '男'in ziduanlist[2]:
                    dict['gender']='men'
                elif '女' in ziduanlist[2]:
                    dict['gender'] = 'women'
                else:
                    dict['gender'] = 'children'
            else:
                dict['product_type'] = ''

            if ziduanlist[1]!='':
                if ziduanlist[1]=='鞋类':
                    dict['product_type']='FPW'
                elif ziduanlist[1]=='非鞋类':
                    dict['product_type']='APP'
            else:
                dict['product_type'] = ''

            dict['platform']='malljd'

            dict['price_type']='MSRP'

            if ziduanlist[4]!='':
                dict['price']=float(ziduanlist[4].replace('￥',''))
            else:
                continue

            dict['screenshot']=''

            list.append(dict)
    return list

malljd_generatedictionarylist1=malljd_generatedictionarylist('1')
malljd_generatedictionarylist2=malljd_generatedictionarylist('2')
malljd_generatedictionarylist3=malljd_generatedictionarylist('3')
malljd_generatedictionarylist4=malljd_generatedictionarylist('4')

malljd_generatedictionarylist=malljd_generatedictionarylist1+malljd_generatedictionarylist2+malljd_generatedictionarylist3+malljd_generatedictionarylist4