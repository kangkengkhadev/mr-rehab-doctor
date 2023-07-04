from django.shortcuts import render,redirect
from firebaseconfig import *
from json import dumps
from datetime import date
# Create your views here.

# convert month
def convertm2name(month):
    mont_dict ={'01':'มกราคม',
     '02':'กุมภาพันธ์',
     '03':'มีนาคม',
     '04':'เมษายน',
     '05':'พฤษภาคม',
     '06':'มิถุนายน',
     '07':'กรกฏาคม',
     '08':'สิงหาคม',
     '09':'กันยายน',
     '10':'ตุลาคม',
     '11':'พฤษจิกายน',
     '12':'ธันวาคม'}
    return mont_dict[month[3:5]]
# get posename from id
def get_posename_id(id):
    doc_ref = db.collection('pose').where('id','==',int(id)).get()
    info = [i for i in doc_ref]
    infodict = [i.to_dict() for i in info]
    return infodict[0]['pose']

# patient page render funtion
def patientpage(request):
    # check session
    if 'doctor_id' in request.session:
        print('have doctor id')
        if request.method == 'GET' and 'selectmonth' in request.GET:
            month = str(request.GET.get('selectmonth'))
        else:
            month = str(date.today())[2:7]
        doctor_id = request.session['doctor_id']
        pid =  request.GET.get('pid')
        info = db.collection('patient').where('patient_id','==',pid).where('status','==','active').where('doctor_id','==',doctor_id).get()
        info = [i for i in info]
        # infodict is general info of user 
        infodict = [i.to_dict() for i in info]
        # get doc info from db 
        doc_ref = db.collection('patient').document(pid)
        doc = doc_ref.get()
        # try to get rehabinfo from db and preprocess 
        try:
            rehab_info = doc.to_dict()['rehab_info']
            dump_month = [str(i) for i in range(1,32)]
            for i in range(len(dump_month)):
                if int(dump_month[i]) < 10:
                    dump_month[i] = '0'+ dump_month[i]
            dump_evo_month = [0 for i in range(1,32)]
            dump_model = dict(zip(dump_month,dump_evo_month))
            subpose_info  = []
            for i in rehab_info:
                 if i[2:7] == month:
                    for j in rehab_info[i]:
                        subpose_info.append(get_posename_id(j))
            subpose_info = list(set(subpose_info))
            print(subpose_info)
            subpose_dict = dict()
            for i in subpose_info:
                 subpose_dict[i] = [0 for i in range(1,32)]
            print(subpose_dict)
            # loop in month 
            new_info = dict()
            for i in rehab_info:
                print('day is',i[:7])
                # loop in day 
                day_count = 0
                num = 0
                # loop in pose
                for key in rehab_info[i]:
                    print('key',key)
                    num+=1
                    count = 0
                    dis = 0
                    for ipose,pose in enumerate(rehab_info[i][key]):
                        if ipose == 0:
                            dis = pose
                            continue
                        count += pose 
                    if month == i[2:7]: 
                        subpose_dict[get_posename_id(key)][int(i[-2:])-1] = int((count/(len(rehab_info[i][key])-1)/dis)*100)
                        print('pose',key,int((count/(len(rehab_info[i][key])-1)/dis)*100))
                    day_count+=count/(len(rehab_info[i][key])-1)/dis
                new_info[i] = (int((day_count/num)*100))
            print('sss',new_info)
            # print(subpose_dict)
            for i in new_info:
                if i[2:7] == month:
                    print(i[8:10])
                    dump_model[i[8:10]] = new_info[i]
            # print(dump_model)
        except:
            # in case cant get info from db 
            dump_month = [str(i) for i in range(1,32)]
            for i in range(len(dump_month)):
                if int(dump_month[i]) < 10:
                    dump_month[i] = '0'+ dump_month[i]
            dump_model = dict()
            for i in dump_month:
                 dump_model[i] = 0
        try:
            # in case have rehab_info in this month 
            poses_evo_in_day = []
            month_id = list(set(map(lambda x:x[2:7],rehab_info.keys())))   
            month_id.remove(month)
            # print([int(i) for i in dump_model.keys()]) 
            return render(request,'patientinfo.html',{'info':infodict[0],'subclass_evo_in_day':dumps(subpose_dict),'evo_date_day':dumps([int(i) for i in dump_model.keys()]), 'sum_evo_in_day':dumps(list(dump_model.values())),'month_id':month_id,'thismonth':month,'pid':pid,'month_name':convertm2name(month)})
        except:
            # in case dont have rehab_info in this month
            month_id = list(set(map(lambda x:x[2:7],rehab_info.keys())))   
            rehabinfo = 0
            return render(request,'patientinfo.html',{'info':infodict[0],'month_id':month_id,'rehabinfo':rehabinfo,'evo_date_day':dumps([i for i in range(0,32)]),'pid':pid ,'evo_in_day':dumps([0 for i in range(0,32)])}) 
    # if dont has session redirect to doctorpage
    else:
        print('dont have doctor id')
        return redirect('/doctorpage')
    
