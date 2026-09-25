import math
import random
from pathlib import Path

from PySide6.QtCore import QPointF, QTimer, Qt, QUrl
from PySide6.QtGui import QColor, QPainter, QPen
from PySide6.QtMultimedia import QAudioOutput, QMediaPlayer
from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QLabel,
    QVBoxLayout,
    QWidget,
)


# =========================
# Particle
# =========================

class Particle:
    def __init__(self, x, y, angle, speed, color):
        self.x = x
        self.y = y

        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed

        self.life = random.uniform(35, 65)
        self.max_life = self.life

        self.color = color
        self.radius = random.uniform(1.5, 3.0)

    def update(self):
        self.x += self.vx
        self.y += self.vy

        self.vx *= 0.985
        self.vy *= 0.985

        self.vy += 0.045
        self.life -= 1

    def draw(self, painter):
        alpha = int(255 * (self.life / self.max_life))

        color = QColor(self.color)
        color.setAlpha(alpha)

        painter.setPen(Qt.NoPen)
        painter.setBrush(color)

        painter.drawEllipse(
            QPointF(self.x, self.y),
            self.radius,
            self.radius,
        )


# =========================
# Fireworks
# =========================

class Fireworks(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.Tool |
            Qt.WindowStaysOnTopHint
        )

        self.setAttribute(Qt.WA_TranslucentBackground)

        self.particles = []
        self.rockets = []

        self.colors = (
            "#ff4d6d",
            "#ffd166",
            "#06d6a0",
            "#4dabf7",
            "#c77dff",
            "#ffffff",
        )

        # Animation
        self.animation_timer = QTimer(self)
        self.animation_timer.timeout.connect(
            self.update_animation
        )
        self.animation_timer.start(16)

        # fireworks spawning
        self.spawn_timer = QTimer(self)
        self.spawn_timer.timeout.connect(
            self.launch_fireworks
        )
        self.spawn_timer.start(180)

    def launch_fireworks(self):
        width = self.width()
        height = self.height()

        if width <= 0 or height <= 0:
            return

        # Central explosion area
        target_x = random.randint(
            int(width * 0.25),
            int(width * 0.75),
        )

        target_y = random.randint(
            int(height * 0.20),
            int(height * 0.65),
        )

        # Only from bottom-left / bottom / bottom-right
        side = random.choice(
            (
                "bottom_left",
                "bottom",
                "bottom_right",
            )
        )

        if side == "bottom_left":
            x = random.randint(
                0,
                int(width * 0.20),
            )

        elif side == "bottom_right":
            x = random.randint(
                int(width * 0.80),
                width,
            )

        else:
            x = random.randint(
                int(width * 0.35),
                int(width * 0.65),
            )

        y = height + 20

        dx = target_x - x
        dy = target_y - y

        distance = math.hypot(dx, dy)

        speed = random.uniform(8, 12)

        vx = dx / distance * speed
        vy = dy / distance * speed

        self.rockets.append(
            {
                "x": float(x),
                "y": float(y),
                "target_x": target_x,
                "target_y": target_y,
                "vx": vx,
                "vy": vy,
                "color": random.choice(self.colors),
            }
        )

    def explode(self, rocket):
        for _ in range(random.randint(65, 100)):
            angle = random.uniform(
                0,
                math.tau,
            )

            speed = random.uniform(2, 7)

            self.particles.append(
                Particle(
                    rocket["x"],
                    rocket["y"],
                    angle,
                    speed,
                    rocket["color"],
                )
            )

    def update_animation(self):
        # Rockets
        for rocket in self.rockets[:]:

            rocket["x"] += rocket["vx"]
            rocket["y"] += rocket["vy"]

            distance = math.hypot(
                rocket["target_x"] - rocket["x"],
                rocket["target_y"] - rocket["y"],
            )

            if distance < 12:
                self.explode(rocket)
                self.rockets.remove(rocket)

        # Particles
        for particle in self.particles[:]:

            particle.update()

            if particle.life <= 0:
                self.particles.remove(particle)

        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)

        painter.setRenderHint(
            QPainter.Antialiasing
        )

        # Rockets
        for rocket in self.rockets:

            color = QColor(rocket["color"])

            painter.setPen(
                QPen(color, 3)
            )

            painter.drawPoint(
                QPointF(
                    rocket["x"],
                    rocket["y"],
                )
            )

        # Particles
        for particle in self.particles:
            particle.draw(painter)


