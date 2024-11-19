program ch0707
implicit none
real , dimension(-180:180) :: Time = 0
integer :: Degree,Strip
real :: value
do Degree = -180,165,15
value = Degree/15.
do Strip = 0,14
   Time(Degree + Strip) = value
enddo
enddo
do Degree = -180,180
    print *,Degree,' ',Time(Degree)
end do
end program ch0707
