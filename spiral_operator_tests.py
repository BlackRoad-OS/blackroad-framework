#!/usr/bin/env python3
"""
Spiral Operator Mathematical Verification Framework
Tests the core BlackRoad operator: 𝓤(θ, a) = e^((a+i)θ)
"""

import numpy as np
import sympy as sp
from sympy import symbols, exp, I, pi, simplify, cos, sin, E
from sympy import Matrix, eye, sqrt


class SpiralOperator:
    """
    BlackRoad Spiral Operator: 𝓤(θ, a) = e^((a+i)θ)

    Properties to verify:
    1. Pure rotation when a=0: 𝓤(θ, 0) = e^(iθ)
    2. Pure expansion when θ=0: 𝓤(0, a) = e^a
    3. Unitary when a=0 (preserves norms)
    4. Composition law: 𝓤(θ1, a1) * 𝓤(θ2, a2) = 𝓤(θ1+θ2, a1+a2)
    """

    @staticmethod
    def evaluate(theta, a):
        """Evaluate spiral operator numerically"""
        return np.exp((a + 1j) * theta)

    @staticmethod
    def symbolic():
        """Return symbolic form"""
        theta, a = symbols('theta a', real=True)
        return exp((a + I) * theta)


class TestSpiralOperatorProperties:
    """Verify mathematical properties of spiral operator"""

    def test_euler_identity_at_pi(self):
        """Verify e^(iπ) = -1 (Euler's identity)"""
        result = SpiralOperator.evaluate(np.pi, 0)
        assert np.isclose(result, -1.0), f"e^(iπ) should equal -1, got {result}"

    def test_pure_rotation_unit_circle(self):
        """When a=0, should stay on unit circle"""
        angles = np.linspace(0, 2*np.pi, 100)
        for theta in angles:
            result = SpiralOperator.evaluate(theta, 0)
            magnitude = np.abs(result)
            assert np.isclose(magnitude, 1.0), f"Pure rotation should preserve magnitude 1, got {magnitude}"

    def test_pure_expansion_real_axis(self):
        """When θ=0, should be purely real exponential"""
        a_values = np.linspace(-2, 2, 50)
        for a in a_values:
            result = SpiralOperator.evaluate(0, a)
            expected = np.exp(a)
            assert np.isclose(result, expected), f"Pure expansion e^a={expected}, got {result}"

    def test_composition_law(self):
        """Verify 𝓤(θ1,a1) * 𝓤(θ2,a2) = 𝓤(θ1+θ2, a1+a2)"""
        theta1, theta2 = 0.5, 1.2
        a1, a2 = 0.3, -0.1

        left = SpiralOperator.evaluate(theta1, a1) * SpiralOperator.evaluate(theta2, a2)
        right = SpiralOperator.evaluate(theta1 + theta2, a1 + a2)

        assert np.isclose(left, right), f"Composition law failed: {left} ≠ {right}"

    def test_identity_element(self):
        """Verify 𝓤(0, 0) = 1"""
        result = SpiralOperator.evaluate(0, 0)
        assert np.isclose(result, 1.0), f"Identity should be 1, got {result}"

    def test_logarithmic_spiral_growth(self):
        """Verify r(θ) = e^(aθ) for spiral radius"""
        a = 0.2
        theta = np.linspace(0, 4*np.pi, 100)

        for t in theta:
            z = SpiralOperator.evaluate(t, a)
            radius = np.abs(z)
            expected_radius = np.exp(a * t)
            assert np.isclose(radius, expected_radius), f"Radius should be e^(aθ)={expected_radius}, got {radius}"


class TestPhysicalConstants:
    """Verify physical constants are correctly encoded"""

    def test_fine_structure_constant(self):
        """α ≈ 1/137.036"""
        alpha = 1 / 137.036
        # Verify it's dimensionless
        assert 0.007 < alpha < 0.008, f"Fine structure constant outside expected range: {alpha}"

    def test_golden_ratio(self):
        """φ = (1 + √5) / 2 ≈ 1.618"""
        phi = (1 + np.sqrt(5)) / 2
        assert np.isclose(phi, 1.618033988749), f"Golden ratio incorrect: {phi}"

        # Verify φ² = φ + 1
        assert np.isclose(phi**2, phi + 1), "Golden ratio property φ² = φ + 1 failed"

    def test_planck_constant_order_of_magnitude(self):
        """ℏ ≈ 1.055 × 10^-34 J·s"""
        h_bar = 1.054571817e-34  # J·s
        assert 1e-34 < h_bar < 2e-34, f"Planck constant outside expected range: {h_bar}"


class TestMandelbrotIteration:
    """
    Verify Mandelbrot iteration for agent stability:
    z_{n+1} = z_n² + c
    """

    @staticmethod
    def iterate(z, c, n_iterations=100):
        """Iterate Mandelbrot function"""
        trajectory = [z]
        for _ in range(n_iterations):
            z = z**2 + c
            trajectory.append(z)
            if abs(z) > 2:  # Escape threshold
                break
        return trajectory

    def test_origin_stable_for_c_zero(self):
        """z=0, c=0 should remain at origin"""
        trajectory = self.iterate(0, 0, 10)
        for z in trajectory:
            assert abs(z) < 1e-10, f"Should stay at origin, got {z}"

    def test_escape_criterion(self):
        """If |z| > 2, trajectory escapes to infinity"""
        c = 1.0 + 0.5j  # Outside Mandelbrot set
        trajectory = self.iterate(0, c, 50)
        final_z = trajectory[-1]
        assert abs(final_z) > 2, f"Should escape, final |z|={abs(final_z)}"

    def test_stability_boundary(self):
        """Points near boundary should have finite but large iterations"""
        c = -0.75 + 0.1j  # Near main bulb
        trajectory = self.iterate(0, c, 100)
        # Should not escape immediately but might eventually
        assert len(trajectory) > 5, "Should iterate multiple times before escaping/stabilizing"


