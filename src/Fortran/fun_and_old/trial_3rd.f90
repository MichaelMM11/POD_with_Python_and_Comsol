program readfromfile
    implicit none
  
      integer :: row=2, col=3, i, j!, lines_in_file
      real*8, allocatable :: cs(:,:), ds(:,:)
  
    !  N = lines_in_file('sample.txt') ! a function I wrote, which works correctly
   !  write ( *, * ) ' ', N
      allocate(cs(row, col))

      open(unit=15,file='sample.txt', status='old')
      !read(15,*) cs
      
      read(15,*) ((cs(i,j), j=1,col), i=1,row)  ! to guarantee first all rows of col#1, then all rows of col#2...  ! https://community.intel.com/t5/Intel-Fortran-Compiler/Read-two-dimensional-array/m-p/1182856
     print *, cs

      print *, "1,1", cs(1,1)
      print *, "2,1", cs(2,1)
      print *, "1,2", cs(1,2)
      print *, "2,2", cs(2,2)
      print *, "1,3", cs(1,3)
      print *, "2,3", cs(2,3)
      print *, "1,:", cs(1,:)
      print *, "2,:", cs(2,:)
      print *, ":,1", cs(:,1)
      print *, ":,2", cs(:,2)
      print *, ":,3", cs(:,3)
      print *, " "
      print *, cs
      print *, " "

    !   do j=1,col
    !     do i=1,row
    !         ds(i,j) = 1!cs(i,j)
    !     enddo
    ! enddo
    print *, ''
    print *, 2*cs
    !   print *, shape(cs)
    !   print *, size(cs)
    !    do i=1,row
    !     do j=1,col
    !          print *, 'i=', i
    !          print *, 'j=', j
    !         print *, cs(i,j)!, cs(i,2)
    !     enddo
    !     enddo
!         print *, shape(reshape(cs, [3,2]))
!         cs = reshape(cs, [3,2])
!         !       write ( *, * ) ' '
! !       write ( *, * ) ' ', cs
!        print *, cs
! !       print *, cs(2,2)
!        do, i=1,col
!         write(*,*) cs (i,:)
!     enddo
    
   end
