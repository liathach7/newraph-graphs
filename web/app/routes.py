from app import app,db
import sqlalchemy as sa
from flask import render_template, redirect, url_for, send_file,request,session,flash,make_response
from app.forms import EnterEquation
from app.models import User,UserPreset,StepList2,PixelString,MegaList,PixelString3
from app.maths import Functions as f
import io,base64,uuid,matplotlib,os
#from werkzeug.middleware.profiler import ProfilerMiddleware
from datetime import date,datetime,timedelta,timezone
import traceback
#from time import sleep

num_journeys = 20
fig=''

@app.route('/')
@app.route('/enter')
def enter():
    cwd=os.getcwd()
    print('current working directory is ',cwd)
    f.db_delete(User)
    f.db_delete(UserPreset)
    f.db_delete(PixelString)
    f.db_delete(PixelString3)
    f.db_delete(MegaList)
    f.db_delete(StepList2)
    def my_random_string(string_length=10):
        """Returns a random string of length string_length."""
        random = str(uuid.uuid4()) # Convert UUID format to a Python string.
        random = random.replace("-","") # Remove the UUID '-'.
        return random[0:string_length] # Return the random string.
    cookie_value=my_random_string(string_length=10)
    res=make_response(redirect(url_for('index')))
    res.set_cookie('foo',cookie_value)
    return res


@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.cookies.get('foo'):
        cookie_code=request.cookies.get('foo')
    else:
        return '<html><p>the server cant read your cookie</p></html>'
    form = EnterEquation()
    if form.validate_on_submit():
        eq=form.equation.data
        ll_str=form.lower_limit.data
        ul_str=form.upper_limit.data
        ll_flt=float(ll_str)
        ul_flt=float(ul_str)
        if ll_flt>ul_flt:
            flash('the upper limit is too low') 
            return redirect(url_for('index'))
        # for updating database
        entry=db.session.query(User).filter(User.cookie_code==cookie_code)
        i=0
        for e in entry:
            i=+1
        if i>1:
            print('update entry')
            for e in entry:
                ayedee=e.id
            print('id is ',ayedee)
            user=db.session.get(User,ayedee)
            user.lower_limit=ll_str
            user.upper_limit=ul_str
            user.equation=eq
            db.session.commit()
        else:
            print('new entry')
            user=User(lower_limit=ll_str,upper_limit=ul_str,equation=eq,cookie_code=cookie_code)
            db.session.add(user)
            db.session.commit()
        if ll_flt<-15 or ul_flt>15:
            return redirect(url_for('confirm'))
        return redirect(url_for('results'))
    return render_template('index.html', form=form)


@app.route('/confirm')
def confirm():
    return render_template('confirm.html')

@app.route('/suggestion_eq1',methods=['GET','POST'])
def suggestion_eq1():
    if request.cookies.get('foo'):
        cookie_code=request.cookies.get('foo')
    else:
        return '<html><p>the server cant read your cookie</p></html>'
    entry=db.session.query(UserPreset).filter(UserPreset.cookie_code==cookie_code)
    i=0
    for e in entry:
        i=+1
    if i==1:
        print('update entry')
        for e in entry:
            ayedee=e.id
        print('id is ',ayedee)
        user=db.session.get(UserPreset,ayedee)
        user.equation='x^6 - 120*x^2 + 48*x + 389'
        db.session.commit()
    else:
        print('new entry')
        user=UserPreset(equation='x^6 - 120*x^2 + 48*x + 389',cookie_code=cookie_code)
        db.session.add(user)
        db.session.commit()
    return {'boo':'foo'}

@app.route('/suggestion_eq2',methods=['GET','POST'])
def suggestion_eq2():
    if request.cookies.get('foo'):
        cookie_code=request.cookies.get('foo')
    else:
        return '<html><p>the server cant read your cookie</p></html>'
    entry=db.session.query(UserPreset).filter(UserPreset.cookie_code==cookie_code)
    i=0
    for e in entry:
        i=+1
    if i==1:
        print('update entry')
        for e in entry:
            ayedee=e.id
        print('id is ',ayedee)
        user=db.session.get(UserPreset,ayedee)
        user.equation='5*x^3 + 3^x - 5^x + 0.15'
        db.session.commit()
    else:
        print('new entry')
        user=UserPreset(equation='5*x^3 + 3^x - 5^x + 0.15',cookie_code=cookie_code)
        db.session.add(user)
        db.session.commit()
    return {'boo':'foo'}
    
