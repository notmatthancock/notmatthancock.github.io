subroutine inner_product(x, y, n)
    integer i, n
    real(8), dimension(n) :: x,y
    real(8) :: z = dble(0.0)

    !f2py intent(in) x, y
    !f2py intent(hide), depend(x) :: n=shape(x,0)
    !f2py intent(out) z

    do i=1,n
        z = z + x(i)*y(i)
    end do
end subroutine