# =========================
# Result dialog
# =========================

class ResultDialog(QDialog):
    def __init__(
        self,
        window_title,
        completion_text,
        total_letters,
        elapsed_time,
        errors,
        parent=None,
    ):
        super().__init__(parent)

        self.setWindowFlags(
            Qt.Dialog |
            Qt.CustomizeWindowHint |
            Qt.WindowTitleHint |
            Qt.WindowCloseButtonHint
        )

        self.setWindowTitle(
            window_title
        )

        self.setFixedSize(
            360,
            240,
        )

        title = QLabel(
            completion_text
        )

        title.setObjectName(
            "title"
        )

        result = QLabel(
            f"{total_letters}\n\n"
            f"{elapsed_time}\n"
            f"{errors}"
        )

        result.setObjectName(
            "result"
        )

        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok
        )

        buttons.accepted.connect(
            self.accept
        )

        layout = QVBoxLayout(self)

        layout.addWidget(title)
        layout.addWidget(result)
        layout.addWidget(buttons)

        title.setAlignment(
            Qt.AlignCenter
        )

        result.setAlignment(
            Qt.AlignCenter
        )

        self.setStyleSheet("""
            QDialog {
                background-color: #0f172a;
                color: #e6eef5;
                border: 1px solid #1DB954;
                border-radius: 10px;
            }

            QLabel#title {
                font-size: 24px;
                font-weight: bold;
                color: #10B981;
            }

            QLabel#result {
                font-size: 17px;
                color: #e6eef5;
            }

            QDialogButtonBox QPushButton {
                min-width: 80px;
                min-height: 30px;
                font-size: 15px;
                color: #10B981;
                border: 1px solid #2980b9;
                border-radius: 8px;
                background-color: transparent;
            }

            QDialogButtonBox QPushButton:hover {
                background-color: #16233d;
            }
        """)


# =========================
# Celebration
# =========================

class Celebration:
    def __init__(
        self,
        window_title,
        completion_text,
        total_letters,
        elapsed_time,
        errors,
        parent=None,
    ):
        self.parent = parent

        self.window_title = window_title
        self.completion_text = completion_text
        self.total_letters = total_letters
        self.elapsed_time = elapsed_time
        self.errors = errors

        # -------------------------
        # Fireworks
        # -------------------------

        self.fireworks = Fireworks()

        # -------------------------
        # Sound
        # -------------------------

        sounds_folder = (
            Path(__file__).resolve().parent
            / "sounds"
        )

        fireworks_path = (
            sounds_folder
            / "fireworks.mp3"
        )

        self.audio_output = QAudioOutput()

        self.audio_output.setVolume(
            0.09
        )

        self.fireworks_sound = QMediaPlayer()

        self.fireworks_sound.setAudioOutput(
            self.audio_output
        )

        self.fireworks_sound.setSource(
            QUrl.fromLocalFile(
                str(fireworks_path)
            )
        )

        # Infinite loop
        self.fireworks_sound.setLoops(
            QMediaPlayer.Loops.Infinite
        )

        # -------------------------
        # Show
        # -------------------------

        self.fireworks.showFullScreen()
        self.fireworks.raise_()
        self.fireworks.activateWindow()

        self.fireworks_sound.play()

        # Initial fireworks
        for _ in range(6):
            self.fireworks.launch_fireworks()

        # Result window
        QTimer.singleShot(
            800,
            self.show_result,
        )

    def show_result(self):
        dialog = ResultDialog(
            self.window_title,
            self.completion_text,
            self.total_letters,
            self.elapsed_time,
            self.errors,
            self.parent,
        )

        dialog.exec()

        self.close()

    def close(self):
        if self.fireworks_sound:
            self.fireworks_sound.stop()

        if self.fireworks:
            self.fireworks.close()
            self.fireworks.deleteLater()