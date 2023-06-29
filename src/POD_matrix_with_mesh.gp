#!/usr/bin/gnuplot -persist


#@ terminal
#==========
#set terminal pdfcairo enhanced color font ",12" size 16cm,10cm  #
#set terminal postscript eps enhanced color font ",16pt"  #size 6.4,4.8


#@ which modus
#=============
#load '~/gnuplot/settings_for_interaction.gp'
load '~/gnuplot/settings_for_reproduction.gp'


#@ view
#======



#@ key
#=====
set key outside


#@ colour
#========


#unset surface
set hidden3d


#@ colourbar
#===========
set cblabel "T (K)"
#unset colorbox


#@ x settings
#============
set xtics 1
set xlabel "length x (cm)"


#@ y settings
#===========
set ylabel "length y (cm)"


#@ plot settings
#===============
set encoding utf8
set output "mesh_POD.ps"
#file="/home/michael/Git/POD_with_Python_and_Comsol/data/merged_reduced_matrix_reduction_5.dat"
file="/home/michael/Git/POD_with_Python_and_Comsol/data/raw_data.dat"


#@ title
#=======
set title noenhanced
set title "raw_data"


# OK  16 in x, 5 in y
set view map
set pm3d map
set autoscale fix
set ytics 1
set dgrid3d 200,200,2
splot '< tr "," " " < /home/michael/Git/POD_with_Python_and_Comsol/data/raw_data.dat' using 1:2:3
unset table
unset dgrid3d
#splot file u 1:2:3 with pm3d

#splot file u 1:2:3 with points ps 3 pt 7,
#splot file u 1:2:3 with pm3d

# set view map
# set pm3d explicit at b
# set dgrid3d ,,
# splot file u 1:2:3 w pm3, file u 1:2:(1) with lines nosurface




#@ plot
#======
#splot file using 1:2:3 with pm3 notitle
#splot file with image 
#plot file with points





pause mouse close
#unset output





# set terminal gif animate delay 200 size 2014,1024
# set output "mesh.gif"
# do for [i=1:5] {
# set title sprintf("reduction with %d modes",i)
#      splot '/home/michael/Git/POD_with_Python_and_Comsol/data/merged_reduced_matrix_reduction_'.i.'.dat' using 1:2:3 with pm3
# }


# # splot '/home/michael/Git/POD_with_Python_and_Comsol/data/merged_reduced_matrix_reduction_1.dat' using 1:2:3 with pm3
# #  pause mouse close
# # splot '/home/michael/Git/POD_with_Python_and_Comsol/data/merged_reduced_matrix_reduction_2.dat' using 1:2:3 with pm3
# # pause mouse close
# # splot '/home/michael/Git/POD_with_Python_and_Comsol/data/merged_reduced_matrix_reduction_3.dat' using 1:2:3 with pm3
# # pause mouse close
# # splot '/home/michael/Git/POD_with_Python_and_Comsol/data/merged_reduced_matrix_reduction_4.dat' using 1:2:3 with pm3
# # pause mouse close
# # splot '/home/michael/Git/POD_with_Python_and_Comsol/data/merged_reduced_matrix_reduction_5.dat' using 1:2:3 with pm3


#unset output

