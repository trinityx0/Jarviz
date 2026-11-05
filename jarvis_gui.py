import sys
import math
from datetime import datetime

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QLabel, QPushButton, QVBoxLayout,
    QHBoxLayout, QTextEdit
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import (
    QPainter, QColor, QPen, QRadialGradient
)


# ==========================================
# JARVIZ ARC REACTOR
# ==========================================

class ArcReactor(QWidget):

    def __init__(self):
        super().__init__()
        self.angle = 0
        self.setMinimumSize(240, 240)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animate)
        self.timer.start(30)

    def animate(self):
        self.angle = (self.angle + 2) % 360
        self.update()

    def paintEvent(self, event):

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        center = self.rect().center()
        x, y = center.x(), center.y()

        gradient = QRadialGradient(x, y, 100)
        gradient.setColorAt(0, QColor("#164C72"))
        gradient.setColorAt(0.5, QColor("#071C32"))
        gradient.setColorAt(1, QColor("#07111F"))

        painter.setBrush(gradient)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(x - 90, y - 90, 180, 180)

        painter.translate(x, y)
        painter.rotate(self.angle)

        pen = QPen(QColor("#39D9FF"), 4)
        painter.setPen(pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)

        painter.drawEllipse(-72, -72, 144, 144)

        pen.setWidth(2)
        painter.setPen(pen)

        painter.drawEllipse(-53, -53, 106, 106)

        for i in range(8):
            painter.rotate(45)
            painter.drawLine(0, -55, 0, -70)

        painter.setBrush(QColor("#54DCFF"))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(-13, -13, 26, 26)


# ==========================================
# MAIN WINDOW
# ==========================================

class JarvizWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("JARVIZ - Personal AI")
        self.resize(950, 700)

        self.setStyleSheet("""
            QMainWindow {
                background-color: #07111F;
            }

            QLabel {
                color: #D9F4FF;
                font-family: Segoe UI;
            }

            QPushButton {
                background-color: #102B42;
                color: #50DFFF;
                border: 1px solid #2386B0;
                border-radius: 8px;
                padding: 12px;
                font-size: 14px;
            }

            QPushButton:hover {
                background-color: #174765;
            }

            QTextEdit {
                background-color: #091A2B;
                color: #50DFFF;
                border: 1px solid #174765;
                border-radius: 8px;
                padding: 10px;
                font-size: 13px;
            }
        """)

        self.setup_ui()

    def setup_ui(self):

        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(35, 25, 35, 25)
        main_layout.setSpacing(18)

        # HEADER

        header = QHBoxLayout()

        title = QLabel("J.A.R.V.I.Z")
        title.setStyleSheet(
            "font-size: 30px; font-weight: bold; color: #45DFFF;"
        )

        self.clock = QLabel()

        header.addWidget(title)
        header.addStretch()
        header.addWidget(self.clock)

        main_layout.addLayout(header)

        # SUBTITLE

        subtitle = QLabel("PERSONAL ARTIFICIAL INTELLIGENCE SYSTEM")
        subtitle.setStyleSheet(
            "color: #648BA9; font-size: 11px; letter-spacing: 3px;"
        )

        main_layout.addWidget(subtitle)

        # ARC REACTOR

        main_layout.addStretch()

        self.reactor = ArcReactor()
        main_layout.addWidget(
            self.reactor,
            alignment=Qt.AlignmentFlag.AlignCenter
        )

        self.status = QLabel("SYSTEM INITIALIZED")
        self.status.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.status.setStyleSheet(
            "font-size: 20px; color: #45DFFF; font-weight: bold;"
        )

        main_layout.addWidget(self.status)

        # ACTIVITY LOG

        self.log = QTextEdit()
        self.log.setReadOnly(True)
        self.log.setPlaceholderText("JARVIZ activity will appear here...")
        self.log.setMaximumHeight(145)

        main_layout.addWidget(self.log)

        # BUTTONS

        buttons = QHBoxLayout()

        self.wake_button = QPushButton("WAKE UP")
        self.sleep_button = QPushButton("SLEEP")
        self.exit_button = QPushButton("SHUT DOWN")

        self.wake_button.clicked.connect(self.wake_up)
        self.sleep_button.clicked.connect(self.sleep)
        self.exit_button.clicked.connect(self.close)

        buttons.addWidget(self.wake_button)
        buttons.addWidget(self.sleep_button)
        buttons.addWidget(self.exit_button)

        main_layout.addLayout(buttons)

        main_layout.addStretch()

        # CLOCK TIMER

        self.clock_timer = QTimer(self)
        self.clock_timer.timeout.connect(self.update_clock)
        self.clock_timer.start(1000)

        self.update_clock()

        self.sleep()

    # ======================================
    # STATUS FUNCTIONS
    # ======================================

    def update_clock(self):

        now = datetime.now().strftime("%d %b %Y | %I:%M:%S %p")
        self.clock.setText(now)

    def add_log(self, message):

        self.log.append(
            f"[{datetime.now().strftime('%H:%M:%S')}] {message}"
        )

    def wake_up(self):

        self.status.setText("JARVIZ ONLINE")
        self.status.setStyleSheet(
            "font-size: 20px; color: #48FFAE; font-weight: bold;"
        )

        self.add_log("System awakened.")

    def sleep(self):

        self.status.setText("SLEEPING")
        self.status.setStyleSheet(
            "font-size: 20px; color: #FFB84D; font-weight: bold;"
        )

        self.add_log("Entering sleep mode.")


# ==========================================
# START APPLICATION
# ==========================================

if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = JarvizWindow()
    window.show()

    sys.exit(app.exec())