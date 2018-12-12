import arcade
import random

screen_width = 800
screen_height = 600
viewport_margin = 400
player_speed = 10

## Mis olekus mäng on
õpetus = 0
mäng = 1
mäng_läbi = 2
    

class MyGame(arcade.Window):
    
    def __init__(self, width, height):
        super().__init__(width, height)
        
        arcade.set_background_color(arcade.color.BLACK)
        
        self.current_state = õpetus
        self.instructions = []
        
        ## Õpetuse texture
        õpetused = arcade.load_texture("pildid/õpetus.png")
        self.instructions.append(õpetused)
       
        self.view_bottom = 0
        self.view_left = 0
        self.score = 0
        self.game_over = False
        self.score_x = 40
        self.wall_x = 800
        self.last_obstacle_x = 1000
        
    def setup(self):

        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.obstacle_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        
        self.player_sprite = arcade.Sprite("pildid/main_character.png", 1)
        self.player_sprite.center_x = 400
        self.player_sprite.center_y = 30
        self.player_list.append(self.player_sprite)
        
        floor_number = 0
        floor_x = 0
        while floor_number <= 18:
            self.wall_sprite = arcade.Sprite("pildid/põrand.png", 0.12)
            self.wall_sprite.center_x = floor_x
            self.wall_sprite.center_y = 25
            self.wall_list.append(self.wall_sprite)
            
            self.wall_sprite = arcade.Sprite("pildid/põrand.png", 0.12)
            self.wall_sprite.center_x = floor_x
            self.wall_sprite.center_y = 580
            self.wall_list.append(self.wall_sprite)
            floor_number += 1
            floor_x += 45
            
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite, self.wall_list, gravity_constant = 2)
        self.player_sprite.change_x = player_speed
           
        pass
    
    def draw_instructions_page(self, page_number):
        page_texture = self.instructions[page_number]
        arcade.draw_texture_rectangle(screen_width // 2, screen_height // 2, page_texture.width, page_texture.height, page_texture, 0)
   
    # Game over screen
    def draw_game_over(self):
        output = "Mäng läbi!"
        arcade.draw_text(output, 240, 400, arcade.color.WHITE, 54)
        
        output = "Vajuta, et uuesti alustada"
        arcade.draw_text(output, 310, 300, arcade.color.WHITE, 24)
       
    def draw_game(self):
        self.player_list.draw()
        self.wall_list.draw()
        self.obstacle_list.draw()
        self.coin_list.draw()
        
        # Skoor
        output = f"Score: {self.score}"
        arcade.draw_text(output, self.score_x, 20, arcade.color.WHITE, 14)
    
    # Õpetuse screeni joonistamine
    def on_draw(self):
        arcade.start_render()
        
        if self.current_state == õpetus:
            self.draw_instructions_page(0)

        elif self.current_state == mäng:
            self.draw_game()

        else:
            self.draw_game()
            self.draw_game_over()
            
    def on_mouse_press(self, x, y, button, modifiers):

        if self.current_state == õpetus:
            self.setup()
            self.current_state = mäng
        elif self.current_state == mäng_läbi:
            self.setup()
            self.current_state = mäng
        
    def update(self, delta_time):
        if self.current_state == mäng:
            changed = False
            right_bndry = self.view_left + screen_width - viewport_margin
            if self.player_sprite.right > right_bndry:
                self.view_left += self.player_sprite.right - right_bndry
                changed = True
            use_spatial_hash=False
            if changed:
                arcade.set_viewport(self.view_left, screen_width + self.view_left, self.view_bottom, screen_height + self.view_bottom)
                self.wall_sprite = arcade.Sprite("pildid/põrand.png", 0.12)
                self.wall_sprite.center_x = self.wall_x
                self.wall_sprite.center_y = 25
                if self.wall_x - self.player_sprite.center_x < 500:
                    self.wall_list.append(self.wall_sprite)
                
                self.wall_sprite = arcade.Sprite("pildid/põrand.png", 0.12)
                self.wall_sprite.center_x = self.wall_x
                self.wall_sprite.center_y = 580
                if self.wall_x - self.player_sprite.center_x < 500:
                    self.wall_list.append(self.wall_sprite)
                    self.wall_x += 45
                
                if self.wall_x % 50 == 0:
                    self.obstacle_sprite = arcade.Sprite("pildid/spike.png", 0.3)
                    self.obstacle_sprite.center_x = self.last_obstacle_x + random.randint(300, 600)
                    self.obstacle_sprite.center_y = 68
                    self.obstacle_list.append(self.obstacle_sprite)
                    self.coin_sprite = arcade.Sprite("pildid/coin.png", 0.08)
                    self.coin_sprite.center_x = self.last_obstacle_x + 50
                    self.coin_sprite.center_y = 70
                    for x in random.sample(range(self.coin_sprite.center_x, self.obstacle_sprite.center_x - 50), 1):
                        self.coin_sprite.center_x = x
                        self.coin_list.append(self.coin_sprite)
                    self.last_obstacle_x = self.obstacle_sprite.center_x
                        
                    
            for wall in self.wall_list:
                if self.player_sprite.center_x > wall.center_x + 400:
                    self.wall_list[0].kill()
                    
            for obstacle in self.obstacle_list:
                if self.player_sprite.center_x > obstacle.center_x + 600:
                    self.obstacle_list[0].kill()
                    
            for coin in self.coin_list:
               if self.player_sprite.center_x > coin.center_x + 600:
                    self.coin_list[0].kill()
            
            coins_hit = arcade.check_for_collision_with_list(self.player_sprite, self.coin_list)
            for coin in coins_hit:
                coin.kill()
                self.score += 1
                
            if not self.game_over:
                self.obstacle_list.update()
                self.wall_list.update()
                self.coin_list.update()
            
            self.score_x += 10
                
            if len(arcade.check_for_collision_with_list(self.player_sprite, self.obstacle_list)) > 0:
                self.current_state = mäng_läbi
                self.set_mouse_visible(True)
            self.physics_engine.update()
    
    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP:
            self.player_sprite.change_y = 30
            
    def on_key_release(self, key, modifiers):
        if key == arcade.key.UP:
            self.player_sprite.change_y = 0    
    
def main():
    game = MyGame(screen_width, screen_height)
    game.setup()
    arcade.run()
    
if __name__ == "__main__":
    main()
