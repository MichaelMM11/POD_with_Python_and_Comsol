
program main

IMPLICIT NONE

real :: a = 0.3
real :: b = 2.2
real :: inc = 0.3
integer :: d
integer :: i
real :: q

real :: x=0
d = (b-a) / inc
!real :: t(28)


WRITE(*,*) 'd =', d

WRITE(*,*) 'inc =', aint(inc*100)/100
!WRITE(*,*) 'mod =', mod(inc,100.)
!WRITE(*,*) 'modulo =', modulo(inc,100.)

DO i = 0, d
    q = a + inc * i
    WRITE(*,*) 'q = ', q
!    WRITE(*,'(f4.2)')  q
!    WRITE(*,*) ''
END DO






end program main
