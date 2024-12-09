for word in words:
    if font.size(current_line + word)[0] > (0.75 * GAME_WIDTH):
        lines.append(current_line)
        current_line = word + " "
    else:
        current_line += word + " "
