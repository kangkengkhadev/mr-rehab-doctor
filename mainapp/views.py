from django.shortcuts import render,redirect
from firebaseconfig import *
# Create your views here.
import random
import string

def get_random_string(length = 10):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

def doctorpage(request):
      try:
            error = request.GET.get('error')
      except:
            error = ''
      if 'doctor_id' in request.session:
            doctor_id = request.session['doctor_id']
            doctor_info = db.collection('doctor').where('uid','==',doctor_id).get()
            doctor_info  = [i.to_dict() for i in doctor_info]
            data = db.collection('patient').where("doctor_id",'==',doctor_id).get()
            active_list = [i.to_dict() for i in data if i.to_dict()['status'] == 'active']
            waiting_list = [i.to_dict() for i in data if i.to_dict()['status'] == 'waiting']
            data_list = active_list+waiting_list
            return render(request, 'index.html', {'doctor_info':doctor_info[0],'data': data_list,'error':error})
      else:
            return redirect('/login/')

def del_dsession(request):
      del request.session['doctor_id']
      return redirect('/doctorpage')

def signup_page(request):
      return render(request, 'register.html')


def login_page(request):
      return render(request, 'login.html')

def postsignIn(request):
      message = "something wrong please try again"
      try:
            email=request.POST.get('email')
            password=request.POST.get('password')
            user=authe.sign_in_with_email_and_password(email,password)
            uid = user['localId']
            checkhave = db.collection('doctor').where('uid','==',uid).get()
            count = 0
            for i in range(len(checkhave)):
                  count +=1 
            if count ==0:
                  return render(request,"login.html",{"message":message})
            info = db.collection('doctor').where('uid','==',uid).get()
            request.session['doctor_id'] = info[0].to_dict()['uid']
            request.session['name'] = info[0].to_dict()['name']
            request.session['lastname'] = info[0].to_dict()['lastname']
            return redirect('/doctorpage')
      except:
            return render(request,"login.html",{"message":message})
  
def postsignUp(request):
      message = "You email already logged in or your password does not matched"
      try:
            email = request.POST.get('email')
            password = request.POST.get('password')
            confirm_pass = request.POST.get('confirm_password')
            if confirm_pass != password:
                  return render(request, "register.html",{'message':message})
            user=authe.create_user_with_email_and_password(email,password)
            uid = user['localId']
            name = request.POST.get('name')
            lastname = request.POST.get('lastname')
            phone = request.POST.get('phone')
            role = request.POST.get('role')
            line = request.POST.get('line')
            hospital = request.POST.get('hospital')
            data = {'rehab_info':{},'uid':uid,'name':name,'lastname':lastname,'phone':phone,'role':role,'email':email,'line_id':line,'hospital':hospital}
            print('ddddd')
            db.collection('doctor').document(uid).set(data)
            # print('ddddddddddddd')
            request.session['doctor_id'] = uid
            request.session['name'] = name
            request.session['lastname'] = lastname
            return redirect('/doctorpage')
      except Exception as error:
            return render(request, "register.html",{'message':message})

def patientdata(request):
      try:
            if 'doctor_id' in request.session:
                  doctor_id = request.session['doctor_id']
                  doctor_info = db.collection('doctor').where('uid','==',doctor_id).get()
                  doctor_info  = [i.to_dict() for i in doctor_info]
                  poses_db = db.collection('pose').get()
                  poses = [pose.to_dict() for pose in poses_db]
                  uid = request.GET.get('uid')
                  name = request.GET.get('name')
                  lastname = request.GET.get('lastname')
                  age = request.GET.get('age')
                  line_id = request.GET.get('line_id')
                  gender = request.GET.get('gender')
                  kin_contact = request.GET.get('kin_contact')
                  phone = request.GET.get('phone')
                  hospital_number = request.GET.get('hospital_number')
                  dicease = request.GET.get('dicease')
                  month = request.GET.get('month')
                  returned = request.GET.get('returned')
                  return render(request,"addpatient.html",{'returned':returned,'doctor_info':doctor_info[0],'uid':uid,'poses':poses,'name':name,'uid':uid,'lastname':lastname,'phone':phone,'hospital_number':hospital_number,'dicease':dicease,'month':month,'age':age,'line_id':line_id,'gender':gender,'kin_contact':kin_contact})
            else:
                return redirect('/login/')
      except:
            return redirect('/doctorpage/')
