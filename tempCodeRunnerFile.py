    draw_bg()
                draw_shop()
                world.draw()
                draw_decoration()
                screen.blit(empty_heath_bar, (10, 10))
                CoinBarPlayer.draw()
                health_chart(player)
                bullet_char(player)
                draw_text(f'x {coin_player}', font, WHITE, 15 + CoinBarPlayer.image.get_width(), 79)
                # Nếu có người chơi
                if player:
                    player.draw()
                    draw_enemy(player)
                    coin_group.update(screen_scroll)
                    draw_coin()
                    bullet_enemy(player)
                    screen_scroll = player.move()
                    bg_scroll -= screen_scroll

                    # Kiểm tra coi người chơi chạm với đồng xu
                    for coin in coin_group:
                        if coin.rect.colliderect(player.coin_collision):
                            coin_group.remove(coin)
                            coin_player += 1
                            coin_recieved.play()

                    # Kiểm tra va chạm với mấy cái cửa hàng
                    for shop in shop_group:
                        if shop.rect.colliderect(player.coin_collision):
                            screen.blit(board, (870, 10))
                            # Ghi thông tin người chơi
                            draw_text('Info Player', font, 'White', 900, 20)
                            draw_text(f'Health: {player.health}', font, 'White', 880, 50)
                            draw_text(f'Max Health: {player.max_health}', font, 'White', 880, 75)
                            draw_text(f'Bullet speed: {speed_bullet}', font, 'White', 880, 105)
                            draw_text(f'Dame bonus: {dame_bullet}', font, 'White', 880, 135)
                            draw_text(f'Cooldown: {bullet_cooldown}', font, 'White', 880, 165)
                            pygame.draw.rect(screen, 'White', (SCREEN_WIDTH - 202, 208, 150, 20))
                            draw_text('+ 1 Dame: 10 xu', font, 'Black', SCREEN_WIDTH - 200, 210)
                            pygame.draw.rect(screen, 'White', (SCREEN_WIDTH - 202, 258, 150, 20))
                            draw_text('+ 15 Health: 10 xu', font, 'Black', SCREEN_WIDTH - 200, 260)
                            pygame.draw.rect(screen, 'White', (SCREEN_WIDTH - 202, 308, 150, 20))
                            draw_text('+ Speed BL: 15 xu', font, 'Black', SCREEN_WIDTH - 200, 310)
                            pygame.draw.rect(screen, 'White', (SCREEN_WIDTH - 202, 358, 150, 20))
                            draw_text('+ Full HP: 5 xu', font, 'Black', SCREEN_WIDTH - 200, 360)
                            pygame.draw.rect(screen, 'White', (SCREEN_WIDTH - 202, 408, 150, 20))
                            draw_text('+ Cooldown: 5 xu', font, 'Black', SCREEN_WIDTH - 200, 410)
                            if dame_upgrade.draw(screen):
                                if coin_player >= 10:
                                    dame_bullet += 1
                                    coin_player -= 10
                            if health_upgrade.draw(screen):
                                if coin_player >= 10:
                                    player.max_health += 15
                                    health_tile += 1
                                    coin_player -= 10
                            if speed_bullet_upgrade.draw(screen):
                                if coin_player >= 15 and speed_bullet < 2:
                                    speed_bullet += 1
                                    coin_player -= 15
                            if recover_health_upgrade.draw(screen):
                                if coin_player >= 5:
                                    player.health = player.max_health
                                    coin_player -= 5
                            if cooldown_upgrade.draw(screen):
                                if coin_player >= 5 and bullet_cooldown < 30:
                                    bullet_cooldown += 1
                                    coin_player -= 5

                    # Lấy sự kiện từ người chơi
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False
                        if event.type == pygame.KEYDOWN:
                            if event.type == pygame.K_ESCAPE:
                                running = False
                        # Sự kiện người chơi
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_a:
                                player.moving_left = True
                            if event.key == pygame.K_d:
                                player.moving_right = True
                            if event.key == pygame.K_w and player.in_air == False:
                                player.move_jump = True
                                jump.play()
                            if event.key == pygame.K_j:
                                player.rechange = True
                            if event.key == pygame.K_LCTRL:
                                player.run = True
                            if event.key == pygame.K_SPACE and player.shoot_cooldown == 0 and player.bullet > 0:
                                player.shoot = True
                                player.gun()
                                shot.play()
                        if event.type == pygame.KEYUP:
                            if event.key == pygame.K_a:
                                player.moving_left = False
                            if event.key == pygame.K_d:
                                player.moving_right = False
                            if event.key == pygame.K_w:
                                player.move_jump = False
                            if event.key == pygame.K_LCTRL:
                                player.run = False

                    if home_btn.draw(screen):
                        bg_scroll = 0
                        main_game = False
                        play_game = False
                        # Reset lại dữ liệu thế giới
                        world_data = reset_level()
                        # Tải level mới
                        level = 1
                        with open(f'Level/level{level}_data.csv', newline = '') as csvfile:
                            reader = csv.reader(csvfile, delimiter = ',')
                            for x, row in enumerate(reader):
                                for y, tile in enumerate(row):
                                    world_data[x][y] = int(tile)
                        world = World()
                        player = world.process_data(world_data)

                    # Kiểm tra coi người chơi có chạm vô cục next Level không
                    for pos in level_complete_group:
                        if player.coin_collision.colliderect(pos.rect) and check_enmy_alive():
                            level += 1
                            if level < MAX_LEVELS:
                                bg_scroll = 0
                                world_data = reset_level()
                                # Tải level mới
                                with open(f'Level/level{level}_data.csv', newline = '') as csvfile:
                                    reader = csv.reader(csvfile, delimiter = ',')
                                    for x, row in enumerate(reader):
                                        for y, tile in enumerate(row):
                                            world_data[x][y] = int(tile)
                                play_audio = False
                                world = World()
                                player = world.process_data(world_data)
                            elif level == MAX_LEVELS + 1:
                                level_complete_group.remove(pos)
                                victory = True


                    if player.health <= 0:
                        if play_audio == False:
                            game_over_audio.play()
                            play_audio = True
                        if menu_btn.draw(screen):
                            bg_scroll = 0
                            main_game = False
                            play_game = False
                            play_audio = False
                            world_data = reset_level()
                            # Tải level mới
                            with open(f'Level/level{level}_data.csv', newline = '') as csvfile:
                                reader = csv.reader(csvfile, delimiter = ',')
                                for x, row in enumerate(reader):
                                    for y, tile in enumerate(row):
                                        world_data[x][y] = int(tile)
                            world = World()
                            player = world.process_data(world_data)
                        if restart_btn.draw(screen):
                            bg_scroll = 0
                            play_audio = False
                            world_data = reset_level()
                            # Tải level mới
                            with open(f'Level/level{level}_data.csv', newline = '') as csvfile:
                                reader = csv.reader(csvfile, delimiter = ',')
                                for x, row in enumerate(reader):
                                    for y, tile in enumerate(row):
                                        world_data[x][y] = int(tile)
                            world = World()
                            player = world.process_data(world_data)
