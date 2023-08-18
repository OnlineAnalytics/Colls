import pandas as pd
from scipy.stats import zscore, binned_statistic_2d
import numpy as np
import ipywidgets as widgets
import matplotlib.pyplot as plt
from mplsoccer import PyPizza, add_image, FontManager,Pitch,VerticalPitch
import warnings
import streamlit as st
from statistics import mean
from streamlit import components
import os
import matplotlib.font_manager as fm
import matplotlib
matplotlib.rcParams.update({'font.size': 22})

hide_github_icon = """
<style>
.css-1jc7ptx, .e1ewe7hr3, .viewerBadge_container__1QSob, .styles_viewerBadge__1yB5_, .viewerBadge_link__1S137, .viewerBadge_text__1JaDK{ display: none; } #MainMenu{ visibility: hidden; } footer { visibility: hidden; } header { visibility: hidden; }
</style>
"""
st.markdown(hide_github_icon,unsafe_allow_html=True)

st.markdown("""
        <style>
               .block-container {
                    padding-top: 0rem;
                    padding-bottom: 0rem;
                    padding-right: 1rem;
                }
        </style>
        """, unsafe_allow_html=True)

#Remove Warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)
pd.options.mode.chained_assignment = None
df = pd.read_csv('./ath2.csv')
st.markdown('<p style="font-size: 45px; font-weight: bold;">Atherton Collieries xG Maps</p>', unsafe_allow_html=True)
st.markdown('<p style="font-size: 25px; font-weight: bold;">Season total xG For {:.2f} - {:.2f} Season total xG Against</p>'.format(round(sum(df[df['Team']=='Colls'].xG),2),round(sum(df[df['Team']!='Colls'].xG),2)), unsafe_allow_html=True)
st.markdown('<p style="font-size: 25px; font-weight: bold;">Goals For {} - {} Goals Against</p>'.format(len(df[(df['Team']=='Colls') & (df['Event']=='Goal')]),len(df[(df['Team']!='Colls') & (df['Event']=='Goal')])), unsafe_allow_html=True)
with st.sidebar:
    st.markdown('<h1 style="font-family: Consolas; font-size: 34px;">Select type of xG map.</h1>', unsafe_allow_html=True)
    option = st.selectbox(' ',('xG For', 'xG Against', 'Expected shot location','Expected goal location'))
   
if option == 'xG For':
 d = df[df['Team']=='Colls']
 pl = d.Player.unique().tolist()
 pl.insert(0,'All')
 top = st.selectbox("Select 'All' to see all shots, or pick a specific player", pl)
 
 if top == 'All':
  d = df[df['Team']=='Colls']
  d.Y = 100-d.Y
  pitch = VerticalPitch(pitch_type='opta', half = True)
  fig, ax = pitch.draw(figsize=(50,50))
  pitch.scatter(d[d['Event'] =='Shot Off'].X,d[d['Event'] =='Shot Off'].Y,s=(d[d['Event'] =='Shot Off'].xG*90000),alpha = 0.8,label = 'Shot Off',ax=ax)
  pitch.scatter(d[d['Event'] =='Shot Saved'].X,d[d['Event'] =='Shot Saved'].Y,s=(d[d['Event'] =='Shot Saved'].xG*90000),c='orange',alpha=0.8,label = 'Saved', ax=ax)
  pitch.scatter(d[d['Event'] =='Goal'].X,d[d['Event'] =='Goal'].Y,s=(d[d['Event'] =='Goal'].xG*90000),c='green',alpha=0.8,label = 'Goal', ax=ax)
  pitch.scatter(d[d['Event'] =='Shot Blocked'].X,d[d['Event'] =='Shot Blocked'].Y,s=(d[d['Event'] =='Shot Blocked'].xG*90000),c='red',alpha=0.8,label = 'Blocked', ax=ax)
  
  plt.legend(fontsize=80,loc=1)
  st.pyplot(fig)
  st.write(d.groupby('Player').agg({'xG':'sum'}))
 if top !='All':
   d = df[df['Team']=='Colls']
   d.Y = 100-d.Y
   player = top
   d = d[d['Player']==player]
   pitch = VerticalPitch(pitch_type='opta', half = True)
   fig, ax = pitch.draw(figsize=(50,50))
   pitch.scatter(d[d['Event'] =='Shot Off'].X,d[d['Event'] =='Shot Off'].Y,s=(d[d['Event'] =='Shot Off'].xG*90000),alpha = 0.8,label = 'Shot Off',ax=ax)
   pitch.scatter(d[d['Event'] =='Shot Saved'].X,d[d['Event'] =='Shot Saved'].Y,s=(d[d['Event'] =='Shot Saved'].xG*90000),c='orange',alpha=0.8,label = 'Saved', ax=ax)
   pitch.scatter(d[d['Event'] =='Goal'].X,d[d['Event'] =='Goal'].Y,s=(d[d['Event'] =='Goal'].xG*90000),c='green',alpha=0.8,label = 'Goal', ax=ax)
   pitch.scatter(d[d['Event'] =='Shot Blocked'].X,d[d['Event'] =='Shot Blocked'].Y,s=(d[d['Event'] =='Shot Blocked'].xG*90000),c='red',alpha=0.8,label = 'Blocked', ax=ax)
   plt.legend(fontsize=80,loc=1)
   st.pyplot(fig)
   st.write(d.groupby('Player').agg({'xG':'sum'}))

