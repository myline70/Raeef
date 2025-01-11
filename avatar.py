from PyQt6.QtSvgWidgets import QSvgWidget
from PyQt6.QtCore import QTimer

SVG_AVATAR = '''
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 500">
    <g id="head">
        <path d="M200 400 C 300 400 350 300 350 200 C 350 100 300 50 200 50 C 100 50 50 100 50 200 C 50 300 100 400 200 400" 
              fill="#FFD6C4"/>
    </g>
    <g id="hair">
        <path d="M200 50 C 100 50 50 100 50 200 C 50 150 70 100 150 80 C 200 70 250 90 300 70 C 350 90 370 150 350 200 C 350 100 300 50 200 50" 
              fill="#7EB5E8"/>
    </g>
    <g id="eyes">
        <g id="leftEye">
            <ellipse cx="150" cy="200" rx="40" ry="45" fill="white"/>
            <circle cx="150" cy="200" r="25" fill="black"/>
        </g>
        <g id="rightEye">
            <ellipse cx="250" cy="200" rx="40" ry="45" fill="white"/>
            <circle cx="250" cy="200" r="25" fill="black"/>
        </g>
    </g>
    <g id="mouth">
        <path id="mouthPath" d="M160 300 Q 200 {}, 240 300" fill="none" stroke="#FF9999" stroke-width="3"/>
    </g>
</svg>
'''

class AnimatedSvgWidget(QSvgWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.load(SVG_AVATAR.encode('utf-8'))

        # إعداد حركات الفم والعين
        self.mouth_shapes = ["320", "340", "360", "340"]  # حركة الفم
        self.eye_states = ["200", "195"]  # رمش العين (حركة بسيطة للأعلى والأسفل)
        self.current_mouth = 0
        self.current_eye = 0

        self.timer = QTimer()
        self.timer.timeout.connect(self.animate_features)

    def start_animation(self):
        self.timer.start(200)  # تحديث الحركة كل 200 مللي ثانية

    def stop_animation(self):
        self.timer.stop()
        self.current_mouth = 0
        self.current_eye = 0
        self.update_avatar(mouth_pos="320", eye_state="200")  # إعادة الوضع الافتراضي

    def animate_features(self):
        # تحديث الفم
        self.current_mouth = (self.current_mouth + 1) % len(self.mouth_shapes)
        mouth_pos = self.mouth_shapes[self.current_mouth]

        # تحديث العين
        self.current_eye = (self.current_eye + 1) % len(self.eye_states)
        eye_state = self.eye_states[self.current_eye]

        self.update_avatar(mouth_pos, eye_state)

    def update_avatar(self, mouth_pos, eye_state):
        # تحديث الـ SVG مع تغيير حركة الفم والعين
        updated_svg = SVG_AVATAR.format(mouth_pos)
        updated_svg = updated_svg.replace(
            '<circle cx="150" cy="200" r="25" fill="black"/>',
            f'<circle cx="150" cy="{eye_state}" r="25" fill="black"/>'
        )
        updated_svg = updated_svg.replace(
            '<circle cx="250" cy="200" r="25" fill="black"/>',
            f'<circle cx="250" cy="{eye_state}" r="25" fill="black"/>'
        )
        self.load(updated_svg.encode('utf-8'))