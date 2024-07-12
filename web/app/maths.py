from __future__ import division
import numpy as np
import numpy.ma as ma
import matplotlib
matplotlib.use('Agg') #gets rid of the user warning and inability to use plt.close(fig)
#from matplotlib import pyplot as plt
from matplotlib.figure import Figure
import matplotlib.animation as animation
from pyparsing import (Literal, CaselessLiteral, Word, Combine, Group, Optional,
                       ZeroOrMore, Forward, nums, alphas, oneOf)
import base64,requests,tempfile,os,io,random,itertools,operator,math
from flask import session
from app.models import User,MegaList,PixelString,PixelString3,StepList2,UserPreset
import sqlalchemy as sa
from app import db
from datetime import date,datetime,timedelta,timezone
#from app.config import VOLUME_PATH
from pathlib import Path
from time import sleep


class Functions():
    def unlock(num):
        if num==1:
            return True
    def x_range3(a, b, c):
        x_array=np.linspace(a, b, c)
        return np.round(x_array,8)
    def x_range4(a,b):
        x_array=np.arange(a,b,0.02)
        return np.round(x_array,8)
    def find_mean2(a, b):
        mean = (a + b) / 2
        return mean
    def thinner(x_range):
        my_range=list(range(len(x_range)))
        for i in reversed(my_range):
            if i==0 or i==list(reversed(my_range))[0]:
                n=1
            elif i % 2 != 0 or n<5:
                x_range.remove(x_range[i])
                n+=1
            else:
                n=1
        return x_range
    def y_range(equation, x_range):
        nsp=NumericStringParser()
        old_equation = equation
        y_range_string = []
        y_range_int = []
        for x in x_range:
            new_equation = old_equation.replace('x',str(x))
            y_range_string.append(new_equation)
        for y_string in y_range_string:
            y_int = nsp.eval(y_string)
            y_range_int.append(y_int)
        return y_range_int 
    def y_single(equation,x):
        nsp=NumericStringParser()
        new_equation = equation.replace('x',str(x))
        y_int = nsp.eval(new_equation)
        return y_int
    def graph(x, y,equation):
        fig2 = Figure()
        ax2 = fig2.subplots()
        """ax1.spines['left'].set_position('zero')
        ax1.spines['right'].set_color('none')
        ax1.yaxis.tick_left()"""
        min_y=min(y)
        max_y=max(y)
        min_x=min(x)
        max_x=max(x)
        if min_y>0 or max_y<0:
            ax2.spines.bottom.set_bounds(min_x,max_x)
        else:
            ax2.spines['bottom'].set_position('zero')
            #ax2.xaxis.set_label_position['bottom']
        ax2.spines['top'].set_color('none')
        ax2.xaxis.tick_bottom()
        ax2.plot(x, y, c='b', label=equation)
        ax2.legend(loc='upper left')
        return fig2
    def deriv_graph(x, y):
        fig4 = Figure()
        ax4 = fig4.subplots()
        """ax1.spines['left'].set_position('zero')
        ax1.spines['right'].set_color('none')
        ax1.yaxis.tick_left()"""
        ax4.spines['bottom'].set_position('zero')
        ax4.spines['top'].set_color('none')
        ax4.xaxis.tick_bottom()
        ax4.plot(x, y, c='b', label="equation")
        ax4.legend(loc='upper left')
        return fig4
    def stem_graph(x,y):
        fig1 = Figure()
        ax1=fig1.subplots()
        ax1.stem(x,y,linefmt='green',markerfmt='D',bottom=0)
        ax1.set_xlabel('x starting point')
        ax1.set_ylabel('number of steps to reach root')
        text='\n'.join(['if steps=-5, x went out of range',
        'if steps=-10, there were too many steps'])
        props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
        ax1.text(0.05, 0.95, text, transform=ax1.transAxes, fontsize=9,
        verticalalignment='top', bbox=props)#
        #session_id=str(id(session))
        #file_str='app//temp//stem_graph'+session_id+'.png'
        #fig1.savefig(file_str)
        #with open(file_str, "rb") as image_file:
        #    data = base64.b64encode(image_file.read()).decode()
        #print('data format in maths.py is ',data)
        #os.remove(file_str)
        session_id=str(id(session))
        file_name='stem_graph'+session_id+'.png'
        #file_path = os.path.join(VOLUME_PATH, file_name)
        file_path=os.path.join('app','temp',file_name)
        fig1.savefig(file_path)
        return file_path
    def tsg_error(x_range2,y_range2,error):
        file_str='app//static//error_8_steps.png'
        with open(file_str, "rb") as image_file:
            data = base64.b64encode(image_file.read()).decode()
        return data
    def zoom_graph(equation,lower_limit,upper_limit):
        x_range=np.arange(-20,20,0.05)
        y_range=[Functions.y_single(equation,x) for x in x_range]
        input_range=np.arange(lower_limit,upper_limit,0.1)
        y_input_range=[Functions.y_single(equation,x) for x in input_range]
        #find a root in equation
        y_range2=[]
        for y in y_range:
            new_y=abs(y)
            y_range2.append(new_y)
        root=min(y_range2)
        index=y_range2.index(root)
        x_range3=np.arange(-95,-85,0.05)
        y_range3=[]
        for i in range(len(x_range3)):
            y_range3.append(0)
        fig3 = Figure()
        ax3 = fig3.subplots()
        # setting x axis to always show
        ax3.spines['bottom'].set_position('zero')
        ax3.spines['top'].set_color('none')
        ax3.xaxis.tick_bottom()
        #
        min_x=min(x_range)
        max_x=max(x_range)
        min_y=min(y_range)
        max_y=max(y_range)
        ax3.set_xlim(min_x,max_x)
        ax3.set_ylim(min_y,max_y)
        label1=equation
        ax3.plot(x_range,y_range,c='b',label=label1)
        ax3.plot(input_range,y_input_range,c='purple',label='section analysed')
        ax3.plot(x_range3,y_range3,c='black')
        ax3.legend(loc='upper left')
        #
        #for zooming in
        frames=250
        #x axis
        x_min_casc_min1=min(x_range)
        x_min_casc_max1=root-4
        frames1=62
        x_min_casc1=np.linspace(x_min_casc_min1,x_min_casc_max1,frames1)
        x_min_casc_min2=x_min_casc_max1
        x_min_casc_max2=root-0.5
        frames2=63
        moving_frames=frames1+frames2
        x_min_casc2=np.linspace(x_min_casc_min2,x_min_casc_max2,frames2)
        x_max_casc_min1=max(x_range)
        x_max_casc_max1=root+4
        x_max_casc1=np.linspace(x_max_casc_min1,x_max_casc_max1,frames1)
        x_max_casc_min2=x_max_casc_max1
        x_max_casc_max2=root+0.5
        x_max_casc2=np.linspace(x_max_casc_min2,x_max_casc_max2,frames2)
        #
        #
        y_min_casc_min1=min(y_range)
        new_index=index-80
        new_index2=index+80
        current_range=y_range[new_index:new_index2]
        y_min_casc_max1=min(current_range)
        y_min_casc1=np.linspace(y_min_casc_min1,y_min_casc_max1,frames1)
        y_min_casc_min2=y_min_casc_max1
        new_index=index-10
        new_index2=index+10
        current_range=y_range[new_index:new_index2]
        y_min_casc_max2=min(current_range)
        y_min_casc2=np.linspace(y_min_casc_min2,y_min_casc_max2,frames2)
        #
        y_max_casc_min1=max(y_range)
        new_index=index-80
        new_index2=index+80
        current_range=y_range[new_index:new_index2]
        y_max_casc_max1=max(current_range)
        y_max_casc1=np.linspace(y_max_casc_min1,y_max_casc_max1,frames1)
        y_max_casc_min2=y_max_casc_max1
        new_index=index-10
        new_index2=index+10
        current_range=y_range[new_index:new_index2]
        y_max_casc_max2=max(current_range)
        y_max_casc2=np.linspace(y_max_casc_min2,y_max_casc_max2,frames2)
        #concatenate
        x_min_casc=np.concatenate([x_min_casc1,x_min_casc2])
        x_max_casc=np.concatenate([x_max_casc1,x_max_casc2])
        y_min_casc=np.concatenate([y_min_casc1,y_min_casc2])
        y_max_casc=np.concatenate([y_max_casc1,y_max_casc2])
        #
        moving=ax3.plot(x_range3,y_range3,c='black',label='hi there')[0]
        #

        def update(frame):
            #
            if frame<moving_frames:
                if frame%4==0:
                    min_x=x_min_casc[frame]
                    max_x=x_max_casc[frame]
                    min_y=y_min_casc[frame]
                    max_y=y_max_casc[frame]

                    diff_x=(max_x-min_x)/10
                    diff_y=(max_y-min_y)/10
                    min_x-=diff_x
                    max_x+=diff_x
                    min_y-=diff_y
                    max_y+=diff_y

                    ax3.set_xlim(min_x,max_x)
                    ax3.set_ylim(min_y,max_y)
                #
                    moving.set_xdata(x_range[:frame])
                    moving.set_ydata(y_range[:frame])
            return(moving)
        ani=animation.FuncAnimation(fig=fig3,func=update,frames=frames,interval=3,repeat=False)
        writer=animation.PillowWriter(fps=25,metadata=dict(artist='Me'),bitrate=1800)
        session_id=str(id(session))
        file_name='zoom_graph'+session_id+'.png'
        file_path=os.path.join('app','temp',file_name)
        ani.save(file_path,writer=writer)
        return file_path
    
    def tang_graph(megalist_x,megalist_y,equation,mask_starts):
        #tang_range_total = megalist_x[0] + megalist_x[1] + megalist_x[2] + megalist_x[3]
        x_min = min(megalist_x)
        x_max = max(megalist_x)
        R2 = x_max - x_min
        number_of_steps2 = 200
        F2 = number_of_steps2 / R2
        x_min1 = x_min - (R2 / 2)
        x_max1 = x_max + (R2 / 2)
        x_min2 = math.floor(x_min1 * F2)
        x_max2 = math.ceil((x_max1 * F2) + 1)
        x_range3 = [x / F2 for x in range(x_min2, x_max2)]
        y_range4 = [Functions.y_single(equation,x) for x in x_range3]
        # making sure the y-range in graph  is a bit larger than just the range of the tangent lines
        y_max = max(y_range4) + ((max(y_range4) - min(y_range4))/10)
        y_min = min(y_range4) - ((max(y_range4) - min(y_range4))/10)
        label1=equation
        fig3 = Figure()
        ax3 = fig3.subplots()
        # setting y axis to always show at left and within data range
        """ax3 = plt.gca()
        if y_min>0:
            ax1.set_ylim([0,y_max])
        elif y_max<0:
            ax1.set_ylim([y_min,0])
        else:
            ax1.set_ylim([y_min,y_max])"""
        #
        # setting x axis to always show
        ax3.spines['bottom'].set_position('zero')
        ax3.spines['top'].set_color('none')
        ax3.xaxis.tick_bottom()
        #
        ax3.plot(x_range3, y_range4, c='b', label=label1)
        
        #x_range=np.concatenate([megalist_x[0],megalist_x[1],megalist_x[2],megalist_x[3]])
        #y_range=np.concatenate([megalist_y[0],megalist_y[1],megalist_y[2],megalist_y[3]])
        ax3.plot(megalist_x[0],megalist_y[0],c='darkgreen',label='tangents')
        ax3.legend(loc='upper left')
        m_y_range=ma.array(megalist_y)
        m_y_range[mask_starts[0]]=ma.masked
        m_y_range[mask_starts[1]]=ma.masked
        m_y_range[mask_starts[2]]=ma.masked
        moving=ax3.plot(megalist_x,m_y_range,c='darkgreen',label=label1)[0]
        def update(frame):
            moving.set_xdata(megalist_x[:frame])
            moving.set_ydata(m_y_range[:frame])
            return(moving)
        ani=animation.FuncAnimation(fig=fig3,func=update,frames=len(megalist_x),interval=4000,repeat=False)
        writer=animation.PillowWriter(fps=15,metadata=dict(artist='Me'),bitrate=1800)
        session_id=str(id(session))
        file_name='ran_tan'+session_id+'.gif'
        file_path=os.path.join('app','temp',file_name)
        ani.save(file_path,writer=writer)
        return file_path
    def tang_graph_start(megalist_x2,megalist_y2,tang_starts2,equation,mask_starts):
        try:
            tang_range_total = megalist_x2[0] + megalist_x2[1] + megalist_x2[2] + megalist_x2[3] + megalist_x2[4]# + megalist_x2[5] + megalist_x2[6] + megalist_x2[7]
        except IndexError:
            file_str='app//static//error_8_steps.jpg'
            with open(file_str, "rb") as image_file:
                data = base64.b64encode(image_file.read()).decode()
            return data
        #sets main function, makes sure it's always displayed
        x_min = min(tang_range_total)
        x_max = max(tang_range_total)
        R2 = x_max - x_min
        x_min2=x_min -(4*R2)
        x_max2=x_max + (4*R2)
        x_range10=np.arange(x_min2,x_min,0.1)
        x_range11=np.arange(x_min,x_max,0.01)
        x_range12=np.arange(x_max,x_max2,0.1)
        my_array=np.append(x_range10,x_range11)
        x_range3=np.append(my_array,x_range12)
        try:
            y_range4 = [Functions.y_single(equation,x) for x in x_range3]
        except:
            sleep(5)
            try:
                y_range4 = [Functions.y_single(equation,x) for x in x_range3]
            except:
                sleep(15)
                y_range4 = [Functions.y_single(equation,x) for x in x_range3]
        label1=equation
        fig3 = Figure()
        ax3 = fig3.subplots()
        # setting x axis to always show
        ax3.spines['bottom'].set_position('zero')
        ax3.spines['top'].set_color('none')
        ax3.xaxis.tick_bottom()
        ax3.plot(x_range3, y_range4, c='b', label=equation)
        #hack to freeze gif at end
        freezer_x=[]
        freezer_y=[]
        added_x=megalist_x2[4][-1]
        added_y=megalist_y2[4][-1]
        for i in range(30):
            freezer_x.append(added_x)
            freezer_y.append(added_y)
        x_range=np.concatenate([megalist_x2[0],megalist_x2[1],megalist_x2[2],megalist_x2[3],megalist_x2[4],freezer_x])
        y_range=np.concatenate([megalist_y2[0],megalist_y2[1],megalist_y2[2],megalist_y2[3],megalist_y2[4],freezer_y])
        #initial axes range
        min_x=min(x_range[:33])
        max_x=max(x_range[:33])
        min_y=min(y_range[:33])
        max_y=max(y_range[:33])
        diff_x=(max_x-min_x)/4
        diff_y=(max_y-min_y)/4
        min_x-=diff_x
        max_x+=diff_x
        min_y-=diff_y
        max_y+=diff_y
        ax3.set_xlim(min_x,max_x)
        ax3.set_ylim(min_y,max_y)
        #hack to show label
        ax3.plot(x_range[0],y_range[0],c='darkgreen',label='tangents')
        ax3.legend(loc='upper left')
        #masked starts
        m_y_range=ma.array(y_range)
        m_y_range[mask_starts[0]]=ma.masked
        m_y_range[mask_starts[1]]=ma.masked
        m_y_range[mask_starts[2]]=ma.masked
        m_y_range[mask_starts[3]]=ma.masked
        #m_y_range[mask_starts[4]]=ma.masked
        #m_y_range[mask_starts[5]]=ma.masked
        #m_y_range[mask_starts[6]]=ma.masked
        moving=ax3.plot(x_range,m_y_range,c='darkgreen',label=label1)[0]
        def update(frame):
            diff_div=6
            if frame==86:
                min_x=min(x_range[54:106])
                max_x=max(x_range[54:106])
                min_y=min(y_range[54:106])
                max_y=max(y_range[54:106])
                diff_div=0.25
                diff_x=(max_x-min_x)*diff_div
                diff_y=(max_y-min_y)*diff_div
                min_x-=diff_x
                max_x+=diff_x
                min_y-=diff_y
                max_y+=diff_y
                ax3.set_xlim(min_x,max_x)
                ax3.set_ylim(min_y,max_y)
            elif 86>frame>1:
                if frame%2==0:
                    min_x_list=[]
                    max_x_list=[]
                    min_y_list=[]
                    max_y_list=[]
                    smoother_num=25
                    if frame<32:
                        lower_limit=0
                        upper_limit=frame+20
                        smoother_num=math.floor(upper_limit/2)
                    else:
                        upper_limit=frame+20
                        lower_limit=frame-32
                    #print('frame: ',frame,'\nupper lim: ',upper_limit,'\nlower lim: ',lower_limit,
                    #'\nsmoother num: ',smoother_num)
                    x_axis_limits=list(x_range[lower_limit:upper_limit])
                    y_axis_limits=list(y_range[lower_limit:upper_limit])
                    for i in range(smoother_num):
                        min_x=min(x_axis_limits)
                        x_axis_limits.remove(min_x)
                        min_x_list.append(min_x)
                    for i in range(smoother_num):
                        max_x=max(x_axis_limits)
                        x_axis_limits.remove(max_x)
                        max_x_list.append(max_x)
                    for i in range(smoother_num):
                        min_y=min(y_axis_limits)
                        y_axis_limits.remove(min_y)
                        min_y_list.append(min_y)
                    for i in range(smoother_num):
                        max_y=max(y_axis_limits)
                        y_axis_limits.remove(max_y)
                        max_y_list.append(max_y)
                    #
                    min_x=np.mean(min_x_list)
                    max_x=np.mean(max_x_list)
                    min_y=np.mean(min_y_list)
                    max_y=np.mean(max_y_list)
                    if frame==77:
                        diff_div=4.5
                    if frame==78:
                        diff_div=3
                    if frame==79:
                        diff_div=2.25
                    if frame==80:
                        diff_div=1.5
                    if frame==81:
                        diff_div=1.125
                    if frame==82:
                        diff_div=0.75
                    if frame==83:
                        diff_div=0.5625
                    if frame==84:
                        diff_div=0.375
                    if frame==85:
                        diff_div=0.333
                    diff_x=diff_div*(max_x-min_x)
                    diff_y=diff_div*(max_y-min_y)
                    min_x-=diff_x
                    max_x+=diff_x
                    min_y-=diff_y
                    max_y+=diff_y
                    ax3.set_xlim(min_x,max_x)
                    ax3.set_ylim(min_y,max_y)
            moving.set_xdata(x_range[:frame])
            moving.set_ydata(m_y_range[:frame])
            return(moving)
        ani=animation.FuncAnimation(fig=fig3,func=update,frames=len(x_range),interval=8000,repeat=False)
        writer=animation.PillowWriter(fps=15,metadata=dict(artist='Me'),bitrate=1800)
        session_id=str(id(session))
        file_name='tang_graph_start'+session_id+'.gif'
        file_path=os.path.join('app','temp',file_name)
        ani.save(file_path,writer=writer)
        dir_path_linux=Path('app').joinpath('temp')
        return file_path
    def tang_graph_end(megalist_x3,megalist_y3,tang_starts2,equation,mask_starts):
        tang_range_total = megalist_x3[0] + megalist_x3[1] + megalist_x3[2] + megalist_x3[3] + megalist_x3[4]
        #sets main function, makes sure it's always displayed
        x_min = min(tang_range_total)
        x_max = max(tang_range_total)
        R2 = abs(x_max - x_min)
        x_min2 = x_min - (4*R2)
        x_max2= x_max + (4*R2)
        x_range10=np.arange(x_min2,x_min,0.1)
        x_range11=np.arange(x_min,x_max,0.01)
        x_range12=np.arange(x_max,x_max2,0.1)
        my_array=np.append(x_range10,x_range11)
        x_range3=np.append(my_array,x_range12)
        y_range4 = [Functions.y_single(equation,x) for x in x_range3]
        label1=equation
        fig3 = Figure()
        ax3 = fig3.subplots()
        # setting x axis to always show
        ax3.spines['bottom'].set_position('zero')
        ax3.spines['top'].set_color('none')
        ax3.xaxis.tick_bottom()
        ax3.plot(x_range3, y_range4, c='b', label=equation)
                #hack to freeze gif at end
        freezer_x=[]
        freezer_y=[]
        added_x=megalist_x3[-1][-1]
        added_y=megalist_y3[-1][-1]
        for i in range(30):
            freezer_x.append(added_x)
            freezer_y.append(added_y)
        x_range=np.concatenate([megalist_x3[0],megalist_x3[1],megalist_x3[2],megalist_x3[3],megalist_x3[4],freezer_x])
        y_range=np.concatenate([megalist_y3[0],megalist_y3[1],megalist_y3[2],megalist_y3[3],megalist_y3[4],freezer_y])
        #initial axes range
        min_x=min(x_range[:33])
        max_x=max(x_range[:33])
        min_y=min(y_range[:33])
        max_y=max(y_range[:33])
        diff_x=(max_x-min_x)/4
        diff_y=(max_y-min_y)/4
        min_x-=diff_x
        max_x+=diff_x
        min_y-=diff_y
        max_y+=diff_y
        ax3.set_xlim(min_x,max_x)
        ax3.set_ylim(min_y,max_y)
        #hack to show label
        ax3.plot(x_range[0],y_range[0],c='darkgreen',label='tangents')
        ax3.legend(loc='upper left')
        #masked starts
        m_y_range=ma.array(y_range)
        m_y_range[mask_starts[0]]=ma.masked
        m_y_range[mask_starts[1]]=ma.masked
        m_y_range[mask_starts[2]]=ma.masked
        m_y_range[mask_starts[3]]=ma.masked
        moving=ax3.plot(x_range,m_y_range,c='darkgreen',label=label1)[0]
        def update(frame):
            diff_div=6
            if frame==86:
                min_x=min(x_range[54:106])
                max_x=max(x_range[54:106])
                min_y=min(y_range[54:106])
                max_y=max(y_range[54:106])
                diff_div=0.25
                diff_x=(max_x-min_x)*diff_div
                diff_y=(max_y-min_y)*diff_div
                min_x-=diff_x
                max_x+=diff_x
                min_y-=diff_y
                max_y+=diff_y
                ax3.set_xlim(min_x,max_x)
                ax3.set_ylim(min_y,max_y)
            elif 86>frame>1:
                if frame%2==0:
                    min_x_list=[]
                    max_x_list=[]
                    min_y_list=[]
                    max_y_list=[]
                    smoother_num=25
                    if frame<32:
                        lower_limit=0
                        upper_limit=frame+20
                        smoother_num=math.floor(upper_limit/2)
                    else:
                        lower_limit=frame-32
                        upper_limit=frame+20
                    x_axis_limits=list(x_range[lower_limit:upper_limit])
                    y_axis_limits=list(y_range[lower_limit:upper_limit])
                    for i in range(smoother_num):
                        min_x=min(x_axis_limits)
                        x_axis_limits.remove(min_x)
                        min_x_list.append(min_x)
                    for i in range(smoother_num):
                        max_x=max(x_axis_limits)
                        x_axis_limits.remove(max_x)
                        max_x_list.append(max_x)
                    for i in range(smoother_num):
                        min_y=min(y_axis_limits)
                        y_axis_limits.remove(min_y)
                        min_y_list.append(min_y)
                    for i in range(smoother_num):
                        max_y=max(y_axis_limits)
                        y_axis_limits.remove(max_y)
                        max_y_list.append(max_y)
                    #
                    min_x=np.mean(min_x_list)
                    max_x=np.mean(max_x_list)
                    min_y=np.mean(min_y_list)
                    max_y=np.mean(max_y_list)
                    if frame==77:
                        diff_div=4.5
                    if frame==78:
                        diff_div=3
                    if frame==79:
                        diff_div=2.25
                    if frame==80:
                        diff_div=1.5
                    if frame==81:
                        diff_div=1.125
                    if frame==82:
                        diff_div=0.75
                    if frame==83:
                        diff_div=0.5625
                    if frame==84:
                        diff_div=0.375
                    if frame==85:
                        diff_div=0.333
                    diff_x=diff_div*(max_x-min_x)
                    diff_y=diff_div*(max_y-min_y)
                    min_x-=diff_x
                    max_x+=diff_x
                    min_y-=diff_y
                    max_y+=diff_y
                    #print('frame(end): ',frame,'x-axes: ',min_x,' to ',max_x,'. y axis:',min_y,' to ',max_y)
                    ax3.set_xlim(min_x,max_x)
                    ax3.set_ylim(min_y,max_y)
            moving.set_xdata(x_range[:frame])
            moving.set_ydata(m_y_range[:frame])
            return(moving)
        ani=animation.FuncAnimation(fig=fig3,func=update,frames=len(x_range),interval=8000,repeat=False)
        writer=animation.PillowWriter(fps=15,metadata=dict(artist='Me'),bitrate=1800)
        session_id=str(id(session))
        file_name='tang_end_graph'+session_id+'.gif'
        file_path=os.path.join('app','temp',file_name)
        ani.save(file_path,writer=writer)
        dir_path_linux=Path('app').joinpath('temp')
        return file_path
    def one_d_graph(lower_limit,upper_limit,ran_x):
        fig6=Figure()
        fig6.set_size_inches(10,1)
        #fig6.set_dpi(50)
        ax6=fig6.subplots()
        my_list=[lower_limit,ran_x,upper_limit]
        ax6.spines['top'].set_visible(False)
        ax6.spines['right'].set_visible(False)
        ax6.spines['left'].set_visible(False)
        ax6.spines['bottom'].set_position('zero')
        ax6.spines['bottom'].set_alpha(0.2)
        ax6.get_yaxis().set_visible(False)
        #ax.set_xlabel('rna')
        ax6.scatter(my_list[1], 0, s=300, c='red')
        ax6.set_xticks(my_list, ['Lower limit','random x', 'Upper limit'])
        for i in range(3):
            ax6.annotate(my_list[i], (my_list[i], 0), textcoords="offset points",
                        xytext=(0, 0),  # distance from text to points (x,y)
                        ha='center')
        return fig6
    def coloured_graph(x,y,step_list):
        fig5 = Figure()
        ax5 = fig5.subplots()
        """ax1.spines['left'].set_position('zero')
        ax1.spines['right'].set_color('none')
        ax1.yaxis.tick_left()"""
        ax5.spines['bottom'].set_position('zero')
        ax5.spines['top'].set_color('none')
        ax5.xaxis.tick_bottom()
        ax5.scatter(x, y, c=step_list,cmap='Purples', label="number of steps")
        ax5.legend(loc='upper left')
        session_id=str(id(session))
        file_str='app//temp//coloured_graph'+session_id+'.png'
        fig5.savefig(file_str)
        return file_str
    def error_fig(x,y,error):
        fig = Figure()
        ax = fig.subplots()
        #ax2.spines['bottom'].set_position('zero')
        #ax2.spines['top'].set_color('none')
        #ax2.xaxis.tick_bottom()
        ax.plot(x, y, c='b', label="equation")
        ax.legend(loc='upper left')
        fig.savefig('useless_graph.png')
        with open('useless_graph.png', "rb") as image_file:
            data = base64.b64encode(image_file.read()).decode()
        os.remove('useless_graph.png')
        return data
    def deriv(x_range, equation):
        x_range_lower = []
        dx=abs(float(x_range[0]) - float(x_range[1]))
        for x in x_range:
            x=x - dx/2
            x_range_lower.append(x)
        x_range_higher=[]
        for x in x_range:
            x = x + dx /2
            x_range_higher.append(x)
        y_range_lower=Functions.y_range(equation,x_range_lower)
        y_range_higher=Functions.y_range(equation,x_range_higher)
        deriv_range=[(y_range_higher[i] - y_range_lower[i]) / dx
        for i in range(min(len(y_range_higher),len(y_range_higher)))]
        return deriv_range
    def range_enlarger(x_range):
        dx = abs(x_range[0] - x_range[1])
        length = abs(x_range[0] - x_range[-1])
        first_value = x_range[0] - length
        x_range1 = []
        x_range1.append(first_value)
        for i in range(1,19):
            x = first_value + i * dx
            x_range1.append(x)
        first_value = x_range[-1]
        x_range3 = []
        for i in range(1, 20):
            x = first_value + i * dx
            x_range3.append(x)
        return list(itertools.chain(x_range1, x_range, x_range3))
    def dx(x_range):
        difference_in_x=abs(x_range[0]-x_range[1])/8
        return difference_in_x
    def deriv_single(x,equation):
        nsp=NumericStringParser()
        #diff_x=Functions.dx(x_range)
        diff_x=0.02
        y1=nsp.eval(equation.replace('x',str(x-diff_x)))
        #y1=Functions.y_single(equation,x-diff_x)
        y2=nsp.eval(equation.replace('x',str(x)))
        #y2=Functions.y_single(equation,x)
        dy=y2-y1
        deriv=dy/diff_x
        return deriv
    def newton_function(x,step,equation,step_list):
        #nsp=NumericStringParser()
        tol = 1/100
        new_equation=equation.replace('x',str(x))
        y=NumericStringParser().eval(new_equation)
        deriv=Functions.deriv_single(x,equation)
        if abs(y) < tol:
            step_list.append(step)
            return step_list
        elif x < -10000 or x > 10000:
            step=-5
            step_list.append(step)
            return step_list
        elif step == 500:
            step=-10
            step_list.append(step)
            return step_list
        else:
            step += 1
            Functions.newton_function(x-y/deriv,step,equation,step_list)
    def tang(step_list,x_range,tang_list,equation,megalist_x,megalist_y,tang_starts2,x_list,mask_starts):
        maxi=max(step_list)
        weighted_list = step_list.copy()
        for pos in range(len(step_list)):
            if weighted_list[pos] < 5:
                weighted_list[pos] = 0
            elif weighted_list[pos] < (maxi / 4):
                weighted_list[pos] = 1
            elif weighted_list[pos] < (maxi / 2):
                weighted_list[pos] = 2
            elif weighted_list[pos] < (maxi * 0.75):
                weighted_list[pos] = 4
            else:
                weighted_list[pos] = 8
        if sum(weighted_list)==0:
            error='\n'.join(['no value','there were not enough steps found on this function to draw tangents'])
            return
            exit
        x=random.choices(x_range, weighted_list)[0]
        pos=x_range.index(x)
        x_list.append(x)
        tang_starts=step_list[pos]
        tang_starts-=4
        tang_starts=[x+1 for x in range(tang_starts)]
        tang_starts2.append(tang_starts[-1] + 4)
        position=random.choice(tang_starts)
        tang_list.append(position)
        Functions.draw_tangents(equation,x,0,tang_list[0],1,1,megalist_x,megalist_y,mask_starts)
    def draw_tangents(equation,x,step,position,x1,y_x1,megalist_x,megalist_y,mask_starts):
        tol=1/100
        new_equation=equation.replace('x',str(x))
        y=NumericStringParser().eval(new_equation)
        deriv = Functions.deriv_single(x,equation)
        if abs(y) < tol:
            return megalist_x
        elif step == 0:
            step += 1
            x1=x
            y_x1=y
            return Functions.draw_tangents(equation,x-y/deriv,step,position,x1,y_x1,megalist_x,megalist_y,mask_starts)
        elif step-position==0:
            jump=(abs(x1-x))/10
            x_range_tang1=[]
            for i in range(11):
                if x1<x:
                    added=x1+(i*jump)
                    x_range_tang1.append(added)
                else:
                    added = x1 - (i * jump)
                    x_range_tang1.append(added)
            y_range_tang1 = [((x_tang - x) * (y_x1 / (x1 - x))) for x_tang in x_range_tang1]
            mask_start=len(x_range_tang1)
            mask_starts.append(mask_start)
            for value in x_range_tang1:
                megalist_x.append(value)
            for value in y_range_tang1:
                megalist_y.append(value)
            step += 1
            y_x1 = y
            x1 = x
            return Functions.draw_tangents(equation,x-y/deriv,step,position,x1,y_x1,megalist_x,megalist_y,mask_starts)
        elif step-position==1:
            jump=(abs(x1-x))/10
            x_range_tang2=[]
            for i in range(11):
                if x1<x:
                    added=x1+(i*jump)
                    x_range_tang2.append(added)
                else:
                    added = x1 - (i * jump)
                    x_range_tang2.append(added)
            y_range_tang2 = [((x_tang - x) * (y_x1 / (x1 - x))) for x_tang in x_range_tang2]
            mask_start=len(x_range_tang2)+mask_starts[-1]
            mask_starts.append(mask_start)
            for value in x_range_tang2:
                megalist_x.append(value)
            for value in y_range_tang2:
                megalist_y.append(value)
            step += 1
            y_x1 = y
            x1 = x
            return Functions.draw_tangents(equation,x-y/deriv,step,position,x1,y_x1,megalist_x,megalist_y,mask_starts)
        elif step-position==2:
            jump=(abs(x1-x))/10
            x_range_tang3=[]
            for i in range(11):
                if x1<x:
                    added=x1+(i*jump)
                    x_range_tang3.append(added)
                else:
                    added = x1 - (i * jump)
                    x_range_tang3.append(added)
            y_range_tang3 = [((x_tang - x) * (y_x1 / (x1 - x))) for x_tang in x_range_tang3]
            mask_start=len(x_range_tang3)+mask_starts[-1]
            mask_starts.append(mask_start)
            for value in x_range_tang3:
                megalist_x.append(value)
            for value in y_range_tang3:
                megalist_y.append(value)
            step += 1
            y_x1 = y
            x1 = x
            return Functions.draw_tangents(equation,x-y/deriv,step,position,x1,y_x1,megalist_x,megalist_y,mask_starts)
        elif step-position==3:
            jump=(abs(x1-x))/10
            x_range_tang4=[]
            for i in range(11):
                if x1<x:
                    added=x1+(i*jump)
                    x_range_tang4.append(added)
                else:
                    added = x1 - (i * jump)
                    x_range_tang4.append(added)
            last=x_range_tang4[-1]
            for i in range(40):
                x_range_tang4.append(last)
            y_range_tang4 = [((x_tang - x) * (y_x1 / (x1 - x))) for x_tang in x_range_tang4]
            #mask_start=len(x_range_tang4)+mask_starts[-1]
            #mask_starts.append(mask_start)
            for value in x_range_tang4:
                megalist_x.append(value)
            for value in y_range_tang4:
                megalist_y.append(value)
            step += 1
            y_x1 = y
            x1 = x
            return Functions.draw_tangents(equation,x-y/deriv,step,position,x1,y_x1,megalist_x,megalist_y,mask_starts)
        else:
            step+=1
            y_x1=y
            x1=x
            return Functions.draw_tangents(equation,x-y/deriv,step,position,x1,y_x1,megalist_x,megalist_y,mask_starts)
    def draw_tangents_start(equation,x,step,x1,y_x1,megalist_x2,megalist_y2,tang_starts2,mask_starts,x_range2,y_range2,error):
        tol=1/100
        num_points=21
        nm_div=20
        new_equation=equation.replace('x',str(x))
        y=NumericStringParser().eval(new_equation)
        deriv = Functions.deriv_single(x,equation)
        if tang_starts2<8:
            return Functions.tsg_error(x_range2,y_range2,error)
        if abs(y) < tol:
            return Functions.tang_graph_start(megalist_x2,megalist_y2,tang_starts2,equation,mask_starts)
        elif step == 0:
            step += 1
            x1=x
            y_x1=y
            return Functions.draw_tangents_start(equation,x-y/deriv,step,x1,y_x1,megalist_x2,megalist_y2,tang_starts2,mask_starts,x_range2,y_range2, error)
        elif step==1:
            jump=(abs(x1-x))/nm_div
            x_range_tang=[]
            for i in range(num_points):
                if x1<x:
                    added=x1+(i*jump)
                    x_range_tang.append(added)
                else:
                    added = x1 - (i * jump)
                    x_range_tang.append(added)
            y_range_tang = [((x_tang - x) * (y_x1 / (x1 - x))) for x_tang in x_range_tang]
            mask_start=len(x_range_tang)
            mask_starts.append(mask_start)
            megalist_x2.append(x_range_tang)
            megalist_y2.append(y_range_tang)
            step += 1
            y_x1 = y
            x1 = x
            return Functions.draw_tangents_start(equation,x-y/deriv,step,x1,y_x1,megalist_x2,megalist_y2,tang_starts2,mask_starts,x_range2,y_range2, error)
        elif step==2:
            jump=(abs(x1-x))/nm_div
            x_range_tang=[]
            for i in range(num_points):
                if x1<x:
                    added=x1+(i*jump)
                    x_range_tang.append(added)
                else:
                    added = x1 - (i * jump)
                    x_range_tang.append(added)
            y_range_tang = [((x_tang - x) * (y_x1 / (x1 - x))) for x_tang in x_range_tang]
            mask_start=len(x_range_tang) + mask_starts[-1]
            mask_starts.append(mask_start)
            megalist_x2.append(x_range_tang)
            megalist_y2.append(y_range_tang)
            step += 1
            y_x1 = y
            x1 = x
            return Functions.draw_tangents_start(equation,x-y/deriv,step,x1,y_x1,megalist_x2,megalist_y2,tang_starts2,mask_starts,x_range2,y_range2, error)
        elif step==3:
            jump=(abs(x1-x))/nm_div
            x_range_tang=[]
            for i in range(num_points):
                if x1<x:
                    added=x1+(i*jump)
                    x_range_tang.append(added)
                else:
                    added = x1 - (i * jump)
                    x_range_tang.append(added)
            y_range_tang = [((x_tang - x) * (y_x1 / (x1 - x))) for x_tang in x_range_tang]
            mask_start=len(x_range_tang) + mask_starts[-1]
            mask_starts.append(mask_start)
            megalist_x2.append(x_range_tang)
            megalist_y2.append(y_range_tang)
            step += 1
            y_x1 = y
            x1 = x
            return Functions.draw_tangents_start(equation,x-y/deriv,step,x1,y_x1,megalist_x2,megalist_y2,tang_starts2,mask_starts,x_range2,y_range2, error)
        elif step==4:
            jump=(abs(x1-x))/nm_div
            x_range_tang=[]
            for i in range(num_points):
                if x1<x:
                    added=x1+(i*jump)
                    x_range_tang.append(added)
                else:
                    added = x1 - (i * jump)
                    x_range_tang.append(added)
            y_range_tang = [((x_tang - x) * (y_x1 / (x1 - x))) for x_tang in x_range_tang]
            mask_start=len(x_range_tang) + mask_starts[-1]
            mask_starts.append(mask_start)
            megalist_x2.append(x_range_tang)
            megalist_y2.append(y_range_tang)
            step += 1
            y_x1 = y
            x1 = x
            return Functions.draw_tangents_start(equation,x-y/deriv,step,x1,y_x1,megalist_x2,megalist_y2,tang_starts2,mask_starts,x_range2,y_range2, error)
        elif step==5:
            jump=(abs(x1-x))/nm_div
            x_range_tang=[]
            for i in range(num_points):
                if x1<x:
                    added=x1+(i*jump)
                    x_range_tang.append(added)
                else:
                    added = x1 - (i * jump)
                    x_range_tang.append(added)
            y_range_tang = [((x_tang - x) * (y_x1 / (x1 - x))) for x_tang in x_range_tang]
            mask_start=len(x_range_tang) + mask_starts[-1]
            mask_starts.append(mask_start)
            megalist_x2.append(x_range_tang)
            megalist_y2.append(y_range_tang)
            step += 1
            y_x1 = y
            x1 = x
            return Functions.draw_tangents_start(equation,x-y/deriv,step,x1,y_x1,megalist_x2,megalist_y2,tang_starts2,mask_starts,x_range2,y_range2, error)
        else:
            return Functions.tang_graph_start(megalist_x2,megalist_y2,tang_starts2,equation,mask_starts)
            #step+=1
            #y_x1=y
            #x1=x
            #return Functions.draw_tangents_start(equation,x-y/deriv,x_range,step,x1,y_x1,megalist_x2,megalist_y2,tang_starts2,mask_starts,x_range2,y_range2, error)
    def draw_tangents_end(equation,x,step,x1,y_x1,megalist_x3,megalist_y3,tang_starts2,mask_starts):
        tol=1/10000
        num_points=21
        nm_div=20
        new_equation=equation.replace('x',str(x))
        y=NumericStringParser().eval(new_equation)
        deriv = Functions.deriv_single(x,equation)
        error=error='tang_starts2 is ',tang_starts2
        if tang_starts2<5:
            return error
        if abs(y) < tol:
            return Functions.tang_graph_end(megalist_x3,megalist_y3,tang_starts2,equation,mask_starts)
        elif step == 0:
            step += 1
            x1=x
            y_x1=y
            return Functions.draw_tangents_end(equation,x-y/deriv,step,x1,y_x1,megalist_x3,megalist_y3,tang_starts2,mask_starts)
        elif tang_starts2-step==5:
            jump=(abs(x1-x))/nm_div
            x_range_tang=[]
            for i in range(num_points):
                if x1<x:
                    added=x1+(i*jump)
                    x_range_tang.append(added)
                else:
                    added = x1 - (i * jump)
                    x_range_tang.append(added)
            y_range_tang = [((x_tang - x) * (y_x1 / (x1 - x))) for x_tang in x_range_tang]
            mask_start=len(x_range_tang)
            mask_starts.append(mask_start)
            megalist_x3.append(x_range_tang)
            megalist_y3.append(y_range_tang)
            step += 1
            y_x1 = y
            x1 = x
            return Functions.draw_tangents_end(equation,x-y/deriv,step,x1,y_x1,megalist_x3,megalist_y3,tang_starts2,mask_starts)
        elif tang_starts2-step==4:
            jump=(abs(x1-x))/nm_div
            x_range_tang=[]
            for i in range(num_points):
                if x1<x:
                    added=x1+(i*jump)
                    x_range_tang.append(added)
                else:
                    added = x1 - (i * jump)
                    x_range_tang.append(added)
            y_range_tang = [((x_tang - x) * (y_x1 / (x1 - x))) for x_tang in x_range_tang]
            mask_start=len(x_range_tang) + mask_starts[-1]
            mask_starts.append(mask_start)
            megalist_x3.append(x_range_tang)
            megalist_y3.append(y_range_tang)
            step += 1
            y_x1 = y
            x1 = x
            return Functions.draw_tangents_end(equation,x-y/deriv,step,x1,y_x1,megalist_x3,megalist_y3,tang_starts2,mask_starts)
        elif tang_starts2-step==3:
            jump=(abs(x1-x))/nm_div
            x_range_tang=[]
            for i in range(num_points):
                if x1<x:
                    added=x1+(i*jump)
                    x_range_tang.append(added)
                else:
                    added = x1 - (i * jump)
                    x_range_tang.append(added)
            y_range_tang = [((x_tang - x) * (y_x1 / (x1 - x))) for x_tang in x_range_tang]
            mask_start=len(x_range_tang) + mask_starts[-1]
            mask_starts.append(mask_start)
            megalist_x3.append(x_range_tang)
            megalist_y3.append(y_range_tang)
            step += 1
            y_x1 = y
            x1 = x
            return Functions.draw_tangents_end(equation,x-y/deriv,step,x1,y_x1,megalist_x3,megalist_y3,tang_starts2,mask_starts)
        elif tang_starts2-step==2:
            jump=(abs(x1-x))/nm_div
            x_range_tang=[]
            for i in range(num_points):
                if x1<x:
                    added=x1+(i*jump)
                    x_range_tang.append(added)
                else:
                    added = x1 - (i * jump)
                    x_range_tang.append(added)
            y_range_tang = [((x_tang - x) * (y_x1 / (x1 - x))) for x_tang in x_range_tang]
            mask_start=len(x_range_tang) + mask_starts[-1]
            mask_starts.append(mask_start)
            megalist_x3.append(x_range_tang)
            megalist_y3.append(y_range_tang)
            step += 1
            y_x1 = y
            x1 = x
            return Functions.draw_tangents_end(equation,x-y/deriv,step,x1,y_x1,megalist_x3,megalist_y3,tang_starts2,mask_starts)
        elif tang_starts2-step==1:
            jump=(abs(x1-x))/nm_div
            x_range_tang=[]
            for i in range(num_points):
                if x1<x:
                    added=x1+(i*jump)
                    x_range_tang.append(added)
                else:
                    added = x1 - (i * jump)
                    x_range_tang.append(added)
            y_range_tang = [((x_tang - x) * (y_x1 / (x1 - x))) for x_tang in x_range_tang]
            mask_start=len(x_range_tang) + mask_starts[-1]
            mask_starts.append(mask_start)
            megalist_x3.append(x_range_tang)
            megalist_y3.append(y_range_tang)
            step += 1
            y_x1 = y
            x1 = x
            return Functions.draw_tangents_end(equation,x-y/deriv,step,x1,y_x1,megalist_x3,megalist_y3,tang_starts2,mask_starts)
        else:
            step+=1
            y_x1=y
            x1=x
            return Functions.draw_tangents_end(equation,x-y/deriv,step,x1,y_x1,megalist_x3,megalist_y3,tang_starts2,mask_starts)

    def db_delete(table):
        #deleting old entries
        now=datetime.now(timezone.utc)
        fmt='%Y-%m-%d %H:%M:%S.%f'
        now_str=now.strftime(fmt)
        now_new=datetime.strptime(now_str,fmt)
        query=sa.select(table)
        entries=db.session.scalars(query)
        i=0
        nums=[0,1,2,3,10,25,50,100,250,500,1000]
        for e in entries:
            ts=e.timestamp
            u_id=e.id
            ts_str=str(ts)
            ts_con=datetime.strptime(ts_str,fmt)
            diff=now_new-ts_con
            if diff>timedelta(hours=1):
                if i in nums:
                    entry2=db.session.get(table,u_id)
                    db.session.delete(entry2)
                    db.session.commit()
            #elif i>0:
            #    print('no entries')
            else:
                if i in nums:
                    entry2=db.session.get(table,u_id)
            i+=1


        



