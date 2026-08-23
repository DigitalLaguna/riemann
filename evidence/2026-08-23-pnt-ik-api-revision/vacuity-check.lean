-- Vacuity check for the ORIGINAL lemma 3 hypothesis (commit 0197a66):
--   (hpos : ∀ n, 0 < f n)  with  f : ArithmeticFunction ℝ  (= ZeroHom ℕ ℝ)
-- ArithmeticFunction.map_zero gives f 0 = 0, so hpos 0 : 0 < 0 => False.
import Mathlib.Data.Real.Basic
import Mathlib.NumberTheory.ArithmeticFunction.Defs

example (f : ArithmeticFunction ℝ) (hf : f.IsMultiplicative)
    (hpos : ∀ n, 0 < f n) : False := by
  have := hpos 0
  simp at this
