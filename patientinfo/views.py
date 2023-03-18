from django.shortcuts import render,redirect
from firebaseconfig import *
from json import dumps
from datetime import date
# Create your views here.

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

def get_sum_info_rehab_evo(muldoc_incol,month):
        rehab_info = muldoc_incol[0].document(month).get().to_dict()
                # print(rehab_info)
        days = []
        evo_in_day = []
        for day in rehab_info:
                # print(rehab_info[day])
            evos = []
            cpose = 0
            for ppose in rehab_info[day]:
                    # print(rehab_info[day][ppose])
                c = 0
                cpose += 1
                for i,v in enumerate(rehab_info[day][ppose][1:]):
                    c += v 
                sums = c/(i+1)
                evos.append(int((sums/rehab_info[day][ppose][0])*100))
            evo = sum(evos)/cpose
            days.append(day)
            evo_in_day.append(evo)
            dict_evo = {}
            for i,key in enumerate(days):
                dict_evo[key] = evo_in_day[i]
            date_day = [i for i in range(32)]
            real_evo = []
            for i in date_day:
                if str(i) in dict_evo.keys():
                    real_evo.append(dict_evo[str(i)])
                else:
                    real_evo.append(0)    
        return date_day,real_evo
    
    
def get_deep_info_rehab(muldoc_incol,month): 
    rehab_info = muldoc_incol[0].document(month).get().to_dict()
    dict_day_pose = dict()
    for day in rehab_info: 
        dict_poseid_detail = dict()
        for pose in rehab_info[day]:
            sum_do_pose = 0
            for i_detail_pose,detail_pose in enumerate(rehab_info[day][pose]):
                if i_detail_pose == 0:
                    must_do_post = detail_pose 
                else:
                    sum_do_pose += detail_pose
            percent = (sum_do_pose/(len(rehab_info[day][pose])-1))/must_do_post
            dict_poseid_detail[pose] = int(percent*100)
        dict_day_pose[day] = dict_poseid_detail 
    post_id_all = set()
    for i in dict_day_pose:
        for j in dict_day_pose[i]:
            post_id_all.update(j)
    post_id_all = list( post_id_all)
    poses_evo_in_day = dict()
    for i in post_id_all:
        date_sum = []
        for day_in_date in range(0,32):
            try:
                date_sum.append(dict_day_pose[str(day_in_date)][str(i)])
                        
            except:
                date_sum.append(0)
        poses_evo_in_day[i] = date_sum
    pose_from_db = db.collection('pose').get()
    pose_from_db = [i.to_dict() for i in pose_from_db]
    pose_name_and_info_rahab = dict()
    for i in pose_from_db:
        try: 
            pose_name_and_info_rahab[i['pose']] = poses_evo_in_day[str(i['id'])]
        except:
            pass
    return pose_name_and_info_rahab  


def patientpage(request):
    if 'doctor_id' in request.session:
        if request.method == 'GET' and 'selectmonth' in request.GET:
            month = str(request.GET.get('selectmonth'))
        else:
            month = str(date.today())[2:7]
        doctor_id = request.session['doctor_id']
        pid =  request.GET.get('pid')
        info = db.collection('patient').where('patient_id','==',pid).where('status','==','active').where('doctor_id','==',doctor_id).get()
        info = [i for i in info]
        infodict = [i.to_dict() for i in info]
        rehab_col = db.collection('patient').document(info[0].id).collections() 
        try:   
            muldoc_incol = [i for i in rehab_col]
            month_id = [i.id for i in muldoc_incol[0].get()]
            month_id.remove(month)
        except:
            rehabinfo = 0
            return render(request,'patientinfo.html',{'info':infodict[0],'rehabinfo':rehabinfo,'evo_date_day':dumps([i for i in range(0,32)]), 'evo_in_day':dumps([0 for i in range(0,32)])}) 
        
        if muldoc_incol != []:
            poses_evo_in_day  = get_deep_info_rehab(muldoc_incol,month)
            date_day,real_evo = get_sum_info_rehab_evo(muldoc_incol,month)     
            return render(request,'patientinfo.html',{'info':infodict[0],'evo_date_day':dumps(date_day), 'sum_evo_in_day':dumps(real_evo),'subclass_evo_in_day':dumps(poses_evo_in_day),'month_id':month_id,'thismonth':month,'pid':pid,'month_name':convertm2name(month)})
        else:
            rehabinfo = 0
            return render(request,'patientinfo.html',{'info':infodict[0],'rehabinfo':rehabinfo,'evo_date_day':dumps([i for i in range(0,32)]), 'evo_in_day':dumps([0 for i in range(0,32)])}) 
    else:
        return redirect('/doctorpage')
    
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
            key = doc[0].id
            db.collection('patient').document(key).update({'poses':pose})
            
            return redirect('/patientinfo/?pid='+patient_id)
      except:
            return redirect('/doctorpage')
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
        general_id = request.POST.get('general_id')
        month = request.POST.get('month')
        data = {'dicease':dicease,'month':month,'name':name,'lastname':lastname,'phone':phone,'general_id':general_id,'age':age,'line_id':line_id,'gender':gender,'kin_contact':kin_contact}
        info_id= db.collection('patient').where('patient_id','==',pid).get()
        info = [i.id for i in info_id]
        db.collection('patient').document(info[0]).update(data)
        return redirect('/patientinfo/?pid='+pid) 
    else:
        return redirect('/doctorpage') 