@app.route('/suggestion_eq3',methods=['GET','POST'])
def suggestion_eq3():
    if request.cookies.get('foo'):
        cookie_code=request.cookies.get('foo')
    else:
        return '<html><p>the server cant read your cookie</p></html>'
    entry=db.session.query(UserPreset).filter(UserPreset.cookie_code==cookie_code)
    i=0
    for e in entry:
        i=+1
    if i==1:
        print('update entry')
        for e in entry:
            ayedee=e.id
        print('id is ',ayedee)
        user=db.session.get(UserPreset,ayedee)
        user.equation='x^3 - x^2 + 0.25'
        db.session.commit()
    else:
        print('new entry')
        user=UserPreset(equation='x^3 - x^2 + 0.25',cookie_code=cookie_code)
        db.session.add(user)
        db.session.commit()
    return {'boo':'foo'}

@app.route('/suggestion1',methods=['GET','POST'])
def suggestion1():
    if request.cookies.get('foo'):
        cookie_code=request.cookies.get('foo')
    else:
        return '<html><p>the server cant read your cookie</p></html>'
    form=EnterEquation()
    entry=db.session.query(UserPreset).filter(UserPreset.cookie_code==cookie_code)
    for e in entry:
        eq_preset=e.equation
    form.equation.data=eq_preset
    if form.validate_on_submit():
        eq=form.equation.data
        ll_str=form.lower_limit.data
        ul_str=form.upper_limit.data
        ll_flt=float(ll_str)
        ul_flt=float(ul_str)
        if ll_flt>ul_flt:
            flash('the upper limit is too low') 
            return redirect(url_for('index'))
        # for updating database
        entry=db.session.query(User).filter(User.cookie_code==cookie_code)
        i=0
        for e in entry:
            i=+1
        if i==1:
            print('update entry')
            for e in entry:
                ayedee=e.id
            print('id is ',ayedee)
            user=db.session.get(User,ayedee)
            user.lower_limit=ll_str
            user.upper_limit=ul_str
            user.equation=eq
            db.session.commit()
        else:
            print('new entry')
            user=User(lower_limit=ll_str,upper_limit=ul_str,equation=eq,cookie_code=cookie_code)
            db.session.add(user)
            db.session.commit()
        if ll_flt<-15 or ul_flt>15:
            return redirect(url_for('confirm'))
        return redirect(url_for('results'))
    return render_template('index.html', form=form)

@app.route('/results', methods=['GET', 'POST'])
def results():
    try:
        if request.cookies.get('foo'):
            cookie_code=request.cookies.get('foo')
        else:
            return '<html><p>the server cant read your cookie</p></html>'
        entry=db.session.query(User).filter(User.cookie_code==cookie_code)
        for e in entry:
            eq=e.equation
            print(eq)
        y_test=f.y_range(eq,[1,2])
        #traceback.print_stack()
        return render_template('results.html')
    except:
        flash("something's not right. Was the equation typed correctly?")
        return redirect(url_for('index'))

@app.route('/graph')
def graph():
    num_journeys2=num_journeys *2
    if request.cookies.get('foo'):
        cookie_code=request.cookies.get('foo')
    else:
        print('<html><p>the server cant read your cookie</p></html>')
    entry=db.session.query(User).filter(User.cookie_code==cookie_code)
    for e in entry:
        eq=e.equation
        ll_str=e.lower_limit
        ul_str=e.upper_limit
        ll_flt=float(ll_str)
        ul_flt=float(ul_str)
    x_range2 = f.x_range3(ll_flt, ul_flt, num_journeys2)
    y_range = f.y_range(eq, x_range2)
    fig = f.graph(x_range2, y_range,eq)
    print('*')
    print(type(fig))
    img = io.BytesIO()
    fig.savefig(img)
    img.seek(0)
    return send_file(img, mimetype='image/png')

