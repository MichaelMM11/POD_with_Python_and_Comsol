!gfortran abc.f90  ! -> a.out
!gfortran -c abc.f90  !-> abc.o
!gfortran abc.o -o fac  ! ./fac
!gfortran abc.f90 - fact  ! ./fact
!./abt > tat.txt  ! execution text is written into file
! x(0:n) = [(i*increment, i=0,n)]  ! same as do i=0,1 x(i)...end do
!! print matrix neatly for the eye
! do i = 1,3
!     do j = 1,3
!         write(*,'f8.3,t3', advance='no'), mat(i,j)
!     end do
!     write(*,*)
! end do
!!=========
!   print *, "The Matrix is:"
!   do i = 1.3
!            write (*, 10) (mat (i, j), j = 1,3)
!        end do
!   10format (1000000f8.3)
  
!     print *, "The Sliced Matrix is:"
!     do i = 1,2
!            write (*, 10) (slice (i, j), j = 1,2)
!        end do


! INSTALLATION
! https://www.netlib.org/lapack/explore-html/d3/dcc/md__r_e_a_d_m_e.html#autotoc_md1
! https://www.youtube.com/watch?v=fFO7Kt5gXC4
! sudo apt-get install liblapack3
! apt-cache policy liblapack3
!gfortran main.f90 -llapack



! https://github.com/arunprasaad2711/Youtube_Tutorials/blob/master/Fortran%20Programs/Lapack_ex1/lapack_ex2.f95
program readfromfile

    ! implicit none

    ! integer, parameter :: sp = selected_real_kind(6, 37)
    ! integer, parameter :: dp = selected_real_kind(15, 307)
    ! integer, parameter :: qp = selected_real_kind(33, 4931)

    ! real(kind=dp), parameter :: pi = 4.0_dp*atan(1.0_dp)  ! 2*asin(1.), 2*acos(0.)

    ! integer :: row=2, col=4, i, j  !, lines_in_file
    ! real(kind=dp), allocatable :: cs(:,:), ds(:,:)
    ! character (len = 20) file_out_name, file_in_name

    implicit none
    integer, parameter :: n = 3
    real(kind=8), dimension(n) :: x, b
    real(kind=8), dimension(n,n) :: a, aiu, s, u, vt, work
    integer :: i, info, lda, ldb, nrhs
    integer, dimension(n) :: ipiv
    
    character (len=1) :: jobz
    integer :: m
    integer :: ldu, ldvt, lwork
    integer, dimension(24) :: iwork

    ! a = reshape((/3.0,2.0,-1.0,2.0,-2.0,0.5,-1.0,4.0,-1.0/),(/n,n/))
    ! a = reshape((/1, 0, 2, 1, 2, 5, 1, 5, -1/),(/n,n/))  ! pass in col-major syntax, i.e. row is running, col is fixed during initialisation
    ! a = reshape((/2, 0, 0, 0, 3, 4, 0, 4, 9/),(/n,n/))

    a = reshape((/-1.01, 3.98, 3.98, 0.86, 0.53, 0.53, -4.60, -7.04, -7.04/),(/n,n/))
    !a = reshape((/-1.01, 0.86, -4.60, 3.98, 0.53, -7.04, 3.98, 0.53, -7.04/),(/n,n/))
    !a = reshape((/1, 4, 7, 2, 5, 8, 3, 6, 9/), (/n,n/))

    b = (/1.0, -2.0, 0.0/)
    b = (/6, -4, 27/)
    x = b
    print *, 'a=', a
    print *, 'b=', b



    nrhs = 1 ! number of right hand sides in b
    lda = n  ! leading dimension of a
    ldb = n  ! leading dimension of b

    call dgesv(n, nrhs, a, lda, ipiv, x, ldb, info)


    jobz = 'a'
    m = n

    a = aiu
    lda = m
    s = aiu
    u = aiu
    ldu = 3
    vt = aiu
    ldvt = 3
    work = aiu
    lwork = 80






    call dgesdd(jobz, m, n, a, lda, s, u, ldu, vt, ldvt, work, lwork, iwork, info)

    print *, 'after dgesdd'
    print *,'jobz= '
    print *, jobz
    print *,'m= '
    print *, m
    print *,'n= '
    print *, n
    print *,'a= '
    print *, a
    print *,'lda= '
    print *, lda
    print *,'s= '
    print *, s
    print *,'u= '
    print *, u
    ! print *,'ldu= '
    ! print *, ldu
    ! print *,'vt= '
    ! print *, vt
    ! print *,'ldvt= '
    ! print *, ldvt
    ! print *,'work= '
    ! print *, work
    ! print *,'lwork= '
    ! print *, lwork
    ! print *,'iwork= '
    ! print *, iwork
    ! print *,'info= '
    ! print *, info

    ! print *, IPIV

    ! print *, " The Solution Using the lapack subroutine is:"
    
    ! do i=1,n
    !     print '("X",i1," is:",f16.6)', i,x(i)
    ! end do


