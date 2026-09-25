### Expandable abc checker ###
import sys
import time
from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (QApplication, QLabel, QPushButton, QHBoxLayout, QVBoxLayout,
                               QWidget, QStyle, QLineEdit, QComboBox, QProgressBar)
from celebration import Celebration

### ABC language packs ###
abc_lists = (
    ("aut", "A, B, C, D, E, F, G, H, I, J, K, L, M, N, O, P, Q, R, S, T, U, V, W, X, Y, Z, Ä, Ö, Ü, ẞ"),
    ("bel", "A, B, C, D, E, F, G, H, I, J, K, L, M, N, O, P, Q, R, S, T, U, V, W, X, Y, Z"),
    ("bgr", "А, Б, В, Г, Д, Е, Ж, З, И, Й, К, Л, М, Н, О, П, Р, С, Т, У, Ф, Х, Ц, Ч, Ш, Щ, Ъ, Ь, Ю, Я"),
    ("hrv", "A, B, C, Č, Ć, D, Dž, Đ, E, F, G, H, I, J, K, L, Lj, M, N, Nj, O, P, R, S, Š, T, U, V, Z, Ž"),
    ("cyp", "Α, Β, Γ, Δ, Ε, Ζ, Η, Θ, Ι, Κ, Λ, Μ, Ν, Ξ, Ο, Π, Ρ, Σ, Τ, Υ, Φ, Χ, Ψ, Ω"),
    ("cze", "A, Á, B, C, Č, D, Ď, E, É, Ě, F, G, H, Ch, I, Í, J, K, L, M, N, Ň, O, Ó, P, Q, R, Ř, S, Š, T, Ť, U, Ú, Ů, V, W, X, Y, Ý, Z, Ž"),
    ("deu", "A, B, C, D, E, F, G, H, I, J, K, L, M, N, O, P, Q, R, S, T, U, V, W, X, Y, Z"),
    ("dnk", "A, B, C, D, E, F, G, H, I, J, K, L, M, N, O, P, Q, R, S, T, U, V, W, X, Y, Z, Æ, Ø, Å"),
    ("eng", "A, B, C, D, E, F, G, H, I, J, K, L, M, N, O, P, Q, R, S, T, U, V, W, X, Y, Z"),
    ("esp", "A, B, C, D, E, F, G, H, I, J, K, L, M, N, Ñ, O, P, Q, R, S, T, U, V, W, X, Y, Z"),
    ("est", "A, B, D, E, F, G, H, I, J, K, L, M, N, O, P, R, S, Š, Z, Ž, T, U, V, Õ, Ä, Ö, Ü"),
    ("fin", "A, B, C, D, E, F, G, H, I, J, K, L, M, N, O, P, Q, R, S, T, U, V, W, X, Y, Z, Å, Ä, Ö"),
    ("fra", "A, B, C, D, E, F, G, H, I, J, K, L, M, N, O, P, Q, R, S, T, U, V, W, X, Y, Z"),
    ("gre", "Α, Β, Γ, Δ, Ε, Ζ, Η, Θ, Ι, Κ, Λ, Μ, Ν, Ξ, Ο, Π, Ρ, Σ, Τ, Υ, Φ, Χ, Ψ, Ω"),
    ("hun", "A, Á, B, C, Cs, D, Dz, Dzs, E, É, F, G, Gy, H, I, Í, J, K, L, Ly, M, N, Ny, O, Ó, Ö, Ő, P, Q, R, S, Sz, T, Ty, U, Ú, Ü, Ű, V, W, X, Y, Z, Zs"),
    ("irl", "A, B, C, D, E, F, G, H, I, L, M, N, O, P, R, S, T, U"),
    ("ita", "A, B, C, D, E, F, G, H, I, L, M, N, O, P, Q, R, S, T, U, V, Z"),
    ("lav", "A, Ā, B, C, Č, D, E, Ē, F, G, Ģ, H, I, Ī, J, K, Ķ, L, Ļ, M, N, Ņ, O, P, R, S, Š, T, U, Ū, V, Z, Ž"),
    ("ltu", "A, Ą, B, C, Č, D, E, Ę, Ė, F, G, H, I, Į, Y, J, K, L, M, N, O, P, R, S, Š, T, U, Ų, Ū, V, Z, Ž"),
    ("lux", "A, Ä, B, C, D, E, É, Ë, F, G, H, I, J, K, L, M, N, O, P, Q, R, S, T, U, V, W, X, Y, Z"),
    ("mlt", "A, B, Ċ, D, E, F, Ġ, G, Għ, H, Ħ, I, Ie, J, K, L, M, N, O, P, Q, R, S, T, U, V, W, X, Ż, Z"),
    ("nld", "A, B, C, D, E, F, G, H, I, J, K, L, M, N, O, P, Q, R, S, T, U, V, W, X, Y, Z"),
    ("pol", "A, Ą, B, C, Ć, D, E, Ę, F, G, H, I, J, K, L, Ł, M, N, Ń, O, Ó, P, R, S, Ś, T, U, W, Y, Z, Ź, Ż"),
    ("prt", "A, B, C, D, E, F, G, H, I, J, K, L, M, N, O, P, Q, R, S, T, U, V, W, X, Y, Z"),
    ("rou", "A, Ă, Â, B, C, D, E, F, G, H, I, Î, J, K, L, M, N, O, P, Q, R, S, Ș, T, Ț, U, V, W, X, Y, Z"),
    ("svk", "A, Á, Ä, B, C, Č, D, Ď, Dz, Dž, E, É, F, G, H, Ch, I, Í, J, K, L, Ĺ, Ľ, M, N, Ň, O, Ó, Ô, P, Q, R, Ŕ, S, Š, T, Ť, U, Ú, V, W, X, Y, Ý, Z, Ž"),
    ("svn", "A, B, C, Č, D, E, F, G, H, I, J, K, L, M, N, O, P, R, S, Š, T, U, V, Z, Ž"),
    ("swe", "A, B, C, D, E, F, G, H, I, J, K, L, M, N, O, P, Q, R, S, T, U, V, W, X, Y, Z, Å, Ä, Ö"),
    )

