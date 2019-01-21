import pypyodbc, time, datetime,functools

dsk_list=[]

""" --- create connection string to data base --- """

con=pypyodbc.connect('DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};UID=admin;UserCommitSync=Yes;Threads=3;SafeTransactions=0;PageTimeout=5;MaxScanRows=8;MaxBufferSize=2048;FIL={MS Access};DriverId=25;DefaultDir=C:/автозаказ/База Молоко;DBQ=C:/автозаказ/База Молоко/ПоставщикСкладМагазин.mdb;')
cursor=con.cursor()
"""cursor.tables()
rows = cursor.fetchall()
for row in rows:
    print(row)"""


"""--- save data from access "py_dsc_download_table" in variable "result_dwnl_table"  ---"""

cursor.execute("SELECT * FROM py_dsc_download_table")
result_dwnl_table=cursor.fetchall()
#print("----result_dwnl_table----",result_dwnl_table)
#for row in result_dwnl_table:
    #print(row)


#input('put enter')


### test reading date date ####

date1=result_dwnl_table[0][1]
date_time=date1.isocalendar()
print(date_time)


"""--- save data from access "calc_dictinct_AP" in variable "tovars"  ---"""

table={}
cursor.execute("SELECT * FROM calc_dictinct_AP")
tovars=cursor.fetchall()
print(tovars)




"""--- structuring data to array "table"  ---"""

for number_kod in tovars:
    tovarkod=number_kod[0]
    print(tovarkod,"--------")
    array_numberkod={}
    table.update({tovarkod:array_numberkod})
    for row in result_dwnl_table:
        #print(row[1])
        #print(number_kod)
        if tovarkod==row[0]:
            key_date=row[1]
            value_date=[row[2],row[3],row[4]]
            #print(key_date)
            #print(value_date)
            array_numberkod.update({key_date:value_date})
        else: pass
        #print(array_numberkod)
print("--- END OF structuring data to array table  ---",table)






##############
###Part 2: serching for UCENKA
#############


### create Ucenka table:

ucenka_table={}

# create table from dates, sales, dsk and other parametrs in next four day:
# kod:{date:[sale,rest]}


"""--- save data from access "py_table_prognoz" in variable "result_table_prognoz"  ---"""

cursor.execute("SELECT * FROM py_table_prognoz")
result_table_prognoz=cursor.fetchall()
print(result_table_prognoz)



table_prognoz={}

"""--- structuring data to array "table_prognoz"  ---"""

for number_kod in tovars:
    tovarkod=number_kod[0]
    print(tovarkod,"--------")
    array_numberkod={}
    table_prognoz.update({tovarkod:array_numberkod})
    for row in result_table_prognoz:
        #print(row[1])
        #print(number_kod)
        if tovarkod==row[0]:
            key_date=row[1]
            dsk_tmp=0
            value_date=[row[2],row[3],dsk_tmp]
            #print(key_date)
            #print(value_date)
            array_numberkod.update({key_date:value_date})
        else: pass
        #print(array_numberkod)
print("----table_prognoz---- \n",table_prognoz)
#input("press enter")

con.close()
tmp_table_prognoz=table_prognoz




#algoritm of searching UCENKA

