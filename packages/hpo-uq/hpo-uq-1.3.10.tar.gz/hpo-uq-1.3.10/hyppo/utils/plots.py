# System
import re
import os
import ast
import glob

# Externals
import numpy
import plotly.graph_objects as go
import matplotlib as mpl
import matplotlib.pyplot as plt
import pickle5 as pickle
from scipy import signal
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
from matplotlib import ticker, cm
from matplotlib.colors import LogNorm
from matplotlib.ticker import FormatStrFormatter
from mpl_toolkits.mplot3d import Axes3D
from plotly.subplots import make_subplots

# Locals
from .extract import *
from ..dnnmodels import training
from ..datasets import get_data
from ..hyperparams import set_hyperparams

def plot_convergence(loss,stdev,isurr=None,ylim=[],xlim=[],save=None):
    plt.style.use('seaborn')
    plt.figure(figsize=(6,4),dpi=100)
    plt.plot(loss,color='black',lw=0.5,zorder=1,
             label='Surrogate Modeling',drawstyle='steps-post')
    plt.fill_between(range(len(loss)),loss-stdev/2,loss+stdev/2,
                     alpha=0.5,lw=0,color='tomato',step='post',
                     label='Standard Deviation')
    if isurr!=None:
        plt.axvline(isurr,color='black',lw=1,ls='dashed')
    if len(ylim)>0:
        plt.ylim(ylim)
    if len(xlim)>0:
        plt.xlim(xlim)
    else:
        plt.xlim(0,len(loss))
    plt.xlabel('Index of function evaluations')
    plt.ylabel('Loss')
    plt.legend(loc='upper right')
    plt.tight_layout()
    if save==None:
        plt.show()
    else:
        plt.savefig(save+'.pdf')
        plt.close()

def get_custom_data(results,config=None,sensitivity=False):
    hp_names = []
    customdata = results[['params','loss','stdev']].to_numpy().T
    text_coord = \
        '<b>Model Results:</b><br>' + \
        'Mean Loss of %{customdata[1]:.5f}<br>' + \
        'Uncertainty of %{customdata[2]:.5f}<br>' + \
        '%{customdata[0]:,} trainable parameters<br><br>' + \
        '<b>Hyperparameter Set:</b><br>'
    if config!=None:
        with open(config) as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
    for hp_name in results.columns:
        hp_fmt, hp_vals = 'i', results[hp_name].to_numpy()
        if hp_name.startswith('hp'):
            hp_idx = hp_name[2:]
            if type(config)==dict:
                scale = config['prms']['mult'][int(hp_idx)-1]
                hp_name = config['prms']['names'][int(hp_idx)-1]
                hp_vals = hp_vals*float(scale)
                if '.' in str(scale):
                    hp_fmt = '.%if' % len(str(scale).split('.')[-1])
            text_coord += (hp_name+' = %{customdata['+str(int(hp_idx)+2)+']:'+hp_fmt+'}<br>')
            customdata = numpy.vstack((customdata,hp_vals))
            hp_names.append(hp_name)
    text_coord += '<extra></extra>'
    return text_coord, customdata.T, hp_names

def hpo_solutions(results,ms=20,edgewidth=2,config=None,log=True):
    text_coord, custom_data, _ = get_custom_data(results,config)
    fig = go.Figure(
        data=go.Scatter(
            x=results.loss,
            y=results.stdev,
            mode='markers',
            customdata=custom_data,
            hovertemplate=text_coord,
            marker=dict(
                size=ms,
                opacity=0.5,
                color=results.params,
                colorbar=dict(
                    thickness=20,
                    title='Number of trainable parameters',
                    titleside='right'
                ),
                line=dict(
                    color='black',
                    width=edgewidth,
                ),
            ),
        )
    )
    if log:
        fig.update_xaxes(type='log')
        fig.update_yaxes(type='log')
    fig.update_layout(
        autosize=True,
        xaxis_title='Loss',
        yaxis_title='1-'+u'\u03C3'+' Deviation',
        font=dict(size=15),
        margin=dict(l=0, r=0, b=0, t=0),
    )
    fig.write_html('solutions.html')
    fig.show()

def hpo_sensitivity(results,ms=20,edgewidth=2,ncols=3,config=None,log=False):
    """
    Parameters
    ----------
    results : :class:`pandas.core.frame.DataFrame`
      Extracted solutions from HYPPO log product files.
    ms : :class:`int`
      Marker size
    edgewidth : :class:`float`
      Marker edge line width
    ncols : :class:`int`
      Number of columns for multiplot figure
    config : :class:`str`
      Path to configuration file. If None, no scaling will be done
      and the hyperparameter name will be hp1, hp2,...
    log : :class:`bool`
      Display loss axes in logarithmic scale

    Examples
    --------
    >>> import hyppo
    >>> solutions = hyppo.extract('logs/*.log')
    >>> hyppo.hpo_sensitivity(solutions,config='config.yaml')
    
    .. raw:: html
       
       <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
       <embed type="text/html" src="../_static/plotly/sensitivity.html" width="100%" height="600">
    """
    text_coord, custom_data, hp_names = get_custom_data(results,config,sensitivity=True)
    n_hps = custom_data.shape[1]-3
    nrows = int(numpy.ceil(n_hps/ncols))
    fig = make_subplots(rows=nrows, cols=ncols, start_cell="top-left",
                        horizontal_spacing=0.03, vertical_spacing=0.08)
    for n,(irow,jcol) in enumerate([(i+1,j+1) for i in range(nrows) for j in range(ncols)]):
        if n+1>n_hps:
            break
        fig.add_trace(
            go.Scatter(
                x=custom_data[:,3+n],
                y=results.loss,
                mode='markers',
                customdata=custom_data,
                hovertemplate=text_coord,
                marker=dict(
                    size=ms,
                    opacity=0.5,
                    color=results.stdev,
                    colorbar=dict(
                        thickness=20,
                        title='1-'+u'\u03C3'+' Deviation',
                        titleside='right'
                    ),
                    line=dict(
                        color='black',
                        width=edgewidth,
                    ),
                ),
            ),row=irow, col=jcol)
        fig['layout']['xaxis%i' % (n+1)]['title'] = hp_names[n]
        if n%ncols==0:
            fig['layout']['yaxis%i' % (n+1)]['title'] = 'Loss'
    if log:
        fig.update_yaxes(type='log')
    fig.update_layout(
        autosize=True,
        margin=dict(l=0, r=0, b=0, t=0),
        showlegend=False,
    )
    fig.write_html('sensitivity.html')
    fig.show()