@app.route('/zoom_graph',methods=['POST'])
def zoom_graph():
    print('reached zoom_graph')
    if request.cookies.get('foo'):
        cookie_code=request.cookies.get('foo')
    else:
        print('<html><p>the server cant read your cookie</p></html>')
    entry=db.session.query(User).filter(User.cookie_code==cookie_code)
    for e in entry:
        eq=e.equation
        ll_str=e.lower_limit
        ul_str=e.upper_limit
        ll_flt=float(ll_str)
        ul_flt=float(ul_str)
    gif_url=f.zoom_graph(eq,ll_flt,ul_flt)
    #deleting previous pixel string if there
    entries=db.session.query(PixelString).filter(PixelString.cookie_code==cookie_code)
    for e in entries:
        db.session.delete(e)
        db.session.commit()
    entry2=PixelString(cookie_code=cookie_code,pix_str=gif_url)
    db.session.add(entry2)
    db.session.commit()
    return {'show_word':'boo'}

@app.route('/zoom_graph2')
def zoom_graph2():
    print('reached zoom_graph2')
    if request.cookies.get('foo'):
        cookie_code=request.cookies.get('foo')
    else:
        print('<html><p>the server cant read your cookie</p></html>')
    entry=db.session.query(PixelString).filter(PixelString.cookie_code==cookie_code)
    for e in entry:
        gif_url=e.pix_str
    with open(gif_url,"rb") as image:
        f=image.read()
        b=bytearray(f)
    gif_bytes=io.BytesIO(b)
    os.remove(gif_url)
    return send_file(gif_bytes,mimetype='image/gif')

@app.route('/stem_graph',methods=['POST'])
def stem_graph():
    if request.cookies.get('foo'):
        cookie_code=request.cookies.get('foo')
    else:
        return '<html><p>the server cant read your cookie</p></html>'
    entry=db.session.query(User).filter(User.cookie_code==cookie_code)
    for e in entry:
        eq=e.equation
        ll_str=e.lower_limit
        ul_str=e.upper_limit
        ll_flt=float(ll_str)
        ul_flt=float(ul_str)
    x_range2 = f.x_range3(ll_flt, ul_flt, num_journeys)
    y_range = f.y_range(eq, x_range2)
    step=0
    step_list=[]
    print('reached here,1')
    for x in x_range2:
        f.newton_function(x,step,eq,step_list)
    print(type(step_list))
    print(step_list)
    #deleting previous step list if there
    steps=db.session.query(StepList2).filter(StepList2.cookie_code==cookie_code)
    for step in steps:
        print(step.num_steps,', ',step.cookie_code,' is about to get deleted')
        db.session.delete(step)
        db.session.commit()
        #new_entry=e
        #ayedee=e.id
    #entree=db.session.get(StepList2,ayedee)
    #query=entree.steps2.select()
    #steps=db.session.scalars(query)
    #for step in steps:
    #    db.session.delete(step)
    #db.session.commit()
    #^
    for step in step_list:
        s=StepList2(num_steps=step,cookie_code=cookie_code)
        db.session.add(s)
        db.session.commit()
    #img=f.stem_graph(x_range2,step_list)
    #img_str=base64.b64decode(img)
    #entry2=PixelString(cookie_code=cookie_code,pix_str=img_str)
    #db.session.add(entry2)
    #db.session.commit()
    print('the cookie_code is ',cookie_code)
    #deleting previous pixel string if there
    entries=db.session.query(PixelString).filter(PixelString.cookie_code==cookie_code)
    for e in entries:
        db.session.delete(e)
        db.session.commit()
    img_url=f.stem_graph(x_range2,step_list)
    entry2=PixelString(cookie_code=cookie_code,pix_str=img_url)
    db.session.add(entry2)
    db.session.commit()
    return {'some text':'other text'}
    
