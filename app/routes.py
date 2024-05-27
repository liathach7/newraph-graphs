from app import app,db
import sqlalchemy as sa
from flask import render_template, redirect, url_for, send_file,request,session,flash
from app.forms import EnterEquation
from app.models import User,UserPreset,StepList,StepList2,PixelString,MegaList,PixelString2,PixelString3
from app.maths import Functions as f
import io,base64
import matplotlib
from werkzeug.middleware.profiler import ProfilerMiddleware
from datetime import date,datetime,timedelta,timezone
#from flask_session import Session
import traceback
#from time import sleep

#app.wsgi_app = ProfilerMiddleware(app.wsgi_app)
#app.run(debug = True)
num_journeys = 20
fig=''

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = EnterEquation()
    session_id=id(session)
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
        entry=db.session.query(User).filter(User.session_id==session_id)
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
            user=User(lower_limit=ll_str,upper_limit=ul_str,equation=eq,session_id=session_id)
            db.session.add(user)
            db.session.commit()
        #deleting old entries
        now=datetime.now(timezone.utc)
        fmt='%Y-%m-%d %H:%M:%S.%f'
        now_str=now.strftime(fmt)
        now_new=datetime.strptime(now_str,fmt)
        query=sa.select(User)
        entries=db.session.scalars(query)
        for e in entries:
            ts=e.timestamp
            u_id=e.id
            ts_str=str(ts)
            ts_con=datetime.strptime(ts_str,fmt)
            diff=now_new-ts_con
            if diff>timedelta(days=5):
                entry2=db.session.get(User,u_id)
                db.session.delete(entry2)
                db.session.commit()
        if ll_flt<-15 or ul_flt>15:
            return redirect(url_for('confirm'))
        return redirect(url_for('results'))
    return render_template('index.html', form=form,session_id=session_id)
"""def index2():
    print ('begin')
    sleep(3) # simulate delay
    print ('end')
    return 'success'"""

@app.route('/confirm')
def confirm():
    return render_template('confirm.html')

@app.route('/suggestion_eq1',methods=['GET','POST'])
def suggestion_eq1():
    session_id=id(session)
    entry=db.session.query(UserPreset).filter(UserPreset.session_id==session_id)
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
        user=UserPreset(equation='x^6 - 120*x^2 + 48*x + 389',session_id=session_id)
        db.session.add(user)
        db.session.commit()
    return {'boo':'foo'}

@app.route('/suggestion_eq2',methods=['GET','POST'])
def suggestion_eq2():
    session_id=id(session)
    entry=db.session.query(UserPreset).filter(UserPreset.session_id==session_id)
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
        user=UserPreset(equation='5*x^3 + 3^x - 5^x + 0.15',session_id=session_id)
        db.session.add(user)
        db.session.commit()
    return {'boo':'foo'}
    
@app.route('/suggestion_eq3',methods=['GET','POST'])
def suggestion_eq3():
    session_id=id(session)
    entry=db.session.query(UserPreset).filter(UserPreset.session_id==session_id)
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
        user=UserPreset(equation='x^3 - x^2 + 0.25',session_id=session_id)
        db.session.add(user)
        db.session.commit()
    return {'boo':'foo'}

@app.route('/suggestion1',methods=['GET','POST'])
def suggestion1():
    form=EnterEquation()
    session_id=id(session)
    entry=db.session.query(UserPreset).filter(UserPreset.session_id==session_id)
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
        entry=db.session.query(User).filter(User.session_id==session_id)
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
            user=User(lower_limit=ll_str,upper_limit=ul_str,equation=eq,session_id=session_id)
            db.session.add(user)
            db.session.commit()
        if ll_flt<-15 or ul_flt>15:
            return redirect(url_for('confirm'))
        return redirect(url_for('results'))
    #deleting old entries
    now=datetime.now(timezone.utc)
    fmt='%Y-%m-%d %H:%M:%S.%f'
    now_str=now.strftime(fmt)
    now_new=datetime.strptime(now_str,fmt)
    query=sa.select(UserPreset)
    entries=db.session.scalars(query)
    for e in entries:
        ts=e.timestamp
        u_id=e.id
        ts_str=str(ts)
        ts_con=datetime.strptime(ts_str,fmt)
        diff=now_new-ts_con
        if diff>timedelta(days=5):
            entry2=db.session.get(UserPreset,u_id)
            db.session.delete(entry2)
            db.session.commit()
    return render_template('index.html', form=form,session_id=session_id)