def plot_sensitivity(results,ms=20,edgewidth=0.1,ncols=3,config=None,log=False,save=True,show=False,**kwargs):
    text_coord, custom_data, hp_names = get_custom_data(results,config,sensitivity=True)
    n_hps = custom_data.shape[1]-3
    nrows = int(numpy.ceil(n_hps/ncols))
    plt.style.use('seaborn')
    fig,ax = plt.subplots(nrows,ncols,figsize=(ncols*3+1,3*nrows),dpi=200,sharey=True)
    # ax = ax.flatten
    plt.subplots_adjust(top=0.97,wspace=0.07,hspace=0.3,right=0.9,left=0.07,bottom=0.08)
    for n,(irow,jcol) in enumerate([(i,j) for i in range(nrows) for j in range(ncols)]):
        if n+1>n_hps:
            break
        im = ax[irow][jcol].scatter(custom_data[:,3+n],results.loss,c=results.stdev,lw=edgewidth,ec='black',alpha=0.5,s=ms,cmap='plasma')
        if n%ncols==0:
            ax[irow][jcol].set_ylabel('Loss')
        ax[irow][jcol].set_xlabel(hp_names[n])
    cax = plt.axes([0.92, 0.08, 0.02, 0.89])
    cbar = plt.colorbar(im,cax=cax)
    cbar.set_alpha(1)
    cbar.draw_all()
    cbar.set_label(r'1-$\mathrm{\sigma}$ Deviation')
    cbar.ax.xaxis.set_ticks_position('top')
    cbar.ax.xaxis.set_label_position('top')
    if save: plt.savefig('figure.pdf')
    if show: plt.show()
    plt.close()
    
def model_visualization_1d(X,Y,path,evaluation,surrogate,imax=10,sigma=False,ylim=[-0.5,2.5]):
    scaler = round(1/(X[1]-X[0]))
    os.makedirs('%s/plots' % (path),exist_ok=True)
    plt.style.use('seaborn')
    for i,hp1s in enumerate(surrogate['hp1']):
        if i==imax:
            break
        model = pickle.load(open('%s/models/surrogate_%i/model.pkl' % (path,hp1s),'rb'))
        if sigma:
            Y_pred, Y_sigma = model.predict(X.reshape(-1, 1)*scaler,return_std=True)
        else:
            Y_pred = model.predict(X.reshape(-1, 1)*scaler,return_std=False)
        Y_pred = Y_pred.squeeze()
        fig,ax = plt.subplots(1,3,figsize=[12,4],dpi=200,sharex=True,sharey=True)
        fig.suptitle('Surrogate Modeling - Iteration %i / %i - Hyperparameters (%.2f)' % (i+1,imax,hp1s/scaler))
        ax[0].set_ylim(ylim)
        ax[0].plot(X,Y,'black')
        ax[1].plot(X,Y,'black',ls='dashed')
        ax[1].plot(X,Y_pred,'black')
        if sigma:
            ax[1].fill_between(X,Y_pred-Y_sigma/2,Y_pred+Y_sigma/2,alpha=0.2,lw=0,color='blue',step='post')
        ax[2].plot(X,Y-Y_pred,'black')
        for k in range(2):
            ax[k].set_xlabel('X')
            for hp,loss in zip(evaluation['hp1'],evaluation['loss']):
                ax[k].plot([hp/scaler], [loss], 'bx', mew=3)
            for n,(hp,loss) in enumerate(zip(surrogate['hp1'],surrogate['loss'])):
                if n>i: break
                ax[k].plot([hp/scaler], [loss], 'rx', mew=3)
        ax[0].set_ylabel('Y')
        plt.tight_layout()
        plt.savefig('%s/plots/iter_%02i' % (path,i+1))
        plt.close()
    
