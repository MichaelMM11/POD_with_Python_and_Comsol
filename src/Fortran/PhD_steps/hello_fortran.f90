program hello

use my_lib
implicit none

integer, parameter :: len_x = 2
real, dimension (1:len_x) :: x
integer :: i

call linspace(x, 1.2, 5.4, len_x)

do i = 1,len_x
    write(*,*) i, x(i)
end do

write(*,*) "hello World from Fortran"

end program hello