@app.route('/results', methods=['GET', 'POST'])
def results():
    try:
        session_id=id(session)
        entry=db.session.query(User).filter(User.session_id==session_id)
        for e in entry:
            eq=e.equation
            print(eq)
        y_test=f.y_range(eq,[1,2])
        #traceback.print_stack()
        return render_template('results.html',session_id=session_id)
    except:
        flash("something's not right. Was the equation typed correctly?")
        return redirect(url_for('index'))

@app.route('/graph')
def graph():
    num_journeys2=num_journeys *2
    session_id=id(session)
    entry=db.session.query(User).filter(User.session_id==session_id)
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
    #data=request.get_json()
    session_id=id(session)
    entry=db.session.query(User).filter(User.session_id==session_id)
    for e in entry:
        eq=e.equation
        ll_str=e.lower_limit
        ul_str=e.upper_limit
        ll_flt=float(ll_str)
        ul_flt=float(ul_str)
    gif=f.zoom_graph(eq,ll_flt,ul_flt)
    gif_str=base64.b64decode(gif)
    entry2=PixelString(session_id=session_id,pix_str=gif_str)
    db.session.add(entry2)
    db.session.commit()
    return {'show_word':'boo'}

@app.route('/zoom_graph2')
def zoom_graph2():
    print('reached zoom_graph2')
    session_id=id(session)
    entry=db.session.query(PixelString).filter(PixelString.session_id==session_id)
    for e in entry:
        gif_str=e.pix_str
    gif_bytes=io.BytesIO(gif_str)
    for e in entry:
        db.session.delete(e)
        db.session.commit()
    return send_file(gif_bytes,mimetype='image/gif')

@app.route('/stem_graph',methods=['POST'])
def stem_graph():
    session_id=id(session)
    entry=db.session.query(User).filter(User.session_id==session_id)
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
    for e in entry:
        new_entry=e
        #deletes previous step_list if there
        ayedee=e.id
    user=db.session.get(User,ayedee)
    query=user.steps2.select()
    steps=db.session.scalars(query)
    for step in steps:
        db.session.delete(step)
    db.session.commit()
    #^
    for step in step_list:
        s=StepList2(num_steps=step,parent=new_entry)
        db.session.add(s)
        db.session.commit()
    #x_range2 = f.x_range3(float(session['lower_limit']), float(session['upper_limit']), num_journeys)
    img=f.stem_graph(x_range2,step_list)
    img_str=base64.b64decode(img)
    entry2=PixelString(session_id=session_id,pix_str=img_str)
    db.session.add(entry2)
    db.session.commit()
    return {'some text':'other text'}
    
@app.route('/stem_graph2')
def stem_graph2():
    print('reached here,2')
    session_id=id(session)
    entry=db.session.query(PixelString).filter(PixelString.session_id==session_id)
    for e in entry:
        img_str=e.pix_str
    img_bytes=io.BytesIO(img_str)
    for e in entry:
        db.session.delete(e)
        db.session.commit()
    return send_file(img_bytes,mimetype='image/png')

@app.route('/steps', methods=['GET', 'POST'])
def steps():
    session_id=id(session)
    entry=db.session.query(User).filter(User.session_id==session_id)
    for e in entry:
        eq=e.equation
        ll_str=e.lower_limit
        ul_str=e.upper_limit
        ll_flt=float(ll_str)
        ul_flt=float(ul_str)
        query=e.steps2.select()
        steps=db.session.scalars(query)
        step_list=[]
        for step in steps:
            s1=step.num_steps
            step_list.append(s1)
    x_range2 = f.x_range3(ll_flt, ul_flt, num_journeys)
    y_range = f.y_range(eq, x_range2)
    img=f.coloured_graph(x_range2,y_range,step_list)
    img_str=base64.b64decode(img)
    entry2=PixelString(session_id=session_id,pix_str=img_str)
    db.session.add(entry2)
    db.session.commit()
    return {'some text':'other text'}