# change pose in patient_page function
def changepose(request):
      try:  
            if 'doctor_id' in request.session:
                  patient_id = request.GET.get('patient_id') 
                  user_db = db.collection('patient').where('patient_id','==',patient_id).get()
                  users = [i.to_dict() for i in user_db]
                  user = users[0]
                  pose_db = db.collection('pose').get()
                  pose = []
                  for i,v in enumerate(pose_db):
                        pdict = v.to_dict()
                        if (i+1) % 4 == 0:
                              pdict['row'] = 1
                        pose.append(pdict)
                  hadposes = []
                  for i in user['poses']:
                        for j in pose:
                              if j['pose'] == i['pose']:
                                    hadposes.append({'pose':i['pose'],'countpose':i['countpose'],'dopose':i['dopose'],'id':j['id']})
                  print(hadposes)
                  return render(request, 'changepose.html', {'pose':pose,'patient_id':patient_id,'had_pose':hadposes})
            else:
                  return redirect('/login/')
      except:
            return redirect('/doctorpage')
               
def savechangepose(request):
      try:
            doctor_id = request.session['doctor_id']
            patient_id = request.POST.get('patient_id')
            info = db.collection('patient').where('patient_id','==',patient_id).where('status','==','active').where('doctor_id','==',doctor_id).get()
            info = [i.to_dict() for i in info]
            poses_db = db.collection('pose').get()
            poses_indb = [pose.to_dict() for pose in poses_db]
            countpose = request.POST.getlist('countpose[]')        
            dopose = request.POST.getlist('dopose[]')
            pose = [{'pose':poses_indb[i]['pose'],'countpose':countpose[i],'dopose':dopose[i]} for i in range(len(poses_indb))]  
            pose = [i for i in pose if int(i['countpose']) != 0 and int(i['dopose']) != 0]
            doc = db.collection('patient').where('patient_id','==',patient_id).get()
            for i in pose:
                  for p in poses_indb:
                        if p['pose'] == i['pose']:
                              i['id'] = p['id']
                              i['detail'] = p['detail']
                              i['link_img'] = p['link_img']
                              i['tracking'] = p['tracking']
            key = doc[0].id
            db.collection('patient').document(key).update({'poses':pose})
            
            return redirect('/patientinfo/?pid='+patient_id)
      except:
            return redirect('/doctorpage')
      
# change patient_info 
def changepatientinfo(request):
    if 'doctor_id' in request.session and ( request.method == 'GET' and 'pid' in request.GET): 
        pid = request.GET.get('pid')
        info = db.collection('patient').where('patient_id','==',pid).where('status','==','active').get()
        infodict = [i.to_dict() for i in info]
        return render(request,'changepatientinfo.html',{'info':infodict[0]})
    else:
        return redirect('/doctorpage')
    

def savechangepinfo(request):
    if 'doctor_id' in request.session: 
        name = request.POST.get('name')
        pid = request.POST.get('pid')
        lastname = request.POST.get('lastname')
        phone = request.POST.get('phone')
        dicease = request.POST.get('dicease')
        age = request.POST.get('age')
        line_id = request.POST.get('line_id')
        gender = request.POST.get('gender')
        kin_contact = request.POST.get('kin_contact')
        hospital_number = request.POST.get('hospital_number')
        month = request.POST.get('month')
        data = {'dicease':dicease,'month':month,'name':name,'lastname':lastname,'phone':phone,'hospital_number':hospital_number,'age':age,'line_id':line_id,'gender':gender,'kin_contact':kin_contact}
        info_id= db.collection('patient').where('patient_id','==',pid).get()
        info = [i.id for i in info_id]
        db.collection('patient').document(info[0]).update(data)
        return redirect('/patientinfo/?pid='+pid) 
    else:
        return redirect('/doctorpage') 