from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.graphics import Rectangle, Color
from kivy.clock import Clock
import random

class GameWidget(Widget):
    def __init__(self, **kwargs):
        super(GameWidget, self).__init__(**kwargs)
        
        # النقاط وحالة اللعبة
        self.score = 0
        
        with self.canvas:
            # خلفية ساحة المعركة (لون داكن)
            Color(0.1, 0.1, 0.2, 1)
            self.bg = Rectangle(pos=(0, 0), size=(1000, 1000))
            
            # اللاعب (مركبة حربية في الأسفل)
            Color(0, 0.8, 1, 1)
            self.player = Rectangle(pos=(180, 50), size=(40, 40))
            
            # العدو
            Color(1, 0.2, 0.2, 1)
            self.enemy = Rectangle(pos=(random.randint(50, 300), 600), size=(40, 40))
            
            # الطلقة
            Color(1, 1, 0, 1)
            self.bullet = Rectangle(pos=(-100, -100), size=(10, 20))

        # عداد النقاط على الشاشة
        self.score_label = Label(text=f"Score: {self.score}", pos=(20, 700), font_size=24)
        self.add_widget(self.score_label)

        # تحريك اللعبة وعملية التحديث
        Clock.schedule_interval(self.update, 1.0 / 60.0)

    def on_touch_move(class_self, touch):
        # تحريك اللاعب يميناً ويساراً حسب حركة إصبعك على الشاشة
        class_self.player.pos = (touch.x - 20, class_self.player.pos[1])
        # إطلاق رصاصة تلقائياً عند التحريك
        class_self.bullet.pos = (class_self.player.pos[0] + 15, class_self.player.pos[1] + 40)

    def update(self, dt):
        # تحرك العدو إلى الأسفل ببطء
        ex, ey = self.enemy.pos
        ey -= 3
        if ey < 0:
            # إذا وصل العدو لأسفل الشاشة يعود للأعلى بموقع عشوائي
            ey = 700
            ex = random.randint(50, 300)
        self.enemy.pos = (ex, ey)

        # تحرك الطلقة إلى الأعلى
        bx, by = self.bullet.pos
        by += 10
        self.bullet.pos = (bx, by)

        # التحقق من اصطدام الطلقة بالعدو
        if abs(bx - ex) < 30 and abs(by - ey) < 30:
            self.score += 1
            self.score_label.text = f"Score: {self.score}"
            # إعادة تعيين العدو للأعلى
            self.enemy.pos = (random.randint(50, 300), 700)
            self.bullet.pos = (-100, -100)

class WarGameApp(App):
    def build(self):
        return GameWidget()

if __name__ == '__main__':
    WarGameApp().run()
