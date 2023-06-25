#!/usr/bin/gnuplot -persist

#load '~/Desktop/SSoT/GNUplot/viridis.pal'


load '~/gnuplot/settings_for_interaction.gp'
#load '~/gnuplot/settings_for_reproduction.gp'



set title "my title"
set xlabel "This 日本語 is"
set ylabel "my y axis label"



file="x.txt"
plot file u 1:2 w lp ls 1, \
     file u 1:3 w l  ls 2, \
     file u 1:4 w p  ls 3, \
     file u 1:5 w l  ls 4




pause -1 "Hit any key to continue: "