def selectpose(request):
      try:  
            if 'doctor_id' in request.session:
                  doctor_id = request.session['doctor_id']
                  doctor_info = db.collection('doctor').where('uid','==',doctor_id).get()
                  doctor_info  = [i.to_dict() for i in doctor_info]
                  month = request.POST.get('month')
                  uid = request.POST.get('uid')
                  name = request.POST.get('name')
                  age = request.POST.get('age')
                  line_id = request.POST.get('line_id')
                  gender = request.POST.get('gender')
                  kin_contact = request.POST.get('kin_contact')  
                  lastname = request.POST.get('lastname')
                  phone = request.POST.get('phone')
                  hospital_number = request.POST.get('hospital_number')
                  dicease = request.POST.get('dicease')
                  pose_db = db.collection('pose').get()
                  pose = []
                  for i,v in enumerate(pose_db):
                        pdict = v.to_dict()
                        if (i+1) % 4 == 0:
                              pdict['row'] = 1
                        pose.append(pdict)
                  return render(request, 'selectpose.html', {'doctor_info':doctor_info[0],'dicease':dicease,'month':month,'name':name, 'lastname':lastname,'phone':phone,'hospital_number':hospital_number,'uid':uid,'pose':pose,'age':age,'line_id':line_id,'gender':gender,'kin_contact':kin_contact})
            else:
                  return redirect('/login/')
      except:
            return render(request, 'addpatient.html')

            
def addpatientcase(request):
      try :
            poses_db = db.collection('pose').get()
            poses_indb = [pose.to_dict() for pose in poses_db]
            month = request.POST.get('month')            
            uid = request.POST.get('uid')
            name = request.POST.get('name')
            lastname = request.POST.get('lastname')
            phone = request.POST.get('phone')
            dicease = request.POST.get('dicease') 
            age = request.POST.get('age')
            line_id = request.POST.get('line_id')
            gender = request.POST.get('gender')
            kin_contact = request.POST.get('kin_contact')
            hospital_number = request.POST.get('hospital_number')
            countpose = request.POST.getlist('countpose[]')        
            dopose = request.POST.getlist('dopose[]')
            patient_id = get_random_string()
            status_db = db.collection('patient').where('hospital_number','==',hospital_number).where('doctor_id','==',uid).get()
            for i in status_db:
                 if i.to_dict()['status'] != 'success':
                     return redirect('/doctorpage')  
            check_patient_id = db.collection('patient').where('patient_id','==',patient_id).get()
            pose = [{'pose':poses_indb[i]['pose'],'countpose':countpose[i],'dopose':dopose[i]} for i in range(len(poses_indb))]  
            pose = [i for i in pose if int(i['countpose']) != 0 and int(i['dopose']) != 0]  
            for i in pose:
                  for p in poses_indb:
                        if p['pose'] == i['pose']:
                              i['id'] = p['id']
                              i['detail'] = p['detail']
                              i['link_img'] = p['link_img']
                              i['tracking'] = p['tracking']
            status = 'waiting'
            while len(check_patient_id) > 0:
                  patient_id = get_random_string()
                  check_patient_id = db.collection('patient').where('patient_id','==',patient_id).get()
            data = {'rehab_info':{},'dicease':dicease,'month':month,'status':status,'name':name, 'patient_id':patient_id,'lastname':lastname,'poses':pose,'phone':phone,'hospital_number':hospital_number,'doctor_id':uid,'age':age,'line_id':line_id,'gender':gender,'kin_contact':kin_contact}
            db.collection('patient').document(patient_id).set(data)
            return redirect('/doctorpage')
      except:
            return redirect('/doctorpage')
      

