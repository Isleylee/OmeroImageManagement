# login/views.py

from django.shortcuts import render, redirect, get_object_or_404
from .models import Acquisition, Image, AcqOptional, ImageOptional,User,IMG
from .forms import UserForm, RegisterForm, ForgetForm, ResetForm
import hashlib

# index view, return the index page
def index(request):
    result_list = Acquisition.objects.order_by().values('strain_genotype','worm_stage').distinct()
    strain_list = Acquisition.objects.order_by().values('strain_genotype').distinct()

    imgs = IMG.objects.all()

    for strain in strain_list:
        strain['stage'] = []
        for query in result_list:
            if query['strain_genotype'] == strain['strain_genotype']:
                strain['stage'].append(query['worm_stage'].encode('utf8'))

    context = {'strain_list': strain_list, 'stage_list':result_list, 'img':imgs}

    # get the image information and create a new image in mysql database
    if request.method == 'POST':
        new_img = IMG(
            img=request.FILES.get('img'),
            name = request.FILES.get('img').name,
            acquisition = Acquisition(id = Acquisition.objects.get(strain_genotype=request.POST.get('strain').encode('utf8'),worm_stage=request.POST.get('worm_stage').encode('utf8')).id),
            worm_stage = request.POST.get('worm_stage'),
            img_date = request.POST.get('date'),
            sex = request.POST.get('sex'),
        )
        new_img.save()

    return render(request, 'login/index.html', context)

#  login view
def login(request):
    if request.session.get('is_login', None):
        return redirect('/index')

    if request.method == "POST":
        login_form = UserForm(request.POST)
        message = "Please check input content!"
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                user = User.objects.get(name=username)
                if user.password == hash_code(password):  # Hash code compared with database
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.name
                    return redirect('/index/')
                else:
                    message = "Incorrect password!"
            except:
                message = "User doesn't exist!"
        return render(request, 'login/login.html', locals())

    login_form = UserForm()
    return render(request, 'login/login.html', locals())


# register view
def register(request):
    if request.session.get('is_login', None):
        # In login page you shouldn't register
        return redirect("/index/")
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        message = "Please check input content!"
        if register_form.is_valid():  # Obtain data
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            email = register_form.cleaned_data['email']
            sex = register_form.cleaned_data['sex']
            if password1 != password2:  # Check if two input are the same
                message = "Not the same password!"
                return render(request, 'login/register.html', locals())
            else:
                same_name_user = User.objects.filter(name=username)
                if same_name_user:  # User name not duplicate
                    message = 'Username exists, please input again!'
                    return render(request, 'login/register.html', locals())
                same_email_user = User.objects.filter(email=email)
                if same_email_user:  # E-mail address not duplicate
                    message = 'This E-mail was used, please input again!'
                    return render(request, 'login/register.html', locals())

                # Create new user

                new_user = User.objects.create()
                new_user.name = username
                new_user.password = hash_code(password1)  # Use hash code for password
                new_user.email = email
                new_user.sex = sex
                new_user.save()
                return redirect('/login/')  # Reload to login page
    register_form = RegisterForm()
    return render(request, 'login/register.html', locals())



# class ForgetPwdView(View):
#
#     def get(self,request):
#         forget_form=ForgetForm()
#         return render(request,'forget.html',{'forget_form':forget_form})
#     def post(self,request):
#         forget_form = ForgetForm(request.POST)
#         if forget_form.is_valid():
#             email=request.POST.get('email','')
#             send_register_email(email,'forget')
#             return render(request,'send_success.html')
#         else:
#             return render(request,'forget.html',{'forget_form':forget_form})
#
#
#
# class ResetView(View):
#
#     def get(self,request,active_code):
#         record=EmailVerifyRecord.objects.filter(code=active_code)
#         print(record)
#         if record:
#             for i in record:
#                 email=i.email
#                 is_register=UserProfile.objects.filter(email=email)
#                 if is_register:
#                     return render(request,'pwd_reset.html',{'email':email})
#         return redirect('index')
#
#
#

# class ModifyView(View):
#
#     def post(self,request):
#         reset_form=ResetForm(request.POST)
#         if reset_form.is_valid():
#             pwd1=request.POST.get('newpwd1','')
#             pwd2=request.POST.get('newpwd2','')
#             email=request.POST.get('email','')
#             if pwd1!=pwd2:
#                 return render(request,'pwd_reset.html',{'msg':''})
#             else:
#                 user=UserProfile.objects.get(email=email)
#                 user.password=make_password(pwd2)
#                 user.save()
#                 return redirect('index')
#         else:
#             email=request.POST.get('email','')
#             return render(request,'pwd_reset.html',{'msg':reset_form.errors})

# log out view
def logout(request):
    if not request.session.get('is_login', None):

        return redirect("/index/")
    request.session.flush()

    # del request.session['is_login']
    # del request.session['user_id']
    # del request.session['user_name']
    return redirect("/index/")

def hash_code(s, salt='mysite'):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()


#  get strain with stage selected
def getStrain_stage(request, strain, stage):


