num_of_row_in_csv = sum(1 for row in player_reader) - 1
        for row_key in list(player_reader)[num_of_row_in_csv:num_of_row_in_csv+1]:
            print(row_key)
            text = STAT_FONT.render(row_key, 1, (255, 255, 255))
            win.blit(text, (WIN_WIDTH/2 - text.get_width()/2, 10))



except:
        #No csv found, a csv will be created with header
        print("log: No csv not found, a csv named FrappyBird_Score, printing high score board")
        with open('FrappyBird_Score.csv', 'w', newline='') as score_file:
            player_writer = csv.writer(score_file, delimiter=',')
            player_writer.writerow(['Name', 'High Score'])
        print_high_score_board'''