@app.route('/stem_graph2')
def stem_graph2():
    print('reached here,2')
    if request.cookies.get('foo'):
        cookie_code=request.cookies.get('foo')
    else:
        print('<html><p>the server cant read your cookie</p></html>')
    entry=db.session.query(PixelString).filter(PixelString.cookie_code==cookie_code)
    for e in entry:
        img_url=e.pix_str
    #for some reason when moving app to docker io.BytesIO needed a bytes object instead of a string, hence byte array
    #with open(img_url, "rb") as image_file:
    #    img_str = base64.b64encode(image_file.read()).decode()
    #
    with open(img_url, "rb") as image:
        f = image.read()
        b = bytearray(f)
    img_bytes=io.BytesIO(b)
    #img_bytes=io.BytesIO(img_str)
    #print('type is ',type(img_bytes))
    #for e in entry:
    #    db.session.delete(e)
    #    db.session.commit()
    os.remove(img_url)
    return send_file(img_bytes,mimetype='image/png')

@app.route('/steps', methods=['GET', 'POST'])
def steps():
    if request.cookies.get('foo'):
        cookie_code=request.cookies.get('foo')
    else:
        print('<html><p>the server cant read your cookie</p></html>')
    entry=db.session.query(User).filter(User.cookie_code==cookie_code)
    for e in entry:
        eq=e.equation
        ll_str=e.lower_limit
        ul_str=e.upper_limit
        ll_flt=float(ll_str)
        ul_flt=float(ul_str)
    entries=db.session.query(StepList2).filter(StepList2.cookie_code==cookie_code)
    step_list=[]
    for e in entries:
        s1=e.num_steps
        step_list.append(s1)
    #query=e.steps2.select()
    #steps=db.session.scalars(query)
    #step_list=[]
    #for step in steps:
    #    s1=step.num_steps
    #    step_list.append(s1)
    x_range2 = f.x_range3(ll_flt, ul_flt, num_journeys)
    y_range = f.y_range(eq, x_range2)
    img_url=f.coloured_graph(x_range2,y_range,step_list)
    #deleting previous pixel string if there
    entries=db.session.query(PixelString).filter(PixelString.cookie_code==cookie_code)
    for e in entries:
        db.session.delete(e)
        db.session.commit()
    entry2=PixelString(cookie_code=cookie_code,pix_str=img_url)
    db.session.add(entry2)
    db.session.commit()
    #checks if another entry with same cookie code already exists in database
    """tester=db.session.query(PixelString).filter(User.cookie_code==cookie_code)
    i=0
    for t in tester:
        i+=1
    if i>1:
        print('i > 0')
        for t in tester:
            ayedee=t.id
        entry=db.session.get(PixelString,ayedee)
        print('entry id is',entry.id,'\nentry cookie code is ',entry.cookie_code,'\nentry pix_str is ',entry.pix_str,'\ntmime stamp ',entry.timestamp)
        entry.pix_str=img_url
        print('entry id is',entry.id,'\nentry cookie code is ',entry.cookie_code,'\nentry pix_str is ',entry.pix_str,'\ntmime stamp ',entry.timestamp)
    else:
        print('i < 1')
        entry=PixelString(cookie_code=cookie_code,pix_str=img_url)
        db.session.add(entry)
    query=sa.select(PixelString)
    entries=db.session.scalars(query)
    for e in entries:
        print('entry id is',entry.id,'\nentry cookie code is ',entry.cookie_code,'\nentry pix_str is ',entry.pix_str,'\ntmime stamp ',entry.timestamp)
    db.session.commit()
    print('db commit')
    query=sa.select(PixelString)
    entries=db.session.scalars(query)
    for e in entries:
        print('entry id is',entry.id,'\nentry cookie code is ',entry.cookie_code,'\nentry pix_str is ',entry.pix_str,'\ntmime stamp ',entry.timestamp)"""
    return {'some text':'other text'}