## split the stage name which contains("_")
    stage_split  = stage.split("_")
    if(len(stage_split)>1):
        ch = stage_split[0]
        for i in range(1, len(stage_split)):
            ch = ch + " " + stage_split[i]
        selected_stage = ch
    else:
        selected_stage = stage

    # get strain list
    strain_list = Acquisition.objects.order_by().values('strain_genotype').distinct()
    splitgene = strain.split("_")
    niceoutput = splitgene[0]
    if(len(splitgene) >1):
        niceoutput = niceoutput + '(' + splitgene[1]+')'

    stages = []
    images = getStages(strain,stages)
    stages = images.keys()

    new_stages = []
    flag = 1

    for s in stages:
        split = s.split(" ")
        print(split)
        if(len(split)>1):
            ch = split[0]
            for i in range(1,len(split)):
                ch = ch + "_" + split[i]
            print(ch)
            new_stages.append(ch)
        else:
            new_stages.append(split[0])

    #Create all image download url
    allImage = ""

    for key, value in images.items():
        if(key == selected_stage):
            for imageid in value:
                allImage += "image-"
                allImage += str(imageid)
                allImage += "|"


    context = {'strain_list': strain_list, 'selected_stage': selected_stage, 'output':niceoutput, 'stages':new_stages,'strain':strain, 'images': images,'flag':flag,  'allImage':allImage}

    return render(request, "login/strain.html",context)

# get strains that stage is not selected
def getStrains(request, strain):


    strain_list = Acquisition.objects.order_by().values('strain_genotype').distinct()
    splitgene = strain.split("_")
    niceoutput = splitgene[0]
    if(len(splitgene) >1):
        niceoutput = niceoutput + '(' + splitgene[1]+')'

    stages = []
    images = getStages(strain,stages)
    stages = images.keys()
    if stages[0] == None:
        selected_stage = None
    else:
        selected_stage = stages[0]

    new_stages = []

    for s in stages:
        split = s.split(" ")
        print(split)
        if(len(split)>1):
            ch = split[0]
            for i in range(1,len(split)):
                ch = ch + "_" + split[i]
            print(ch)
            new_stages.append(ch)
        else:
            new_stages.append(split[0])

    print(new_stages)

    context = {'strain_list': strain_list, 'selected_stage': selected_stage, 'output':niceoutput, 'stages':new_stages,'strain':strain, 'images': images}

    return render(request, "login/strain.html",context)

# image datails view, similar to getStrain()
def getImageDetails(request,strain, stage, imageid):
    stage_split  = stage.split("_")
    if(len(stage_split)>1):
        ch = stage_split[0]
        for i in range(1, len(stage_split)):
            ch = ch + " " + stage_split[i]
        selected_stage = ch
    else:
        selected_stage = stage

    strain_list = Acquisition.objects.order_by().values('strain_genotype').distinct()
    splitgene = strain.split("_")
    niceoutput = splitgene[0]
    if(len(splitgene) >1):
        niceoutput = niceoutput + '(' + splitgene[1]+')'

    stages = []
    images = getStages(strain,stages)
    stages = images.keys()

    new_stages = []
    flag = 1

    for s in stages:
        split = s.split(" ")
        if(len(split)>1):
            ch = split[0]
            for i in range(1,len(split)):
                ch = ch + "_" + split[i]
            new_stages.append(ch)
        else:
            new_stages.append(split[0])

    allImage = ""

    for key, value in images.items():
        if(key == selected_stage):
            for imageid in value:
                allImage += "image-"
                allImage += str(imageid)
                allImage += "|"

    context = {'strain_list': strain_list, 'selected_stage': selected_stage, 'output':niceoutput, 'stages':new_stages,'strain':strain, 'images': images,'flag':flag, 'image':imageid,
               'allImage':allImage}

    return render(request, "login/imagedetails.html", context)


# check whether strains are in mysql
def checkStrain(strain):
    result = Acquisition.objects.filter(strain_genotype=strain)
    return len(result)

# check whether stages are in mysql
def checkStage(stage):
    stages = stageList()
    return stage in stages


# return image information in stages
def getStages(strain, stages, opt=[]):
    images = {}
    stages = stageList()

    for stage in stages:
        imagedata = queryStage(strain,stage,opt)
        if(len(imagedata) !=0):
            for im in imagedata:
                split = stage.split(" ")
                print(split)
                if (len(split) > 1):
                    ch = split[0]
                    for i in range(1, len(split)):
                        ch = ch + "_" + split[i]
                else:
                    ch = stage
                if ch not in images.keys():
                    images[ch] = im
                else:
                    images[ch].append(im[0])

    return images

# return image id
def queryStage(acq, stage, search):
    acqfileds = getAcqfields()
    acqoptfields = getAcqoptfields()
    imgfields = getImgfields()
    imgoptfields = getImgoptfields()


    ImageId = Image.objects.filter(acquisition__strain_genotype = acq, worm_stage=stage).values('merged_id').distinct()

    info = []
    if (len(ImageId) == 0):
        return info

    for item in ImageId:
        info.append(item.values())

    return info

def stageList():
    return ["L1", "L2", "L3", "L4", "YA", "Day 1 Adult", "See Worm Specific CSV File"]

def getAcqfields():
    return ['magnification', 'experimenter', 'img_method']


def getAcqoptfields():
    return []

def getImgfields():
    return ['FAKEROI', 'sex', 'orientation']

def getImgoptfields():
    return ['GRASP Signal', 'Mobilization']

def getTableacqfields():
    return getAcqoptfields()+['acq_date', 'microscope', 'camera', 'scope_website', 'num_ap', 'gfp_time', 'gfp_power', 'rfp_time', 'rfp_power']

def getTableimgfields():
    return getImgfields()+['worm_stage', 'img_date']





