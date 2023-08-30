#!/usr/bin/gnuplot -persist


file="/home/michael/Desktop/FreeFEM/Th.msh"

#@ which modus
#=============
load '~/gnuplot/settings_for_interaction.gp'
#load '~/gnuplot/settings_for_reproduction.gp'


#@ plot
#======

plot file u 2:3 w lp
#plot sin(x)





pause -1 "hit"