@app.route('/coloured_graph')
def coloured_graph():
    if request.cookies.get('foo'):
        cookie_code=request.cookies.get('foo')
    else:
        print('html><p>the server cant read your cookie</p></html>')
    entry=db.session.query(PixelString).filter(PixelString.cookie_code==cookie_code)
    for e in entry:
        img_url=e.pix_str
    with open(img_url,"rb") as image:
        f=image.read()
        b=bytearray(f)
    img_bytes=io.BytesIO(b)
    os.remove(img_url)
    return send_file(img_bytes,mimetype='image/png')

@app.route('/ran_tan',methods=['GET', 'POST'])
def ran_tan():
    #collect entry from database
    if request.cookies.get('foo'):
        cookie_code=request.cookies.get('foo')
    else:
        return '<html><p>the server cant read your cookie</p></html>'
    entry=db.session.query(User).filter(User.cookie_code==cookie_code)
    for e in entry:
        eq=e.equation
        ll_str=e.lower_limit
        ul_str=e.upper_limit
        ll_flt=float(ll_str)
        ul_flt=float(ul_str)
    entries=db.session.query(StepList2).filter(StepList2.cookie_code==cookie_code)
    step_list=[]
    for e in entries:
        s1=e.num_steps
        step_list.append(s1)
        #query=e.steps2.select()
        #steps=db.session.scalars(query)
        #step_list=[]
        #for step in steps:
        #    s1=step.num_steps
        #    step_list.append(s1)
    print('step list: ',step_list)
    x_range = f.x_range3(ll_flt, ul_flt, num_journeys)
    x_range2=x_range.tolist()
    x_list=[]
    tang_list=[]
    megalist_x=[]
    megalist_y=[]
    mask_starts=[]
    tang_starts2=[]
    f.tang(step_list,x_range2,tang_list,eq,megalist_x,megalist_y,tang_starts2,x_list,mask_starts)
    print('megalist ',megalist_x)
    #add megalist to database
    entries=db.session.query(MegaList).filter(MegaList.cookie_code==cookie_code)
    for e in entries:
        print(e.id,', ',e.timestamp,', ',e.x,' is about to get deleted')
        db.session.delete(e)
        db.session.commit()
        new_entry=e
        #deletes previous mega_list if there
        #ayedee=e.id
    #user=db.session.get(User,ayedee)
    #query=user.megalist.select()
    #ml_entries=db.session.scalars(query)
    #for ml_entry in ml_entries:
    #    db.session.delete(ml_entry)
    #db.session.commit()
    #^
    for i in range(len(megalist_x)):
        x=megalist_x[i]
        y=megalist_y[i]
        if i < len(mask_starts):
            mask_start=mask_starts[i]
        else:
            mask_start=-1
            # add into code later that a mask_start with this value is ignored
        ml=MegaList(x=x,y=y,mask_start=mask_start,cookie_code=cookie_code)
        db.session.add(ml)
        db.session.commit()
    try:
        ran_x=x_list[0]
    except:
        return '<p>this equation didnt result in enough steps. go back and try a different one</p>'
    position=tang_list[0]
    ran_tan_position=str(position)
    tan1_start=megalist_x[0]
    tan2_start=megalist_x[11]
    tan3_start=megalist_x[22]
    tan4_start=megalist_x[33]
    if tang_starts2[-1]<8:
        error_mes='Sorry there are not enough steps in this journey to show the tangets. PLease try reloading'
    else:
        error_mes=''
    print('tang starts 2 is ',tang_starts2)
    # for updating database
    entry2=db.session.query(PixelString3).filter(PixelString3.cookie_code==cookie_code)
    i=0
    for e in entry2:
        i=+1
    if i==1:
        print('update entry')
        for e in entry2:
            ayedee=e.id
        print('id is ',ayedee)
        user=db.session.get(PixelString3,ayedee)
        user.ran_x=ran_x
        user.ran_tan_position=position
        user.ran_num_steps=tang_starts2[-1]
        db.session.commit()
    else:
        print('new entry')
        user=PixelString3(ran_x=ran_x,ran_tan_position=position,ran_num_steps=tang_starts2[-1],tang_str='',start_str='',end_str='',cookie_code=cookie_code)
        db.session.add(user)
        db.session.commit()
    return render_template('ran_tan.html',step_list=step_list,ran_x=ran_x,
    position=position,tan1_start=tan1_start,tan2_start=tan2_start,
    tan3_start=tan3_start,tan4_start=tan4_start,tang_starts2=tang_starts2[-1],equation=eq,error_mes=error_mes)