def model_visualization_2d(X,Y,path,evaluation,surrogate,imax=10,sigma=False):
    scaler = round(1/(X[1]-X[0]))
    X1, Y1 = numpy.meshgrid(X, Y)
    R = numpy.sqrt(X1**2 + Y1**2)
    Z = 0.4 - (1. / numpy.sqrt(2 * numpy.pi)) * numpy.exp(-.5*R**2)
    Z_scaler = round(Z.max(),1)
    os.makedirs('%s/plots' % (path),exist_ok=True)
    plt.style.use('seaborn')
    for i,(hp1s,hp2s) in enumerate(zip(surrogate['hp1'],surrogate['hp2'])):
        if i==imax:
            break
        model = pickle.load(open('%s/models/surrogate_%i_%i/model.pkl' % (path,hp1s,hp2s),'rb'))
        comb = numpy.array([(x,y) for y in Y for x in X]).reshape(-1, 2)*scaler
        Y_pred = model.predict(comb).reshape(len(X),len(Y))
        Y_pred[Y_pred<0], Y_pred[Y_pred>0.4] = 0.0, Z_scaler
        fig,ax = plt.subplots(1,3,figsize=[12,4],dpi=200,sharex=True,sharey=True)
        fig.suptitle('Surrogate Modeling - Iteration %i / %i - Hyperparameters (%.2f, %.2f)' % (i+1,imax,hp1s/scaler,hp2s/scaler))
        im0 = ax[0].contourf(X1,Y1,Z,levels=numpy.linspace(0,Z_scaler,scaler),cmap='viridis')
        im1 = ax[1].contourf(X1,Y1,Y_pred,levels=numpy.linspace(0,Z_scaler,scaler),cmap='viridis')
        im2 = ax[2].contourf(X1,Y1,Z-Y_pred,levels=numpy.linspace(-Z_scaler,Z_scaler,scaler),cmap='bwr')
        for k in range(3):
            ax[k].set_xlabel('X')
            for hp1,hp2 in zip(evaluation['hp1'],evaluation['hp2']):
                ax[k].plot(hp1/scaler, hp2/scaler, 'kx', mew=3)
            for n,(hp1,hp2) in enumerate(zip(surrogate['hp1'],surrogate['hp2'])):
                if n>i: break
                ax[k].plot(hp1/scaler, hp2/scaler, 'rx', mew=3)
            cbar = plt.colorbar(eval('im%i' % k), ax=ax[k],ticks=[0,Z_scaler/2,Z_scaler] if k<2 else [-Z_scaler,0,Z_scaler],
                                shrink=0.8, orientation='horizontal', location='top')
        ax[0].set_ylabel('Y')
        plt.tight_layout()
        plt.savefig('%s/plots/iter_%02i' % (path,i+1))
        plt.close()
    
    
def scatter_solutions(input_data,save=True,show=False,**kwargs):
    """
    Scatter plot of all evaluated HPO solutions. A top histogram is also displayed
    to show the distribution of losses found across all solutions. Multiple set of
    HPO solutions can be displayed next to each other, see examples.
    
    Parameters
    ----------
    input_data : :class:`list`
        Input extracted list of solutions.
    save : :class:`bool`
        Save the figure into a PDF with filename figure.pdf
    show : :class:`bool`
        Display figure.
        
    Examples
    --------
    A simple example of the ``input_data`` list can be as follows:
    
    >>> input_data = [solutions]
    
    where ``solutions`` is a set of solutions extracted from the saved log files
    using the :method:`hyppo.extract` function.
    
    
    More than one datasets can also be considered. For instance, let's consider two
    set of solutions, one, ``data1``, contains solutions obtained using Gaussian
    Process surrogate modeling, the other, ``data2``, are solutions obtained doing
    only random sampling, the ``input_data`` can be built as follows:
    
    >>> input_data = [[data1,'Gaussian Process'],[data2,'Random Sampling']]
    """
    plt.style.use('seaborn')
    fig, ax = plt.subplots(2,len(input_data),figsize=(4*len(input_data)+2,5),gridspec_kw={'height_ratios': [1, 3]},dpi=200,sharex=True,sharey='row')
    if len(input_data)==1:
        ax = numpy.array(ax,ndmin=2).T
    plt.subplots_adjust(left=0.05,top=0.93,right=0.9,wspace=0.05,hspace=0.1)
    for i,data in enumerate(input_data):
        if type(data)==list:
            data, title = data
            ax[0][i].set_title('(%i) %s' % (i+1,title))
        print('Dataset %i : %i solutions displayed' % (i+1,len(data)))
        ax[0][i].hist(data.loss,range=[0,1.6],rwidth=0.9,bins=16,histtype='bar')
        im = ax[1][i].scatter(data.loss,data.stdev,c=data.hp3*5e-5,lw=0.1,alpha=0.5,s=20,cmap='plasma')
        ax[1][i].minorticks_off()
        ax[1][i].set_xlabel('Best Wasserstein Distance')
        # ax[i].set_xlim([0,0.25])
        # ax[i].set_ylim([0,0.1])
        ax[1][i].scatter([0.125],[0.030], facecolors='none', edgecolors='tomato',s=1200,lw=2)
    ax[1][0].set_ylabel(r'1-$\mathrm{\sigma}$ Deviation')
    cax = plt.axes([0.91, 0.125, 0.02, 0.575])
    cbar = plt.colorbar(im,cax=cax,format='%.0e')
    cbar.set_alpha(1)
    cbar.draw_all()
    cbar.set_label('Generator Learning Rate')
    if save: plt.savefig('figure.pdf')
    if show: plt.show()
    plt.close()
    
# class PlotResults():
    
#     def __init__(self, data, y_predicted, output_name):
#         self.output_name = output_name
#         n_out = data['test']['y_data'].shape[-1]
#         if data['dataset']=='network':
#             if n_out==1:
#                 self.unity(data, y_predicted)
#             else:
#                 self.multi_pred(data, y_predicted)
#         elif data['dataset']=='generic':
#             if n_out==1:
#                 self.simple_pred(data, y_predicted)
            
