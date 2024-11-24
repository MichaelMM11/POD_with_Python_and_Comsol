exe_name="abc"
gfortran main.f90 -llapack -lblas -o $exe_name
#gfortran -o $exe_name main.f90 --llapack
./$exe_name





#clear
#ls
#echo "removing files"
##rm *.mod *.o, *.exe
#echo "compiling main file"
#gfortran -c stats.f95
#echo "building an executable"
#gfortran *.o -o stats.exe
#echo "Running the executable"
#./stats.exe