@app.route('/tang_graph',methods=['POST'])
def tang_graph():
    if request.cookies.get('foo'):
        cookie_code=request.cookies.get('foo')
    else:
        print('<html><p>the server cant read your cookie</p></html>')
    entry=db.session.query(User).filter(User.cookie_code==cookie_code)
    for e in entry:
        eq=e.equation
    values=db.session.query(MegaList).filter(MegaList.cookie_code==cookie_code)
    megalist_x=[]
    megalist_y=[]
    mask_starts=[]
    for v in values:
        x=v.x
        y=v.y
        if v.mask_start == -1:
            computer='distract'
        else:
            mask_start=v.mask_start
            mask_starts.append(mask_start)
        megalist_x.append(x)
        megalist_y.append(y)
    gif_url=f.tang_graph(megalist_x,megalist_y,eq,mask_starts)
    # for updating database
    entry=db.session.query(PixelString3).filter(PixelString3.cookie_code==cookie_code)
    for e in entry:
        ayedee=e.id
        ran_tan_position=e.ran_tan_position
        ran_num_steps=e.ran_num_steps
    update=db.session.get(PixelString3,ayedee)
    update.tang_str=gif_url
    db.session.commit()
    #^
    print('reached tang_graph')
    str1=str(ran_tan_position)
    str2=str(ran_num_steps)
    my_str='Starting from position '+str1+' of '+str2
    return {'key':my_str}

@app.route('/tang_graph2')
def tang_graph2():
    if request.cookies.get('foo'):
        cookie_code=request.cookies.get('foo')
    else:
        print('<html><p>the server cant read your cookie</p></html>')
    entry=db.session.query(PixelString3).filter(PixelString3.cookie_code==cookie_code)
    for e in entry:
        gif_url=e.tang_str
    with open(gif_url, "rb") as image:
        f = image.read()
        b = bytearray(f)
    gif_bytes=io.BytesIO(b)
    os.remove(gif_url)
    return send_file(gif_bytes,mimetype='image/gif')

@app.route('/tang_graph_start',methods=['POST'])
def tang_graph_start():
    if request.cookies.get('foo'):
        cookie_code=request.cookies.get('foo')
    else:
        print('<html><p>the server cant read your cookie</p></html>')
    entry=db.session.query(User).filter(User.cookie_code==cookie_code)
    for e in entry:
        eq=e.equation
        ll_str=e.lower_limit
        ll_flt=float(ll_str)
        ul_str=e.upper_limit
        ul_flt=float(ul_str)
    x_range= f.x_range3(ll_flt, ul_flt, num_journeys)
    x_range2=x_range.tolist()
    x_range3=f.x_range4(ll_flt, ul_flt)
    y_range = f.y_range(eq, x_range2)
    megalist_x2=[]
    megalist_y2=[]
    error=''
    entry2=db.session.query(PixelString3).filter(PixelString3.cookie_code==cookie_code)
    for e in entry2:
        ran_x=e.ran_x
        ran_num_steps=e.ran_num_steps
        ayedee=e.id
    gif_url=f.draw_tangents_start(eq,ran_x,0,0,0,megalist_x2,megalist_y2,ran_num_steps,[],x_range2,y_range,error)
    update=db.session.get(PixelString3,ayedee)
    update.start_str=gif_url
    db.session.commit()
    my_str=''
    return {'key':my_str}
    