!     file_in_name  = 'sample.dat'
!     file_out_name = "output.txt"

!     allocate(cs(row, col))

!     open(unit=15,file=file_in_name, status='old')
!     read(15,*) ((cs(i,j), j=1,col), i=1,row)

 
!     !print *, cs
!     ds= TRANSPOSE(cs)
!     !print *, ds

!     open ( unit = 17, file = file_out_name, status = 'replace' )
!     write ( 17, '(a)'       ) '#  ' // trim ( file_out_name )
!     !print *, ds
!     do i = 1, row
!         !write (17,*) ((ds(i,j), j=1,col), i=1,row)
!         write (17,*) cs(i,:)
!     end do
! write (17,*) 'abc'
!      do j = 1, col
!          !write (17,*) ((ds(i,j), j=1,col), i=1,row)
!          write (17,*) ds(:,j)
!      end do

!     ! close ( unit = 17 )









!     !  N = lines_in_file('sample.txt') ! a function I wrote, which works correctly
!     !  write ( *, * ) ' ', N
!       allocate(cs(row, col))

!       open(unit=15,file='sample.txt', status='old')
!       !read(15,*) cs
      
!       read(15,*) ((cs(i,j), j=1,col), i=1,row)  ! to guarantee first all rows of col#1, then all rows of col#2...  ! https://community.intel.com/t5/Intel-Fortran-Compiler/Read-two-dimensional-array/m-p/1182856
!      print *, cs

!       print *, "1,1", cs(1,1)
!       print *, "2,1", cs(2,1)
!       print *, "1,2", cs(1,2)
!       print *, "2,2", cs(2,2)
!       print *, "1,3", cs(1,3)
!       print *, "2,3", cs(2,3)
!       print *, "1,:", cs(1,:)
!       print *, "2,:", cs(2,:)
!       print *, ":,1", cs(:,1)
!       print *, ":,2", cs(:,2)
!       print *, ":,3", cs(:,3)
!       print *, " "
!       print *, cs
!       print *, " "

!     !   do j=1,col
!     !     do i=1,row
!     !         ds(i,j) = 1!cs(i,j)
!     !     enddo
!     ! enddo
!     print *, ''
!     print *, 2*cs
!     !   print *, shape(cs)
!     !   print *, size(cs)
!     !    do i=1,row
!     !     do j=1,col
!     !          print *, 'i=', i
!     !          print *, 'j=', j
!     !         print *, cs(i,j)!, cs(i,2)
!     !     enddo
!     !     enddo
! !         print *, shape(reshape(cs, [3,2]))
! !         cs = reshape(cs, [3,2])
! !         !       write ( *, * ) ' '
! ! !       write ( *, * ) ' ', cs
! !        print *, cs
! ! !       print *, cs(2,2)
! !        do, i=1,col
! !         write(*,*) cs (i,:)
! !     enddo
    print *, 'all fine'
end program readfromfile
