import curses
import time


class Log:
    def __init__(self) -> None:
        self.log = open("log.txt", "w")

    def write(self, text: str) -> None:
        self.log.write(text + "\r\n")

    def close(self) -> None:
        self.log.flush()
        self.log.close()


class Screen:
    def __init__(self) -> None:
        self.stdscr = curses.initscr()
        nlines, ncols = self.stdscr.getmaxyx()
        self.nlines = nlines-3
        self.ncols = ncols-3
        self._boarder()

    def __str__(self) -> str:
        return f"nlines={self.nlines} ncols={self.ncols}"

    def _boarder(self) -> None:
        for x in range(self.ncols):
            self.stdscr.addstr(self.nlines, x, "_")

        for y in range(self.nlines):
            self.stdscr.addstr(y, 0, "|")

    def _should_skip(self, x: int, y: int) -> bool:
        return y < 0

    def write(self, x: int, y: int, text: str) -> None:
        scr_x = 2*x
        scr_y = self.nlines-y

        if self._should_skip(scr_x, scr_y):
            return

        self.stdscr.addstr(self.nlines-y, 2*x, text)
        self.stdscr.refresh()

    def close(self) -> None:
        self.stdscr.clear()
        self.stdscr.refresh()
        time.sleep(0.000_1)


def wait() -> None:
    try:
        while True:
            time.sleep(60)
    except KeyboardInterrupt:
        pass


def calc_x(x0: int, v: int, t: float) -> int:
    return x0 + int(v*t)


def calc_y(y0: int, v0: int, a: float, t: float) -> int:
    return y0 + int(v0*t) + int(a*t*t / 2)


def main() -> None:
    log = Log()

    try:
        scr = Screen()
        log.write(str(scr))
        refresh_rate = 0.1

        for i in range(100):
            x = calc_x(0, 50, i*refresh_rate)
            y = calc_y(0, 10, -1, i)
            log.write(f"x={x} y={y}")
            scr.write(x, y, "o")
            time.sleep(refresh_rate)

    except Exception as e:
        wait()
        scr.close()
        log.write(str(e))
    except KeyboardInterrupt:
        scr.close()
    finally:
        log.close()


if __name__ == '__main__':
    main()
