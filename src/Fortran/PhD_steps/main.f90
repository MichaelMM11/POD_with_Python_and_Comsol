program main
    implicit none

    ! constants
    integer, parameter :: sp = selected_real_kind(6, 37)
    integer, parameter :: dp = selected_real_kind(15, 307)
    integer, parameter :: qp = selected_real_kind(33, 4931)

    ! parameter
    integer :: row, col, i, j, k, stat, n

    real(kind=dp), allocatable :: M(:,:), ds(:,:), x

    character (len=20) file_out_name, file_in_name


    ! parameter declaration
    !file_in_name  = 'sample.dat'
    file_out_name = "output.txt"


    ! wip
    !allocate(M(:, 3))
    print *, 'pass filename'
    read(*,*) file_in_name
    print *, "your input was ", file_in_name

    print *, 'pass the dimension of the file'
    read(*,*) row, col
    print *, "the allocated matrix dimension will be:"
    print *, "rows: ", row
    print *, "cols: ", col
    allocate(M(row, col))

    open(unit=15, file=file_in_name, status='old')
    read(15,*) ((M(i,j), i=1,row), j=1,col)
    close(15)
    print *, "M=", M
    print *, "M_row=", size(M, 1)
    print *, "M_col=", size(M, 2)
    print *,""

    ! works not
    print *, ""
    print *, "M(1,:)=", M(1,:)
    print *, "M(2,:)=", M(2,:)
    print *, "M(3,:)=", M(3,:)
    print *, "M(4,:)=", M(4,:)

    print *, ""
    print *, "M(:,1)=", M(:,1)
    print *, "M(:,2)=", M(:,2)
    print *, "M(:,3)=", M(:,3)
    print *, "M(:,4)=", M(:,4)

    print *, ""
    print *, "M(1,1)=", M(1,1)
    print *, "M(1,2)=", M(1,2)
    print *, "M(1,3)=", M(1,3)
    print *, "M(1,4)=", M(1,4)
    
    print *, ""
    print *, "M(2,1)=", M(2,1)
    print *, "M(2,2)=", M(2,2)
    print *, "M(2,3)=", M(2,3)
    print *, "M(2,4)=", M(2,4)

    print *, ""
    print *, "M(3,1)=", M(3,1)
    print *, "M(3,2)=", M(3,2)
    print *, "M(3,3)=", M(3,3)
    print *, "M(3,4)=", M(3,4)

    print *, ""
    print *, "M(4,1)=", M(4,1)
    print *, "M(4,2)=", M(4,2)
    print *, "M(4,3)=", M(4,3)
    print *, "M(4,4)=", M(4,4)

    ! print *, M(2,1)
    ! print *, M(2,2)
    ! print *, M(2,3)
    ! print *, M(2,4)

     open(1, file=file_out_name, status='replace')

     !sample.dat
     !3 4
     ! this works
     do j=1,col
       ! write(1,'("|")',advance='no')
        do i=1,row
            write(1,'(f8.3,t3)',advance='no') M(i,j)
        end do
       write(1,'("")')
    end do

    !do i = 1, row
        ! do i=1, col
        !     write(1,*) M(:,i)
        ! end do
    !end do
    ! close(1)
    ! print *, size(M,1)
    ! print *, size(M,2)

    !close(17)
    !call printmat(M, row, col)
    ! do i=1,row
    !     write (*,*) M(i,:) ! unlimited format used, with 6 positions for each integer, separated by a space
    ! end do
    ! do j = 1, col
    !     do i = 1, row
    !         WRITE (*,'(f0.4)',advance="no")  M(i,j)
    !     end do
    ! end do

    !open(unit=15, file=file_in_name, status='old')

    !    read(*,*) i, M(1:i)
!    print *, i  !,j, k
    ! read(15,*) ((snapshotM(i,j), j=1,col), i=1,row)
    ! row = size(snapshotM, dim=1)
    ! col = size(snapshotM, dim=2)
    ! print *, row
    ! print *, col
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





end program main


subroutine printmat(a, r, c)
    implicit none
    real(kind=8) :: a (r,c)
    integer i,j,r,c
    do i=1, r
        do j=1,c
            WRITE (*,'(f0.4)',advance="no")  a(i,j) ! print elements
            WRITE (*,'(a)', advance="no") ", " ! separate elements with comma
        enddo
        print *, '' ! print newline
    enddo
end subroutine
