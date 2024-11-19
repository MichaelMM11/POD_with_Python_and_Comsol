! gfortran -o dsvd -std=f2018 -Wall -pedantic -O3 -ffast-math -march=native -frecursive dsvd.f90 -lblas -larpack
! original code, https://github.com/opencollab/arpack-ng/blob/master/EXAMPLES/SVD/dsvd.f
! p110, http://li.mit.edu/Archive/Activities/Archive/CourseWork/Ju_Li/MITCourses/18.335/Doc/ARPACK/Lehoucq97.pdf
! to do, replace matmul() with dgemv (?), remove() transpose()
module svd

    use, intrinsic :: iso_c_binding, only: ik => c_int, rk => c_double
    implicit none
   
    private
   
    integer, public, parameter :: maxm = 512 ! -- max # of rows a(maxm,maxn)
    integer, public, parameter :: maxn = 256 ! -- max # of cols a(maxm,maxn)
    integer, public, parameter :: maxnev = 32 ! -- max # of singular values to compute (also max # of right singular vectors), maxnev <= maxn (?)
    integer, public, parameter :: maxncv = 16 ! -- largest # of basis vectors in in the Implicitly Restarted Arnoldi Process, optimal value (?)
    real(rk), public, parameter :: svd_level = 1.0E-6_rk ! -- singular value threshold
    integer, parameter :: ldu = maxm
    integer, parameter :: ldv = maxn
   
    public :: svd_
   
    external :: dsaupd
    external :: dseupd
   
    contains
   
    subroutine svd_(nr,nc,ns,matrix,list,rvec,lvec)
      integer, intent(in) :: nr ! number of rows
      integer, intent(in) :: nc ! number of cols
      integer, intent(in) :: ns ! number of singular values to compute
      real(rk), dimension(nr,nc), intent(in) :: matrix ! input matrix
      real(rk), dimension(ns), intent(out) :: list ! list of singular values
      real(rk), dimension(nc,ns), intent(out) :: rvec ! right singular vectors
      real(rk), dimension(nr,ns), intent(out) :: lvec ! left singular vectors
      real(rk), dimension(nc,nr) :: tmatrix ! transpose of input matrix
      real(rk), dimension(ns,ns) :: diag ! diagonal matrix
      integer :: i
   
      ! local arrays
      real(rk) :: v(ldv, maxncv) = 0.0_rk
      real(rk) :: workl(maxncv*(maxncv+8))
      real(rk) :: workd(3*maxn)
      real(rk) :: s(maxncv,2) = 0.0_rk
      real(rk) :: resid(maxn)
      real(rk) :: ax(maxm)
      logical :: select(maxncv)
      integer :: iparam(11)
      integer :: ipntr(11)
   
      ! local scalars
      character :: bmat*1
      character :: which*2
      integer :: ido
      integer :: m
      integer :: n
      integer :: nev
      integer :: ncv
      integer :: lworkl
      integer :: info
      integer :: ierr
      integer :: ishfts
      integer :: maxitr
      integer :: mode1
      integer :: nconv
      real(rk) :: tol
      real(rk) :: sigma
   
      ! transpose
      tmatrix = transpose(matrix)
   
      ! set dimensions
      m = nr
      n = nc
   
      ! arpack parameters
      nev   = ns ! # of singular values to compute, nev < n (?) nev == n (?)
      ncv   = n ! length of arnoldi factorization
      bmat  = 'I' ! OP = A'A
      which = 'LM' ! compute largest (magnitude) singular values, also LA
   
      ! arpack stopping rules and initials
      lworkl = ncv*(ncv+8) ! work array
      tol = 0.0_rk ! tolerance
      info = 0 ! initial error code
      ido = 0 ! reverse communication parameter
   
      ! arpack algorithm
      ishfts = 1   ! 0/1
      maxitr = 256 ! max number of iteraions
      mode1 = 1
      iparam(1) = ishfts
      iparam(3) = maxitr ! on out, actual number of iterations
      iparam(7) = mode1  ! mode
   
      ! main loop
      do
        call dsaupd(ido,bmat,n,which,nev,tol,resid,ncv,v,ldv,iparam,ipntr,workd,workl,lworkl,info)
        if (.not.(ido .eq. -1 .or. ido .eq. 1)) exit
        call dot (m, n, matrix, workd(ipntr(1)), ax)
        call tdot (m, n, tmatrix, ax, workd(ipntr(2)))
      end do
   
      ! compute singular vectors
      call dseupd (.true.,'All',select,s,v,ldv,sigma,bmat,n,which,nev,tol,resid,ncv,v,ldv,iparam,ipntr,workd,workl,lworkl,ierr)
   
      ! scale, note abs added for small negative vals
      nconv =  iparam(5)
      s(1:nconv,1) = sqrt(abs(s(1:nconv,1)))
   
      ! reverse
      s(1:nev,1) = s(nev:1:-1,1)
   
      ! set singular values
      list = s(1:nev,1)
   
      ! remove small
      where (list < svd_level) list = 0.0_rk
   
      ! set right vectors
      rvec(:,1:nev:1) = v(1:n,nev:1:-1)
   
      ! compute and set left vectors, u = a v s^-1
      diag = 0.0_rk
      do i = 1 , nev, 1
        if(list(i) > svd_level) diag(i, i) = 1.0_rk/list(i)
      end do
      lvec = matmul(matrix,matmul(rvec,diag))
   
    end subroutine svd_
   
    subroutine dot(row,col,matrix,x,w)
      integer, intent(in) :: row
      integer, intent(in) :: col
      real(rk), intent(in) :: matrix(row,col)
      real(rk), intent(in) :: x(col)
      real(rk), intent(out) :: w(row)
      w = matmul(matrix,x)
    end subroutine dot
   
    subroutine tdot(row,col,matrix,w,y)
      integer, intent(in) :: row
      integer, intent(in) :: col
      real(rk), intent(in) :: matrix(col,row)
      real(rk), intent(in) :: w(row)
      real(rk), intent(out) :: y(col)
      y = matmul(matrix,w)
    end subroutine tdot
   
   end module svd
