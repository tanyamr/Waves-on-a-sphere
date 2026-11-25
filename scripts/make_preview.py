"""Generate the README preview: python scripts/make_preview.py."""
from pathlib import Path
import io
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.special import sph_harm_y
from PIL import Image

OUT = Path(__file__).resolve().parents[1] / 'assets'
OUT.mkdir(exist_ok=True)
lon, lat = np.meshgrid(np.linspace(-np.pi, np.pi, 100), np.linspace(-np.pi/2, np.pi/2, 60))
x, y, z = np.cos(lat)*np.cos(lon), np.cos(lat)*np.sin(lon), np.sin(lat)
modes = [(0,0),(1,0),(2,0),(2,2),(5,3),(5,-3)]
frames = []
for ell, m in modes:
    h = sph_harm_y(ell, abs(m), np.pi/2-lat, lon)
    field = h.real if m == 0 else np.sqrt(2)*(h.real if m > 0 else h.imag)
    vmax = max(np.abs(field).max(), 1e-10)
    norm = plt.Normalize(-vmax, vmax)
    fig = plt.figure(figsize=(9,4.5), facecolor='#101827')
    fig.suptitle('WAVES ON A SPHERE', color='white', fontsize=19, weight='bold', y=.95)
    ax = fig.add_subplot(121, projection='3d', facecolor='#101827')
    ax.plot_surface(x,y,z,facecolors=plt.cm.RdBu_r(norm(field)),rstride=1,cstride=1,shade=False)
    ax.set_box_aspect((1,1,1)); ax.set_axis_off(); ax.view_init(elev=20,azim=35)
    b = fig.add_subplot(122, facecolor='#101827')
    b.pcolormesh(np.degrees(lon),np.degrees(lat),field,cmap='RdBu_r',norm=norm,shading='auto')
    b.set(xlabel='Longitude',ylabel='Latitude',xticks=[-180,0,180],yticks=[-90,0,90])
    b.tick_params(colors='#cbd5e1')
    b.xaxis.label.set_color('#cbd5e1'); b.yaxis.label.set_color('#cbd5e1')
    for spine in b.spines.values(): spine.set_visible(False)
    b.set_title(f'One pattern: degree {ell}, order {m}',color='white',pad=15)
    fig.text(.5,.04,'Color = field value  |  Each pattern uses its own color scale',ha='center',color='#cbd5e1',fontsize=10)
    fig.subplots_adjust(left=.02,right=.96,bottom=.22,top=.78,wspace=.22)
    buf=io.BytesIO(); fig.savefig(buf,format='png',dpi=110,facecolor=fig.get_facecolor()); plt.close(fig)
    buf.seek(0); frames.append(Image.open(buf).convert('RGB'))
frames[3].save(OUT/'preview.png')
frames[0].save(OUT/'harmonics.gif',save_all=True,append_images=frames[1:],duration=1400,loop=0)
print('Saved assets/preview.png and assets/harmonics.gif')
