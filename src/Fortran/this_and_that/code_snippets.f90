integer, parameter :: sp = selected_real_kind(6, 37)
integer, parameter :: dp = selected_real_kind(15, 307)
integer, parameter :: qp = selected_real_kind(33, 4931)
! angle alpha = (atan(y/x)*180/pi)  ! in degrees

real, parameter :: eps = 0.0000001  ! epsilon

real(kind=dp), parameter :: pi = 4.0_dp*atan(1.0_dp)  ! 2*asin(1.), 2*acos(0.)
real*8, allocatable :: cs(:,:), ds(:,:)

real(kind=dp), parameter :: tol = 1e-9_dp
