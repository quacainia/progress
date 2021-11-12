import datetime
import math
import os
import sys
import time


class ProgressBar():

    def __init__(self, lines):
        if isinstance(lines, int):
            self.__lines = [{} for i in range(lines)]
        else:
            self.__lines = lines
            for i, line in enumerate(lines):
                if not isinstance(line, dict):
                    self.__lines[i] == {}
        self.__started = False
        self.__last_msg = None

    def refresh(self, pct, lines):
        self.__last_msg = (pct, lines)
        if isinstance(lines, str):
            lines = [lines]

        if self.__started:
            for i in self.__lines:
                sys.stdout.write('\033[F')  # Go to previous line
                sys.stdout.write('\033[K')  # Clearn current line
        for i, line_prefs in enumerate(self.__lines):
            try:
                is_progress_bar = (i == 0)
                padded_string = self.get_padded_string(
                    lines[i],
                    brackets=is_progress_bar,
                    options=line_prefs
                )
                if is_progress_bar:
                    text = self.get_highlighted_string(
                        padded_string,
                        pct
                    )
                else:
                    text = padded_string
                print(text)
            except IndexError:
                print()
        self.__started = True

    def print(self, *args):
        for i in range(len(self.__lines)):
            sys.stdout.write('\033[F')  # Go to previous line
            sys.stdout.write('\033[K')  # Clearn current line
        print(*args)
        for i in range(len(self.__lines)):
            print()
        self.refresh(*self.__last_msg)

    def get_padded_string(self, string, brackets=False, options={}):
        align = options.get('align', 'left')

        padding = 3 if brackets else 1
        columns = os.get_terminal_size().columns - padding
        string = string[:columns]

        line_string = ''

        if align == 'right':
            line_string = string.rjust(columns, ' ')
        else:
            line_string = string.ljust(columns, ' ')

        if brackets:
            line_string = f"[{line_string}]"

        return line_string

    def get_highlighted_string(
            self,
            bar_string,
            pct
    ):
        num_bars = round(pct*len(bar_string))
        highlighted_string = (
            '\033[7m'
            + bar_string[:num_bars]
            + '\033[0m'
            + bar_string[num_bars:]
        )
        return highlighted_string


def get_time_remaining_string(start, end):
    time_delta = math.ceil(end - start)
    diff = datetime.timedelta(seconds=time_delta)
    return str(diff)


def main(run_time=10, should_stop_callback=None):

    start_time = time.time()
    current_time = time.time()

    pb = ProgressBar(2)

    while True:
        time_remaining_string = get_time_remaining_string(
            current_time, start_time+run_time)
        # print(time_remaining_string)

        pct = (current_time - start_time) / run_time
        pb.refresh(
            pct,
            [
                time_remaining_string,
                f"{int(pct*100):d}%"
            ]
        )

        if should_stop_callback:
            if should_stop_callback():
                break

        wait_time = current_time + 0.2 - time.time()
        if wait_time > 0:
            time.sleep(wait_time)

        current_time = time.time()

        if current_time >= start_time + run_time:
            pb.refresh(
                1,
                [get_time_remaining_string(1, 1), "100%"]
            )
            break


if __name__ == '__main__':
    main()
