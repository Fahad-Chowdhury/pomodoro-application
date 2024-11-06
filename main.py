import os
import tkinter
import math


PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20


class Pomodoro():

    def __init__(self):
        self.reps = 0
        self.window = None
        self.title_label = None
        self.canvas = None
        self.timer_text = None
        self.start_button = None
        self.reset_button = None
        self.check_marks = None
        self.timer = None
        self.setup_ui()

    def setup_ui(self):
        """ Setup the User Interface. """
        self._setup_window()
        self._setup_timer_label()
        self._setup_canvas()
        self._setup_start_button()
        self._setup_reset_button()
        self._setup_checkmarks_label()

    def _setup_window(self):
        """ Setup the window. """
        self.window = tkinter.Tk()
        self.window.title("Pomodoro Timer")
        self.window.config(padx=100, pady=50, bg=YELLOW)

    def _setup_timer_label(self):
        """ Setup Timer Label. """
        self.title_label = tkinter.Label(text="Timer", fg=GREEN, bg=YELLOW,
                                         font=(FONT_NAME, 50))
        self.title_label.grid(column=1, row=0)

    def _setup_canvas(self):
        """ Setup Canvas with tomato image and also the timer text. """
        self.canvas = tkinter.Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(current_dir, "tomato.png")
        self.tomato_image = tkinter.PhotoImage(file=image_path)
        self.canvas.create_image(100, 112, image=self.tomato_image)
        self.timer_text = self.canvas.create_text(106, 130, text="00:00", fill="white",
                                                  font=(FONT_NAME, 30, "bold"))
        self.canvas.grid(column=1, row=1)

    def _setup_start_button(self):
        """ Setup Start Button. """
        self.start_button = tkinter.Button(text="Start", command=self.start_timer)
        self.start_button.grid(column=0, row=2)

    def _setup_reset_button(self):
        """ Setup Reset Button. """
        self.reset_button = tkinter.Button(text="Reset", command=self.reset_timer)
        self.reset_button.grid(column=2, row=2)

    def _setup_checkmarks_label(self):
        """ Setup Checkmark Label. """
        self.check_marks = tkinter.Label(text="", fg=GREEN, bg=YELLOW,
                                         font=(FONT_NAME, 30))
        self.check_marks.grid(column=1, row=3)

    def _update_timer_label(self, text, font_color):
        """ Update Timer Label with given text and with font color. """
        self.title_label.config(text=text, fg=font_color)

    def _set_checkmarks_label(self, text):
        """ Set Checkmark label with given text. """
        self.check_marks.config(text=text)

    def _update_checkmarks_label(self):
        """ Update Checkmark label with number of ticks corresponding to completed
        work sessions. """
        work_sessions_complete = math.floor(self.reps / 2)
        check_marks = "✓" * work_sessions_complete
        self._set_checkmarks_label(check_marks)

    def reset_timer(self):
        """ Reset the timer, along with updating title label and checkmarks. """
        self.window.after_cancel(self.timer)
        self.canvas.itemconfig(self.timer_text, text="00:00")
        self._update_timer_label("Timer", GREEN)
        self._set_checkmarks_label("")
        self.reps = 0
        self.start_button.config(state=tkinter.NORMAL)

    def start_timer(self):
        """ Start the timer for entire pomodoro cycle. Set work timer (25 mins) and
        when a work session is complete start a short break timer (5 minutes).
        After four work cycle is completed with breaks start a long break. """
        self.start_button.config(state=tkinter.DISABLED)
        self.reps += 1
        if self.reps % 8 == 0:
            # Start timer for long break
            self._update_timer_label("Break", RED)
            self.count_down(LONG_BREAK_MIN * 60)
        elif self.reps % 2 == 0:
            # Start timer for short break
            self._update_timer_label("Break", PINK)
            self.count_down(SHORT_BREAK_MIN * 60)
        else:
            # Start timer for work
            self._update_timer_label("Work", GREEN)
            self.count_down(WORK_MIN * 60)

    def count_down(self, count_seconds):
        """ Count down timer from given count_seconds to zero and update the timer label
        each second. When count down is complete start the timer for the next cycle. """
        count_minutes = math.floor(count_seconds / 60)
        count_seconds = count_seconds % 60
        count_str = f"{count_minutes}:{count_seconds:02d}"
        self.canvas.itemconfig(self.timer_text, text=count_str)
        if count_seconds > 0:
            self.timer = self.window.after(1000, self.count_down, count_seconds - 1)
        else:
            self._update_checkmarks_label()
            self.start_timer()


def main():
    """ Main method to execute Pomodoro app. """
    pomodoro = Pomodoro()
    pomodoro.window.mainloop()


if __name__ == "__main__":
    main()
