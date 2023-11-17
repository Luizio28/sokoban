import curses

screen = curses.initscr()
curses.resize_term(28,86)
curses.start_color()

def setcursor (y, x):
   pass

def drawglyph(i,j,string):
    screen.addstr(i,j,string)
    screen.refresh()


def console_cursor(a):
    match a:
        case "hide":
            curses.curs_set(0)
        case "show":
            curses.curs_set(1)
        
def print_line(i,j,string: str,k):
    drawglyph(i,j,string+" "*(k-len(list(string))))