#     def simple_pred(self, data, y_predicted):
#         os.makedirs('predictions', exist_ok=True)
#         # Get real test data
#         y_real = data['test']['y_data'].reshape(-1,1)
#         # Get prediction data
#         y_pred = y_predicted.reshape(-1,1)
#         ## 'De-normalize' the data
#         #sc = data['scaler']
#         #y_predicted_descaled = sc.inverse_transform(y_pred)
#         #y_test_descaled = sc.inverse_transform(y_real)
#         # Initialize figure
#         plt.style.use('seaborn')
#         fig, ax = plt.subplots(2,2,figsize=(10,7),dpi=200)
#         # Plot data and prediction
#         ax[0,0].plot(y_real, color = 'black', linewidth=1, label = 'True value')
#         ax[0,0].plot(y_pred, color = 'red',  linewidth=1, label = 'Predicted')
#         ax[0,0].legend(frameon=False)
#         ax[0,0].set_ylabel("Raw Data")
#         ax[0,0].set_xlabel("Index")
#         ax[0,0].set_title("Predicted data")
#         # Plot cross-correlation
#         norm_test = y_real.copy().ravel()
#         norm_test -= numpy.median(norm_test)
#         norm_test /= max(abs(norm_test))
#         norm_pred = y_pred.copy().ravel()
#         norm_pred -= numpy.median(norm_pred)
#         norm_pred /= max(abs(norm_pred))
#         lags, xcorr, _, _ = ax[0][1].xcorr(norm_test,norm_pred,maxlags=500)
#         ax[0,1].clear()
#         ax[0,1].fill_between(lags,xcorr,color='black',lw=0)
#         ax[0,1].set_ylim(-1,1)
#         ax[0,1].set_xlim(lags[0],lags[-1])
#         ax[0,1].set_xlabel('Lags')
#         ax[0,1].set_ylabel('Correlation Coefficient')
#         ax[0,1].set_title('Cross Correlation')
#         # Plot residuals
#         ax[1,0].plot(y_real-y_pred, color='black', lw=1) 
#         ax[1,0].set_ylim(-1,1)
#         ax[1,0].set_ylabel("Residual")
#         ax[1,0].set_xlabel("Hour")
#         ax[1,0].set_title("Residual plot")
#         # Plot scattered values
#         imin = max(min(y_real),min(y_pred))
#         imax = min(max(y_real),max(y_pred))
#         ax[1,1].scatter(y_pred, y_real, s=2, color='black')
#         ax[1,1].plot([imin,imax], [imin,imax], lw=1, ls='dashed', color='red')
#         ax[1,1].set_xlim(0,1)
#         ax[1,1].set_ylim(0,1)
#         ax[1,1].set_ylabel("Y true")
#         ax[1,1].set_xlabel("Y predicted")
#         ax[1,1].set_title("Scatter plot")
#         # Save figure
#         plt.tight_layout()
#         plt.savefig(os.path.join('predictions',self.output_name+'.pdf'))
#         plt.close()
            
#     def multi_pred(self, data, y_predicted):
#         results_dir = os.path.join('predictions',self.output_name)
#         os.makedirs(results_dir, exist_ok=True)
#         nlinks = data['test']['y_data'].shape[1]
#         for i in range(nlinks):
#             # Get network link's indexx
#             link = i if data['link']=='all' else data['link']
#             n = 0
#             x_scaled = data['test']['X_data'][n][i].reshape(-1,1)
#             y_scaled = data['test']['y_data'][n][i].reshape(-1,1)
#             p_scaled = y_predicted[n][i].reshape(-1,1)
#             sc = data['scaler'][i]
#             x = sc.inverse_transform(x_scaled)
#             y = sc.inverse_transform(y_scaled)
#             p = sc.inverse_transform(p_scaled)
#             # Initializing figure
#             plt.style.use('seaborn')
#             plt.figure(figsize=(12,7),dpi=200)
#             # Plot first time series sample
#             plt.subplot(2, 2, 1)
#             plt.plot(numpy.concatenate((x,y)), color='black', lw=1, label='True value')
#             t = numpy.arange(len(x),len(x)+len(y))
#             plt.plot(t, p, color='red',  lw=1, label='Predicted')
#             plt.legend(frameon=False)
#             plt.ylabel("Traffic")
#             plt.xlabel("Hour")
#             plt.title("Test data")
#             # Plot average cross-correlation among all test data
#             plt.subplot(2, 2, 2)
#             #xcors = []
#             #for y,p in zip(data['test']['y_data'],y_predicted):
#             #    xcors.append(numpy.correlate(y[i],p[i],"full"))
#             #xcor = numpy.array(numpy.mean(xcors,axis=0))
#             xcor = numpy.correlate(y.flatten(),p.flatten(),"full")
#             lags = numpy.arange(len(xcor)) - len(xcor)//2
#             idxs = numpy.where(abs(lags)<=5) 
#             plt.plot(lags[idxs],xcor[idxs], color='black', lw=1)
#             plt.xlabel('Lag')
#             plt.ylabel('Cross-correlation (real-prediction)')
#             plt.axvline(0,color='red',lw=2)
#             plt.axvline(-1,color='red',ls='dashed',lw=2)
#             plt.xlim(-5,5)
#             plt.ylim(min(xcor[idxs]),max(xcor[idxs]))
#             # Plot average residual plot
#             plt.subplot(2, 2, 3)
#             plt.plot(y-p,color='black',lw=1)
#             plt.xlabel('Residual')
#             plt.ylabel('Hour')
#             # Plot average scatter plot
#             imin = max(min(p),min(y))
#             imax = min(max(p),max(y))
#             plt.subplot(2, 2, 4)
#             plt.scatter(y,p,color='black',s=10)
#             plt.plot([imin,imax], [imin,imax], lw=1, ls='dashed', color='red')
#             plt.xlabel('Residual')
#             plt.ylabel('Hour')
#             # Complete figure
#             plt.tight_layout()
#             plt.savefig(os.path.join(results_dir,'results_link_%03i'%(link+1)))
#             plt.close()        
            