@app.route('/tang_graph_start2')
def tang_graph_start2():
    if request.cookies.get('foo'):
        cookie_code=request.cookies.get('foo')
    else:
        print('<html><p>the server cant read your cookie</p></html>')
    try:
        entry=db.session.query(PixelString3).filter(PixelString3.cookie_code==cookie_code)
        for e in entry:
            gif_url=e.start_str
        with open(gif_url, "rb") as image:
            f = image.read()
            b = bytearray(f)
        gif_bytes=io.BytesIO(b)
        os.remove(gif_url)
        return send_file(gif_bytes,mimetype='image/gif')
    except:
        with open('app//static//error_try_reloading.png', "rb") as image_file:
            data = base64.b64encode(image_file.read()).decode()
            img_str=base64.b64decode(data)
            img_bytes=io.BytesIO(img_str)
        return send_file(img_bytes,mimetype='image/gif')

@app.route('/tang_graph_end',methods=['POST'])
def tang_graph_end():
    if request.cookies.get('foo'):
        cookie_code=request.cookies.get('foo')
    else:
        print('<html><p>the server cant read your cookie</p></html>')
    entry=db.session.query(User).filter(User.cookie_code==cookie_code)
    for e in entry:
        eq=e.equation
    entry2=db.session.query(PixelString3).filter(PixelString3.cookie_code==cookie_code)
    for e in entry2:
        ran_x=e.ran_x
        ran_num_steps=e.ran_num_steps
        ayedee=e.id
    gif_url=f.draw_tangents_end(eq,ran_x,0,0,0,[],[],ran_num_steps,[])
    update=db.session.get(PixelString3,ayedee)
    update.end_str=gif_url
    db.session.commit()
    my_str=''
    return {'key':my_str}

@app.route('/tang_graph_end2')
def tang_graph_end2():
    if request.cookies.get('foo'):
        cookie_code=request.cookies.get('foo')
    else:
        print('<html><p>the server cant read your cookie</p></html>')
    entry=db.session.query(PixelString3).filter(PixelString3.cookie_code==cookie_code)
    for e in entry:
        gif_url=e.end_str
    with open(gif_url, "rb") as image:
        f = image.read()
        b = bytearray(f)
    gif_bytes=io.BytesIO(b)
    os.remove(gif_url)
    return send_file(gif_bytes,mimetype='image/gif')

@app.route('/one_d_graph')
def one_d_graph():
    if request.cookies.get('foo'):
        cookie_code=request.cookies.get('foo')
    else:
        print('<html><p>the server cant read your cookie</p></html>')
    entry=db.session.query(User).filter(User.cookie_code==cookie_code)
    for e in entry:
        ll_str=e.lower_limit
        ul_str=e.upper_limit
        ll_flt=float(ll_str)
        ul_flt=float(ul_str)
    entry2=db.session.query(PixelString3).filter(PixelString3.cookie_code==cookie_code)
    for e in entry2:
        ran_x=e.ran_x
    fig=f.one_d_graph(ll_flt,ul_flt,round(ran_x,3))
    img=io.BytesIO()
    fig.savefig(img)
    img.seek(0)
    return send_file(img,mimetype='image/png')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/youtube_image')
def youtube_image():
    with open('app//static//newton_method.png', "rb") as image_file:
        data = base64.b64encode(image_file.read()).decode()
    img_str=base64.b64decode(data)
    img_bytes=io.BytesIO(img_str)
    return send_file(img_bytes,mimetype='image/png')

@app.route('/eg1')
def eg1():
    with open('app//static//eg1.png', "rb") as image_file:
        data = base64.b64encode(image_file.read()).decode()
    img_str=base64.b64decode(data)
    img_bytes=io.BytesIO(img_str)
    return send_file(img_bytes,mimetype='image/png')

@app.route('/eg2')
def eg2():
    with open('app//static//eg2.png', "rb") as image_file:
        data = base64.b64encode(image_file.read()).decode()
    img_str=base64.b64decode(data)
    img_bytes=io.BytesIO(img_str)
    return send_file(img_bytes,mimetype='image/png')
    
@app.route('/test',methods=['GET','POST'])
def test():
    return {'some text':'boo'}

@app.route('/test2',methods=['GET','POST'])
def test2():
    return render_template('test2.html')

