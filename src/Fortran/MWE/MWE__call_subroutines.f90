program consts
! recompile and execute the program multiple time to see the effect of undevalued variables 
! output is NaN, 3.22E-36, 6.61E-2, 1.10E+15, 3.30E+38, -1701604.75

    !implicit none  ! the whole point what happens when not used

real :: y
call sub(y)
call subba(y)
end program consts

subroutine sub(x)
    implicit none
    real x

    write (*,*) 'x= ', x
    return
end subroutine sub

subroutine subba(x)
    write (*,*) 'x= ', x
    return
end subroutine subba