# Visually similar characters accepted as alternative input
letter_matches = {
    "A": ("А", "Α"), "А": ("A", "Α"), "Α": ("А", "A"),
    "B": ("В", "Β"), "В": ("B", "Β"), "Β": ("В", "B"),
    "C": ("С",), "С": ("C",),
    "E": ("Е", "Ε"), "Е": ("E", "Ε"), "Ε": ("Е", "E"),
    "H": ("Н",), "Н": ("H",),
    "I": ("Ι",), "Ι": ("I",),
    "K": ("К", "Κ"), "К": ("K", "Κ"), "Κ": ("К", "K"),
    "M": ("М",), "М": ("M",),
    "N": ("Ν",), "Ν": ("N",),
    "O": ("О", "Ο"), "О": ("O", "Ο"), "Ο": ("О", "O"),
    "P": ("Р", "Ρ"), "Р": ("P", "Ρ"), "Ρ": ("Р", "P"),
    "T": ("Т", "Τ"), "Т": ("T", "Τ"), "Τ": ("Т", "T"),
    "X": ("Х", "Χ"), "Х": ("X", "Χ"), "Χ": ("Х", "X"),
    "Y": ("Υ",), "Υ": ("Y",),
    "Z": ("Ζ",), "Ζ": ("Z",),
}

