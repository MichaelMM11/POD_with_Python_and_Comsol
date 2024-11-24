! To compile program with LAPACK:
! gfortran FILENAME.f90 -L/home/pato/src/lia/lapack -llapack -lrefblas
program main
    implicit none

    integer, parameter :: m=3,n=3 ! constants for test.

    real :: a (n,n) ! A matrix
    real :: b (n) ! B matrix
    real :: pivot(n)
    real :: rc ! return code
    a = reshape([ &
      &  2., 1., -1., &
      & -3., -1., 2., &
        -2., 1., 2.], [3, 3])

    a = transpose(a) ! From row major (human readable) to column major (LAPACK)
    b = [8., -11., -3.]
    print *, pivot(n)
    print *, rc
    call sgesv(n, 1, a, 3, pivot, b, 3, rc)
    print *, pivot(n)
    print *, rc
    print *, a
    print *, ""
    !call printmat(b, 3, 1)
    call printmat(a,3,3)
end program

subroutine printmat(a, r, c)
    implicit none
    real :: a (r,c)
    integer i,j,r,c
    do j=1, c
        do i=1, r
            WRITE (*,'(f0.4)',advance="no")  a(i,j) ! print elements
            WRITE (*,'(a)', advance="no") ", " ! separate elements with comma
        enddo
        print *, '' ! print newline
    enddo
end subroutine