#     def unity(self, data, y_predicted):
#         """
#         Previous version of result plot. To be used when datasets are built with
#         stepsize of unity in time domain and prediction is done for a single value.
#         """
#         results_dir = os.path.join('predictions',self.output_name)
#         os.makedirs(results_dir, exist_ok=True)
#         nlinks = data['test']['y_data'].shape[1]
#         for i in range(nlinks):
#             link = i if data['link']=='all' else data['link']
#             datasets = [data[set_name]['y_data'][:,i] for set_name in ['train','valid','test']]
#             all_data = numpy.concatenate(datasets).reshape(-1,1)
#             y_real = data['test']['y_data'][:,i].reshape(-1,1)
#             y_pred = y_predicted[:,i].reshape(-1,1)
#             # 'De-normalize' the data
#             sc = data['scaler'][i]
#             y_predicted_descaled = sc.inverse_transform(y_pred)
#             #y_train_descaled = sc.inverse_transform(optidata.y_train)
#             y_test_descaled = sc.inverse_transform(y_real)
#             y_pred = y_pred.ravel()
#             #y_pred = [round(yx, 2) for yx in y_pred] #round to second decimal
#             y_tested = y_real.ravel()
#             # Show results
#             plt.style.use('seaborn')
#             plt.figure(figsize=(10,7),dpi=200)
#             plt.subplot(3, 1, 1)
#             plt.plot(all_data, color = 'black', linewidth=1, label = 'True value')
#             plt.axvspan(0,len(datasets[0]),alpha=0.2,color='blue')
#             plt.axvspan(len(datasets[0]),len(datasets[0])+len(datasets[1]),alpha=0.2,color='yellow')
#             plt.axvspan(len(datasets[0])+len(datasets[1]),len(datasets[0])+len(datasets[1])+len(datasets[2]),alpha=0.2,color='red')
#             plt.xlim(0,len(all_data))
#             plt.ylabel("Traffic")
#             plt.xlabel("Hour")
#             plt.title(data['links'][link]+" - All data")
#             plt.subplot(3, 2, 3)
#             plt.plot(y_test_descaled, color = 'black', linewidth=1, label = 'True value')
#             plt.plot(y_predicted_descaled, color = 'red',  linewidth=1, label = 'Predicted')
#             plt.legend(frameon=False)
#             plt.ylabel("Traffic")
#             plt.xlabel("Hour")
#             plt.title("Predicted data (%i days)"%(len(y_test_descaled)/24))
#             plt.subplot(3, 2, 4)
#             plt.plot(y_test_descaled[:75], color = 'black', linewidth=1, label = 'True value')
#             plt.plot(y_predicted_descaled[:75], color = 'red', label = 'Predicted')
#             plt.legend(frameon=False)
#             plt.ylabel("Traffic")
#             plt.xlabel("Hour")
#             plt.title("Predicted data (first 75 hours)")
#             plt.subplot(3, 2, 5)
#             plt.plot(y_test_descaled-y_predicted_descaled, color='black', lw=1)
#             plt.ylabel("Residual")
#             plt.xlabel("Hour")
#             plt.title("Residual plot")
#             imin = max(min(y_predicted_descaled),min(y_test_descaled))
#             imax = min(max(y_predicted_descaled),max(y_test_descaled))
#             plt.subplot(3, 2, 6)
#             plt.scatter(y_predicted_descaled, y_test_descaled, s=2, color='black')
#             plt.plot([imin,imax], [imin,imax], lw=1, ls='dashed', color='red')
#             plt.ylabel("Y true")
#             plt.xlabel("Y predicted")
#             plt.title("Scatter plot")
#             plt.tight_layout()
#             plt.savefig(os.path.join(results_dir,'pred_link_%03i'%(link+1)))
#             plt.close()
#             #mse = mean_squared_error(y_test_descaled, y_predicted_descaled)
#             #r2 = r2_score(y_test_descaled, y_predicted_descaled)
#             #print("mse=" + str(round(mse,2)))
#             #print("r2=" + str(round(r2,2)))