### GUI language packs ###
language_packs = {
    "English": {
        "window_title": "ABC Learner",
        "errors": "Errors: ",
        "prev_char": "Previous character: ",
        "hint": "Hint",
        "hint_tooltip": "Shows the next letter as a hint.",
        "reset": "Reset",
        "enter": "Enter",
        "total_letters": "Total Letters: ",
        "time": "Elapsed Time: ",
        "completed": "Alphabet Completed!",
        "alphabets": (
            "Austrian Alphabet",
            "Belgian Alphabet",
            "Bulgarian Alphabet",
            "Croatian Alphabet",
            "Cypriot Alphabet",
            "Czech Alphabet",
            "German Alphabet",
            "Danish Alphabet",
            "English Alphabet",
            "Spanish Alphabet",
            "Estonian Alphabet",
            "Finnish Alphabet",
            "French Alphabet",
            "Greek Alphabet",
            "Hungarian Alphabet",
            "Irish Alphabet",
            "Italian Alphabet",
            "Latvian Alphabet",
            "Lithuanian Alphabet",
            "Luxembourgish Alphabet",
            "Maltese Alphabet",
            "Dutch Alphabet",
            "Polish Alphabet",
            "Portuguese Alphabet",
            "Romanian Alphabet",
            "Slovak Alphabet",
            "Slovenian Alphabet",
            "Swedish Alphabet",
        ),
    },
    "Deutsch": {
        "window_title": "ABC-Lerner",
        "errors": "Fehler: ",
        "prev_char": "Vorheriges Zeichen: ",
        "hint": "Hinweis",
        "hint_tooltip": "Zeigt den nächsten Buchstaben als Hinweis.",
        "reset": "Zurücksetzen",
        "enter": "Enter",
        "total_letters": "Anzahl der Buchstaben: ",
        "time": "Vergangene Zeit: ",
        "completed": "Alphabet Abgeschlossen!",
        "alphabets": (
            "Österreichisches Alphabet",
            "Belgisches Alphabet",
            "Bulgarisches Alphabet",
            "Kroatisches Alphabet",
            "Zypriotisches Alphabet",
            "Tschechisches Alphabet",
            "Deutsches Alphabet",
            "Dänisches Alphabet",
            "Englisches Alphabet",
            "Spanisches Alphabet",
            "Estnisches Alphabet",
            "Finnisches Alphabet",
            "Französisches Alphabet",
            "Griechisches Alphabet",
            "Ungarisches Alphabet",
            "Irisches Alphabet",
            "Italienisches Alphabet",
            "Lettisches Alphabet",
            "Litauisches Alphabet",
            "Luxemburgisches Alphabet",
            "Maltesisches Alphabet",
            "Niederländisches Alphabet",
            "Polnisches Alphabet",
            "Portugiesisches Alphabet",
            "Rumänisches Alphabet",
            "Slowakisches Alphabet",
            "Slowenisches Alphabet",
            "Schwedisches Alphabet",
        ),
    },
    "Français": {
        "window_title": "ABC Learner",
        "errors": "Erreurs: ",
        "prev_char": "Caractère précédent: ",
        "hint": "Indice",
        "hint_tooltip": "Affiche la lettre suivante comme indice.",
        "reset": "Réinitialiser",
        "enter": "Entrée",
        "total_letters": "Nombre de lettres : ",
        "time": "Temps écoulé : ",
        "completed": "Alphabet Terminé!",
        "alphabets": (
            "Alphabet autrichien",
            "Alphabet belge",
            "Alphabet bulgare",
            "Alphabet croate",
            "Alphabet chypriote",
            "Alphabet tchèque",
            "Alphabet allemand",
            "Alphabet danois",
            "Alphabet anglais",
            "Alphabet espagnol",
            "Alphabet estonien",
            "Alphabet finlandais",
            "Alphabet français",
            "Alphabet grec",
            "Alphabet hongrois",
            "Alphabet irlandais",
            "Alphabet italien",
            "Alphabet letton",
            "Alphabet lituanien",
            "Alphabet luxembourgeois",
            "Alphabet maltais",
            "Alphabet néerlandais",
            "Alphabet polonais",
            "Alphabet portugais",
            "Alphabet roumain",
            "Alphabet slovaque",
            "Alphabet slovène",
            "Alphabet suédois",
        ),
    },
    "Magyar": {
        "window_title": "Ábécétanuló",
        "errors": "Hibák: ",
        "prev_char": "Előző karakter: ",
        "hint": "Tipp",
        "hint_tooltip": "Megjeleníti a következő betűt segítségként.",
        "reset": "Visszaállítás",
        "enter": "Enter",
        "total_letters": "Betűk száma: ",
        "time": "Eltelt idő: ",
        "completed": "Ábécé Teljesítve!",
        "alphabets": (
            "Osztrák ábécé",
            "Belga ábécé",
            "Bolgár ábécé",
            "Horvát ábécé",
            "Ciprusi ábécé",
            "Cseh ábécé",
            "Német ábécé",
            "Dán ábécé",
            "Angol ábécé",
            "Spanyol ábécé",
            "Észt ábécé",
            "Finn ábécé",
            "Francia ábécé",
            "Görög ábécé",
            "Magyar ábécé",
            "Ír ábécé",
            "Olasz ábécé",
            "Lett ábécé",
            "Litván ábécé",
            "Luxemburgi ábécé",
            "Máltai ábécé",
            "Holland ábécé",
            "Lengyel ábécé",
            "Portugál ábécé",
            "Román ábécé",
            "Szlovák ábécé",
            "Szlovén ábécé",
            "Svéd ábécé",
        ),
    },
}


