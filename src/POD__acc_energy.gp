#!/usr/bin/gnuplot -persist


#@ terminal
#==========
set terminal pdfcairo enhanced color font ",12" size 16cm,10cm  #
#set terminal postscript eps enhanced color font ",16pt" #size 6.4,4.8


#@ which modus
#=============
#load '~/gnuplot/settings_for_interaction.gp'
load '~/gnuplot/settings_for_reproduction.gp'


#@ modifications to settings
#===========================
set style line 1 linecolor rgb "#FC2D2D" \
                 linewidth 1.25 \
                 dashtype "--" \
                 pointtype 7 \
                 pointsize 0.75


#@ x settings
#============
set xlabel "Mode number"
set xtics 1
set xrange[0:8]


#@ y settings
#============
set ylabel 'acc. Energy'
set yrange[*:*]


#@ plot settings
#===============
set encoding utf8
set key autotitle columnheader
set key right bottom
set key noenhanced
set output "POD__acc_energy.pdf"


#@ plot
#======
file="/home/michael/Git/POD_with_Python_and_Comsol/data/eigenvalue_energy_table.dat"
plot file u 1:6 with linespoints \
                ls 1


unset output