__author__ = 'Paul McGuire'
__version__ = '$Revision: 0.0 $'
__date__ = '$Date: 2009-03-20 $'
__source__ = '''http://pyparsing.wikispaces.com/file/view/fourFn.py
http://pyparsing.wikispaces.com/message/view/home/15549426
'''
__note__ = '''
All I've done is rewrap Paul McGuire's fourFn.py as a class, so I can use it
more easily in other places.
'''

# module pyparsing.py
#
# Copyright (c) 2003-2022  Paul T. McGuire
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

class NumericStringParser(object):
    '''
    Most of this code comes from the fourFn.py pyparsing example

    '''

    def pushFirst(self, strg, loc, toks):
        self.exprStack.append(toks[0])

    def pushUMinus(self, strg, loc, toks):
        if toks and toks[0] == '-':
            self.exprStack.append('unary -')

    def __init__(self):
        """
        expop   :: '^'
        multop  :: '*' | '/'
        addop   :: '+' | '-'
        integer :: ['+' | '-'] '0'..'9'+
        atom    :: PI | E | real | fn '(' expr ')' | '(' expr ')'
        factor  :: atom [ expop factor ]*
        term    :: factor [ multop factor ]*
        expr    :: term [ addop term ]*
        """
        point = Literal(".")
        e = CaselessLiteral("E")
        fnumber = Combine(Word("+-" + nums, nums) +
                          Optional(point + Optional(Word(nums))) +
                          Optional(e + Word("+-" + nums, nums)))
        ident = Word(alphas, alphas + nums + "_$")
        plus = Literal("+")
        minus = Literal("-")
        mult = Literal("*")
        div = Literal("/")
        lpar = Literal("(").suppress()
        rpar = Literal(")").suppress()
        addop = plus | minus
        multop = mult | div
        expop = Literal("^")
        pi = CaselessLiteral("PI")
        expr = Forward()
        atom = ((Optional(oneOf("- +")) +
                 (ident + lpar + expr + rpar | pi | e | fnumber).setParseAction(self.pushFirst))
                | Optional(oneOf("- +")) + Group(lpar + expr + rpar)
                ).setParseAction(self.pushUMinus)
        # by defining exponentiation as "atom [ ^ factor ]..." instead of
        # "atom [ ^ atom ]...", we get right-to-left exponents, instead of left-to-right
        # that is, 2^3^2 = 2^(3^2), not (2^3)^2.
        factor = Forward()
        factor << atom + \
            ZeroOrMore((expop + factor).setParseAction(self.pushFirst))
        term = factor + \
            ZeroOrMore((multop + factor).setParseAction(self.pushFirst))
        expr << term + \
            ZeroOrMore((addop + term).setParseAction(self.pushFirst))
        # addop_term = ( addop + term ).setParseAction( self.pushFirst )
        # general_term = term + ZeroOrMore( addop_term ) | OneOrMore( addop_term)
        # expr <<  general_term
        self.bnf = expr
        # map operator symbols to corresponding arithmetic operations
        epsilon = 1e-12
        self.opn = {"+": operator.add,
                    "-": operator.sub,
                    "*": operator.mul,
                    "/": operator.truediv,
                    "^": operator.pow}
        self.fn = {"sin": math.sin,
                   "cos": math.cos,
                   "tan": math.tan,
                   "exp": math.exp,
                   "abs": abs,
                   "trunc": lambda a: int(a),
                   "round": round,
                   "sgn": lambda a: abs(a) > epsilon and cmp(a, 0) or 0}

    def evaluateStack(self, s):
        op = s.pop()
        if op == 'unary -':
            return -self.evaluateStack(s)
        if op in "+-*/^":
            op2 = self.evaluateStack(s)
            op1 = self.evaluateStack(s)
            return self.opn[op](op1, op2)
        elif op == "PI":
            return math.pi  # 3.1415926535
        elif op == "E":
            return math.e  # 2.718281828
        elif op in self.fn:
            return self.fn[op](self.evaluateStack(s))
        elif op[0].isalpha():
            return 0
        else:
            return float(op)

    def eval(self, num_string, parseAll=True):
        self.exprStack = []
        results = self.bnf.parseString(num_string, parseAll)
        val = self.evaluateStack(self.exprStack[:])
        return val