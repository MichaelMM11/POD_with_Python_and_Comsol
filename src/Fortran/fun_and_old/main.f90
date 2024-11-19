program main

    implicit none
    integer :: n, unit, i
    real, allocatable, dimension(:,:) :: x

    open(unit=9, file="data.dat",status="replace")
        !READ(*,*)  n, (x(i), i=1, n)
        read(*,*) x
        !allocate (x)
        !print *, x
        print *, "all fine"
        write (*,*) "all fine"
    close(unit)
    print *, n

end program main
!216
!265
