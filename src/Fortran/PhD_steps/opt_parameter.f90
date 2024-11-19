module my_ifaces
    implicit none
    contains
    subroutine expert(array, len, abstol, reltol)
        real :: array(:)
        integer :: len
        real, optional :: abstol, reltol
        real :: abstol0, reltol0

        abstol0 = 1e-6
        if ( present(abstol) ) abstol0 = abstol
        
        reltol0 = 1e-8
        if ( present(reltol) ) reltol0 = reltol

        ! code using abstol0 and reltol0
        print *, 'abstol =', abstol0
        print *, 'reltol =', reltol0
    end subroutine expert

    subroutine use_iface
        real :: array(100)
        call expert(array, 100)
        ! uses abstol = 1e-6, reltol = 1e-8

        call expert(array, 100, 1e-3)
        ! uses abstol = 1e-3, reltol = 1e-8

        call expert(array, 100, reltol=1e-3)
        ! uses abstol = 1e-6, reltol = 1e-3
    end subroutine use_iface
end module my_ifaces
