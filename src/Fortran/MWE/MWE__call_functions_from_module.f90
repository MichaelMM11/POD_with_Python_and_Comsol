! gfortran -c funct.f90 tabul.f90
! gfortran funct.o tabul.o
! ./a.out

! gfortran funct.o tabul.o my_name
! ./my_name

! gfortran funct.f90 tabul.f90 -o main

! gfortran a.f90 funct.f90 tabul.f90 -o main
program tabulate
    use user_functions
    use abc

    implicit none
    real    :: x, xbegin, xend
    integer :: i, steps

    write(*,*) 'Please enter the range (begin, end) and the number of steps:'
    read(*,*)  xbegin, xend, steps

    do i = 0, steps
        x = xbegin + i * (xend - xbegin) / steps
        write(*,'(2f10.4)') x, f(x)
        write(*,'(2f10.4)') x, h(x)
        !write(*,*) x, g(x)
    end do
end program tabulate