# def hyper_plot(input_data, hyperprms=None, fname='hyper', limits=None, **kwargs):
#     """
#     >>> quickrun.py hyper_plot out.log
#     """
#     os.makedirs('hyperplot', exist_ok=True)
#     labels = ['batch','epochs','layers','hidden_units','dropout']
#     nparams = len(labels)
#     results = numpy.empty((0,len(labels)+1))
#     for line in open(input_data):
#         if 'EVALUATION' in line:
#             results = numpy.vstack((results,[0]*(len(labels)+1)))
#         if 'Hyperparameters' in line:
#             hyperprms = ast.literal_eval(line.split('Hyperparameters:')[-1].strip())
#             for i,key in enumerate(labels):
#                 assert key in hyperprms.keys(), '%s hyperparameter not in list.'%key
#                 results[-1,i] = hyperprms[key] if type(hyperprms[key])!=list else hyperprms[key][0]
#         #if 'Testing' in line:
#         #    results[-1,-1] = float(line.split()[-1])
#         if 'Testing' in line:
#             results[-1,-1] = float(line.split()[-1])
#         if 'OPTIMIZATION' in line:
#             break
#     if limits==None:
#         vmin, vmax = results[:,-1].min(), results[:,-1].max()
#     else:
#         (vmin,vmax) = limits
#     norm = mpl.colors.Normalize(vmin=vmin, vmax=vmax)
#     cmap = mpl.cm.ScalarMappable(norm=norm, cmap=mpl.cm.turbo)
#     for i in range(len(results)):
#         plt.style.use('seaborn')
#         fig = plt.figure(figsize=(8,7),dpi=200)
#         ax = fig.add_subplot(111, polar=True)
#         lines, _ = plt.thetagrids(numpy.arange(0,360,360./nparams),labels=labels, fmt=None)
#         ax.set_yticklabels([])
#         rticks = numpy.arange(0,1.1,0.1)[1:]
#         for j in range(len(labels)):
#             for k,val in enumerate(numpy.linspace(0,results[:,j].max(),11)[1:]):
#                 val = round(val,2) if labels[j] in ['layers','dropout'] else int(val)
#                 ax.text(numpy.pi / 180 * 360./nparams * j, rticks[k], val, fontsize=5, ha='center', va='center')
#         ax.text(0, 0, '0', fontsize=5, ha='center', va='center')
#         for j in range(nparams):
#             next_col = 0 if j+1==nparams else j+1
#             theta1 = numpy.pi / 180 * 360./nparams * j
#             theta2 = numpy.pi / 180 * 360./nparams * next_col
#             r1 = results[i,j]/results[:,j].max()
#             r2 = results[i,next_col]/results[:,next_col].max()
#             color = cmap.to_rgba(results[i,-1])
#             ax.plot([theta1,theta2],[r1,r2],color=color, lw=2, alpha=0.5)
#             ax.fill_between([theta1,theta2], [0,0], [r1,r2], alpha=0.2, color=color, ec=None)
#         ax.set_rmin(0)
#         ax.set_rmax(1)
#         cbar = plt.colorbar(cmap,pad=0.1,shrink=0.75)
#         cbar.set_label('MSE Loss', fontsize=12)
#         #cbar.ax.hlines(results[i,-1], 0, 1, color='white')
#         plt.title('Evaluation %i - MSE Loss %.5f (Test data)\n'%(i+1,results[i,-1]))
#         ax1 = fig.add_subplot(198)
#         ax1.axis('off')
#         ymin = (vmin+vmax)/2-(vmax-vmin)/0.75/2
#         ymax = (vmin+vmax)/2+(vmax-vmin)/0.75/2
#         ax1.set_ylim(ymin,ymax)
#         y = (results[i,-1]-ymin)/(ymax-ymin)
#         ax1.annotate('',xy=(0.6,y),xycoords='axes fraction',xytext=(0.4,y),
#                      arrowprops=dict(color='black',lw=2))
#         plt.tight_layout()
#         plt.savefig('hyperplot/evaluation_%03i'%(i+1))
#         plt.close()

# def layer_loss(input_data, output_name=None, verbose=False, **kwargs):
#     """
#     Plot to display the change in MSE Loss with increasing number of layers.
#     The function reads some recorded values which correspond to the output of
#     a training with generic variable set to False in the input yaml file.
#     """
#     data = numpy.loadtxt(input_data) if type(input_data)==str else input_data
#     x = numpy.arange(2,int(data[-1,0])+1,2)
#     y = numpy.array([numpy.mean(data[i:i+10,1]) for i in range(0,len(data),10)])
#     e = numpy.array([numpy.std(data[i:i+10,1]) for i in range(0,len(data),10)])
#     if verbose:
#         for n,loss,err in zip(x,y,e):
#             print(n,'%.03E'%loss,'%.03E'%err)
#     plt.style.use('seaborn')
#     plt.figure(dpi=200)
#     plt.fill_between(x, y-e, y+e,
#                      color='turquoise',
#                      alpha=0.3,
#                      label=r'$\pm\,1\,\sigma$ around mean')
#     plt.scatter(data[:,0],data[:,1],
#                 c='gold',alpha=0.5,s=100,
#                 edgecolors='black',
#                 linewidth=0,
#                 label='Individual trial loss')
#     plt.scatter(data[:,0],data[:,1],
#                 c='black',alpha=0.5,s=10,
#                 edgecolors='black',linewidth=0)
#     plt.plot(x, y, 'orangered',label='Mean loss')
#     plt.xlabel('Number of layers')
#     plt.ylabel('MSE Loss')
#     plt.legend(loc='best')
#     plt.tight_layout()
#     if output_name==None: plt.show()
#     else: plt.savefig(output_name)
#     plt.close()

# def plot_xcross(data,predict,end=24*7,show=False,odir='./',fname='xcross'):
#     xcross_dir = os.path.join(odir, 'cross-correlations')
#     os.makedirs(xcross_dir, exist_ok=True)
#     nlinks = data.shape[1]
#     plt.style.use('seaborn')
#     fig,axs = plt.subplots(2,nlinks,figsize=(4*nlinks,10),dpi=200)
#     for i in range(nlinks):
#         ax = axs[0] if nlinks==1 else axs[0,i]
#         ax.plot(data[:end,i],color='black',lw=0.5,label='Real')
#         ax.plot(predict[:end,i],color='red',lw=0.8,label='Prediction')
#         ax.set_xlabel('Time [hour]')
#         ax.set_ylabel('Traffic')
#         ax.xaxis.set_label_position('top') 
#         ax.legend(loc='best',handlelength=1,handleheight=0.07)
#         ax.xaxis.tick_top()
#         xcorr = numpy.correlate(data[:end,i], predict[:end,i],"full")
#         lags = numpy.arange(len(xcorr)) - len(xcorr)//2
#         idxs = numpy.where(abs(lags)<=5) 
#         ax = axs[1] if nlinks==1 else axs[1,i]
#         ax.plot(lags[idxs],xcorr[idxs])
#         ax.set_xlabel('Lag')
#         ax.set_ylabel('Cross-correlation (real-prediction)')
#         ax.axvline(0,color='black',lw=2)
#         ax.axvline(-1,color='black',ls='dashed',lw=2)
#         ax.set_xlim(-5,5)
#         ax.set_ylim(min(xcorr[idxs]),max(xcorr[idxs]))
#     plt.tight_layout()
#     plt.savefig(os.path.join(xcross_dir,fname))
#     if show: plt.show()
#     plt.close()
    