def algoritm_ucenka(table_prognoz ):
    #print("------table_values----- \n",table_values)
    #print("------table_prognoz----- \n",table_prognoz)

    
      
            

    ## Algorithms of calculating standart UCENKA:

    def monday_algorithm(date_number, tovarkod_array,tovarkod_array2,tovarkod):
        delta_mon=datetime.timedelta(days=1)
        etalon_ofmonday_day=date_number-delta_mon
        if etalon_ofmonday_day in tovarkod_array.keys():
            dsk_m=tovarkod_array[etalon_ofmonday_day][1]*0.45
        else:
            dsk_m=tovarkod_array2[etalon_ofmonday_day][2]*0.45

        a=table_prognoz[tovarkod][date_number][1]-dsk_m
        #print("!!!!!!!! \n !!!!!!!! \n dates_less \n !!!!!\n !!!!!!\n!!!!!\n",dates_less)

        if a<0:
            #correction in dsk
            dsk_m=table_prognoz[tovarkod][date_number][1]
            #correction in rest
            table_prognoz[tovarkod][date_number][1]=0
            for date_number_less in dates_less:

                #
                #
                #
                # Leter we mast insert an recurtion function, but now only cycle
                #
                #
                b=table_prognoz[tovarkod][date_number_less][1]-dsk_m
                if b<0:
                    
                    
                    #correction in rest
                    table_prognoz[tovarkod][date_number_less][1]=0
                else:
                    #correction in rest
                    table_prognoz[tovarkod][date_number_less][1]=b
            
        else:
            #correction in rest
            table_prognoz[tovarkod][date_number][1]=a
            table_prognoz[tovarkod][date_number][2]=dsk_m
            for date_number_less in dates_less:

                #
                #
                #
                # Leter we mast insert an recurtion function, but now only cycle
                #
                #
                b=table_prognoz[tovarkod][date_number_less][1]-dsk_m
                if b<0:
                    
                    
                    #correction in rest
                    table_prognoz[tovarkod][date_number_less][1]=0
                else:
                    #correction in rest
                    table_prognoz[tovarkod][date_number_less][1]=b
        dsk_m=int(round(dsk_m))

        kod_date_dsk=(tovarkod,date_number,dsk_m)
        dsk_list.append(kod_date_dsk)
        
    def tuesday_algoritm(date_number, tovarkod_array,tovarkod_array2,tovarkod):
        dsk_tuesday_list=[]        

        dates_ucen=[]
        for dates in tovarkod_array2.keys():
            dates_ucen.append(dates)
        
        dates_ucen.sort()
        
        for date_ucen in dates_ucen:
            
            if (datetime.datetime.isoweekday(date_ucen) in (1,3,4,5,6,7)):
                pass
            
            elif (tovarkod_array2[date_ucen][0] is None):pass
                
            else:
                dsk_t=tovarkod_array2[date_ucen][0]
                dsk_tuesday_list.append(dsk_t)
        r=0

        try: r=functools.reduce(lambda x, y: x + y, dsk_tuesday_list)
        except :r=0
        else: r=functools.reduce(lambda x, y: x + y, dsk_tuesday_list)

        lendsk=len(dsk_tuesday_list)
        if lendsk==0:
            lendsk=1

        dsk_tues=r/lendsk;
        a=table_prognoz[tovarkod][date_number][1]-dsk_tues
        #print("!!!!!!!! \n !!!!!!!! \n dates_less \n !!!!!\n !!!!!!\n!!!!!\n",dates_less)

        if a<0:
            #correction in dsk
            dsk_tues=table_prognoz[tovarkod][date_number][1]
            #correction in rest
            table_prognoz[tovarkod][date_number][1]=0
            for date_number_less in dates_less:

                #
                #
                #
                # Leter we mast insert an recurtion function, but now only cycle
                #
                #
                b=table_prognoz[tovarkod][date_number_less][1]-dsk_tues
                if b<0:
                    
                    
                    #correction in rest
                    table_prognoz[tovarkod][date_number_less][1]=0
                else:
                    #correction in rest
                    table_prognoz[tovarkod][date_number_less][1]=b
            
        else:
            #correction in rest
            table_prognoz[tovarkod][date_number][1]=a
            table_prognoz[tovarkod][date_number][2]=dsk_tues
            for date_number_less in dates_less:

                #
                #
                #
                # Leter we mast insert an recurtion function, but now only cycle
                #
                #
                b=table_prognoz[tovarkod][date_number_less][1]-dsk_tues
                if b<0:
                    
                    
                    #correction in rest
                    table_prognoz[tovarkod][date_number_less][1]=0
                else:
                    #correction in rest
                    table_prognoz[tovarkod][date_number_less][1]=b

        dsk_tues=int(round(dsk_tues))
        kod_date_dsk=(tovarkod,date_number,dsk_tues)
        dsk_list.append(kod_date_dsk)
        

    

    
    
    def standart_algoritm(date_number, tovarkod_array,tovarkod_array2, tovarkod):


       ## finding etalon rest and other parametrs two days before UCENKA in section tovarkod:

        intovar_dsk_list=[]
        #print("---zero intovar_dsk_list for kod ",tovarkod,"is ", intovar_dsk_list)


        tovarkod_array2_keys=[]
        for keys_ in tovarkod_array2.keys():
            tovarkod_array2_keys.append(keys_)
        tovarkod_array2_keys.sort()
        
        print("@@@@@@@@@ \n #######tovarkod_array2_keys \n ######## \n@@@@@@@ \n",tovarkod_array2_keys)

        for date_ in tovarkod_array2_keys:
            ucenka_date=date_+delta
            print("--date_:",date_)
            
            if ((date_>=etalon_day) or (datetime.datetime.isoweekday(date_) in (6,7))):
                print("---date_>=etalon_day--",date_>=etalon_day)
                print("----datetime.datetime.isoweekday(date_)in (6,7)--",(datetime.datetime.isoweekday(date_) in (6,7)))
                
                print("condition if ((date_>=etalon_day) or ((datetime.datetime.isoweekday(date_) in (6,7)))) ")
            
            
            elif ucenka_date in tovarkod_array.keys(): pass
            elif ((ucenka_date not in tovarkod_array2_keys)and (tovarkod_array2[ucenka_date][0] is None)):
                print("condition ((ucenka_date not in tovarkod_array2_keys)and (tovarkod_array2[ucenka_date][0]==None))")
            elif tovarkod_array2[ucenka_date][0] is None: pass

            else:
                print("### searching UCENKA in range[Wednesday - Sunday]")

                ### searching UCENKA in range[Wednesday - Sunday]
                
                #print(date_,"---",etalon_day,(date_>=etalon_day) )

                
                ucenka2day=tovarkod_array2[ucenka_date][0]
                ### searching sale each second day
                sale2day=tovarkod_array2[ucenka_date][1]
                    
                #print("--------ucenka2day *100=\n",ucenka2day*100)                
                #print("----sale2day*100=\n",sale2day*100)
                
                ### rest in a lot of table before two days UCENKA
                print("serching PROBLEM in DATE ", date_, "tovar ",tovarkod  )

                print("rest0=tovarkod_array2[date_]",tovarkod_array2[date_] )               

                rest0=tovarkod_array2[date_][2]
                print("etalon_rest",etalon_rest)
                print("--ucenka2day--",ucenka2day)
                print("---=rest0*100=\n",rest0*100)

                ### finding one of n approximation to UCENKA

                dskx=ucenka2day*(etalon_rest/rest0)*1
                #*((etalon_rest/etalon_sale2)/(rest0/sale2day))

                intovar_dsk_list+=[dskx];
                print("next intovar_dsk_list for kod ",tovarkod,"is ", intovar_dsk_list)

        print("last intovar_dsk_list for kod ",tovarkod,"is ", intovar_dsk_list)
        r=functools.reduce(lambda x, y: x + y, intovar_dsk_list)

        dsk=r/len(intovar_dsk_list);

        a=table_prognoz[tovarkod][date_number][1]-dsk
        print("!!!!!!!! \n !!!!!!!! \n dates_less \n !!!!!\n !!!!!!\n!!!!!\n",dates_less)

        if a<0:
            #correction in dsk
            dsk=table_prognoz[tovarkod][date_number][1]
            #correction in rest
            table_prognoz[tovarkod][date_number][1]=0
            for date_number_less in dates_less:

                #
                #
                #
                # Leter we mast insert an recurtion function, but now only cycle
                #
                #
                b=table_prognoz[tovarkod][date_number_less][1]-dsk
                if b<0:
                    
                    
                    #correction in rest
                    table_prognoz[tovarkod][date_number_less][1]=0
                else:
                    #correction in rest
                    table_prognoz[tovarkod][date_number_less][1]=b
            
        else:
            #correction in rest
            table_prognoz[tovarkod][date_number][1]=a
            table_prognoz[tovarkod][date_number][2]=dsk
            for date_number_less in dates_less:

                #
                #
                #
                # Leter we mast insert an recurtion function, but now only cycle
                #
                #
                b=table_prognoz[tovarkod][date_number_less][1]-dsk
                if b<0:
                    
                    
                    #correction in rest
                    table_prognoz[tovarkod][date_number_less][1]=0
                else:
                    #correction in rest
                    table_prognoz[tovarkod][date_number_less][1]=b
                    
                

        dsk=int(round(dsk))
        kod_date_dsk=(tovarkod,date_number,dsk)
        dsk_list.append(kod_date_dsk)    
                
         

        

    termin=2 ##expiration date -1
    


    
    print("---stage of dsk_list:\n",dsk_list)

    

    table_prognoz_keys=table_prognoz.keys()
    #print("!!!table_prognoz_keys!!!", table_prognoz_keys)

    for kod in table_prognoz_keys:
        tovarkod=kod
        tovarkod_array2=table[tovarkod]
        i=0
        tovarkod_array=table_prognoz[kod]
        #print("----- for kod in table_prognoz.keys()tovarkod_array is",tovarkod_array)
                
        n=len(tovarkod_array.keys())
        dates=[]
                       
        for date_number in tovarkod_array.keys():
            dates.append(date_number)

        dates.sort()
        dates_less=dates[:]
        print("-!!!!!!!------DATES ARRAY ----!!!!!:\n",dates)

        for date_number in dates:
            dates_less.remove(date_number)

            # finding etalon date and etalon sale two days before UCENKA

            delta=datetime.timedelta(days=termin)
            etalon_day=date_number-delta
            print(" ----- etalon_day is --- \n",etalon_day)
            print(" The tovarkod_array2 is \n",tovarkod_array2)

            ## choose table of data etalon rest:

            if etalon_day in (tovarkod_array.keys()):
                etalon_rest=tovarkod_array[etalon_day][1]
            else:
                etalon_rest=tovarkod_array2[etalon_day][2]

            #print("----etalon_rest *100 =\n",etalon_rest*100)

            ## choosing predictive sale in any date of statistik:

            etalon_sale2=tovarkod_array[date_number][0]
            #print("----etalon_sale2 *100 =\n",etalon_sale2*100)


            
            weekday_prognoz=datetime.datetime.isoweekday(date_number)
            print('the number of weekday is № ',weekday_prognoz)
            if weekday_prognoz in [3,4,5,6,7]:
                print('Choose the standard algorithm...',weekday_prognoz)
                standart_algoritm(date_number, tovarkod_array,tovarkod_array2,tovarkod)
            elif weekday_prognoz==1:
                print('Choose the monday algorithm...')
                monday_algorithm(date_number, tovarkod_array,tovarkod_array2,tovarkod)
            elif weekday_prognoz==2:
                print('Choose the tuesday algorithm...')
                tuesday_algoritm(date_number, tovarkod_array,tovarkod_array2,tovarkod)
            else: print('mistake in searching days number')
            i+=1
    



   