@app.route('/coloured_graph')
def coloured_graph():
    session_id=id(session)
    entry=db.session.query(PixelString).filter(PixelString.session_id==session_id)
    for e in entry:
        img_str=e.pix_str
    img_bytes=io.BytesIO(img_str)
    for e in entry:
        db.session.delete(e)
        db.session.commit()
    img_bytes=io.BytesIO(img_str)
    return send_file(img_bytes,mimetype='image/png')

@app.route('/ran_tan',methods=['GET', 'POST'])
def ran_tan():
    #collect entry from database
    session_id=id(session)
    entry=db.session.query(User).filter(User.session_id==session_id)
    for e in entry:
        eq=e.equation
        ll_str=e.lower_limit
        ul_str=e.upper_limit
        ll_flt=float(ll_str)
        ul_flt=float(ul_str)
        query=e.steps2.select()
        steps=db.session.scalars(query)
        step_list=[]
        for step in steps:
            s1=step.num_steps
            step_list.append(s1)
    x_range = f.x_range3(ll_flt, ul_flt, num_journeys)
    x_range2=x_range.tolist()
    x_list=[]
    tang_list=[]
    megalist_x=[]
    megalist_y=[]
    mask_starts=[]
    tang_starts2=[]
    f.tang(step_list,x_range2,tang_list,eq,megalist_x,megalist_y,tang_starts2,x_list,mask_starts)
    #add megalist to database
    for e in entry:
        new_entry=e
        #deletes previous mega_list if there
        ayedee=e.id
    user=db.session.get(User,ayedee)
    query=user.megalist.select()
    ml_entries=db.session.scalars(query)
    for ml_entry in ml_entries:
        db.session.delete(ml_entry)
    db.session.commit()
    #^
    for i in range(len(megalist_x)):
        x=megalist_x[i]
        y=megalist_y[i]
        if i < len(mask_starts):
            mask_start=mask_starts[i]
        else:
            mask_start=-1
            # add into code later that a mask_start with this value is ignored
        ml=MegaList(x=x,y=y,mask_start=mask_start,parent=new_entry)
        db.session.add(ml)
    db.session.commit()
    ran_x=x_list[0]
    position=tang_list[0]
    #session['ran_tan_position']=str(position)
    ran_tan_position=str(position)
    tan1_start=megalist_x[0]
    tan2_start=megalist_x[11]
    tan3_start=megalist_x[22]
    tan4_start=megalist_x[33]
    #session['ran_number_of_steps']=str(tang_starts2[-1])
    #session['ran_number_of_steps_int']=int(session['ran_number_of_steps'])
    #session['ran_mask_starts']=mask_starts
    if tang_starts2[-1]<8:
        error_mes='Sorry there are not enough steps in this journey to show the tangets. PLease try reloading'
    else:
        error_mes=''
    print('tang starts 2 is ',tang_starts2)
    # for updating database
    entry2=db.session.query(PixelString3).filter(PixelString3.session_id==session_id)
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
        user=PixelString3(ran_x=ran_x,ran_tan_position=position,ran_num_steps=tang_starts2[-1],tang_str='',start_str='',end_str='',session_id=session_id)
        db.session.add(user)
        db.session.commit()
    #deleting old entries
    now=datetime.now(timezone.utc)
    fmt='%Y-%m-%d %H:%M:%S.%f'
    now_str=now.strftime(fmt)
    now_new=datetime.strptime(now_str,fmt)
    query=sa.select(PixelString3)
    entries=db.session.scalars(query)
    for e in entries:
        ts=e.timestamp
        u_id=e.id
        ts_str=str(ts)
        ts_con=datetime.strptime(ts_str,fmt)
        diff=now_new-ts_con
        if diff>timedelta(days=5):
            entry2=db.session.get(PixelString3,u_id)
            db.session.delete(entry2)
            db.session.commit()
    return render_template('ran_tan.html',step_list=step_list,ran_x=ran_x,
    position=position,tan1_start=tan1_start,tan2_start=tan2_start,
    tan3_start=tan3_start,tan4_start=tan4_start,tang_starts2=tang_starts2[-1],equation=eq,error_mes=error_mes,session_id=session_id)



