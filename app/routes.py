from app import app
from flask import render_template, redirect, url_for, send_file,request,session,flash
from app.forms import EnterEquation
#from app.models import UserInput
from app.maths import Functions as f
import io,base64
import matplotlib
from werkzeug.middleware.profiler import ProfilerMiddleware
from flask_session import Session
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
    #form.equation.data='x^2 - x + 1'
    session['session_id']=id(session)
    if form.validate_on_submit():
        session['equation']=form.equation.data
        session['lower_limit']=form.lower_limit.data
        session['upper_limit']=form.upper_limit.data
        diff = float(session['upper_limit'])-float(session['lower_limit'])
        ll=float(session['lower_limit'])
        ul=float(session['upper_limit'])
        if float(session['lower_limit'])>float(session['upper_limit']):
            flash('the upper limit is too low') 
            return redirect(url_for('index'))
        elif ll<-15 or ul>15:
            return redirect(url_for('confirm'))
        else:
            return redirect(url_for('results'))
    return render_template('index.html', form=form,session_id=session['session_id'])
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
    session['suggested']='x^6 - 120*x^2 + 48*x + 389'
    return {'boo':'foo'}

@app.route('/suggestion_eq2',methods=['GET','POST'])
def suggestion_eq2():
    session['suggested']='5*x^3 + 3^x - 5^x + 0.15'
    return {'boo':'foo'}
    
@app.route('/suggestion_eq3',methods=['GET','POST'])
def suggestion_eq3():
    session['suggested']='x^3 - x^2 + 0.25'
    return {'boo':'foo'}

@app.route('/suggestion1',methods=['GET','POST'])
def suggestion1():
    form=EnterEquation()
    form.equation.data=session['suggested']
    if form.validate_on_submit():
        session['equation']=form.equation.data
        session['lower_limit']=form.lower_limit.data
        session['upper_limit']=form.upper_limit.data
        ll=float(session['lower_limit'])
        ul=float(session['upper_limit'])
        if float(session['lower_limit'])>float(session['upper_limit']):
            flash('the upper limit is too low') 
            return redirect(url_for('suggestion1'))
        elif ll<-15 or ul>15:
            return redirect(url_for('confirm'))
        else:
            return redirect(url_for('results'))
    return render_template('index.html', form=form,session_id=session['session_id'])

@app.route('/results', methods=['GET', 'POST'])
def results():
    try:
        y_test=f.y_range(session['equation'],[1,2])
        equation = session['equation']
        lower_limit = session['lower_limit']
        upper_limit = session['upper_limit']
        #traceback.print_stack()
        return render_template('results.html',session_id=session['session_id'])
    except:
        flash("something's not right. Was the equation typed correctly?")
        return redirect(url_for('index'))

@app.route('/graph')
def graph():
    num_journeys2=num_journeys *2
    x_range2 = f.x_range3(float(session['lower_limit']), float(session['upper_limit']), num_journeys2)
    y_range = f.y_range(session['equation'], x_range2)
    fig = f.graph(x_range2, y_range,session['equation'])
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
    equation=session['equation']
    lower_limit=float(session['lower_limit'])
    upper_limit=float(session['upper_limit'])
    gif=f.zoom_graph(equation,lower_limit,upper_limit)
    gif_str=base64.b64decode(gif)
    session['zoom_graph']=gif_str
    return {'show_word':'boo'}

@app.route('/zoom_graph2')
def zoom_graph2():
    print('reached zoom_graph2')
    gif_bytes=io.BytesIO(session['zoom_graph'])
    return send_file(gif_bytes,mimetype='image/gif')

@app.route('/stem_graph',methods=['POST'])
def stem_graph():
    x_range2 = f.x_range3(float(session['lower_limit']), float(session['upper_limit']), num_journeys)
    y_range = f.y_range(session['equation'], x_range2)
    step=0
    step_list=[]
    print('reached here,1')
    for x in x_range2:
        f.newton_function(x,step,session['equation'],step_list)
    session['step_list']=step_list
    #x_range2 = f.x_range3(float(session['lower_limit']), float(session['upper_limit']), num_journeys)
    img=f.stem_graph(x_range2,session['step_list'])
    img_str=base64.b64decode(img)
    session['stem_graph']=img_str
    return {'some text':'other text'}
    

@app.route('/stem_graph2')
def stem_graph2():
    print('reached here,2')
    img_bytes=io.BytesIO(session['stem_graph'])
    return send_file(img_bytes,mimetype='image/png')