### Main window ###
class abc_gui(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ABC Learner")
        self.setFixedSize(400, 400)
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.MSWindowsFixedSizeDialogHint)
        self.setWindowIcon(self.style().standardIcon(QStyle.SP_MessageBoxInformation))
        self.setStyleSheet("""
                            QWidget {
                                background: qlineargradient(x1:0,y1:0,x2:1,y2:1, stop:0 #0f172a, stop:1 #071029);
                                color: #e6eef5;
                                }
                            QPushButton[style="reset/enter"] {
                                font-size: 15px;
                                color: #10B981;
                                border-radius: 10px;
                                border: 1px solid #2980b9;
                                padding: 10px;
                                min-width: 85px;
                                max-width: 85px;
                                min-height: 25px;
                                max-height: 25px;
                                background-color: transparent;
                                }
                            QPushButton[style="hint"] {
                                font-size: 15px;
                                color: #10B981;
                                border-radius: 15px;
                                border: 1px solid #2980b9;
                                }
                            QPushButton[style="hint"]:pressed {
                                margin: 2px;
                                padding-top: 3px;
                                padding-left: 3px;
                                }
                            QLineEdit {
                                font-size: 25px;
                                margin: 10px;
                                }
                            QLabel {
                                font-size: 25px;
                                }                        
                            """)

        # ABC langs dictionary, contains each abc list called by it's lang abbreviation [0]
        self.abc_langs = tuple(tuple(char.strip().lower() for char in abc[1].split(",")) for abc in abc_lists)

        self.abc = self.abc_langs[8]
        self.curr_lang = language_packs["English"]
        self._curr_pos = 0
        self.errors = 0
        self.prev_char = ""
        self.char = ""
        self.show_elapsed = ""
        self.is_timer_on = 0

        # GUI layout
        self.main_layout = QVBoxLayout(self)
        
        self.top_toolbar_widget = QWidget(self)
        self.top_toolbar = QHBoxLayout(self.top_toolbar_widget)
        
        self.layout_choices = QHBoxLayout(self)
        self.layout_checker = QVBoxLayout(self)
        self.layout_results = QHBoxLayout(self)

        self.main_layout.addWidget(self.top_toolbar_widget)
        self.main_layout.addLayout(self.layout_choices)
        self.main_layout.addStretch()
        self.main_layout.addLayout(self.layout_checker)
        self.main_layout.addLayout(self.layout_results)
        self.main_layout.addStretch()

        # ABC choice (push buttons)
        self.select_abc = QComboBox(self)
        self.select_abc.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.select_abc.addItems((abc for abc in self.curr_lang["alphabets"]))
        self.select_abc.setCurrentIndex(8)
        
        self.select_lang = QComboBox(self)
        self.select_lang.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.select_lang.addItems([
            "Language: English",
            "Sprache: Deutsch",
            "Langue : Français",
            "Nyelv: Magyar"
        ])

        self.top_toolbar.addWidget(self.select_abc)
        self.top_toolbar.addStretch()
        self.top_toolbar.addWidget(self.select_lang)

        # Input (line edit) & information labels
        self.user_place = QLabel()
        self.user_place.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.user_progress_bar = QProgressBar()
        self.user_progress_bar.setFixedWidth(300)
        self.user_progress_bar.setRange(0, 100)
        self.user_progress_bar.setValue(0)
        self.user_progress_bar.setFormat("00:00")
        self.user_progress_bar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.user_progress_bar.setStyleSheet("""
                                            QProgressBar {
                                                background: #4B0082;
                                                border-radius:10px;
                                                color: #00FFFF;
                                                font-weight: bold;
                                                font-size: 14px;
                                                }
                                            QProgressBar::chunk {
                                                background: #1DB954;
                                                border-radius:10px; 
                                                }
                                            """)

        self.user_errors = QLabel()
        self.user_prev_char = QLabel()

        # Extra positioning Widget
        input_container = QWidget()
        input_container.setFixedWidth(350)
        input_container.setFixedHeight(60)

        self.user_input = QLineEdit(input_container)
        self.user_input.setFixedWidth(230)
        self.user_input.setFixedHeight(60)
        self.user_input.setMaxLength(10)

        self.hint_button = QPushButton(self.curr_lang["hint"], input_container)
        self.hint_button.setFixedWidth(60)
        self.hint_button.setFixedHeight(40)

        # Position user_input (QLineEdit) in the center
        self.user_input.move((input_container.width() - self.user_input.width()) // 2, 0)
        # Position hint_button (QPushButton) to the right
        self.hint_button.move(self.user_input.x() + self.user_input.width(), 10)
        self.hint_button.setProperty("style", "hint")
        self.hint_button.setToolTip(self.curr_lang["hint_tooltip"])
        
        self.layout_checker.addWidget(self.user_place, alignment=Qt.AlignmentFlag.AlignCenter)
        self.layout_checker.addWidget(self.user_progress_bar, alignment=Qt.AlignmentFlag.AlignCenter)
        self.layout_checker.addStretch()
        self.layout_checker.addWidget(self.user_errors)
        self.layout_checker.addWidget(self.user_prev_char)
        self.layout_checker.addStretch()
        self.layout_checker.addWidget(input_container,alignment=Qt.AlignmentFlag.AlignCenter)
        self.layout_checker.addStretch()

        # (Push buttons) -> operation with inputs
        self.layout_results.addStretch()
        self.user_input_reset = QPushButton(f"{self.curr_lang["reset"]}")
        self.user_input_check = QPushButton(f"{self.curr_lang["enter"]}")
        self.user_input_reset.setProperty("style", "reset/enter")
        self.user_input_check.setProperty("style", "reset/enter")

        self.layout_results.addWidget(self.user_input_reset)
        self.layout_results.addWidget(self.user_input_check)
        self.layout_results.addStretch()
        
        # Connectors
        self.select_abc.currentIndexChanged.connect(self.change_abc)
        self.select_lang.currentIndexChanged.connect(self.change_language)
        self.user_input_reset.pressed.connect(lambda: self.buttons_pressed_fix(0, self.user_input_reset))
        self.user_input_check.pressed.connect(lambda: self.buttons_pressed_fix(1, self.user_input_check))
        self.user_input.returnPressed.connect(lambda: self.buttons_pressed_fix(1, self.user_input_check))
        self.hint_button.pressed.connect(lambda: self.buttons_pressed_fix(2, self.hint_button))
        self.reset()

    # Current alphabeth position
    @property
    def curr_pos(self):
        return self._curr_pos
    
    # Updates user progress bar
    @curr_pos.setter
    def curr_pos(self, value):
        self._curr_pos = value
        self.user_progress()

    # Fix "user_input" and "hint" [pressed] event overlap
    def buttons_pressed_fix(self, idx, button):
        self.button_pressed(button)
        if idx == 1:
            self.check_char(self.user_input.text())
        elif idx == 2:
            self.hint_button_pressed()
        else:
            self.reset()

    # Creates a brief pressed effect on the button
    def button_pressed(self, button):
        button.setStyleSheet("margin: 3px; padding-top: 2px; padding-left: 2px;")
        QTimer.singleShot(40, lambda: button.setStyleSheet(""))
    
    # Shows the correct next letter when the hint is triggered. (help func)
    def hint_button_pressed(self):
        self.user_input.setFocus()
        if self.curr_pos >= len(self.abc):
            return
        if self.user_input.text().strip() == self.abc[self.curr_pos]:
            self.user_input.setText(self.user_input.text().strip())
            return
        self.user_input.setText(self.abc[self.curr_pos])
        self.errors += 1
        self.user_errors.setText(f"{self.curr_lang["errors"]}{self.errors}")
    
    # Progress bar progress update
    def user_progress(self):
        curr_percent = int(self.curr_pos / len(self.abc) * 100)
        self.user_progress_bar.setValue(curr_percent)
    
    # Progress bar timer
    def user_progress_timer(self, stop):
        if not self.is_timer_on:
            self.time = time.time()
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.update_time)
            self.timer.start(100)
        if stop:
            self.timer.stop()

    # Updates time elapsed
    def update_time(self):
        elapsed = int(time.time() - self.time)
        self.show_elapsed = f"{elapsed // 60:02d}:{elapsed % 60:02d}" 
        self.user_progress_bar.setFormat(self.show_elapsed)

    # [Enter] function #
    def check_char(self, char):
        self.user_input.setFocus()
        if self.curr_pos >= len(self.abc):
            return
        self.user_progress()
        curr_char = self.abc[self.curr_pos]
        char = char.strip().lower()
        if char == "":
            return
        is_similar_letter = curr_char.upper() in letter_matches.get(char.upper(), ())
        if char == curr_char or is_similar_letter:
            self.user_place.setText(f"{self.curr_pos+1}/{len(self.abc)}")
            self.user_prev_char.setText(f"{self.curr_lang["prev_char"]}{char}")
            self.char = char
            self.curr_pos += 1
            if self.curr_pos == len(self.abc):
                self.user_progress_timer(1)
                self.is_timer_on = 0
                self.user_input.setText("")
                # Celebration Dialog Box
                total_letters = f"{self.curr_lang["total_letters"]}{self.curr_pos}/{len(self.abc)}"
                elapsed_time = f"{self.curr_lang["time"]}{self.show_elapsed}"
                errors = f"{self.curr_lang["errors"]}{self.errors}"

                self.celebration = Celebration(
                    window_title=self.curr_lang["window_title"],
                    completion_text=self.curr_lang["completed"],
                    total_letters=total_letters,
                    elapsed_time=elapsed_time,
                    errors=errors,
                    parent=self,
                    )
                return
        else:
            self.errors += 1
            self.user_errors.setText(f"{self.curr_lang["errors"]}{self.errors}")

        self.user_progress_timer(0)
        self.is_timer_on = 1
        self.user_input.setText("")

    # [Reset] function #
    def reset(self):
        self.user_progress_timer(1)
        self.user_progress_bar.setFormat("00:00")
        self.is_timer_on = 0
        self.curr_pos = 0
        self.errors = 0
        self.prev_char = ""
        self.user_place.setText(f"0/{len(self.abc)}")
        self.user_errors.setText(f"{self.curr_lang["errors"]}0")
        self.user_prev_char.setText(f"{self.curr_lang["prev_char"]}")
        self.user_input.setText("")
        self.user_input.setFocus()

    # Connects self.select_lang - switch ui language to the selected language #
    def change_language(self, index):
        selected_language = ("English", "Deutsch", "Français", "Magyar")[index]
        self.curr_lang = language_packs[selected_language]
        # abc list localization
        self.select_abc.blockSignals(True)
        abc_idx = self.select_abc.currentIndex()
        self.select_abc.clear()
        self.select_abc.addItems((abc for abc in self.curr_lang["alphabets"]))
        self.select_abc.setCurrentIndex(abc_idx)
        self.select_abc.blockSignals(False)
        # user interface localization
        self.user_place.setText(f"{self.curr_pos}/{len(self.abc)}")
        self.user_prev_char.setText(f"{self.curr_lang["prev_char"]}{self.char}")
        self.user_errors.setText(f"{self.curr_lang["errors"]}{self.errors}")
        self.user_input_reset.setText(f"{self.curr_lang["reset"]}")
        self.user_input_check.setText(f"{self.curr_lang["enter"]}")
        self.hint_button.setText(f"{self.curr_lang["hint"]}")
        self.hint_button.setToolTip(f"{self.curr_lang["hint_tooltip"]}")

    # Set alphabets #
    def change_abc(self, index):
        self.abc = self.abc_langs[index]
        self.reset()


if __name__ == "__main__":
    app = QApplication([])
    main_window = abc_gui()
    main_window.show()
    sys.exit(app.exec())