@app.route('/tang_graph',methods=['POST'])
def tang_graph():
    session_id=id(session)
    entry=db.session.query(User).filter(User.session_id==session_id)
    for e in entry:
        eq=e.equation
        query=e.megalist.select()
        values=db.session.scalars(query)
        megalist_x=[]
        megalist_y=[]
        mask_starts=[]
        for value in values:
            x=value.x
            y=value.y
            if value.mask_start == -1:
                computer='distract'
            else:
                mask_start=value.mask_start
                mask_starts.append(mask_start)
            megalist_x.append(x)
            megalist_y.append(y)
    gif=f.tang_graph(megalist_x,megalist_y,eq,mask_starts)
    gif_str=base64.b64decode(gif)
    # for updating database
    entry=db.session.query(PixelString3).filter(PixelString3.session_id==session_id)
    for e in entry:
        ayedee=e.id
        ran_tan_position=e.ran_tan_position
        ran_num_steps=e.ran_num_steps
    update=db.session.get(PixelString3,ayedee)
    update.tang_str=gif_str
    db.session.commit()
    #^
    print('reached tang_graph')
    str1=str(ran_tan_position)
    str2=str(ran_num_steps)
    my_str='Starting from position '+str1+' of '+str2
    return {'key':my_str}

@app.route('/tang_graph2')
def tang_graph2():
    session_id=id(session)
    entry=db.session.query(PixelString3).filter(PixelString3.session_id==session_id)
    for e in entry:
        gif_str=e.tang_str
    gif_bytes=io.BytesIO(gif_str)
    return send_file(gif_bytes,mimetype='image/gif')

@app.route('/tang_graph_start',methods=['POST'])
def tang_graph_start():
    session_id=id(session)
    entry=db.session.query(User).filter(User.session_id==session_id)
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
    session_id=id(session)
    entry2=db.session.query(PixelString3).filter(PixelString3.session_id==session_id)
    for e in entry2:
        ran_x=e.ran_x
        ran_num_steps=e.ran_num_steps
        ayedee=e.id
    gif=f.draw_tangents_start(eq,ran_x,0,0,0,megalist_x2,megalist_y2,ran_num_steps,[],x_range2,y_range,error)
    gif_str=base64.b64decode(gif)
    update=db.session.get(PixelString3,ayedee)
    update.start_str=gif_str
    db.session.commit()
    my_str=''
    return {'key':my_str}
    

@app.route('/tang_graph_start2')
def tang_graph_start2():
    session_id=id(session)
    entry=db.session.query(PixelString3).filter(PixelString3.session_id==session_id)
    for e in entry:
        gif_str=e.start_str
    gif_bytes=io.BytesIO(gif_str)
    return send_file(gif_bytes,mimetype='image/gif')

@app.route('/tang_graph_end',methods=['POST'])
def tang_graph_end():
    #x_range = f.x_range3(float(session['lower_limit']), float(session['upper_limit']), num_journeys)
    #x_range2=x_range.tolist()
    session_id=id(session)
    entry=db.session.query(User).filter(User.session_id==session_id)
    for e in entry:
        eq=e.equation
    entry2=db.session.query(PixelString3).filter(PixelString3.session_id==session_id)
    for e in entry2:
        ran_x=e.ran_x
        ran_num_steps=e.ran_num_steps
        ayedee=e.id
    gif=f.draw_tangents_end(eq,ran_x,0,0,0,[],[],ran_num_steps,[])
    gif_str=base64.b64decode(gif)
    update=db.session.get(PixelString3,ayedee)
    update.end_str=gif_str
    db.session.commit()
    my_str=''
    return {'key':my_str}

@app.route('/tang_graph_end2')
def tang_graph_end2():
    session_id=id(session)
    entry=db.session.query(PixelString3).filter(PixelString3.session_id==session_id)
    for e in entry:
        gif_str=e.end_str
    gif_bytes=io.BytesIO(gif_str)
    return send_file(gif_bytes,mimetype='image/gif')

@app.route('/one_d_graph')
def one_d_graph():
    session_id=id(session)
    entry=db.session.query(User).filter(User.session_id==session_id)
    for e in entry:
        ll_str=e.lower_limit
        ul_str=e.upper_limit
        ll_flt=float(ll_str)
        ul_flt=float(ul_str)
    entry2=db.session.query(PixelString3).filter(PixelString3.session_id==session_id)
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




