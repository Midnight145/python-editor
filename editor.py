import curses, sys, os
# from curses import wrapper

# TODO: Make it so you can backspace newlines, then I think that this is done.
# TODO: Backspacing doesn't actually work, it always deletes from the end of the file
# TODO: Same with adding characters
# TODO: Move characters forward instead of overwriting
# TODO: IDEA: lines = file.readlines() and use the cursor's x, y coords as index for the lines


def main(stdscr, path):
    stdscr.clear()
    curses.noecho()
    stdscr.refresh()
    try:
        file = open(path, 'r+')
    except FileNotFoundError:
        open(path, 'w').close()
        os.lchmod(path, 0o644)
        file = open(path, 'r+')
    characters = []
    for line in file:
        stdscr.addstr(line)
        for char in line:
            characters.append(char)
    while True:
        try:
            (y, x) = stdscr.getyx()
            character = stdscr.getch()
            stdscr.refresh()
            if character == 127:
                try:
                    stdscr.delch(y, x-1)
                    del characters[-1]
                except curses.error:
                    pass
            elif character == 258:
                try:
                    stdscr.move(y+1, x)
                except curses.error:
                    pass
            elif character == 259:
                try:
                    stdscr.move(y-1, x)
                except curses.error:
                    pass
            elif character == 260:
                try:
                    stdscr.move(y, x-1)
                except curses.error:
                    pass
            elif character == 261:
                try:
                    stdscr.move(y, x+1)
                except curses.error:
                    pass
            else:
                stdscr.addch(character)
                characters.append(chr(character))
        except KeyboardInterrupt:
            with open("temp.txt", "w+") as f:
                if characters[-1] != '\n':
                    characters.append('\n')
                f.write(''.join(characters))
                os.rename(path, path + '.bak')
                os.rename("temp.txt", path)
            file.close()
            return 0


curses.wrapper(main, sys.argv[1])
print("Backup created at {}".format(sys.argv[1] + '.bak'))