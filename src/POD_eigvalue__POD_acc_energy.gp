#!/usr/bin/gnuplot -persist


set encoding utf8
set terminal pdfcairo enhanced color font "Computer-Modern,14" size 17cm,10.5cm



#load '~/gnuplot/settings_for_interaction.gp'
load '~/gnuplot/settings_for_reproduction.gp'

file="/home/michael/Git/POD_with_Python_and_Comsol/data/eigenvalue_energy_table.dat"


set style line 1 linecolor rgb "#FC2D2D" \
                 linewidth 1.25 \
                 dashtype "--" \
                 pointtype 7 \
                 pointsize 0.75

set output "POD__eigenvalue.pdf"
set xlabel "Mode number"
set xtics 1

set yrange[0:*]
set ylabel "Eigenvalue λ_i"
#set logscale y

set key left bottom

plot file u 1:2 with linespoints \
                ls 1




set output "POD__acc_energy.pdf"
set ylabel 'acc. Energy'

plot file u 1:6 with linespoints \
                ls 1

unset output
