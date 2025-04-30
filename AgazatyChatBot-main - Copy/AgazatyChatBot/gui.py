import tkinter as tk
from tkinter import ttk
from chatbot import LeaveChatbot

class ChatbotApp:
    def __init__(self, root):
        self.root = root
        root.title("مساعد طلبات الإجازة")
        root.geometry("850x650")
        root.minsize(750, 550)
        root.configure(bg='#f0f0f0')

        # ألوان الاستخدام
        self.colors = {
            'bg': '#f0f0f0',
            'bot_bg': '#e3f2fd',
            'user_bg': '#e8f5e9',
            'button_bg': '#4caf50',
            'button_fg': 'white',
            'text_fg': '#263238',
            'entry_bg': 'white',
            'scrollbar': '#b0bec5'
        }

        # تحميل البوت
        self.chatbot = LeaveChatbot()

        # الإطار الرئيسي
        main_frame = tk.Frame(root, padx=20, pady=20, bg=self.colors['bg'])
        main_frame.pack(expand=True, fill='both')

        # إطار المحادثة
        chat_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        chat_frame.pack(expand=True, fill='both', pady=(0, 15))

        # تنسيق الشريط الجانبي (scrollbar)
        style = ttk.Style()
        style.configure("TScrollbar",
                        gripcount=0,
                        background=self.colors['scrollbar'],
                        troughcolor=self.colors['bg'],
                        lightcolor=self.colors['scrollbar'],
                        darkcolor=self.colors['scrollbar'])

        scrollbar = ttk.Scrollbar(chat_frame, style="TScrollbar")
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # منطقة عرض المحادثة
        self.chat_display = tk.Text(
            chat_frame,
            height=20,
            width=80,
            state='disabled',
            yscrollcommand=scrollbar.set,
            wrap=tk.WORD,
            font=('Arial', 12),
            bg='white',
            fg=self.colors['text_fg'],
            relief=tk.FLAT,
            highlightthickness=1,
            highlightbackground='#cfd8dc'
        )
        self.chat_display.pack(expand=True, fill='both')
        scrollbar.config(command=self.chat_display.yview)

        # إطار الإدخال
        input_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        input_frame.pack(fill=tk.X, pady=(5, 0))

        self.user_entry = tk.Entry(
            input_frame,
            width=70,
            font=('Arial', 12),
            bg=self.colors['entry_bg'],
            fg=self.colors['text_fg'],
            relief=tk.GROOVE,
            borderwidth=2,
            justify='right'  # ضروري للعربية
        )
        self.user_entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 10))

        self.send_button = tk.Button(
            input_frame,
            text="إرسال",
            command=self.process_input,
            width=10,
            font=('Arial', 12, 'bold'),
            bg=self.colors['button_bg'],
            fg=self.colors['button_fg'],
            activebackground='#388e3c',
            activeforeground='white',
            relief=tk.RAISED,
            borderwidth=2
        )
        self.send_button.pack(side=tk.RIGHT)

        self.user_entry.bind('<Return>', lambda event: self.process_input())
        self.display_message("البوت: مرحبًا! كيف يمكنني مساعدتك اليوم؟", 'bot')
        self.user_entry.focus_set()

    def display_message(self, message, sender='user'):
        self.chat_display.config(state='normal')

        # تهيئة تنسيق الرسائل
        tag_name = 'bot_tag' if sender == 'bot' else 'user_tag'
        bg_color = self.colors['bot_bg'] if sender == 'bot' else self.colors['user_bg']

        self.chat_display.tag_config(
            tag_name,
            background=bg_color,
            lmargin1=40,    # زيادة الهوامش لضبط التحديد
            lmargin2=40,
            rmargin=10,
            spacing2=6,
            justify='right',
            font=('Arial', 12)
        )

        self.chat_display.insert(tk.END, message + "\n\n", tag_name)
        self.chat_display.config(state='disabled')
        self.chat_display.see(tk.END)

    def process_input(self):
        user_text = self.user_entry.get().strip()
        if user_text:
            self.display_message(f"أنت: {user_text}", 'user')
            bot_response = self.chatbot.get_response(user_text)
            self.display_message(f"البوت: {bot_response}", 'bot')
            self.user_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatbotApp(root)
    root.mainloop()
