program hak
implicit none




!integer :: RES

!real :: array(23644)
!real, allocatable :: array(50,50)
!real, dimension(200,25) :: array

integer :: unit
integer :: ncol, nrow
!real :: array(100)

!real :: array(23644)
!real(kind=8), dimension(nrow, ncol), allocatable :: array(:,:)
!real, dimension(:,:), allocatable :: array(:,:)

real, allocatable, dimension(:,:) :: array



READ  (*,*)  nrow, ncol
WRITE (*,*) "nrow = ", nrow
WRITE (*,*) "ncol = ", ncol

!real :: array(23644)
WRITE (*,*) "x = ", nrow * ncol


open(newunit=unit,file="simple_data.dat",status="old")
read(unit,*) array(1,1)
print *, array
print *, "all fine"
close(unit)


end program
