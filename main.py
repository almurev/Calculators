import sys
import math
from PyQt6.QtWidgets import QApplication, QMainWindow
from ui_calculators import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # -------------------------
        # подключения кнопок
        # -------------------------
        self.percentCalc1.clicked.connect(self.calc_percent1)
        self.percentCalc2.clicked.connect(self.calc_percent2)
        self.percentCalc3.clicked.connect(self.calc_percent3)
        self.percentCalc4.clicked.connect(self.calc_percent4)

        self.gcdCalc.clicked.connect(self.calc_gcd_lcm)
        self.lamCalc.clicked.connect(self.calc_laminate)
        self.vatCalc.clicked.connect(self.calc_vat)
        self.matCalc.clicked.connect(self.calc_matrix)

        self.rate10.clicked.connect(lambda: self.vatRate.setText("10"))
        self.rate18.clicked.connect(lambda: self.vatRate.setText("18"))
        self.rate20.clicked.connect(lambda: self.vatRate.setText("20"))

        # -------------------------
        # ВАЖНО: динамика интерфейса
        # -------------------------
        self.rb2.toggled.connect(self.update_gcd_ui)
        self.rb3.toggled.connect(self.update_gcd_ui)
        self.rb4.toggled.connect(self.update_gcd_ui)

        self.aRows.currentIndexChanged.connect(self.update_matrix_ui)
        self.aCols.currentIndexChanged.connect(self.update_matrix_ui)
        self.bRows.currentIndexChanged.connect(self.update_matrix_ui)
        self.bCols.currentIndexChanged.connect(self.update_matrix_ui)

        self.update_gcd_ui()
        self.update_matrix_ui()

    # =========================
    # ПОКАЗ / СКРЫТИЕ НОД/НОК
    # =========================
    def update_gcd_ui(self):

        self.num3.setVisible(False)
        self.num4.setVisible(False)
        self.gcdL3.setVisible(False)
        self.gcdL4.setVisible(False)

        if self.rb3.isChecked():
            self.num3.setVisible(True)
            self.gcdL3.setVisible(True)

        if self.rb4.isChecked():
            self.num3.setVisible(True)
            self.num4.setVisible(True)
            self.gcdL3.setVisible(True)
            self.gcdL4.setVisible(True)

    # =========================
    # МАТРИЦЫ (2×2 / 3×3)
    # =========================
    def update_matrix_ui(self):

        rows_a = int(self.aRows.currentText())
        cols_a = int(self.aCols.currentText())
        rows_b = int(self.bRows.currentText())
        cols_b = int(self.bCols.currentText())

        for i in range(1, 4):
            for j in range(1, 4):

                getattr(self, f"a_{i}_{j}").setVisible(i <= rows_a and j <= cols_a)
                getattr(self, f"b_{i}_{j}").setVisible(i <= rows_b and j <= cols_b)
                getattr(self, f"c_{i}_{j}").setVisible(True)

    # =========================
    # ПРОЦЕНТЫ
    # =========================
    def calc_percent1(self):
        try:
            p = float(self.percentEditPercent.text())
            n = float(self.percentEditNumber.text())
            self.percentResult1.setText(f"{n} → {p}% = {n*p/100:.2f}")
        except:
            self.percentResult1.setText("Ошибка")

    def calc_percent2(self):
        try:
            x = float(self.percentEditX.text())
            y = float(self.percentEditY.text())
            self.percentResult2.setText(f"{x} = {x/y*100:.2f}% от {y}")
        except:
            self.percentResult2.setText("Ошибка")

    def calc_percent3(self):
        try:
            p = float(self.percentAddPercent.text())
            n = float(self.percentAddNumber.text())
            self.percentResult3.setText(f"{n} + {p}% = {n + n*p/100:.2f}")
        except:
            self.percentResult3.setText("Ошибка")

    def calc_percent4(self):
        try:
            n = float(self.percentSubNumber.text())
            p = float(self.percentSubPercent.text())
            self.percentResult4.setText(f"{n} - {p}% = {n - n*p/100:.2f}")
        except:
            self.percentResult4.setText("Ошибка")

    # =========================
    # НОД / НОК
    # =========================
    def calc_gcd_lcm(self):

        try:

            values = []

            # первое и второе число всегда есть
            values.append(int(self.num1.text()))
            values.append(int(self.num2.text()))

            # если выбрано 3 числа
            if self.rb3.isChecked():
                values.append(int(self.num3.text()))

            # если выбрано 4 числа
            elif self.rb4.isChecked():
                values.append(int(self.num3.text()))
                values.append(int(self.num4.text()))

            # НОД
            gcd_result = values[0]

            for value in values[1:]:
                gcd_result = math.gcd(gcd_result, value)

            # НОК
            lcm_result = values[0]

            for value in values[1:]:
                lcm_result = abs(lcm_result * value) // math.gcd(lcm_result, value)

            self.gcdResult1.setText(f"НОД = {gcd_result}")
            self.gcdResult2.setText(f"НОК = {lcm_result}")

        except ValueError:
            self.gcdResult1.setText("Ошибка ввода")
            self.gcdResult2.setText("")

    # =========================
    # ЛАМИНАТ
    # =========================
    def calc_laminate(self):

        try:
            import math

            # комната (см)
            room_len = float(self.roomLen.text())
            room_width = float(self.roomWidth.text())

            # панели (мм → см)
            panel_len = float(self.panelLen.text()) / 10
            panel_width = float(self.panelWidth.text()) / 10

            pack = float(self.packCount.text())

            # --------------------------
            # направление укладки
            # --------------------------
            coef = 1.0

            # по ширине (меняем местами)
            if self.dirWidth.isChecked():
                room_len, room_width = room_width, room_len

            # диагональ → запас
            if self.dirDiag45.isChecked() or self.dirDiag135.isChecked():
                coef = 1.1

            # --------------------------
            # методичка (ряды)
            # --------------------------

            rows = room_width / panel_width
            in_row = room_len / panel_len

            panels = math.ceil(rows * in_row * coef)
            packs = math.ceil(panels / pack)

            self.lamResult1.setText(f"Панелей: {panels}")
            self.lamResult2.setText(f"Упаковок: {packs}")

        except:
            self.lamResult1.setText("Ошибка")
            self.lamResult2.setText("")

    # =========================
    # НДС
    # =========================
    def calc_vat(self):

        total = float(self.vatSum.text())
        rate = float(self.vatRate.text())

        if self.vatAdd.isChecked():
            vat = total * rate / 100
            self.vatRes1.setText(f"{vat:.2f}")
            self.vatRes2.setText(f"{total + vat:.2f}")
        else:
            vat_inside = total * rate / (100 + rate)
            self.vatRes1.setText(f"{vat_inside:.2f}")
            self.vatRes2.setText(f"{total - vat_inside:.2f}")

    # =========================
    # МАТРИЦЫ
    # =========================
    def get_val(self, obj):
        try:
            return float(obj.text())
        except:
            return 0.0

    def calc_matrix(self):

        try:

            # --------------------
            # матрица A
            # --------------------
            a = [
                [self.get_val(self.a_1_1), self.get_val(self.a_1_2), self.get_val(self.a_1_3)],
                [self.get_val(self.a_2_1), self.get_val(self.a_2_2), self.get_val(self.a_2_3)],
                [self.get_val(self.a_3_1), self.get_val(self.a_3_2), self.get_val(self.a_3_3)]
            ]

            # --------------------
            # матрица B
            # --------------------
            b = [
                [self.get_val(self.b_1_1), self.get_val(self.b_1_2), self.get_val(self.b_1_3)],
                [self.get_val(self.b_2_1), self.get_val(self.b_2_2), self.get_val(self.b_2_3)],
                [self.get_val(self.b_3_1), self.get_val(self.b_3_2), self.get_val(self.b_3_3)]
            ]

            # --------------------
            # результат
            # --------------------
            c = [[0 for _ in range(3)] for _ in range(3)]

            op = self.operation.currentText()

            # --------------------
            # СЛОЖЕНИЕ
            # --------------------
            if op == "+":
                for i in range(3):
                    for j in range(3):
                        c[i][j] = a[i][j] + b[i][j]

            # --------------------
            # ВЫЧИТАНИЕ
            # --------------------
            elif op == "-":
                for i in range(3):
                    for j in range(3):
                        c[i][j] = a[i][j] - b[i][j]

            # --------------------
            # УМНОЖЕНИЕ
            # --------------------
            else:
                for i in range(3):
                    for j in range(3):
                        for k in range(3):
                            c[i][j] += a[i][k] * b[k][j]

            # --------------------
            # вывод
            # --------------------
            self.c_1_1.setText(str(c[0][0]))
            self.c_1_2.setText(str(c[0][1]))
            self.c_1_3.setText(str(c[0][2]))

            self.c_2_1.setText(str(c[1][0]))
            self.c_2_2.setText(str(c[1][1]))
            self.c_2_3.setText(str(c[1][2]))

            self.c_3_1.setText(str(c[2][0]))
            self.c_3_2.setText(str(c[2][1]))
            self.c_3_3.setText(str(c[2][2]))

        except:
            pass


app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())