@app.route('/steps', methods=['GET', 'POST'])
def steps():
    x_range2 = f.x_range3(float(session['lower_limit']), float(session['upper_limit']), num_journeys)
    y_range = f.y_range(session['equation'], x_range2)
    img=f.coloured_graph(x_range2,y_range,session['step_list'])
    img_str=base64.b64decode(img)
    session['coloured_graph']=img_str
    return {'some text':'other text'}

@app.route('/coloured_graph')
def coloured_graph():
    img_bytes=io.BytesIO(session['coloured_graph'])
    return send_file(img_bytes,mimetype='image/png')

@app.route('/ran_tan',methods=['GET', 'POST'])
def ran_tan():
    x_range = f.x_range3(float(session['lower_limit']), float(session['upper_limit']), num_journeys)
    x_range2=x_range.tolist()
    x_list=[]
    tang_list=[]
    megalist_x=[]
    megalist_y=[]
    mask_starts=[]
    tang_starts2=[]
    f.tang(session['step_list'],x_range2,tang_list,session['equation'],megalist_x,megalist_y,tang_starts2,x_list,mask_starts)
    session['megalist_x']=megalist_x
    session['megalist_y']=megalist_y
    ran_x=x_list[0]
    session['ran_x']=ran_x
    position=tang_list[0]
    session['ran_tan_position']=str(position)
    tan1_start=megalist_x[0][0]
    tan2_start=megalist_x[1][0]
    tan3_start=megalist_x[2][0]
    tan4_start=megalist_x[3][0]
    session['ran_number_of_steps']=str(tang_starts2[-1])
    session['ran_number_of_steps_int']=int(session['ran_number_of_steps'])
    session['ran_mask_starts']=mask_starts
    if tang_starts2[-1]<8:
        error_mes='Sorry there are not enough steps in this journey to show the tangets. PLease try reloading'
    else:
        error_mes=''
    print('tang starts 2 is ',tang_starts2)
    return render_template('ran_tan.html',step_list=session['step_list'],ran_x=ran_x,
    position=position,tan1_start=tan1_start,tan2_start=tan2_start,
    tan3_start=tan3_start,tan4_start=tan4_start,tang_starts2=tang_starts2[-1],equation=session['equation'],error_mes=error_mes,session_id=session['session_id'])



@app.route('/tang_graph',methods=['POST'])
def tang_graph():
    gif=f.tang_graph(session['megalist_x'],session['megalist_y'],session['equation'],session['ran_mask_starts'])
    gif_str=base64.b64decode(gif)
    session['tang_graph']=gif_str
    print('reached tang_graph')
    str1=session['ran_tan_position']
    str2=session['ran_number_of_steps']
    my_str='Starting from position '+str1+' of '+str2
    return {'key':my_str}

@app.route('/tang_graph2')
def tang_graph2():
    gif_bytes=io.BytesIO(session['tang_graph'])
    return send_file(gif_bytes,mimetype='image/gif')

@app.route('/tang_graph_start',methods=['POST'])
def tang_graph_start():
    x_range= f.x_range3(float(session['lower_limit']), float(session['upper_limit']), num_journeys)
    x_range2=x_range.tolist()
    x_range3=f.x_range4(float(session['lower_limit']), float(session['upper_limit']))
    y_range = f.y_range(session['equation'], x_range2)
    megalist_x2=[]
    megalist_y2=[]
    error=''
    gif=f.draw_tangents_start(session['equation'],session['ran_x'],0,0,0,megalist_x2,megalist_y2,session['ran_number_of_steps_int'],[],x_range2,y_range,error)
    gif_str=base64.b64decode(gif)
    session['tang_graph_start']=gif_str
    my_str=''
    return {'key':my_str}
    

@app.route('/tang_graph_start2')
def tang_graph_start2():
    gif_bytes=io.BytesIO(session['tang_graph_start'])
    return send_file(gif_bytes,mimetype='image/gif')

@app.route('/tang_graph_end',methods=['POST'])
def tang_graph_end():
    #x_range = f.x_range3(float(session['lower_limit']), float(session['upper_limit']), num_journeys)
    #x_range2=x_range.tolist()
    gif=f.draw_tangents_end(session['equation'],session['ran_x'],0,0,0,[],[],session['ran_number_of_steps_int'],[])
    gif_str=base64.b64decode(gif)
    session['tang_graph_end']=gif_str
    my_str=''
    return {'key':my_str}

@app.route('/tang_graph_end2')
def tang_graph_end2():
    gif_bytes=io.BytesIO(session['tang_graph_end'])
    return send_file(gif_bytes,mimetype='image/gif')

@app.route('/one_d_graph')
def one_d_graph():
    fig=f.one_d_graph(float(session['lower_limit']),float(session['upper_limit']),round(session['ran_x'],3))
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




