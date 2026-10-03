subroutine lln_running_mean_f95(n, running_mean)
  implicit none

  integer, intent(in) :: n
  double precision, intent(out) :: running_mean(n)
  integer, parameter :: int64 = selected_int_kind(18)
  integer(kind=int64), parameter :: multiplier = 16807_int64
  integer(kind=int64), parameter :: modulus = 2147483647_int64
  integer(kind=int64) :: state
  double precision :: observation, total, uniform_value
  integer :: i

  state = 310_int64
  total = 0.0d0

  do i = 1, n
    state = mod(multiplier * state, modulus)
    uniform_value = dble(state) / dble(modulus)
    observation = 50.0d0 + sqrt(12.0d0) * 10.0d0 * &
                  (uniform_value - 0.5d0)
    total = total + observation
    running_mean(i) = total / dble(i)
  end do
end subroutine lln_running_mean_f95
