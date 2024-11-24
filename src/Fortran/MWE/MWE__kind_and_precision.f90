program readfromfile
! missing
! to understand the differences between kind= and 1.0_sp
! - https://stackoverflow.com/questions/838310/fortran-90-kind-parameter
    implicit none
! https://hogback.atmos.colostate.edu/fortran/docs/fortran2012.key-6.pdf
! https://annefou.github.io/Fortran/basics/variables.html

! kind
! ====
! - represents twice the number + 1 of digits that are stored/displayed,
!    i.e. kind=4 means there will be 2*4+1 digits stored
! - the precision, however, tells how 'precise/accurate' the value
!    of the number is, i.e. you can store 16 digits of 1/3 but when the
!    precision is sp, then only 6+1 digits will be 'correct'
! - so kind deals with the 'length' and _sp deals with the 'correctness
! - kind represents the number of bytes as storage
! - so kind does not determine the precision, just how many digits will be 
! - _sp|dp|qp means accuracy, sp|dp|qp means digits
! - actually makes in theory sense to have ks,kd,kq to represent
!     the value in kind=, but it's much easier and no overhead to be a bit
!     of sloppy here and make number_of_digits=accuracy(number_of_correct_digits)
    
    ! https://fortranwiki.org/fortran/show/Real+precision
    ! print HAS TO come after variable declaration
    integer, parameter :: sp = selected_real_kind(6, 37)
    integer, parameter :: dp = selected_real_kind(15, 307)
    integer, parameter :: qp = selected_real_kind(33, 4931)
    ! angle alpha = (atan(y/x)*180/pi)  ! in degrees

    ! real(kind=r8), parameter :: pi=4.0_r8*atan(1.0_r8)  ! 2*asin(1.), 2*acos(0.)
    ! - play with 'kind' and _sp, _dp,_qp so see the interaction of
    !    'length' and 'accuracy'
    real(kind=sp), parameter :: pi_sp =4.0_sp*atan(1.0_sp)
    real(kind=dp), parameter :: pi_dp =4.0_sp*atan(1.0_sp)
    real(kind=qp), parameter :: pi_qp =4.0_sp*atan(1.0_sp)

    real(kind=4)  :: a = 1_sp/3._sp
    real(kind=8)  :: b = 1_sp/3._sp
    real(kind=16) :: c = 1_sp/3._sp

    real(kind=sp) :: x= 1_sp/3.0_sp
    real(kind=dp) :: y= 1_dp/3.0_dp
    real(kind=qp) :: z= 1_qp/3.0_qp

    real(kind=sp) :: sp_sp= 1_sp/3.0_sp
    real(kind=sp) :: sp_dp= 1_dp/3.0_dp
    real(kind=sp) :: sp_qp= 1_qp/3.0_qp

    real(kind=dp) :: dp_sp= 1_sp/3.0_sp
    real(kind=dp) :: dp_dp= 1_dp/3.0_dp
    real(kind=dp) :: dp_qp= 1_qp/3.0_qp

    real(kind=qp) :: qp_sp= 1_sp/3.0_sp
    real(kind=qp) :: qp_dp= 1_dp/3.0_dp
    real(kind=qp) :: qp_qp= 1_qp/3.0_qp

    print *, 'sp = ', sp
    print *, 'dp = ', dp
    print *, 'qp = ', qp

    print *, ''

    print *, "a = ", a
    print *, "b = ", b
    print *, "c = ", c

    print *, ''

    print *, "x = ", x
    print *, "y = ", y
    print *, "z = ", z

    print *, ''

    print *, 'pi    =    3.14159265358979323846264338327950288... (real value)'
    print *, "pi_sp = ", pi_sp
    print *, "pi_dp = ", pi_dp
    print *, "pi_qp = ", pi_qp

    print *, ''

    print *, "sp_sp = ", sp_sp
    print *, "sp_dp = ", sp_dp, "Change of value in conversion from 'REAL(8)' to 'REAL(4)'"
    print *, "sp_qp = ", sp_qp, "Change of value in conversion from 'REAL(16)' to 'REAL(4)'"

    print *, ''

    print *, "dp_sp = ", dp_sp
    print *, "dp_dp = ", dp_dp
    print *, "dp_qp = ", dp_qp, "Change of value in conversion from 'REAL(16)' to 'REAL(8)'"

    print *, ''

    print *, "qp_sp = ", qp_sp
    print *, "qp_dp = ", qp_dp
    print *, "qp_qp = ", qp_qp

end program readfromfile
