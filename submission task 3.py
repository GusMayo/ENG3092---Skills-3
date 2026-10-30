import numpy as np


class Polynomial():
    def __init__(self, coefficients):
        self.coeff = coefficients
        self.degree = len(self.coeff) - 1

    def __add__(self, other):
        P_m, P_n = compare(self, other)

        P_n_complete = complete(P_n, P_m)

        Q = Polynomial([P_m.coeff[i] + P_n_complete.coeff[i] for i in range(P_m.degree + 1)])

        return Q

    def __rmul__(self, other):
        CP_m = Polynomial([other * coeff for coeff in self.coeff])

        return CP_m

    def __sub__(self, other):
        return self + -1 * other

    def __mul__(self, other):
        P_m, P_n = compare(self, other)

        m_plus_n = P_m.degree + P_n.degree
        scaling_pol = Polynomial([0 for i in range(m_plus_n + 1)])

        P_m_comp = complete(P_m, scaling_pol)
        P_n_comp = complete(P_n, scaling_pol)
        
        flipped_coeffs = []
        for k in range(-1, -(m_plus_n + 2), -1):
            ck = 0
            for i in range(-1, k-1, -1):
                ck += P_m_comp.coeff[i] * P_n_comp.coeff[k - (i + 1)]
            flipped_coeffs.append(ck)

        coeffs = flipped_coeffs[::-1]
        P_mP_n = Polynomial(coeffs)

        return P_mP_n

    def __str__(self):
        string = ''

        for i in range(self.degree):
            string = string + str(self.coeff[i]) + 'x^' + str(self.degree - i) + ' + '

        string = string[: -5]
        string = string + ' + ' + str(self.coeff[-1])

        return string

    def __call__(self, x):
        rk = self.coeff[0]

        for k in range(self.degree, -1, -1):
            rk = self.coeff[-(k + 1)] + rk * x

        return rk
  
    def derivative(self):
        P_prime = Polynomial([self.coeff[i] * (self.degree - i) for i in range(self.degree)])

        return P_prime

    def antiderivative(self):
        P_int = Polynomial([self.coeff[i]/(self.degree + 1 - i) for i in range(self.degree + 1)])
        P_int.coeff.append(0)

        return P_int

    def definite_integral(self, a, b):
        P_m_anti = self.antiderivative()

        res = P_m_anti(b) - P_m_anti(a)

        return res


def compare(pol1, pol2):
    if pol1.degree >= pol2.degree:
        P_m = pol1
        P_n = pol2

    else:
        P_m = pol2
        P_n = pol2

    return P_m, P_n

def complete(P_n, P_m):
        degree_diff = P_m.degree - P_n.degree
        P_n_complete_coefficients = [0 for i in range(degree_diff)]

        for coeff in P_n.coeff:
            P_n_complete_coefficients.append(coeff)

        P_n_comp = Polynomial(P_n_complete_coefficients)
        return P_n_comp



P_m = Polynomial([1, 2, 3, 4, 4])
P_n = Polynomial([1, 2, 3])

print('\nAll operations:\n')
print('Given P_m(x) = ' + str(P_m))
print('and P_n(x) = ' + str(P_n) + '.\n')

print('P_m + P_n = ' + str(P_m + P_n) + '.\n')
print('2 * P_m = ' + str(2 * P_m) + '.\n')
print('P_m - P_n = ' + str(P_m - P_n) + '.\n')
print('P_n * P_n = ' + str(P_m * P_n) + '.\n')
print('P_m(x0):')
x0 = float(input('enter value for x0: '))
print('P_m(', x0, ') = ', P_m(x0), '.\n')
print('dP_m/dx = ' + str(P_m.derivative()) + '\n.')
print('int(P_m)dx = ' + str(P_m.antiderivative()) + '\n.')
print('intb/a(P_m)dx:')
a, b = float(input('enter value for a: ')), float(input('enter value for b: '))
print('intb/a(P_m)dx = ', P_m.definite_integral(a, b))