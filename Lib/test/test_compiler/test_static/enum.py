import unittest
from compiler.static.types import TypedSyntaxError

from _static import PRIM_OP_EQ_INT, TYPED_INT64

from .common import StaticTestBase


class StaticEnumTests(StaticTestBase):
    def test_mixins_unsupported(self):
        codestr = """
        from __static__ import Enum

        class Foo(int, Enum):
            pass
        """
        with self.assertRaisesRegex(
            TypedSyntaxError,
            "Static Enum types cannot support multiple bases:",
        ):
            self.compile(codestr)

    def test_subclassing_unsupported(self):
        codestr = """
        from __static__ import Enum

        class Foo(Enum):
            pass

        class Bar(Foo):
            pass
        """
        with self.assertRaisesRegex(
            TypedSyntaxError,
            "Static Enum types do not allow subclassing",
        ):
            self.compile(codestr)

    def test_non_int_unsupported(self):
        self.type_error(
            """
            from __static__ import Enum

            class Foo(Enum):
                BAR = "not an int"
            """,
            "Static enum values must be int, not str",
            at='BAR = "not an int"',
        )

    def test_int_overflow(self):
        self.type_error(
            """
            from __static__ import Enum

            class Foo(Enum):
                BAR = 2**63
            """,
            "Value 9223372036854775808 for <module>.Foo.BAR is out of bounds",
            at="BAR = 2**63",
        )

    def test_int_underflow(self):
        self.type_error(
            """
            from __static__ import Enum

            class Foo(Enum):
                BAR = -2**63 - 1
            """,
            "Value -9223372036854775809 for <module>.Foo.BAR is out of bounds",
            at="BAR = -2**63 - 1",
        )

    def test_compare_with_int_disallowed(self):
        codestr = """
        from __static__ import Enum

        class Bit(Enum):
            ZERO = 0
            ONE = 1

        def is_set(bit: Bit) -> bool:
            return bit == 1
        """
        with self.assertRaisesRegex(
            TypedSyntaxError, r"can't compare foo\.Bit to Literal\[1\]"
        ):
            self.compile(codestr, modname="foo")

    def test_compare_different_enums_disallowed(self):
        codestr = """
        from __static__ import Enum

        class Bit(Enum):
            ZERO = 0
            ONE = 1

        class Color(Enum):
            RED = 0
            GREEN = 1
            BLUE = 2

        def foo() -> bool:
            return Bit.ZERO == Color.RED
        """
        with self.assertRaisesRegex(
            TypedSyntaxError,
            r"can't compare <foo\.Bit\.ZERO: 0> to <foo\.Color\.RED: 0>",
        ):
            self.compile(codestr, modname="foo")

    def test_reverse_compare_with_int_disallowed(self):
        codestr = """
        from __static__ import Enum

        class Bit(Enum):
            ZERO = 0
            ONE = 1

        def is_set(bit: Bit) -> bool:
            return 1 == bit
        """
        with self.assertRaisesRegex(
            TypedSyntaxError, r"can't compare Literal\[1\] to foo\.Bit"
        ):
            self.compile(codestr, modname="foo")

    def test_delattr_disallowed(self):
        codestr = """
        from __static__ import Enum

        class Direction(Enum):
            NORTH = 0
            SOUTH = 1
            EAST = 2
            WEST = 3

        def north_pole() -> None:
            # You can't go north at the North Pole.
            del Direction.NORTH
        """
        with self.assertRaisesRegex(
            TypedSyntaxError, "Enum values cannot be modified or deleted"
        ):
            self.compile(codestr)

    def test_setattr_disallowed(self):
        codestr = """
        from __static__ import Enum

        class Color(Enum):
            RED = 0
            GREEN = 1
            BLUE = 2

        def redshift() -> None:
            Color.RED = -1
        """
        with self.assertRaisesRegex(
            TypedSyntaxError, "Enum values cannot be modified or deleted"
        ):
            self.compile(codestr)

    @unittest.skipUnderCinderJIT("(un)boxing not yet supported in JIT")
    def test_enum_function_arg_and_return_type(self):
        codestr = """
        from __static__ import Enum

        class Coin(Enum):
            HEADS = 0
            TAILS = 1

        def flip(coin: Coin) -> Coin:
            if coin == Coin.HEADS:
                return Coin.TAILS
            return Coin.HEADS
        """
        with self.in_strict_module(codestr) as mod:
            self.assertInBytecode(mod.flip, "PRIMITIVE_COMPARE_OP", PRIM_OP_EQ_INT)

            self.assertEqual(mod.flip(mod.Coin.HEADS), mod.Coin.TAILS)
            self.assertEqual(mod.flip(mod.Coin.TAILS), mod.Coin.HEADS)

    @unittest.skipUnderCinderJIT("(un)boxing not yet supported in JIT")
    def test_function_returns_enum(self):
        codestr = """
        from __static__ import Enum

        class Sign(Enum):
            NEGATIVE = -1
            ZERO = 0
            POSITIVE = 1

        def sign(val: float) -> Sign:
            if val < 0:
                return Sign.NEGATIVE
            if val == 0:
                return Sign.ZERO
            return Sign.POSITIVE
        """
        with self.in_strict_module(codestr) as mod:
            self.assertInBytecode(mod.sign, "PRIMITIVE_LOAD_CONST", (-1, TYPED_INT64))
            self.assertInBytecode(mod.sign, "PRIMITIVE_LOAD_CONST", (0, TYPED_INT64))
            self.assertInBytecode(mod.sign, "PRIMITIVE_LOAD_CONST", (1, TYPED_INT64))

            self.assertEqual(mod.sign(0), mod.Sign.ZERO)
            self.assertEqual(mod.sign(-42.0), mod.Sign.NEGATIVE)
            self.assertEqual(mod.sign(42.0), mod.Sign.POSITIVE)

    @unittest.skipUnderCinderJIT("(un)boxing not yet supported in JIT")
    def test_pass_enum_between_static_functions(self):
        codestr = """
        from __static__ import Enum

        class Bit(Enum):
            ZERO = 0
            ONE = 1

        def bitwise_not(bit: Bit) -> Bit:
            if bit == Bit.ZERO:
                return Bit.ONE
            return Bit.ZERO

        def bitwise_or(bit1: Bit, bit2: Bit) -> Bit:
            if bit1 == Bit.ONE or bit2 == Bit.ONE:
                return Bit.ONE
            return Bit.ZERO

        def bitwise_nor(bit1: Bit, bit2: Bit) -> Bit:
            return bitwise_not(bitwise_or(bit1, bit2))
        """
        with self.in_strict_module(codestr) as mod:
            self.assertEqual(mod.bitwise_nor(mod.Bit.ZERO, mod.Bit.ZERO), mod.Bit.ONE)
            self.assertEqual(mod.bitwise_nor(mod.Bit.ZERO, mod.Bit.ONE), mod.Bit.ZERO)
            self.assertEqual(mod.bitwise_nor(mod.Bit.ONE, mod.Bit.ZERO), mod.Bit.ZERO)
            self.assertEqual(mod.bitwise_nor(mod.Bit.ONE, mod.Bit.ONE), mod.Bit.ZERO)

    @unittest.skipUnderCinderJIT("(un)boxing not yet supported in JIT")
    def test_call_converts_int_to_enum(self):
        codestr = """
        from __static__ import Enum

        class Bit(Enum):
            ZERO = 0
            ONE = 1

        def convert_to_bit(num: int) -> Bit:
            return Bit(num)
        """
        with self.in_strict_module(codestr) as mod:
            self.assertEqual(mod.convert_to_bit(0), mod.Bit.ZERO)
            self.assertEqual(mod.convert_to_bit(1), mod.Bit.ONE)

    @unittest.skipUnderCinderJIT("(un)boxing not yet supported in JIT")
    def test_primitive_unbox_shadowcode(self):
        codestr = """
        from __static__ import Enum

        class Bit(Enum):
            ZERO = 0
            ONE = 1

        def convert_to_bit(num: int) -> Bit:
            return Bit(num)
        """
        with self.in_strict_module(codestr) as mod:
            for _ in range(100):
                self.assertEqual(mod.convert_to_bit(0), mod.Bit.ZERO)
                self.assertEqual(mod.convert_to_bit(1), mod.Bit.ONE)
