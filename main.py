#!/usr/bin/env python
import re
import sys
from decimal import *
import gi
from numpy import *
import sympy

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, Gdk


class Calculator(Gtk.ApplicationWindow):
    isAns = False
    entry = None
    lastEntry = ""
    exact = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_default_size(250, 300)
        self.set_title("Calculator")
        self.header = Adw.HeaderBar()
        self.box1 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        grid = Gtk.Grid()
        grid.set_row_homogeneous(True)
        grid.set_column_homogeneous(True)
        grid.set_column_spacing(4)
        grid.set_row_spacing(4)
        grid.set_margin_end(4)
        grid.set_margin_start(4)
        grid.set_margin_top(4)
        grid.set_margin_bottom(4)
        clamp = Adw.Clamp.new()
        Adw.Clamp.set_tightening_threshold(clamp, 5)
        Adw.Clamp.set_child(clamp, grid)

        self.entry = Gtk.Entry()
        b0 = Gtk.Button(label="0")
        b1 = Gtk.Button(label="1")
        b2 = Gtk.Button(label="2")
        b3 = Gtk.Button(label="3")
        b4 = Gtk.Button(label="4")
        b5 = Gtk.Button(label="5")
        b6 = Gtk.Button(label="6")
        b7 = Gtk.Button(label="7")
        b8 = Gtk.Button(label="8")
        b9 = Gtk.Button(label="9")

        bAdd = Gtk.Button(label="+")
        bSub = Gtk.Button(label="-")
        bMul = Gtk.Button(label="*")
        bDiv = Gtk.Button(label="/")

        bClear = Gtk.Button(label="C")
        bEqual = Gtk.Button(label="=")
        bBack = Gtk.Button()
        bDot = Gtk.Button(label=".")
        bSin = Gtk.Button(label="sin")
        bCos = Gtk.Button(label="cos")
        bTan = Gtk.Button(label="tan")
        bSqrt = Gtk.Button(label="√")
        bPow = Gtk.Button(label="^")

        bLParen = Gtk.Button(label="(")
        bRParen = Gtk.Button(label=")")

        bBack.set_icon_name("edit-clear-symbolic")
        bClear.set_icon_name("edit-delete-symbolic")
        bClear.set_tooltip_text("Clear the entry")
        bEqual.set_tooltip_text("Calculate the equation")
        bBack.set_tooltip_text("Remove the last character")
        bDot.set_tooltip_text("Add a decimal point")
        bSin.set_tooltip_text("Sine")
        bCos.set_tooltip_text("Cosine")
        bTan.set_tooltip_text("Tangent")
        bSqrt.set_tooltip_text("Square root")
        bPow.set_tooltip_text("Power")
        bLParen.set_tooltip_text("Left Parenthesis")
        bRParen.set_tooltip_text("Right Parenthesis")
        bAdd.set_tooltip_text("Add")
        bSub.set_tooltip_text("Subtract")
        bMul.set_tooltip_text("Multiply")
        bDiv.set_tooltip_text("Divide")

        bUndo = Gtk.Button(icon_name="edit-undo-symbolic")
        self.header.pack_start(bUndo)
        bUndo.set_tooltip_text("Undo the last operation")
        bUndo.set_focus_on_click(False)
        bUndo.connect("clicked", self.undo)
        
        cExact = Gtk.CheckButton.new_with_label(label="Exact results")
        self.header.pack_start(cExact)
        cExact.set_tooltip_text("Switch between exact results (√2, 1/9) and approximate results (1.414, 0.111)")
        cExact.set_focus_on_click(False)
        cExact.connect("toggled", self.setExact)

        self.entry.set_alignment(xalign=1)

        b0.set_focus_on_click(False)
        b1.set_focus_on_click(False)
        b2.set_focus_on_click(False)
        b3.set_focus_on_click(False)
        b4.set_focus_on_click(False)
        b5.set_focus_on_click(False)
        b6.set_focus_on_click(False)
        b7.set_focus_on_click(False)
        b8.set_focus_on_click(False)
        b9.set_focus_on_click(False)
        bClear.set_focus_on_click(False)
        bDiv.set_focus_on_click(False)
        bSin.set_focus_on_click(False)
        bCos.set_focus_on_click(False)
        bTan.set_focus_on_click(False)
        bSqrt.set_focus_on_click(False)
        bPow.set_focus_on_click(False)
        bLParen.set_focus_on_click(False)
        bRParen.set_focus_on_click(False)
        bAdd.set_focus_on_click(False)
        bSub.set_focus_on_click(False)
        bMul.set_focus_on_click(False)
        bEqual.set_focus_on_click(False)
        bBack.set_focus_on_click(False)
        bDot.set_focus_on_click(False)

        # Text field (0)
        grid.attach(self.entry, 0, 0, 5, 1)

        # First row (1)
        grid.attach_next_to(bClear, self.entry, Gtk.PositionType.BOTTOM, 1, 1)
        grid.attach_next_to(bLParen, bClear, Gtk.PositionType.RIGHT, 1, 1)
        grid.attach_next_to(bRParen, bLParen, Gtk.PositionType.RIGHT, 1, 1)
        grid.attach_next_to(bSqrt, bRParen, Gtk.PositionType.RIGHT, 1, 1)
        grid.attach_next_to(bPow, bSqrt, Gtk.PositionType.RIGHT, 1, 1)

        # Second row (2)
        grid.attach(b7, 0, 2, 1, 1)
        grid.attach_next_to(b8, b7, Gtk.PositionType.RIGHT, 1, 1)
        grid.attach_next_to(b9, b8, Gtk.PositionType.RIGHT, 1, 1)
        grid.attach_next_to(bDiv, b9, Gtk.PositionType.RIGHT, 1, 1)
        grid.attach_next_to(bSin, bDiv, Gtk.PositionType.RIGHT, 1, 1)

        # Third row (3)
        grid.attach(b1, 0, 4, 1, 1)
        grid.attach_next_to(b2, b1, Gtk.PositionType.RIGHT, 1, 1)
        grid.attach_next_to(b3, b2, Gtk.PositionType.RIGHT, 1, 1)
        grid.attach_next_to(bMul, b3, Gtk.PositionType.RIGHT, 1, 1)
        grid.attach_next_to(bCos, bMul, Gtk.PositionType.RIGHT, 1, 1)

        # Fourth row (4)
        grid.attach(b4, 0, 3, 1, 1)
        grid.attach_next_to(b5, b4, Gtk.PositionType.RIGHT, 1, 1)
        grid.attach_next_to(b6, b5, Gtk.PositionType.RIGHT, 1, 1)
        grid.attach_next_to(bSub, b6, Gtk.PositionType.RIGHT, 1, 1)
        grid.attach_next_to(bTan, bSub, Gtk.PositionType.RIGHT, 1, 1)

        # Fifth row (5)
        grid.attach(b0, 0, 5, 1, 1)
        grid.attach_next_to(bDot, b0, Gtk.PositionType.RIGHT, 1, 1)
        grid.attach_next_to(bBack, bDot, Gtk.PositionType.RIGHT, 1, 1)
        grid.attach_next_to(bAdd, bBack, Gtk.PositionType.RIGHT, 1, 1)
        grid.attach_next_to(bEqual, bAdd, Gtk.PositionType.RIGHT, 1, 1)

        # Colorize buttons
        equalContext = Gtk.Widget.get_style_context(bEqual)
        Gtk.StyleContext.add_class(equalContext, "suggested-action")
        clearContext = Gtk.Widget.get_style_context(bClear)
        Gtk.StyleContext.add_class(clearContext, "destructive-action")

        # Set up event handlers
        bAdd.connect("clicked", self.printOperator)
        bSub.connect("clicked", self.printOperator)
        bMul.connect("clicked", self.printOperator)
        bDiv.connect("clicked", self.printOperator)
        bSin.connect("clicked", self.printFunction)
        bCos.connect("clicked", self.printFunction)
        bTan.connect("clicked", self.printFunction)
        bSqrt.connect("clicked", self.printFunction)
        bPow.connect("clicked", self.printFunction)

        bClear.connect("clicked", self.clear)
        bBack.connect("clicked", self.backspace)

        bLParen.connect("clicked", self.printNumber)
        bRParen.connect("clicked", self.printNumber)
        bDot.connect("clicked", self.printNumber)
        b0.connect("clicked", self.printNumber)
        b1.connect("clicked", self.printNumber)
        b2.connect("clicked", self.printNumber)
        b3.connect("clicked", self.printNumber)
        b4.connect("clicked", self.printNumber)
        b5.connect("clicked", self.printNumber)
        b6.connect("clicked", self.printNumber)
        b7.connect("clicked", self.printNumber)
        b8.connect("clicked", self.printNumber)
        b9.connect("clicked", self.printNumber)

        bEqual.connect("clicked", self.runEquation)

        self.entry.connect("activate", self.runEquation)
        # self.connect("key-press-event", self.checkKey)
        # keyname = Gdk.keyval_name(event.keyval)

        self.box1.append(grid)

        # self.set_child(self.box1)
        self.set_child(clamp)
        self.set_titlebar(self.header)

    def checkKey(self, event):
        if event.keyval == Gdk.KEY_plus:
            self.printOperator(Gtk.Button(label="+"))
        elif event.keyval == Gdk.KEY_minus:
            self.printOperator(Gtk.Button(label="-"))
        elif event.keyval == Gdk.KEY_asterisk:
            self.printOperator(Gtk.Button(label="*"))
        elif event.keyval == Gdk.KEY_slash:
            self.printOperator(Gtk.Button(label="/"))
        elif event.keyval == Gdk.KEY_Return or event.keyval == Gdk.KEY_KP_Enter or event.keyval == Gdk.KEY_equal:
            self.runEquation(Gtk.Button())
        elif event.keyval == Gdk.KEY_BackSpace:
            self.backspace(Gtk.Button())
        elif event.keyval == Gdk.KEY_Escape:
            self.clear(Gtk.Button())
        elif event.state == Gdk.ModifierType.CONTROL_MASK and event.keyval == Gdk.KEY_z:
            self.undo(Gtk.Button())
        else:
            self.printNumber(Gtk.Button(label=chr(event.keyval)))

    def runEquation(self, button):
        equation = self.entry.get_text()
        answer = self.solve(equation)
        self.lastEntry = self.entry.get_text()
        self.entry.set_text(answer)
        self.entry.set_position(-1)

    def calculateEval(self, equation):
        equation = eval(equation)
        return str(equation)
        
    # Define a function that takes a string as input and returns the evaluated result
    def solve(self, expression):
        expression = expression.replace("√", "sqrt")
    
        # Parse the string into a sympy.Expr object using the sympify() function
        expr = sympy.sympify(expression)

        # Simplify the expression using the simplify() method
        simplified = expr.simplify()
        
        self.isAns = True
        
        # Evaluate the simplified expression to a given precision and return the result as a string
        if self.exact:
            simplified = str(simplified).replace("sqrt", "√")
            if "." in simplified:
                simplified = simplified.rstrip("0").rstrip(".")
            return simplified
        else:
            simplified = str(simplified.evalf())
            if "." in simplified:
                simplified = simplified.rstrip("0").rstrip(".")
            return simplified

    def calculate(self, equation):
        answer = Decimal('0')
        temp = None

        openParenthesis = None
        closeParenthesis = None
        for i in range(len(equation)):
            c = equation[i]
            if c == '(':
                openParenthesis = i
            elif c == ')':
                closeParenthesis = i
                break


        # I should check for ^/sqrt/cos/sin/tan instead of parentheses. I should also move the calculate parentheses to before this.
        # Also, I should subtract 1 from each of the length comparisons.
        lastOperator = -1
        if openParenthesis is not None:
            cutInput = equation[openParenthesis + 1:closeParenthesis]
            tempAnswer = Decimal(self.calculate(cutInput))
            if openParenthesis >= 1 and equation[openParenthesis - 1] == '^':
                for i in range(openParenthesis - 1):
                    if equation[i] == '+' or equation[i] == '-' or equation[i] == '*' \
                            or equation[i] == '/' or equation[i] == '√' or equation[i] == '^':
                        lastOperator = i
                base = Decimal(equation[lastOperator + 1:openParenthesis - 1])
                temp = base ** tempAnswer
                equation = equation[0:lastOperator + 1] + str(temp) + equation[closeParenthesis + 1:]
            elif openParenthesis >= 1 and equation[openParenthesis - 1] == '√':
                temp = Decimal.sqrt(tempAnswer)
                equation = equation[0:openParenthesis - 1] + str(temp) + equation[closeParenthesis + 1:]
            elif openParenthesis >= 3 and equation[openParenthesis - 3] == 's' and equation[
                openParenthesis - 2] == 'i' and equation[openParenthesis - 1] == 'n':
                temp = self.sin(tempAnswer)
                equation = equation[0:openParenthesis - 3] + str(temp) + equation[closeParenthesis + 1:]
            elif openParenthesis >= 3 and equation[openParenthesis - 3] == 'c' and equation[
                openParenthesis - 2] == 'o' and equation[openParenthesis - 1] == 's':
                temp = self.cos(tempAnswer)
                equation = equation[0:openParenthesis - 3] + str(temp) + equation[closeParenthesis + 1:]
            elif openParenthesis >= 3 and equation[openParenthesis - 3] == 't' and equation[
                openParenthesis - 2] == 'a' and equation[openParenthesis - 1] == 'n':
                temp = self.sin(tempAnswer) / self.cos(tempAnswer)
                equation = equation[0:openParenthesis - 3] + str(temp) + equation[closeParenthesis + 1:]
            else:
                equation = equation[0:openParenthesis] + self.calculate(cutInput) + equation[closeParenthesis + 1:]

        if "(" in equation:
            equation = self.calculate(equation)

        products = re.split("(?=[+/*-])", equation)
        parts = products
        lastWasProduct = False

        i = 1
        while i < len(products):  # Fixes errors when you use a negative number.
            operation = products[i - 1]  # The function can work with them, but the split treats the - as an operation.
            if (operation == "+" or operation == "-" or operation == "*" or operation == "/") and products[i][0] == '-':
                products[i] = operation + products[i]
                del products[i - 1]
            else:
                i += 1

        i = 1
        while i < len(products):
            if products[i][0] == '*':
                if products[i - 1][0].isdigit() or products[i - 1][0] == '-':
                    temp = Decimal(products[i - 1]) * Decimal(products[i][1:])
                else:
                    temp = Decimal(products[i - 1][1:]) * Decimal(products[i][1:])
            elif products[i][0] == '/':
                if products[i - 1][0].isdigit() or products[i - 1][0] == '-' or products[i - 1][0] == '.':
                    temp = Decimal(products[i - 1]) / Decimal(products[i][1])
                else:
                    temp = Decimal(products[i - 1][1]) / Decimal(products[i][1])

            # TODO: Adding any decimal rounds it down, so I need to fix that
            if temp is not None:
                products[i] = str(temp)
                del products[i - 1]
                lastWasProduct = True  # Lets the next loop know to keep on the same index since I removed an element.
            elif products[i - 1][0] == '+' or products[i][0] == '+':
                if products[i - 1][0] == '+':
                    products[i - 1] = parts[i - 1][1]
                if products[i][0] == '+':
                    products[i] = parts[i][1]

            temp = None

            if not lastWasProduct:
                i += 1
            lastWasProduct = False

        for product in products:
            answer = answer + Decimal(product)

        self.isAns = True
        return str(answer)

    def printNumber(self, button):
        number = button.get_label()
        if self.isAns:
            self.entry.set_text(number)
            self.isAns = False
        else:
            self.entry.insert_text(number, self.entry.get_position())
        if self.entry.get_position() > self.entry.get_text_length() - 1 - len(number):
            self.entry.set_position(-1)
        else:
            self.entry.set_position(self.entry.get_position() + len(number))

    def printOperator(self, button):
        operator = button.get_label()
        if self.isAns:
            self.isAns = False
        self.entry.insert_text(operator, self.entry.get_position())
        if self.entry.get_position() > self.entry.get_text_length() - 1 - len(operator):
            self.entry.set_position(-1)
        else:
            self.entry.set_position(self.entry.get_position() + len(operator))

    def printFunction(self, button):
        function = button.get_label()
        function = function + "("
        if self.isAns:
            self.entry.set_text(function)
            self.isAns = False
        else:
            self.entry.insert_text(function, self.entry.get_position())
        if self.entry.get_position() > self.entry.get_text_length() - 1 - len(function):
            self.entry.set_position(-1)
        else:
            self.entry.set_position(self.entry.get_position() + len(function))

    def clear(self, button):
        self.lastEntry = self.entry.get_text()
        self.entry.set_text("")
        self.isAns = False

    def backspace(self, button):
        self.entry.delete_text(self.entry.get_position() - 1, self.entry.get_position())

    def undo(self, button):
        self.entry.set_text(self.lastEntry)
        self.isAns = False
        self.entry.set_position(-1)
        
    def setExact(self, checkbox):
        self.exact = checkbox.get_active()

    def cos(self, x):
        """Return the cosine of x as measured in radians.

        The Taylor series approximation works best for a small value of x.
        For larger values, first compute x = x % (2 * pi).

        >>> print(cos(Decimal('0.5')))
        0.8775825618903727161162815826
        >>> print(cos(0.5))
        0.87758256189
        >>> print(cos(0.5+0j))
        (0.87758256189+0j)

        """
        getcontext().prec += 2
        i, lasts, s, fact, num, sign = 0, 0, 1, 1, 1, 1
        while s != lasts:
            lasts = s
            i += 2
            fact *= i * (i - 1)
            num *= x * x
            sign *= -1
            s += num / fact * sign
        getcontext().prec -= 2
        return +s

    def sin(self, x):
        """Return the sine of x as measured in radians.

        The Taylor series approximation works best for a small value of x.
        For larger values, first compute x = x % (2 * pi).

        >>> print(sin(Decimal('0.5')))
        0.4794255386042030002732879352
        >>> print(sin(0.5))
        0.479425538604
        >>> print(sin(0.5+0j))
        (0.479425538604+0j)

        """
        getcontext().prec += 2
        i, lasts, s, fact, num, sign = 1, 0, x, 1, x, 1
        while s != lasts:
            lasts = s
            i += 2
            fact *= i * (i - 1)
            num *= x * x
            sign *= -1
            s += num / fact * sign
        getcontext().prec -= 2
        return +s


class MyApp(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.win = None
        self.connect('activate', self.on_activate)

    def on_activate(self, app):
        self.win = Calculator(application=app)
        self.win.present()


app = MyApp(application_id="com.example.GtkCalculator")
app.run(sys.argv)
