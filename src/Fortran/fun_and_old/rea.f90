program example_loadtxt
  use stdlib_io, only: loadtxt
  implicit none
  real, allocatable :: x(:, :)
  call loadtxt('from_Comsol_odd_timesteps.txt', x)

  ! Can also use list directed format if the default read fails.
!  call loadtxt('example.dat', x, fmt='*')
end program example_loadtxt