# def sensitivity_plot(sensitivity,ax=None,names=['batch','epochs','layers','nodes','dropout'],**kwargs):
#     flag = (ax==None)
#     if flag:
#         plt.style.use('seaborn')
#         fig,ax = plt.subplots(1,1,figsize=(5.6,5))
#     if type(sensitivity)==str:
#         filehandler = open(sensitivity, 'rb')
#         sensitivity = pickle.load(filehandler)
#     data = sensitivity['S2']
#     for i in range(data.shape[0]):
#         data[i,i]=sensitivity['S1'][i]
#     ax.imshow(sensitivity['S2'].T,cmap='magma',aspect='auto')
#     ax.xticks(range(len(sensitivity['S2'])), names, fontsize=12, rotation=90)
#     ax.gca().xaxis.tick_bottom()
#     ax.yticks(range(len(sensitivity['S2'])), names, fontsize=12)
#     if flag:
#         cb = plt.colorbar()
#         cb.ax.tick_params(labelsize=12)
#         ax.set_title('Sensitivity', fontsize=12)
#         plt.grid(False)
#         plt.tight_layout()
#         plt.savefig('sensitivity.pdf')
#         plt.close()
#     else:
#         return ax

# def dual_sensitivity(input_data,**kwargs):
#     plt.style.use('seaborn')
#     fig,ax = plt.subplots(1,2,figsize=(12,6))
#     for i,path in enumerate(input_data):
#         sensitivity = get_sensitivity(path)
#         ax[i] = sensitivity_plot(sensitivity,ax=ax[i])
# #     cb = plt.colorbar()
# #     cb.ax.tick_params(labelsize=12)
# #     plt.title('Sensitivity', fontsize=12)
# #     plt.grid(False)
#     plt.tight_layout()
#     plt.savefig('sensitivity.pdf')
#     plt.close()

# def tensor_sensitivity(input_data,**kwargs):
#     plt.style.use('seaborn')
#     fig,ax = plt.subplots(1,2,figsize=(12,6))
#     sensitivity = get_sensitivity_from_tensorboard(input_data[0])
# #     for i,path in enumerate(input_data):
# #         sensitivity = get_sensitivity(path)
# #         ax[i] = sensitivity_plot(sensitivity,ax=ax[i])
# # #     cb = plt.colorbar()
# # #     cb.ax.tick_params(labelsize=12)
# # #     plt.title('Sensitivity', fontsize=12)
# # #     plt.grid(False)
# #     plt.tight_layout()
# #     plt.savefig('sensitivity.pdf')
# #     plt.close()

# def evaluation_losses(input_data,**kwargs):
#     losses = get_loss(input_data[0])
#     cmap = plt.cm.Spectral_r
#     norm = plt.Normalize(vmin=min(losses[:,1]), vmax=max(losses[:,1]))
#     imin, imax = losses[:,1].argmin(), losses[:,1].argmax()
#     print('Evaluation %i with highest loss of %.4f'%(imax+1,losses[imax,1]))
#     print('Evaluation %i with lowest loss of %.4f'%(imin+1,losses[imin,1]))
#     plt.style.use('seaborn')
#     plt.figure(figsize=(12,6))
#     plt.bar(losses[:,0],losses[:,1],0.8,color=cmap(norm(losses[:,1])))
#     plt.xlim(losses[0,0]-0.5,losses[-1,0]+0.5)
#     plt.minorticks_on()
# #     plt.yscale('log')
#     plt.xlabel('Evaluation Index')
#     plt.ylabel('Loss')
#     plt.title('Losses across %i evaluations'%len(losses), fontsize=12)
#     plt.tight_layout()
#     plt.savefig('losses.pdf')
#     plt.close()

# def dual_loss(input_data,limit=0.1,**kwargs):
#     loss_data = numpy.array([get_loss(path)[:,1] for path in input_data])
#     plt.style.use('seaborn')
#     fig,ax = plt.subplots(1,2,figsize=(12,6))
#     idx1 = numpy.where(loss_data[0]<limit)[0]
#     idx2 = numpy.where(loss_data[1]<limit)[0]
#     ax[0].hist([loss_data[0][idx1],loss_data[1][idx2]],bins=50,range=[0,0.1],color=['salmon','cornflowerblue'],label=input_data)
#     ax[0].set_title('Histogram',fontsize=12)
#     ax[0].set_xlabel('Loss')
#     ax[0].set_xlim([0,limit])
#     ax[0].legend(loc='best')
#     ax[1].hist([loss_data[0][idx1],loss_data[1][idx2]],bins=50,range=[0,0.1],color=['salmon','cornflowerblue'],label=input_data,cumulative=True)
#     ax[1].set_title('Cumulative',fontsize=12)
#     ax[1].set_xlabel('Loss')
#     ax[1].set_xlim([0,limit])
#     ax[1].yaxis.set_label_position('right')
#     ax[1].yaxis.tick_right()
#     ax[1].legend(loc='best')
#     plt.tight_layout()
#     plt.savefig('dual_loss.pdf')
#     plt.close()
        