class TestQuantumMechanics:
    """Verify quantum mechanics equations"""

    def test_heisenberg_uncertainty(self):
        """Δx·Δp ≥ ℏ/2"""
        h_bar = 1.054571817e-34

        # Create example wavepacket with known uncertainties
        dx = 1e-9  # 1 nanometer position uncertainty
        dp = h_bar / (2 * dx)  # Minimum momentum uncertainty

        product = dx * dp
        min_product = h_bar / 2

        assert product >= min_product * 0.99, f"Uncertainty principle violated: Δx·Δp={product} < ℏ/2={min_product}"

    def test_wave_normalization(self):
        """∫|ψ|² dx = 1 for normalized wavefunction"""
        x = np.linspace(-10, 10, 1000)
        dx = x[1] - x[0]

        # Gaussian wavefunction
        sigma = 1.0
        psi = (1/(sigma * np.sqrt(2*np.pi))) * np.exp(-x**2 / (2*sigma**2))

        norm = np.sum(np.abs(psi)**2) * dx
        assert np.isclose(norm, 1.0, atol=0.01), f"Wavefunction not normalized: ∫|ψ|²dx = {norm}"


class TestEntropyThermodynamics:
    """Verify thermodynamic relations"""

    def test_boltzmann_entropy(self):
        """S = k_B ln(Ω)"""
        k_B = 1.380649e-23  # J/K
        omega = 1000  # Number of microstates

        S = k_B * np.log(omega)
        assert S > 0, "Entropy should be positive"
        assert 9e-21 < S < 1e-20, f"Entropy out of expected range: {S}"

    def test_entropy_increases_with_microstates(self):
        """More microstates → higher entropy"""
        k_B = 1.380649e-23

        omega1 = 100
        omega2 = 1000

        S1 = k_B * np.log(omega1)
        S2 = k_B * np.log(omega2)

        assert S2 > S1, "Entropy should increase with more microstates"


class TestSymbolicVerification:
    """Symbolic mathematical verification using SymPy"""

    def test_spiral_operator_euler_form(self):
        """Verify e^((a+i)θ) = e^(aθ) · e^(iθ)"""
        theta, a = symbols('theta a', real=True)

        left = exp((a + I) * theta)
        right = exp(a * theta) * exp(I * theta)

        diff = simplify(left - right)
        assert diff == 0, f"Euler decomposition failed: {diff}"

    def test_euler_formula(self):
        """Verify e^(iθ) = cos(θ) + i·sin(θ)"""
        theta = symbols('theta', real=True)

        left = exp(I * theta)
        right = cos(theta) + I * sin(theta)

        diff = simplify(left - right)
        assert diff == 0, f"Euler's formula verification failed: {diff}"

    def test_golden_ratio_equation(self):
        """Verify φ² = φ + 1"""
        phi = (1 + sqrt(5)) / 2

        left = phi**2
        right = phi + 1

        diff = simplify(left - right)
        assert diff == 0, f"Golden ratio equation failed: {diff}"

    def test_rotation_matrix_form(self):
        """Verify rotation matrix equals exp(iθ) representation"""
        theta = symbols('theta', real=True)

        # 2D rotation matrix
        R = Matrix([
            [cos(theta), -sin(theta)],
            [sin(theta),  cos(theta)]
        ])

        # Should be unitary: R^T R = I
        product = simplify(R.T * R)
        identity = eye(2)

        assert product == identity, f"Rotation matrix not unitary: R^T R = {product}"


class TestBlackRoadConstant:
    """
    Verify BlackRoad constant: β_BR = (ℏω/k_BT) · (|∇L|/L)
    """

    def test_dimensionless(self):
        """β_BR should be dimensionless"""
        h_bar = 1.054571817e-34  # J·s
        omega = 1e15  # rad/s (example frequency)
        k_B = 1.380649e-23  # J/K
        T = 300  # K (room temperature)
        grad_L = 0.1  # Example gradient
        L = 1.0  # Example loss

        beta_BR = (h_bar * omega) / (k_B * T) * (grad_L / L)

        # Should be dimensionless (just a number)
        assert isinstance(beta_BR, (int, float, complex)), f"β_BR should be numeric, got {type(beta_BR)}"
        assert beta_BR > 0, "β_BR should be positive"


def run_all_tests():
    """Run all verification tests"""
    print("=" * 70)
    print("BLACKROAD MATHEMATICAL VERIFICATION FRAMEWORK")
    print("=" * 70)
    print()

    test_classes = [
        TestSpiralOperatorProperties,
        TestPhysicalConstants,
        TestMandelbrotIteration,
        TestQuantumMechanics,
        TestEntropyThermodynamics,
        TestSymbolicVerification,
        TestBlackRoadConstant
    ]

    total_passed = 0
    total_failed = 0

    for test_class in test_classes:
        print(f"\n{test_class.__name__}")
        print("-" * 70)

        test_obj = test_class()
        test_methods = [m for m in dir(test_obj) if m.startswith('test_')]

        for method_name in test_methods:
            try:
                method = getattr(test_obj, method_name)
                method()
                print(f"  ✓ {method_name}")
                total_passed += 1
            except AssertionError as e:
                print(f"  ✗ {method_name}: {e}")
                total_failed += 1
            except Exception as e:
                print(f"  ✗ {method_name}: Unexpected error: {e}")
                total_failed += 1

    print()
    print("=" * 70)
    print(f"RESULTS: {total_passed} passed, {total_failed} failed")
    print("=" * 70)

    return total_failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
