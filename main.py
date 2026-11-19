"""Run using the project's Python 3.12 virtual environment."""
import sys
from PySide6.QtWidgets import QApplication
from app.ui.main_window import MainWindow


def main() -> int:
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = MainWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
