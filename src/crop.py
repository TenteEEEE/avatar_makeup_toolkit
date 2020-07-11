import os
import skimage.io as io

fdir = './data/face_3/'
fname = '0003.png'
components = ['cheek/', 'eye_brow/', 'eye_line/', 'eye_shadow/', 'lip/']
sdir = './material/'

flist = os.listdir(fdir)

cheek = io.imread(fdir+flist[0])
eye_brow_line = io.imread(fdir+flist[1])
eye = io.imread(fdir+flist[2])
lip = io.imread(fdir+flist[3])

cheek = cheek[2200:3400,300:-300]
eye_brow = eye_brow_line[:230,950:2040] 
eye_line = eye_brow_line[235:770,975:2040]
eye = eye[1800:2900, 600:-600]
lip = lip[3100:3350,1750:-1750]

io.imsave(sdir+components[0]+fname, cheek)
io.imsave(sdir+components[1]+fname, eye_brow)
io.imsave(sdir+components[2]+fname, eye_line)
io.imsave(sdir+components[3]+fname, eye)
io.imsave(sdir+components[4]+fname, lip)