# def param_space(input_data,**kwargs):
#     #data_norm = mpl.colors.Normalize
#     data_norm = mpl.colors.LogNorm
#     limits = [[0.02,0.05],[0.01,1000],[0.008,0.02],[0.0005,0.01]]
#     plt.style.use('seaborn')
#     fig,ax = plt.subplots(len(input_data)//2,4,figsize=(12,6),sharex=True,sharey='row')
#     fig.subplots_adjust(left=0.05,right=0.97,wspace=0.05,hspace=0.05,top=0.85,bottom=0.1)
#     for n,path in enumerate(input_data):
#         # Extract loss from given path
#         x,y,z,e = get_loss(path,grid=True)
#         # Get row and column position
#         i = int(numpy.ceil((n+1)/2)-1)
#         j = 2 if (n+1)%2==0 else 0
#         # Plot losses in 2D parameter space
#         print(path,limits[j])
#         (vmin, vmax) = limits[j]
#         ax[i][j].imshow(z,cmap=mpl.cm.jet,interpolation='bicubic',
#                         norm=data_norm(vmin=vmin,vmax=vmax),
#                         aspect='auto',origin='lower')
#         ax[i][j].scatter(x,y,color='white',s=0.5)
#         print(path,limits[j+1])
#         (vmin, vmax) = limits[j+1]
#         ax[i][j+1].imshow(e,cmap=mpl.cm.jet,interpolation='bicubic',
#                           norm=data_norm(vmin=vmin,vmax=vmax),
#                           aspect='auto',origin='lower')
#         ax[i][j+1].scatter(x,y,color='white',s=0.5)
#         if i+1==len(ax):
#             ax[i][j].set_xlabel('Epochs')
#             ax[i][j+1].set_xlabel('Epochs')
#         if j==0:
#             ax[i][j].set_ylabel('Number of Neurons')
#         ax[i][j].set_xlim(xmin=1,xmax=max(x))
#         ax[i][j].set_ylim(ymin=1,ymax=max(y))
#         ax[i][j+1].set_xlim(xmin=1,xmax=max(x))
#         ax[i][j+1].set_ylim(ymin=1,ymax=max(y))
#     for n,yloc in enumerate([0.070,0.302,0.535,0.769]):
#         (vmin, vmax) = limits[n]
#         labels = ['PyTorch - Loss','PyTorch - Standard Deviation',
#                   'TensorFlow - Loss','TensorFlow - Standard Deviation']
#         norm = data_norm(vmin=vmin, vmax=vmax)
#         cbar = fig.add_axes([yloc, 0.87, 0.18, 0.02])
#         bins = [vmin,vmax]
#         cb = mpl.colorbar.ColorbarBase(cbar, cmap=mpl.cm.jet,norm=norm,
#                                        orientation='horizontal', ticks=bins)
#         cb.set_ticks(bins)
#         #cb.ax.xaxis.set_major_formatter(ScalarFormatter())
#         cb.ax.minorticks_off()
#         cb.ax.xaxis.set_ticks_position('top')
#         cb.ax.xaxis.set_label_position('top')
#         cb.set_label(labels[n])
#     plt.savefig('param_space.pdf')
#     plt.close()
    
# def hist_loss(input_data,**kwargs):
#     nbin, vmin, vmax = 100, 1e-3, 1e5
#     plt.style.use('seaborn')
#     plt.subplots(figsize=(6,4))
#     logbins = numpy.logspace(numpy.log10(vmin),numpy.log10(vmax),nbin+1)
#     for n,path in enumerate(input_data):
#         library = 'TensorFlow' if 'tf' in path else 'PyTorch'
#         n_pred = int(path[1:4])
#         line_style = 'solid' if n_pred==100 else 'dashed'
#         color = 'navy' if library=='PyTorch' else 'orangered'
#         all_trials = get_loss(path,all_losses=True)
#         print(len(all_trials))
#         plt.hist(all_trials,bins=logbins,range=[vmin,vmax],lw=1,
#                  histtype='step',ls=line_style,color=color,
#                  label='%s, prediction on %i points'%(library,n_pred))
#         plt.xlabel('Loss')
#         plt.xlim([vmin,vmax])
#         plt.yscale('log')
#         plt.xscale('log')
#     plt.legend(loc='best')
#     plt.tight_layout()
#     plt.savefig('hist_loss.pdf')
#     plt.close()
    
# def hpo3d(samples,x_idx,y_idx,names=None):
#     # Initialize figure
#     fig = plt.figure()
#     ax = fig.add_subplot(111, projection='3d')
#     # Surface plot of evaluation results
#     X = samples['evals'][:,x_idx]
#     Y = samples['evals'][:,y_idx]
#     Z = samples['evals'][:,-1]
#     surf = ax.plot_trisurf(X, Y, Z, cmap=cm.coolwarm,linewidth=0, alpha=0.7)
#     # Plot surrogate model data
#     x = samples['sgate'][:,x_idx]
#     y = samples['sgate'][:,y_idx]
#     z = samples['sgate'][:,-1]
#     ax.plot3D(x,y,z,color='black',ls='dashed')
#     ax.scatter(x,y,z,color='black',s=30)
#     # Complete figure
#     if names!=None:
#         ax.set_xlabel(names[x_idx])
#         ax.set_ylabel(names[y_idx])
#     ax.set_zlabel('loss')
#     plt.show()
    
# if __name__ == '__main__':
#      #load optimization data
#     optidata = p.load(open('sampledatamlp_gp.data', 'rb'))
#     optidata.library = 'tf'
#     optidata.verbose = 2
#     optidata.dataset = 'network'
#     optidata = get_data(optidata)
#     best_hyp = optidata.xbest #best parameters found
#     x_sc = best_hyp*optidata.mult # scale to actual values
#     prms = set_hyperparams(x_sc, optidata.dl_type) 
#     model = training(data, prms, mode='train')
#     y_predicted = evaluate(model, optidata)
        