algoritm_ucenka(table_prognoz)

#print("--------rezult of dsk_list is: /n", dsk_list)

#print("----table_prognoz---- \n",table_prognoz)


dsk_list.sort()
for row in dsk_list:
    print(row[0],row[1].strftime("%d.%m.%Y"),row[2])



con=pypyodbc.connect('DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};UID=admin;UserCommitSync=Yes;Threads=3;SafeTransactions=0;PageTimeout=5;MaxScanRows=8;MaxBufferSize=2048;FIL={MS Access};DriverId=25;DefaultDir=C:/автозаказ/База Молоко;DBQ=C:/автозаказ/База Молоко/ПоставщикСкладМагазин.mdb;')
cursor=con.cursor()


cursor.execute('DELETE py_ucenka_all_result.kod_ap, py_ucenka_all_result.Date_uc, py_ucenka_all_result.ucenc, *FROM py_ucenka_all_result;')
con.commit()


for row in dsk_list:
    """row[0]=int(round(row[0]))
    row[2]=int(round(row[2]))"""
    d=str(row[1].strftime("%d.%m.%Y"))
    cursor.execute('INSERT INTO py_ucenka_all_result ( kod_ap, Date_uc, ucenc )SELECT ? AS Выражение1, ? AS Выражение2, ? AS Выражение3;',(str(row[0]),d,str(row[2])))
con.commit()


con.close()
input("### THE END)))):")







    

    