if option == 'xG Against':
 d = df[df['Team']!='Colls']
 d.X = 100-d.X
 pitch = VerticalPitch(pitch_type='opta', half = True)
 fig, ax = pitch.draw(figsize=(50,50))
 pitch.scatter(d[d['Event'] =='Shot Off'].X,d[d['Event'] =='Shot Off'].Y,s=(d[d['Event'] =='Shot Off'].xG*90000),alpha = 0.8,label = 'Shot Off',ax=ax)
 pitch.scatter(d[d['Event'] =='Shot Saved'].X,d[d['Event'] =='Shot Saved'].Y,s=(d[d['Event'] =='Shot Saved'].xG*90000),c='orange',alpha=0.8,label = 'Saved', ax=ax)
 pitch.scatter(d[d['Event'] =='Goal'].X,d[d['Event'] =='Goal'].Y,s=(d[d['Event'] =='Goal'].xG*90000),c='green',alpha=0.8,label = 'Goal', ax=ax)
 pitch.scatter(d[d['Event'] =='Shot Blocked'].X,d[d['Event'] =='Shot Blocked'].Y,s=(d[d['Event'] =='Shot Blocked'].xG*90000),c='red',alpha=0.8,label = 'Blocked', ax=ax)
 plt.legend(fontsize=80,loc=1)
   

 st.pyplot(fig)
 st.write(d.groupby('Team').agg({'xG':'sum'}))

if option == 'Expected shot location':
 tob = st.selectbox("For or against?", ('For','Against'))
  
 if tob == 'For':
  shot_df = df[df['Team']=='Colls']
  pitch = VerticalPitch(pitch_type='opta',half=True,line_color='black',line_zorder=10)   
  shot = pitch.bin_statistic(shot_df.X, 100-shot_df.Y, statistic='count', bins=(12, 8), normalize=False)

  fig, ax = pitch.grid(grid_height=0.9, title_height=0.06, axis=False,
                     endnote_height=0.04, title_space=0, endnote_space=0)
  pcm  = pitch.heatmap(shot, cmap='Greens', edgecolor='grey', ax=ax['pitch'])
#legend to our plot
  ax_cbar = fig.add_axes((1, 0.093, 0.03, 0.786))
  cbar = plt.colorbar(pcm, cax=ax_cbar)
  fig.suptitle('Shots 2D histogram', fontsize = 30)
  plt.show()
  shot_count = shot["statistic"]
  st.pyplot(fig)
  
