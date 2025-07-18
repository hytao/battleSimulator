import pandas as pd
import math
import numpy as np
import tkinter as tk
from tkinter import messagebox, scrolledtext, simpledialog
import re
import urllib.parse
import os
import json

# Constants for URL buffering
URL_CACHE_FILE = "url_cache.json"

def load_cached_url():
    """Load the last used Google Sheets URL from cache file"""
    try:
        if os.path.exists(URL_CACHE_FILE):
            with open(URL_CACHE_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('last_url', ''), data.get('last_saved', '')
    except Exception as e:
        print(f"無法載入快取URL: {e}")
    return '', ''

def save_cached_url(url):
    """Save the Google Sheets URL to cache file"""
    try:
        import datetime
        data = {
            'last_url': url,
            'last_saved': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        with open(URL_CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"無法儲存快取URL: {e}")

def clear_cached_url():
    """Clear the cached URL"""
    try:
        if os.path.exists(URL_CACHE_FILE):
            os.remove(URL_CACHE_FILE)
            return True
    except Exception as e:
        print(f"無法清除快取URL: {e}")
    return False

# === 公用函數 ===
def parse_google_sheets_url(url):
    """
    Parse Google Sheets URL to extract sheet ID and GID
    Supports both edit URLs and sharing URLs
    """
    try:
        # Remove any trailing whitespace
        url = url.strip()
        
        # Extract sheet ID from URL pattern: /spreadsheets/d/{SHEET_ID}/
        sheet_id_match = re.search(r'/spreadsheets/d/([a-zA-Z0-9-_]+)', url)
        if not sheet_id_match:
            raise ValueError("無法從URL中找到工作表ID")
        
        sheet_id = sheet_id_match.group(1)
        
        # Extract GID from URL
        gid = '0'  # Default GID
        
        # Look for gid in the URL (could be in edit URL or fragment)
        gid_match = re.search(r'[#&?]gid=([0-9]+)', url)
        if gid_match:
            gid = gid_match.group(1)
        
        return sheet_id, gid
    
    except Exception as e:
        raise ValueError(f"URL解析錯誤: {str(e)}")

def get_google_sheets_url():
    """
    Display a GUI dialog to get Google Sheets URL from user
    Returns (sheet_id, gid) or (None, None) if cancelled
    """
    # Load cached URL
    cached_url, last_saved = load_cached_url()
    
    # Create a larger custom dialog window instead of using simple dialogs
    root = tk.Tk()
    root.title("Google試算表連結輸入")
    
    # Make the window larger and properly sized
    window_width = 900
    window_height = 750  # Increased height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    # Ensure window doesn't exceed screen size
    max_height = int(screen_height * 0.9)  # Use 90% of screen height
    window_height = min(window_height, max_height)
    
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")
    root.resizable(True, True)
    root.minsize(700, 500)  # Set minimum size
    
    # Create a scrollable frame
    main_container = tk.Frame(root)
    main_container.pack(fill='both', expand=True, padx=10, pady=10)
    
    canvas = tk.Canvas(main_container)
    scrollbar = tk.Scrollbar(main_container, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)
    
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    # Main frame with padding inside scrollable frame
    main_frame = tk.Frame(scrollable_frame, padx=30, pady=30)
    main_frame.pack(fill='both', expand=True)
    
    # Title
    title_label = tk.Label(main_frame, text="Google試算表連結輸入", 
                          font=("Arial", 20, "bold"), fg="darkblue")
    title_label.pack(pady=(0, 20))
    
    # Instructions frame with proper text wrapping
    instructions_frame = tk.Frame(main_frame, relief="solid", borderwidth=2, bg="lightyellow")
    instructions_frame.pack(fill='x', pady=(0, 20))
    
    # Instructions with proper line breaks and formatting
    instruction_parts = [
        ("請輸入您的Google試算表網址", "Arial", 14, "bold"),
        ("", "Arial", 10, "normal"),  # Empty line
        ("支援的格式:", "Arial", 12, "bold"),
        ("• https://docs.google.com/spreadsheets/d/SHEET_ID/edit#gid=GID", "Courier", 10, "normal"),
        ("• https://docs.google.com/spreadsheets/d/SHEET_ID/edit?gid=GID", "Courier", 10, "normal"),
        ("• https://docs.google.com/spreadsheets/d/SHEET_ID/edit?usp=sharing&gid=GID", "Courier", 10, "normal"),
        ("", "Arial", 10, "normal"),  # Empty line
        ("設定步驟:", "Arial", 12, "bold"),
        ("1. 開啟您的Google試算表", "Arial", 11, "normal"),
        ("2. 點擊右上角的「共用」按鈕", "Arial", 11, "normal"),
        ("3. 將權限設定為「知道連結的使用者」可以檢視", "Arial", 11, "normal"),
        ("4. 複製分享連結並貼到下方", "Arial", 11, "normal"),
        ("", "Arial", 10, "normal"),  # Empty line
        ("範例:", "Arial", 12, "bold"),
    ]
    
    for text, font_family, font_size, font_weight in instruction_parts:
        if text:  # Skip empty lines for spacing
            label = tk.Label(instructions_frame, text=text, 
                           font=(font_family, font_size, font_weight), 
                           justify='left', anchor='w', bg="lightyellow")
            label.pack(fill='x', padx=15, pady=2)
        else:
            # Add spacing
            tk.Frame(instructions_frame, height=5, bg="lightyellow").pack()
    
    # Example URL in a separate scrollable text widget
    example_frame = tk.Frame(instructions_frame, bg="lightyellow")
    example_frame.pack(fill='x', padx=15, pady=(5, 15))
    
    example_text = tk.Text(example_frame, height=3, wrap=tk.WORD, 
                          font=("Courier", 9), bg="white", relief="sunken", borderwidth=1)
    example_text.pack(fill='x')
    example_text.insert("1.0", "https://docs.google.com/spreadsheets/d/1rf1uZHKJhhCQ_10qvzQkoSaD56ExFxE8SOWAxjXlwyo/edit?gid=489835885#gid=489835885")
    example_text.config(state=tk.DISABLED)
    
    # URL input section
    url_label = tk.Label(main_frame, text="請貼上您的Google試算表網址:", 
                        font=("Arial", 14, "bold"))
    url_label.pack(anchor='w', pady=(20, 10))
    
    # URL entry with scrollable text widget for long URLs
    url_frame = tk.Frame(main_frame)
    url_frame.pack(fill='x', pady=(0, 20))
    
    url_text = tk.Text(url_frame, height=3, wrap=tk.WORD, 
                      font=("Arial", 11), relief="solid", borderwidth=2)
    url_scrollbar = tk.Scrollbar(url_frame, orient="vertical", command=url_text.yview)
    url_text.configure(yscrollcommand=url_scrollbar.set)
    
    url_text.pack(side="left", fill="both", expand=True)
    url_scrollbar.pack(side="right", fill="y")
    
    # Insert cached URL or default text
    if cached_url:
        url_text.insert("1.0", cached_url)
        # Show message about cached URL
        cache_info_text = f"✅ 已載入上次使用的網址"
        if last_saved:
            cache_info_text += f" (儲存時間: {last_saved})"
        cache_info_label = tk.Label(main_frame, text=cache_info_text, 
                                   font=("Arial", 10), fg="darkgreen", bg="lightgreen")
        cache_info_label.pack(pady=(0, 10))
    else:
        url_text.insert("1.0", "https://docs.google.com/spreadsheets/d/")
    
    url_text.focus_set()  # Focus on the text widget
    
    # Result variable to store the return value
    result = [None, None]
    
    def get_url_text():
        return url_text.get("1.0", tk.END).strip()
    
    def on_ok():
        url = get_url_text()
        if not url:
            messagebox.showwarning("輸入錯誤", "請輸入Google試算表網址")
            return
        
        try:
            sheet_id, gid = parse_google_sheets_url(url)
            # Save the URL to cache if parsing was successful
            save_cached_url(url)
            result[0] = sheet_id
            result[1] = gid
            root.quit()
        except ValueError as e:
            messagebox.showerror("URL錯誤", str(e))
    
    def on_cancel():
        result[0] = None
        result[1] = None
        root.quit()
    
    def on_test_mode():
        result[0] = None
        result[1] = None
        root.quit()
    
    def on_clear_cache():
        if clear_cached_url():
            # Clear the text widget and insert default text
            url_text.delete("1.0", tk.END)
            url_text.insert("1.0", "https://docs.google.com/spreadsheets/d/")
            # Update cache info label if it exists
            for widget in main_frame.winfo_children():
                if isinstance(widget, tk.Label) and "已載入上次使用的網址" in widget.cget("text"):
                    widget.destroy()
                    break
            # Hide the clear cache button after clearing
            if cached_url and 'button_row2' in locals():
                button_row2.destroy()
            messagebox.showinfo("快取清除", "已清除快取的網址")
        else:
            messagebox.showerror("錯誤", "無法清除快取")
    
    # Button frame - fixed at bottom with proper spacing
    button_container = tk.Frame(main_container, bg="lightgray")
    button_container.pack(fill='x', side='bottom', pady=(10, 0))
    
    button_frame = tk.Frame(button_container, bg="lightgray")
    button_frame.pack(pady=15)
    
    # First row of buttons
    button_row1 = tk.Frame(button_frame, bg="lightgray")
    button_row1.pack(pady=(0, 10))
    
    # Buttons with larger size and better spacing
    ok_button = tk.Button(button_row1, text="確定", font=("Arial", 14, "bold"),
                         command=on_ok, bg="lightgreen", fg="darkgreen",
                         width=12, height=2, relief="raised", borderwidth=3)
    ok_button.pack(side=tk.LEFT, padx=(0, 15))
    
    cancel_button = tk.Button(button_row1, text="取消", font=("Arial", 14, "bold"),
                             command=on_cancel, bg="lightcoral", fg="darkred",
                             width=12, height=2, relief="raised", borderwidth=3)
    cancel_button.pack(side=tk.LEFT, padx=(0, 15))
    
    test_button = tk.Button(button_row1, text="使用測試模式", font=("Arial", 14, "bold"),
                           command=on_test_mode, bg="lightyellow", fg="darkorange",
                           width=15, height=2, relief="raised", borderwidth=3)
    test_button.pack(side=tk.LEFT)
    
    # Second row - Clear cache button (only show if cache exists)
    if cached_url:
        button_row2 = tk.Frame(button_frame, bg="lightgray")
        button_row2.pack()
        
        clear_cache_button = tk.Button(button_row2, text="清除快取網址", font=("Arial", 12),
                                      command=on_clear_cache, bg="lightgray", fg="black",
                                      width=20, height=1, relief="raised", borderwidth=2)
        clear_cache_button.pack()
    
    # Bind Enter key to OK button (when buttons have focus)
    def on_enter(event):
        on_ok()
    
    root.bind('<Control-Return>', on_enter)  # Ctrl+Enter for OK
    
    # Pack the canvas and scrollbar
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    # Bind mousewheel to canvas
    def on_mousewheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    canvas.bind("<MouseWheel>", on_mousewheel)
    
    # Run the dialog
    root.mainloop()
    root.destroy()
    
    return result[0], result[1]

def safe_int(value, default=0):
    try:
        return int(float(value)) if not pd.isna(value) else default
    except:
        return default

def safe_percentage(value, default=0.0):
    if pd.isna(value) or value is None:
        return default
    try:
        if isinstance(value, str):
            value = value.strip()
            if value.endswith('%'):
                return float(value.rstrip('%')) / 100
            else:
                return float(value)
        return float(value)
    except:
        return default

def distance(unit1, unit2):
    return abs(unit1.row - unit2.row) + abs(unit1.col - unit2.col)

def get_vigor_bonus(moral):
    if moral >= 12:
        return 30
    elif moral >= 8:
        return 20
    elif moral >= 4:
        return 10
    else:
        return 0

def parse_weapon_effect(weapon_effect_str):
    """
    Parse weapon effect string and return effect type and values
    Returns: dict with effect type and parameters
    """
    if not weapon_effect_str or pd.isna(weapon_effect_str):
        return None
    
    effect_str = str(weapon_effect_str).strip()
    if not effect_str:
        return None
    
    # Parse 易傷 effects: "易傷特殊30%" -> damage increase for specific weapon type
    if effect_str.startswith("易傷"):
        # Extract weapon type and percentage
        remaining = effect_str[2:]  # Remove "易傷"
        if remaining.endswith("%"):
            # Find where percentage starts (last consecutive digits before %)
            i = len(remaining) - 2  # Start before %
            while i >= 0 and remaining[i].isdigit():
                i -= 1
            
            if i >= 0:
                weapon_type = remaining[:i+1]
                percentage_str = remaining[i+1:-1]  # Remove %
                try:
                    percentage = float(percentage_str)
                    return {
                        'type': '易傷',
                        'weapon_type': weapon_type,
                        'percentage': percentage
                    }
                except ValueError:
                    pass
    
    # Parse 減防 effects: "減防30%" -> defense reduction
    elif effect_str.startswith("減防"):
        remaining = effect_str[2:]  # Remove "減防"
        if remaining.endswith("%"):
            percentage_str = remaining[:-1]  # Remove %
            try:
                percentage = float(percentage_str)
                return {
                    'type': '減防',
                    'percentage': percentage
                }
            except ValueError:
                pass
    
    # Parse 減攻 effects: "減攻30%" -> attack reduction
    elif effect_str.startswith("減攻"):
        remaining = effect_str[2:]  # Remove "減攻"
        if remaining.endswith("%"):
            percentage_str = remaining[:-1]  # Remove %
            try:
                percentage = float(percentage_str)
                return {
                    'type': '減攻',
                    'percentage': percentage
                }
            except ValueError:
                pass
    
    return None

def apply_weapon_effects(attacker, defender, use_max_weapon, defense_type):
    """
    Apply weapon effects and resistance to modify damage calculation parameters
    Returns: (damage_multiplier_bonus, defense_reduction, attack_reduction, resistance_reduction)
    """
    damage_multiplier_bonus = 0.0
    defense_reduction = 0.0  # This will be 0 since 減防 is now a permanent status effect
    attack_reduction = 0.0
    resistance_reduction = 0.0
    
    # Get weapon properties
    if use_max_weapon:
        weapon_effect = attacker.max_weapon_effect
        weapon_type = attacker.max_weapon_type
    else:
        weapon_effect = attacker.longest_weapon_effect
        weapon_type = attacker.longest_weapon_type
    
    # Parse weapon effects (but don't apply damage bonus from current attack's weapon effect)
    effect = parse_weapon_effect(weapon_effect)
    if effect:
        # Current weapon's 易傷 effect is NOT applied to its own damage calculation
        # It will be applied as a status effect after the attack
        
        # 減防 is now handled as a permanent status effect, not immediate
        # if effect['type'] == '減防':
        #     defense_reduction = effect['percentage']
        
        if effect['type'] == '減攻':
            # This will be applied as a status effect to the defender after this attack
            attack_reduction = effect['percentage']
    
    # Check for existing vulnerability effects on the defender (from previous attacks)
    # For combined weapon types (e.g., "特殊光束"), check all matching vulnerability effects
    if hasattr(defender.pilot, 'vulnerability_effects'):
        for vuln_weapon_type, vuln_percentage in defender.pilot.vulnerability_effects.items():
            # Check if weapon type contains the vulnerability weapon type
            if vuln_weapon_type in weapon_type:
                damage_multiplier_bonus += vuln_percentage
    
    # Apply damage resistance - only for exact weapon type matches
    if (defender.resistance_type and 
        not pd.isna(defender.resistance_type) and 
        str(defender.resistance_type).strip()):
        defender_resistance_type = str(defender.resistance_type).strip()
        # Resistance only applies if weapon type exactly matches resistance type
        if weapon_type == defender_resistance_type:
            resistance_reduction = defender.resistance_percent * 100  # Convert to percentage
    
    return damage_multiplier_bonus, defense_reduction, attack_reduction, resistance_reduction

def apply_status_effects_to_target(attacker, defender, use_max_weapon):
    """
    Apply status effects from weapon to the target unit
    This should be called after damage calculation to apply lasting effects
    """
    # Get weapon properties
    if use_max_weapon:
        weapon_effect = attacker.max_weapon_effect
    else:
        weapon_effect = attacker.longest_weapon_effect
    
    # Parse and apply weapon effects
    effect = parse_weapon_effect(weapon_effect)
    if effect:
        if effect['type'] == '減攻':
            # Apply attack reduction status effect to the defender
            # Same type effects don't stack - take the maximum value
            defender.pilot.attack_reduction_percent = max(
                defender.pilot.attack_reduction_percent, 
                effect['percentage']
            )
            # Cap at 100% to prevent negative attack
            defender.pilot.attack_reduction_percent = min(100.0, defender.pilot.attack_reduction_percent)
        
        elif effect['type'] == '減防':
            # Apply defense reduction status effect to the defender
            # Initialize defense_reduction_percent if it doesn't exist
            if not hasattr(defender.pilot, 'defense_reduction_percent'):
                defender.pilot.defense_reduction_percent = 0.0
            
            # Same type effects don't stack - take the maximum value
            defender.pilot.defense_reduction_percent = max(
                defender.pilot.defense_reduction_percent,
                effect['percentage']
            )
            # Cap at 100% to prevent negative defense
            defender.pilot.defense_reduction_percent = min(100.0, defender.pilot.defense_reduction_percent)
        
        elif effect['type'] == '易傷':
            # Apply vulnerability effect to the defender
            # Initialize vulnerability_effects if it doesn't exist
            if not hasattr(defender.pilot, 'vulnerability_effects'):
                defender.pilot.vulnerability_effects = {}
            
            weapon_type = effect['weapon_type']
            # For same weapon type, take maximum value (no stacking)
            # For different weapon types, they stack by having separate entries
            if weapon_type in defender.pilot.vulnerability_effects:
                defender.pilot.vulnerability_effects[weapon_type] = max(
                    defender.pilot.vulnerability_effects[weapon_type],
                    effect['percentage']
                )
            else:
                defender.pilot.vulnerability_effects[weapon_type] = effect['percentage']

def apply_status_effects_if_damage_dealt(attacker, defender, use_max_weapon, damage_dealt, target_hp_before):
    """
    Apply status effects from weapon to the target unit
    Effects are always applied regardless of damage dealt or HP reduction
    Returns True if status effects were applied, False otherwise
    """
    # Always apply status effects (removed HP check)
    apply_status_effects_to_target(attacker, defender, use_max_weapon)
    return True

def selectTarget(attacker, enemies, action_log, all_units):
    def can_reach_position(start_unit, target_row, target_col, max_move, all_units):
        """Check if a unit can reach a specific position considering movement restrictions"""
        if start_unit.row == target_row and start_unit.col == target_col:
            return True
            
        # Use BFS to find if target position is reachable
        from collections import deque
        queue = deque([(start_unit.row, start_unit.col, 0)])  # (row, col, steps_used)
        visited = set()
        visited.add((start_unit.row, start_unit.col))
        
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        
        while queue:
            current_row, current_col, steps = queue.popleft()
            
            if steps >= max_move:
                continue
                
            for dr, dc in directions:
                new_r = current_row + dr
                new_c = current_col + dc
                
                # Check boundaries
                if not (1 <= new_r <= 7 and 1 <= new_c <= 11):
                    continue
                    
                if (new_r, new_c) in visited:
                    continue
                
                # Check if we reached the target position
                if new_r == target_row and new_c == target_col:
                    # Can only stop here if position is not occupied
                    position_occupied = False
                    for unit in all_units:
                        if (unit != start_unit and unit.current_hp > 0 and 
                            unit.row == new_r and unit.col == new_c):
                            position_occupied = True
                            break
                    if not position_occupied:
                        return True
                
                # Units can move through any position (no blocking), 
                # they just can't stop on occupied positions
                visited.add((new_r, new_c))
                queue.append((new_r, new_c, steps + 1))
        
        return False
    
    max_attack_range = attacker.move + attacker.longest_weapon_range
    action_log.append(f"{attacker.name} 射程 {max_attack_range}")
    
    # Find enemies that can be reached and attacked
    reachable_targets = []
    for enemy in enemies:
        if enemy.current_hp <= 0:
            continue
            
        # Check all positions within weapon range of the enemy
        weapon_range = attacker.longest_weapon_range
        for r in range(max(1, enemy.row - weapon_range), min(8, enemy.row + weapon_range + 1)):
            for c in range(max(1, enemy.col - weapon_range), min(12, enemy.col + weapon_range + 1)):
                manhattan_dist = abs(r - enemy.row) + abs(c - enemy.col)
                if manhattan_dist <= weapon_range:
                    # Check if attacker can reach this attack position
                    if can_reach_position(attacker, r, c, attacker.move, all_units):
                        reachable_targets.append(enemy)
                        log_debug(action_log, f"{enemy.name} 可達成攻擊 (距離 {distance(attacker, enemy)})")
                        break
            else:
                continue
            break
    
    # Log distance info for all enemies
    for enemy in enemies:
        if enemy.current_hp > 0:
            log_debug(action_log, f"{enemy.name} 直線距離 {distance(attacker, enemy)} 移動 {attacker.move} 射程 {attacker.longest_weapon_range}")
    
    if reachable_targets:
        # 找到可攻擊目標：血量最低者
        target = min(reachable_targets, key=lambda e: e.current_hp)
        log_debug(action_log, f"選擇目標 {target.name} (血量最低)")
        return target, True
    else:
        # 找到距離最近的敵人作為移動目標（不攻擊）
        alive_enemies = [e for e in enemies if e.current_hp > 0]
        if not alive_enemies:
            return None, False
        nearest = min(alive_enemies, key=lambda e: distance(attacker, e))
        action_log.append(f"無法攻擊任何目標，向最近敵人 {nearest.name} 移動")
        return nearest, False

def move(attacker, target, can_attack, action_log, all_units):
    def is_position_occupied(row, col, all_units, current_unit):
        """Check if a position is occupied by another unit"""
        for unit in all_units:
            if unit != current_unit and unit.current_hp > 0 and unit.row == row and unit.col == col:
                return True
        return False
    
    def try_move(attacker, target_row, target_col, max_steps, all_units):
        # Direction preference: left > up > down > right
        directions = [(0, -1), (-1, 0), (1, 0), (0, 1)]  # left, up, down, right
        movement_path = []
        
        # If already at target position, no movement needed
        if attacker.row == target_row and attacker.col == target_col:
            log_debug(action_log, f"{attacker.name} 已在目標位置，無需移動")
            return movement_path
        
        for step in range(max_steps):
            best_direction = None
            min_distance = float('inf')
            best_priority = float('inf')  # Lower number = higher priority

            current_dist = abs(attacker.row - target_row) + abs(attacker.col - target_col)
            
            # If already at target, stop moving
            if current_dist == 0:
                break
            
            for priority, (dr, dc) in enumerate(directions):
                new_r = attacker.row + dr
                new_c = attacker.col + dc

                # Check boundaries
                if not (1 <= new_r <= 7 and 1 <= new_c <= 11):
                    continue
                
                # Check if this would be the final step (last movement)
                is_final_step = (step == max_steps - 1)
                
                # Only check for occupied position if this is the final step
                # Units can move through other units, just can't stop on them
                if is_final_step and is_position_occupied(new_r, new_c, all_units, attacker):
                    continue

                dist = abs(new_r - target_row) + abs(new_c - target_col)
                
                # Only consider moves that get us closer to the target
                if dist < current_dist:
                    # Prefer shorter distance first, then direction priority
                    if (dist < min_distance or 
                        (dist == min_distance and priority < best_priority)):
                        min_distance = dist
                        best_priority = priority
                        best_direction = (dr, dc)

            if best_direction:
                movement_path.append((attacker.row, attacker.col))  # Record current position
                new_row = attacker.row + best_direction[0]
                new_col = attacker.col + best_direction[1]
                
                attacker.row = new_row
                attacker.col = new_col
            else:
                # No valid move available that gets us closer
                if len(movement_path) == 0:
                    action_log.append(f"{attacker.name} 無法找到有效移動路徑")
                else:
                    action_log.append(f"{attacker.name} 移動受限，無法繼續前進")
                break
        
        return movement_path

    if not can_attack:
        action_log.append(f"{attacker.name} 向最近敵人 {target.name} 移動中")
        movement_path = try_move(attacker, target.row, target.col, attacker.move, all_units)
        return False, movement_path

    dist = distance(attacker, target)
    if dist <= attacker.move + attacker.max_weapon_range:
        weapon_range = attacker.max_weapon_range
        use_max_weapon = True
        action_log.append(f"{attacker.name} 使用最強武裝向 {target.name} 移動至射範 {weapon_range}")
    else:
        weapon_range = attacker.longest_weapon_range
        use_max_weapon = False
        action_log.append(f"{attacker.name} 使用最遠武裝向 {target.name} 移動至射範 {weapon_range}")

    # Find the optimal position to attack from (within weapon range)
    # Priority: 1) Positions that allow attack, 2) Minimum movement required, 3) Closer to target
    best_attack_position = None
    min_movement_required = float('inf')
    min_attack_distance = float('inf')  # Prefer positions closer to target for better positioning
    
    action_log.append(f"[DEBUG] 尋找最佳攻擊位置，武器射程: {weapon_range}, 可移動距離: {attacker.move}")
    action_log.append(f"[DEBUG] 目標位置: ({target.row}, {target.col})")
    action_log.append(f"[DEBUG] 當前位置: ({attacker.row}, {attacker.col})")
    
    # Check all positions within weapon range of the target
    valid_positions = []
    for r in range(max(1, target.row - weapon_range), min(8, target.row + weapon_range + 1)):
        for c in range(max(1, target.col - weapon_range), min(12, target.col + weapon_range + 1)):
            manhattan_dist_to_target = abs(r - target.row) + abs(c - target.col)
            if manhattan_dist_to_target <= weapon_range:
                # Check if this position is reachable and not occupied
                if not is_position_occupied(r, c, all_units, attacker):
                    # Calculate distance from current position to this attack position
                    movement_required = abs(attacker.row - r) + abs(attacker.col - c)
                    if movement_required <= attacker.move:
                        valid_positions.append({
                            'pos': (r, c),
                            'movement_required': movement_required,
                            'attack_distance': manhattan_dist_to_target
                        })
                        action_log.append(f"[DEBUG] 有效位置 ({r}, {c}): 移動距離={movement_required}, 攻擊距離={manhattan_dist_to_target}")
    
    if valid_positions:
        # Check if current position allows attack
        current_pos_distance = abs(attacker.row - target.row) + abs(attacker.col - target.col)
        current_can_attack = current_pos_distance <= weapon_range
        
        if current_can_attack:
            # If current position allows attack, don't move - stay in current position
            action_log.append(f"[DEBUG] 當前位置可以攻擊，無需移動 (距離: {current_pos_distance}, 射程: {weapon_range})")
            # Return current position as the "best" position with 0 movement required
            best_attack_position = (attacker.row, attacker.col)
            min_movement_required = 0
            min_attack_distance = current_pos_distance
            action_log.append(f"[DEBUG] 選中當前位置: {best_attack_position}, 移動距離: {min_movement_required}, 攻擊距離: {min_attack_distance}")
        else:
            # Current position doesn't allow attack, find optimal position to move to
            action_log.append(f"[DEBUG] 當前位置無法攻擊 (距離: {current_pos_distance}, 射程: {weapon_range})，尋找最佳攻擊位置")
            
            # Add direction preference as tiebreaker
            # Direction preference: left > up > down > right
            def calculate_direction_preference(pos):
                r, c = pos['pos']
                dr = r - attacker.row
                dc = c - attacker.col
                
                # Prefer pure directional movement over mixed movement
                # First, check if it's pure movement (only one direction)
                if dr == 0 and dc != 0:  # Pure horizontal movement
                    if dc < 0:  # Pure left
                        return 0
                    else:  # Pure right
                        return 3
                elif dc == 0 and dr != 0:  # Pure vertical movement
                    if dr < 0:  # Pure up
                        return 1
                    else:  # Pure down
                        return 2
                else:  # Mixed movement - use primary direction but with penalty
                    base_penalty = 10  # Penalty for mixed movement
                    if abs(dc) > abs(dr):  # Horizontal movement is primary
                        if dc < 0:  # Left primary
                            return base_penalty + 0
                        else:  # Right primary
                            return base_penalty + 3
                    else:  # Vertical movement is primary
                        if dr < 0:  # Up primary
                            return base_penalty + 1
                        else:  # Down primary
                            return base_penalty + 2
            
            # Sort by: 1) minimum movement, 2) minimum attack distance, 3) direction preference
            valid_positions.sort(key=lambda x: (x['movement_required'], x['attack_distance'], calculate_direction_preference(x)))
            best_position = valid_positions[0]
            best_attack_position = best_position['pos']
            min_movement_required = best_position['movement_required']
            min_attack_distance = best_position['attack_distance']
            
            action_log.append(f"[DEBUG] 選中最佳位置: {best_attack_position}, 移動距離: {min_movement_required}, 攻擊距離: {min_attack_distance}")
            action_log.append(f"[DEBUG] 方向偏好值: {calculate_direction_preference(best_position)}")
    
    if best_attack_position:
        target_row, target_col = best_attack_position
        if min_movement_required == 0:
            # No movement needed, already in optimal position
            action_log.append(f"{attacker.name} 已在最佳攻擊位置 ({target_row}, {target_col}) - 無需移動, 攻擊距離: {min_attack_distance}")
            movement_path = []  # Empty movement path
        else:
            # Move to the optimal attack position
            action_log.append(f"{attacker.name} 移動到最佳攻擊位置 ({target_row}, {target_col}) - 移動距離: {min_movement_required}, 攻擊距離: {min_attack_distance}")
            movement_path = try_move(attacker, target_row, target_col, attacker.move, all_units)
    else:
        # If no optimal position found, move as close as possible to target
        action_log.append(f"{attacker.name} 找不到最佳攻擊位置，盡可能接近目標")
        movement_path = try_move(attacker, target.row, target.col, attacker.move, all_units)

    return use_max_weapon, movement_path

def damageCalculation(attacker, defender, use_max_weapon=True, defense_type="否", return_debug_info=False, action_log=None):
    # Get weapon properties
    if use_max_weapon:
        weapon_stat = attacker.max_weapon_stat
        weapon_power = attacker.max_weapon_power
        weapon_type = attacker.max_weapon_type
    else:
        weapon_stat = attacker.longest_weapon_stat
        weapon_power = attacker.longest_weapon_power
        weapon_type = attacker.longest_weapon_type

    # Apply weapon effects and resistance
    damage_multiplier_bonus, defense_reduction, attack_reduction, resistance_reduction = apply_weapon_effects(
        attacker, defender, use_max_weapon, defense_type
    )

    if weapon_stat == "射擊":
        attackerCharacterAtk = attacker.pilot.shooting
    elif weapon_stat == "格鬥":
        attackerCharacterAtk = attacker.pilot.melee
    elif weapon_stat == "覺醒":
        attackerCharacterAtk = attacker.pilot.awakening
    elif weapon_stat == "全":
        attackerCharacterAtk = max(attacker.pilot.shooting, attacker.pilot.melee, attacker.pilot.awakening)
    else:
        attackerCharacterAtk = 0
    
    defenderCharacterDef = defender.pilot.defense
    
    # Apply attack reduction from weapon effects (immediate effect during this attack)
    attackerUnitAtk = attacker.atk
    if attack_reduction > 0:
        attackerUnitAtk = attackerUnitAtk * (1 - attack_reduction / 100.0)
    
    # Apply status effects from previous attacks (減攻 effects applied to this attacker)
    if attacker.pilot.attack_reduction_percent > 0:
        attackerUnitAtk = attackerUnitAtk * (1 - attacker.pilot.attack_reduction_percent / 100.0)
    
    # Calculate defender unit defense with support defense bonus if applicable
    if defense_type == "支援防禦":
        defenderUnitDef = math.floor(defender.defense + defender.pilot.support_defense_mod * defender.base_def)
    else:
        defenderUnitDef = defender.defense
    
    # Apply existing defense reduction status effects from previous attacks
    if hasattr(defender.pilot, 'defense_reduction_percent') and defender.pilot.defense_reduction_percent > 0:
        defenderUnitDef = defenderUnitDef * (1 - defender.pilot.defense_reduction_percent / 100.0)

    # Log damage calculation details in debug mode
    if action_log:
        log_debug(action_log, f"=== 傷害計算詳細 ===")
        log_debug(action_log, f"攻擊者: {attacker.name} | 防禦者: {defender.name}")
        log_debug(action_log, f"武器: {weapon_type} | 威力: {weapon_power} | 武器屬性: {weapon_stat}")
        log_debug(action_log, f"攻擊者機體攻擊: {attacker.atk} → {attackerUnitAtk:.1f} (減攻效果後)")
        log_debug(action_log, f"攻擊者駕駛員{weapon_stat}: {attackerCharacterAtk}")
        
        # Show original defense and all reductions applied
        original_def = defender.defense
        existing_def_reduction = getattr(defender.pilot, 'defense_reduction_percent', 0.0)
        log_debug(action_log, f"防禦者機體防禦: {original_def} → {defenderUnitDef:.1f}")
        if existing_def_reduction > 0:
            log_debug(action_log, f"  - 既有減防狀態: -{existing_def_reduction:.1f}%")
        
        log_debug(action_log, f"防禦者駕駛員防禦: {defenderCharacterDef}")
        if defense_type == "支援防禦":
            log_debug(action_log, f"支援防禦加成: +{defender.pilot.support_defense_mod * defender.base_def:.1f}")
        log_debug(action_log, f"武器效果 - 易傷加成: +{damage_multiplier_bonus:.1f}% | 減攻: -{attack_reduction:.1f}%")
        log_debug(action_log, f"抗性減免: -{resistance_reduction:.1f}%")

    characterStatRatio = max(0, attackerCharacterAtk - defenderCharacterDef) / 5000
    unitStatRatio = max(0, math.ceil(attackerUnitAtk / 10.0 - defenderUnitDef / 10.0)) / 5000
    characterSigmoidAdjustment = 1.0 / (math.exp((250 * (defenderCharacterDef - attackerCharacterAtk)) / 100000.0) + 1.0)
    unitSigmoidAdjustment = 1.0 / (math.exp((25 * (defenderUnitDef - attackerUnitAtk)) / 100000.0) + 1.0)

    baseDamage = math.ceil((characterStatRatio + unitStatRatio + characterSigmoidAdjustment + unitSigmoidAdjustment) * weapon_power)

    attackerCombinedStat = math.ceil((attackerUnitAtk + 2 * attackerCharacterAtk) / 10.0)
    targetCombinedStat = math.ceil((defenderUnitDef + 2 * defenderCharacterDef) / 10.0)

    offenseCorrectionExponent = ((5000 - attackerCombinedStat) * 30) / 100000.0
    defenseCorrectionExponent = ((5000 - targetCombinedStat) * 3) / 100000.0

    offenseDamageComponent = 100.0 / (math.exp(offenseCorrectionExponent) + 1.0)
    defenseMitigationComponent = -40.0 / (math.exp(defenseCorrectionExponent) + 1.0)

    damageCorrection = (offenseDamageComponent + defenseMitigationComponent) * baseDamage
    terrainCorrection = 1.0
    battleDamage = math.ceil((baseDamage + damageCorrection) * terrainCorrection)

    sumAttackerDamageDealtPercent = (attacker.pilot.damageIncrease + attacker.pilot.conditionalDamageIncrease + attacker.pilot.temporaryDamageIncrease) * 100
    sumAttackerCritDamageDealtPercent = 0
    attackerVigorDamageBonus = get_vigor_bonus(attacker.pilot.moral)
    sumDefenderDamageTakenPercent = (defender.pilot.conditionalDamageDecrease + defender.pilot.temporaryDamageDecrease) * 100

    # Apply weapon effect damage bonus and resistance reduction
    totalDamageMultiplierPercent = (sumAttackerDamageDealtPercent + sumAttackerCritDamageDealtPercent + 
                                   attackerVigorDamageBonus - sumDefenderDamageTakenPercent + 
                                   damage_multiplier_bonus - resistance_reduction)
    
    # Log damage multiplier details in debug mode
    if action_log:
        log_debug(action_log, f"基礎傷害: {baseDamage} | 戰鬥傷害: {battleDamage}")
        log_debug(action_log, f"傷害修正 - 增傷: +{sumAttackerDamageDealtPercent:.1f}% | 氣勢加成: +{attackerVigorDamageBonus:.1f}% | 減傷: -{sumDefenderDamageTakenPercent:.1f}%")
        log_debug(action_log, f"總傷害乘數: {totalDamageMultiplierPercent:.1f}%")
    
    scaledDamage = math.ceil((totalDamageMultiplierPercent * battleDamage) / 100.0)
    if defense_type == "否":
        defensiveCorrection = 1
    else:
        defensiveCorrection = defender.pilot.defensiveCorrection
    combinedDamage = (battleDamage + scaledDamage) * defensiveCorrection

    criticalCorrectionPercent = 0
    finalDamage = max(0, math.ceil(combinedDamage * ((criticalCorrectionPercent + 100.0) / 100.0)))
    
    # Log final damage calculation in debug mode
    if action_log:
        log_debug(action_log, f"縮放傷害: {scaledDamage} | 防禦修正: {defensiveCorrection:.2f}")
        log_debug(action_log, f"組合傷害: {combinedDamage:.1f} | 最終傷害: {finalDamage}")
        log_debug(action_log, f"=== 傷害計算結束 ===")
    
    if return_debug_info:
        debug_info = {
            'baseDamage': baseDamage,
            'weapon_power': weapon_power,
            'weapon_stat': weapon_stat,
            'weapon_type': weapon_type,
            'attackerCharacterAtk': attackerCharacterAtk,
            'defenderCharacterDef': defenderCharacterDef,
            'defenderUnitDef': defenderUnitDef,
            'attackerUnitAtk': attackerUnitAtk,
            'characterStatRatio': characterStatRatio,
            'totalDamageMultiplierPercent': totalDamageMultiplierPercent,
            'unitStatRatio': unitStatRatio,
            'damage_multiplier_bonus': damage_multiplier_bonus,
            'defense_reduction': defense_reduction,
            'attack_reduction': attack_reduction,
            'resistance_reduction': resistance_reduction
        }
        return finalDamage, debug_info
    
    return finalDamage

def close_battle_window():
    """Close the battle window when the battle is finished"""
    global _battle_window, _auto_play_timer_id
    
    # Cancel any pending auto-play timer
    if _auto_play_timer_id and _battle_window:
        try:
            _battle_window.after_cancel(_auto_play_timer_id)
        except:
            pass
        _auto_play_timer_id = None
    
    if _battle_window is not None:
        try:
            if _battle_window.winfo_exists():
                _battle_window.destroy()
        except:
            pass  # Window already destroyed
        _battle_window = None

# Global variables for window reuse
_battle_window = None
_main_frame = None
_debug_mode = False  # Global debug mode toggle
_damage_summary = {}  # Track damage dealt by each unit
_counter_damage_summary = {}  # Track damage dealt in counter phase
_auto_play = False  # Auto-play mode toggle
_auto_play_timer_id = None  # Timer ID for auto-play

def toggle_debug_mode():
    """Toggle debug mode on/off"""
    global _debug_mode
    _debug_mode = not _debug_mode
    return _debug_mode

def toggle_auto_play():
    """Toggle auto-play mode on/off"""
    global _auto_play, _auto_play_timer_id
    _auto_play = not _auto_play
    
    # Cancel existing timer if switching off
    if not _auto_play and _auto_play_timer_id:
        try:
            _battle_window.after_cancel(_auto_play_timer_id)
        except:
            pass
        _auto_play_timer_id = None
    
    return _auto_play

def add_damage_to_summary(attacker_name, damage, target_name):
    """Add damage to the summary tracker"""
    global _damage_summary
    if attacker_name not in _damage_summary:
        _damage_summary[attacker_name] = 0
    _damage_summary[attacker_name] += damage

def add_counter_damage_to_summary(attacker_name, damage, target_name):
    """Add damage to the counter attack summary tracker"""
    global _counter_damage_summary
    if attacker_name not in _counter_damage_summary:
        _counter_damage_summary[attacker_name] = 0
    _counter_damage_summary[attacker_name] += damage

def get_damage_summary():
    """Get formatted damage summary for attack phase"""
    global _damage_summary
    if not _damage_summary:
        return ""
    
    summary_lines = []
    for unit_name, total_damage in sorted(_damage_summary.items(), key=lambda x: x[1], reverse=True):
        summary_lines.append(f"{unit_name}: {total_damage}")
    
    return " | ".join(summary_lines)

def get_counter_damage_summary():
    """Get formatted damage summary for counter attack phase"""
    global _counter_damage_summary
    if not _counter_damage_summary:
        return ""
    
    summary_lines = []
    for unit_name, total_damage in sorted(_counter_damage_summary.items(), key=lambda x: x[1], reverse=True):
        summary_lines.append(f"{unit_name}: {total_damage}")
    
    return " | ".join(summary_lines)

def reset_damage_summary():
    """Reset damage summary for new combat action"""
    global _damage_summary, _counter_damage_summary
    _damage_summary = {}
    _counter_damage_summary = {}

def log_debug(action_log, message):
    """Add debug message only if debug mode is enabled"""
    global _debug_mode
    if _debug_mode:
        action_log.append(f"[DEBUG] {message}")

def log_action(action_log, message):
    """Add regular action message (always shown)"""
    action_log.append(message)

def get_filtered_log(action_log):
    """Filter log based on debug mode"""
    global _debug_mode
    if _debug_mode:
        return action_log
    else:
        # Only return non-debug messages
        return [msg for msg in action_log if not msg.startswith("[DEBUG]")]

def initialize_battle_window():
    """Initialize the battle window if it doesn't exist"""
    global _battle_window, _main_frame
    
    if _battle_window is None or not _battle_window.winfo_exists():
        _battle_window = tk.Tk()
        _battle_window.title("Battle Map")
        _battle_window.resizable(False, False)
        
        # Center the window on screen - made even larger to ensure buttons are visible
        window_width = 1600
        window_height = 1000
        screen_width = _battle_window.winfo_screenwidth()
        screen_height = _battle_window.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        _battle_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # Create main frame with scrollbar capability
        _main_frame = tk.Frame(_battle_window)
        _main_frame.pack(fill='both', expand=True, padx=20, pady=20)
    
    return _battle_window, _main_frame

def printMap(units, action_text="", active_unit=None, target_unit=None, stage_info="", movement_path=None, dead_units=None, battle_over=False):
    global _auto_play, _auto_play_timer_id, _debug_mode
    
    rows, cols = 7, 11
    
    # Get or create the battle window
    root, main_frame = initialize_battle_window()
    
    # Clear existing content
    for widget in main_frame.winfo_children():
        widget.destroy()
    
    # Title with larger font
    title_label = tk.Label(main_frame, text="=== 戰場地圖 (row x col) ===", 
                          font=("Courier", 18, "bold"))
    title_label.pack(pady=(0, 5))
    
    # Stage indicator with larger font and color
    if stage_info:
        stage_label = tk.Label(main_frame, text=f"當前階段: {stage_info}", 
                              font=("Arial", 16, "bold"), fg="darkblue", bg="lightblue")
        stage_label.pack(pady=(0, 10))
    
    # Create control frame for debug toggle, auto-play toggle, and legend
    control_frame = tk.Frame(main_frame)
    control_frame.pack(pady=(0, 15))
    
    # Debug toggle button
    debug_text = "關閉DEBUG" if _debug_mode else "開啟DEBUG"
    debug_color = "lightcoral" if _debug_mode else "lightgreen"
    
    def toggle_debug():
        global _debug_mode
        _debug_mode = toggle_debug_mode()
        # Refresh the display with new debug setting
        printMap(units, action_text, active_unit, target_unit, stage_info, movement_path, dead_units, battle_over)
    
    debug_button = tk.Button(control_frame, text=debug_text, font=("Arial", 12, "bold"),
                            command=toggle_debug, bg=debug_color, fg="darkred" if _debug_mode else "darkgreen",
                            width=12, height=1, relief="raised", borderwidth=2)
    debug_button.pack(side=tk.LEFT, padx=(0, 10))
    
    # Auto-play toggle button
    auto_text = "停止自動" if _auto_play else "自動播放"
    auto_color = "lightcoral" if _auto_play else "lightblue"
    
    # Define auto_button first, toggle function will be set later
    auto_button = tk.Button(control_frame, text=auto_text, font=("Arial", 12, "bold"),
                           bg=auto_color, fg="darkred" if _auto_play else "darkblue",
                           width=12, height=1, relief="raised", borderwidth=2)
    auto_button.pack(side=tk.LEFT, padx=(0, 20))
    
    # Legend with larger fonts
    legend_frame = tk.Frame(control_frame)
    legend_frame.pack(side=tk.LEFT)
    
    tk.Label(legend_frame, text="Team A:", font=("Arial", 12, "bold"), fg="red").pack(side=tk.LEFT, padx=(0, 15))
    tk.Label(legend_frame, text="■", font=("Arial", 16), fg="red", bg="lightcoral").pack(side=tk.LEFT, padx=(0, 20))
    tk.Label(legend_frame, text="Team B:", font=("Arial", 12, "bold"), fg="blue").pack(side=tk.LEFT, padx=(0, 15))
    tk.Label(legend_frame, text="■", font=("Arial", 16), fg="blue", bg="lightblue").pack(side=tk.LEFT, padx=(0, 20))
    tk.Label(legend_frame, text="Active:", font=("Arial", 12, "bold"), fg="green").pack(side=tk.LEFT, padx=(0, 15))
    tk.Label(legend_frame, text="■", font=("Arial", 16), fg="green", bg="lightgreen").pack(side=tk.LEFT, padx=(0, 20))
    tk.Label(legend_frame, text="Target:", font=("Arial", 12, "bold"), fg="orange").pack(side=tk.LEFT, padx=(0, 15))
    tk.Label(legend_frame, text="■", font=("Arial", 16), fg="orange", bg="orange").pack(side=tk.LEFT)
    
    # Map frame
    map_frame = tk.Frame(main_frame)
    map_frame.pack(pady=(0, 15))
    
    # Create grid of labels for the map
    grid_labels = []
    
    # Column headers with larger font
    header_frame = tk.Frame(map_frame)
    header_frame.grid(row=0, column=0, columnspan=cols+1)
    
    tk.Label(header_frame, text="   ", font=("Courier", 12)).grid(row=0, column=0)
    for c in range(1, cols + 1):
        tk.Label(header_frame, text=f"{c:2}", font=("Courier", 12), width=8).grid(row=0, column=c)
    
    # Determine team memberships
    team_a_units = set()
    team_b_units = set()
    
    for unit in units:
        # Include all units (alive and dead) for team determination
        # Use stored team information if available, otherwise fall back to position
        if hasattr(unit, 'team_name'):
            if unit.team_name == "Team A":
                team_a_units.add(unit.name)
            else:
                team_b_units.add(unit.name)
        else:
            # Fallback: determine by initial position
            if unit.col <= 5:
                team_a_units.add(unit.name)
            else:
                team_b_units.add(unit.name)
    
    # Create movement path set for quick lookup
    movement_cells = set()
    if movement_path:
        movement_cells = set(movement_path)
    
    # Create newly dead units set for special display (only show "被擊毀" for units that just died in this combat)
    newly_dead_units = set()
    if dead_units:
        for dead_unit in dead_units:
            newly_dead_units.add(dead_unit.name)
    
    # Initialize grid with unit positions and colors
    unit_info = {}
    for unit in units:
        r, c = unit.row, unit.col
        if 1 <= r <= rows and 1 <= c <= cols:
            name = unit.name.strip()
            
            # Check if unit is dead and if it's newly dead (for special display)
            is_dead = unit.current_hp <= 0
            is_newly_dead = name in newly_dead_units
            
            # Only show "被擊毀" for newly dead units during combat phases
            # For units that were already dead, don't display them at all during combat phases
            if is_dead:
                # Check if this is a combat phase (攻擊完成 or 戰鬥結束)
                is_combat_phase = (stage_info and ("攻擊完成" in stage_info or "戰鬥結束" in stage_info))
                
                if is_newly_dead and is_combat_phase:
                    # Show newly dead units with special formatting during combat phases
                    display = "被擊毀"
                    # Show overkill damage instead of current HP (which would be 0)
                    hp_display = f"-{unit.overkill_damage}" if unit.overkill_damage > 0 else "0"
                    # Dead units get gray background with white text
                    bg_color, text_color, border_width = "gray", "white", 3
                    support_info_lines = []  # No support info for dead units
                elif not is_combat_phase:
                    # Outside combat phases, show all dead units normally (shouldn't happen since they get removed)
                    display = "被擊毀"
                    # Show overkill damage instead of current HP (which would be 0)
                    hp_display = f"-{unit.overkill_damage}" if unit.overkill_damage > 0 else "0"
                    bg_color, text_color, border_width = "gray", "white", 3
                    support_info_lines = []  # No support info for dead units
                else:
                    # Dead unit that's not newly dead - skip it during combat phases to avoid confusion
                    continue
            else:
                # Alive units - normal display
                display = name[:5] if len(name) > 5 else name  # Allow more characters
                hp_display = f"{unit.current_hp}"
                
                # Determine color based on team, active status, target status
                if active_unit and unit.name == active_unit.name:
                    bg_color, text_color, border_width = "lightgreen", "darkgreen", 4
                elif target_unit and unit.name == target_unit.name:
                    bg_color, text_color, border_width = "orange", "black", 4
                elif unit.name in team_a_units:
                    bg_color, text_color, border_width = "lightcoral", "darkred", 2
                elif unit.name in team_b_units:
                    bg_color, text_color, border_width = "lightblue", "darkblue", 2
                else:
                    bg_color, text_color, border_width = "white", "black", 1
                
                # Generate support info strings for alive units
                support_info_lines = []
                
                # Support attack info (show only if original > 0)
                if unit.pilot.original_support_attack > 0:
                    support_info_lines.append(f"攻{unit.pilot.support_attack}/{unit.pilot.original_support_attack}")
                
                # Support defense info (show only if original > 0) 
                if unit.pilot.original_support_defense > 0:
                    support_info_lines.append(f"防{unit.pilot.support_defense}/{unit.pilot.original_support_defense}")
            
            unit_info[(r, c)] = {
                'text': display,
                'bg_color': bg_color,
                'text_color': text_color,
                'border_width': border_width,
                'hp_info': hp_display,
                'support_info': support_info_lines
            }
    
    # Create map grid with larger cells
    for r in range(1, rows + 1):
        # Row number with larger font
        tk.Label(map_frame, text=f"{r:2} |", font=("Courier", 12)).grid(row=r, column=0, sticky='e')
        
        row_labels = []
        for c in range(1, cols + 1):
            if (r, c) in unit_info:
                info = unit_info[(r, c)]
                text = info['text']
                bg_color = info['bg_color']
                text_color = info['text_color']
                border_width = info['border_width']
                
                # Create frame for unit cell to show HP and support info - made larger
                cell_frame = tk.Frame(map_frame, relief="solid", borderwidth=border_width,
                                    bg=bg_color, width=80, height=70)  # Increased height for support info
                cell_frame.grid(row=r, column=c, padx=2, pady=2, sticky="nsew")
                cell_frame.pack_propagate(False)
                
                # Unit name label with larger font
                name_label = tk.Label(cell_frame, text=text, font=("Courier", 11, "bold"), 
                                    bg=bg_color, fg=text_color)
                name_label.pack(expand=True)
                
                # HP label with larger font
                hp_label = tk.Label(cell_frame, text=info['hp_info'], font=("Courier", 9), 
                                  bg=bg_color, fg=text_color)
                hp_label.pack()
                
                # Support info labels (if any)
                if 'support_info' in info and info['support_info']:
                    for support_line in info['support_info']:
                        support_label = tk.Label(cell_frame, text=support_line, font=("Courier", 7), 
                                               bg=bg_color, fg=text_color)
                        support_label.pack()
                
            elif (r, c) in movement_cells:
                # Movement path cell - highlighted in light yellow
                label = tk.Label(map_frame, text="", font=("Arial", 14), 
                               width=8, height=3, relief="solid", borderwidth=2,
                               bg="lightyellow")
                label.grid(row=r, column=c, padx=2, pady=2)
            else:
                # Empty cell - made larger
                label = tk.Label(map_frame, text="", font=("Courier", 12), 
                               width=8, height=3, relief="solid", borderwidth=1,
                               bg="white")
                label.grid(row=r, column=c, padx=2, pady=2)
            row_labels.append(None)  # Placeholder
        grid_labels.append(row_labels)
    
    # Action text box with larger font and filtered content
    if action_text:
        text_label = tk.Label(main_frame, text="Action Details:", 
                            font=("Arial", 14, "bold"))
        text_label.pack(anchor='w', pady=(15, 5))
        
        # Filter action text based on debug mode
        filtered_text = get_filtered_log(action_text.split('\n'))
        display_text = '\n'.join(filtered_text)
        
        # Limit text box height to ensure buttons are visible - reduced height
        text_box = scrolledtext.ScrolledText(main_frame, height=6, width=120, 
                                           font=("Arial", 10), wrap=tk.WORD)
        text_box.pack(fill='x', pady=(0, 10))
        text_box.insert(tk.END, display_text)
        text_box.config(state=tk.DISABLED)
    
    # Fixed button area at bottom
    bottom_frame = tk.Frame(main_frame)
    bottom_frame.pack(side='bottom', fill='x', pady=(10, 0))
    
    # Instructions and buttons with larger fonts and sizes
    if battle_over:
        instruction_label = tk.Label(bottom_frame, text="Battle Over! Press any key or click End Battle", 
                                    font=("Arial", 14, "bold"))
    else:
        if _auto_play:
            instruction_label = tk.Label(bottom_frame, text="自動播放中 (每2秒自動繼續) - 可按任意鍵、點擊Continue或End Battle", 
                                        font=("Arial", 14, "bold"), fg="darkblue")
        else:
            instruction_label = tk.Label(bottom_frame, text="Press any key, click Continue, or End Battle", 
                                        font=("Arial", 14, "bold"))
    instruction_label.pack(pady=(0, 15))
    
    # Button frame to hold both buttons
    button_frame = tk.Frame(bottom_frame)
    button_frame.pack(pady=5)
    
    # Global variable to track if battle should end
    battle_ended = [False]
    
    def end_battle():
        battle_ended[0] = True
        # Don't destroy window, just break the wait loop
        root.quit()
    
    def continue_action():
        # Don't destroy window, just break the wait loop
        root.quit()
    
    # End Battle button (larger and more prominent)
    end_button = tk.Button(button_frame, text="End Battle", font=("Arial", 16, "bold"),
                          command=end_battle, bg="lightcoral", fg="darkred",
                          width=15, height=3, relief="raised", borderwidth=4)
    end_button.pack(side=tk.LEFT, padx=(0, 30))
    
    # Continue button (only show if battle is not over)
    if not battle_over:
        continue_button = tk.Button(button_frame, text="Continue", font=("Arial", 16, "bold"),
                                   command=continue_action, bg="lightgreen", fg="darkgreen",
                                   width=15, height=3, relief="raised", borderwidth=4)
        continue_button.pack(side=tk.LEFT)
    
    # Bind key press to close window
    def on_key_press(event):
        root.quit()
    
    root.bind('<Key>', on_key_press)
    root.focus_set()  # Ensure the window can receive key events
    
    # Auto-play timer function
    def auto_continue():
        global _auto_play_timer_id
        if _auto_play and not battle_over:
            _auto_play_timer_id = None
            root.quit()
    
    # Define toggle_auto function after all elements are created
    def toggle_auto():
        global _auto_play, _auto_play_timer_id
        _auto_play = toggle_auto_play()
        # Don't refresh the display when toggling auto-play
        # Just update the button text and color
        auto_text = "停止自動" if _auto_play else "自動播放"
        auto_color = "lightcoral" if _auto_play else "lightblue"
        auto_button.config(text=auto_text, bg=auto_color, fg="darkred" if _auto_play else "darkblue")
        
        # Update instruction label
        if not battle_over:
            if _auto_play:
                instruction_label.config(text="自動播放中 (每2秒自動繼續) - 可按任意鍵、點擊Continue或End Battle", fg="darkblue")
                # Start auto-play timer immediately if enabled
                if not _auto_play_timer_id:
                    _auto_play_timer_id = root.after(2000, auto_continue)
            else:
                instruction_label.config(text="Press any key, click Continue, or End Battle", fg="black")
                # Cancel auto-play timer if disabled
                if _auto_play_timer_id:
                    try:
                        root.after_cancel(_auto_play_timer_id)
                    except:
                        pass
                    _auto_play_timer_id = None
    
    # Set the command for the auto button
    auto_button.config(command=toggle_auto)
    
    # Set up auto-play timer if enabled and battle is not over
    if _auto_play and not battle_over:
        _auto_play_timer_id = root.after(2000, auto_continue)  # 2 second delay
    
    # Make window modal and wait for user input
    root.grab_set()
    root.mainloop()  # Use mainloop instead of wait_window
    root.grab_release()
    
    # Cancel auto-play timer if it's still pending
    if _auto_play_timer_id:
        try:
            root.after_cancel(_auto_play_timer_id)
        except:
            pass
        _auto_play_timer_id = None
    
    # Return whether battle was ended
    return battle_ended[0]

# === 類別定義 ===

class Pilot:
    def __init__(self, row):
        self.defensiveCorrection = safe_percentage(row.get('防禦減傷(盾牌)'))
        self.melee = safe_int(row.get('格鬥'))
        self.shooting = safe_int(row.get('射擊'))
        self.awakening = safe_int(row.get('覺醒'))
        self.defense = safe_int(row.get('防禦'))
        self.reaction = safe_int(row.get('反應'))
        self.chanceStage = safe_int(row.get('額外行動次數'))
        self.damageIncrease = safe_percentage(row.get('常駐增傷'))
        self.conditionalDamageIncrease  = safe_percentage(row.get('特殊增傷'))
        self.conditionalDamageDecrease = safe_percentage(row.get('特殊減傷'))
        self.support_defense = safe_int(row.get('支援防禦'))
        self.support_defense_mod = safe_percentage(row.get('支援防禦加成'))
        self.support_attack = safe_int(row.get('支援攻擊'))
        self.support_attack_mod = safe_percentage(row.get('支援攻擊加成'))
        self.moral = safe_int(row.get('初始MP'))
        self.ability1 = row.get('精神1', '')
        self.ability2 = row.get('精神2', '')
        self.ability3 = row.get('精神3', '')
        # Store original values for resetting
        self.original_support_attack = self.support_attack
        self.original_support_defense = self.support_defense
        # temporary
        self.temporaryDamageIncrease = 0.0
        self.temporaryDamageDecrease = 0.0
        # store original support values
        self.original_support_attack = safe_int(row.get('支援攻擊'))
        self.original_support_defense = safe_int(row.get('支援防禦'))
        # Status effects from weapon attacks
        self.attack_reduction_percent = 0.0  # Reduces attack when this unit attacks
        self.defense_reduction_percent = 0.0  # Reduces defense when this unit defends
        self.vulnerability_effects = {}  # Dict: weapon_type -> percentage for 易傷 effects

class Unit:
    def __init__(self, row):
        self.name = row.get('單位', '')
        self.position = safe_int(row.get('位置'))
        self.atk = safe_int(row.get('ATK'))
        self.defense = safe_int(row.get('DEF'))
        self.mobility = safe_int(row.get('MOB'))
        self.hp = safe_int(row.get('HP'))  # Initial/Max HP
        self.current_hp = self.hp  # Real-time HP, starts at max
        self.base_atk = math.floor(safe_int(row.get('atk(base)'))*(1+safe_percentage(row.get('突破'))))
        self.base_def = math.floor(safe_int(row.get('def(base)'))*(1+safe_percentage(row.get('突破'))))
        self.base_mob = math.floor(safe_int(row.get('mob(base)'))*(1+safe_percentage(row.get('突破'))))
        self.base_hp = math.floor(safe_int(row.get('hp(base)'))*(1+safe_percentage(row.get('突破'))))
        self.max_weapon_power = safe_int(row.get('最强武裝'))
        self.max_weapon_stat = row.get('最强武裝屬性', '')
        self.max_weapon_type = row.get('最强武裝類型', '')
        self.max_weapon_range = safe_int(row.get('最强武裝射程', ''))
        self.max_weapon_effect = row.get('最强武裝特效', '')
        self.longest_weapon_power = safe_int(row.get('最遠武裝'))
        self.longest_weapon_stat = row.get('最遠武裝屬性', '')
        self.longest_weapon_type = row.get('最遠武裝類型', '')
        self.longest_weapon_range = safe_int(row.get('最遠武裝射程', ''))
        self.longest_weapon_effect = row.get('最遠武裝特效', '')
        self.move = safe_int(row.get('移動', ''))
        self.original_move = self.move  # Store original movement for resetting after kills
        self.resistance_type = row.get('抗性', '')
        self.resistance_percent = safe_percentage(row.get('抗性數值'))
        self.action_order = safe_int(row.get('行動順序'))
        self.pilot = Pilot(row)
        # 新增屬性 (稍後由 Team 指派)
        self.row = None
        self.col = None
        self.overkill_damage = 0  # Track overkill damage when unit dies

    def heal(self, amount):
        """Heal the unit, but don't exceed max HP"""
        self.current_hp = min(self.hp, self.current_hp + amount)
        return self.current_hp

    def take_damage(self, damage):
        """Apply damage to current HP and track overkill"""
        if self.current_hp > 0:
            # Calculate overkill if damage would kill the unit
            if damage >= self.current_hp:
                self.overkill_damage = damage - self.current_hp
            else:
                self.overkill_damage = 0
        else:
            # Unit is already dead, all damage is overkill
            self.overkill_damage += damage
        
        self.current_hp = max(0, self.current_hp - damage)
        return self.current_hp

    def is_alive(self):
        """Check if unit is still alive"""
        return self.current_hp > 0

    def get_hp_percentage(self):
        """Get current HP as percentage of max HP"""
        return (self.current_hp / self.hp) * 100 if self.hp > 0 else 0

    def reset_hp(self):
        """Reset current HP to max HP"""
        self.current_hp = self.hp

class Team:
    def __init__(self, name, unit_rows):
        self.name = name
        self.units = [Unit(row) for row in unit_rows]

        # Define position mappings for each team
        # Position 1-5 correspond to specific grid coordinates
        if self.name == "Team A":
            position_map = {
                1: (4, 3),
                2: (6, 2), 
                3: (2, 2),
                4: (5, 1),
                5: (3, 1)
            }
            # Add "(红)" to all Team A unit names
            for unit in self.units:
                if not unit.name.endswith("(红)"):
                    unit.name += "(红)"
        elif self.name == "Team B":
            position_map = {
                1: (4, 9),
                2: (6, 10),
                3: (2, 10), 
                4: (5, 11),
                5: (3, 11)
            }
            # Add "(蓝)" to all Team B unit names
            for unit in self.units:
                if not unit.name.endswith("(蓝)"):
                    unit.name += "(蓝)"
        else:
            position_map = {}

        # Track used positions to ensure uniqueness
        used_positions = set()
        valid_units = []  # Only store units with valid positions
        
        # Assign positions based on unit.position
        for unit in self.units:
            unit.team_name = self.name  # Store team information in unit
            
            # Use unit.position to determine grid position
            if unit.position in position_map:
                if unit.position not in used_positions:
                    r, c = position_map[unit.position]
                    unit.row = r
                    unit.col = c
                    used_positions.add(unit.position)
                    unit.initial_pos = (r, c)  # Store initial position
                    valid_units.append(unit)
                else:
                    # Position already used, show error and ignore unit
                    print(f"❌ 錯誤: {self.name} 的單位 '{unit.name}' 位置 {unit.position} 重複，該單位將被忽略")
            else:
                # Invalid position number, show error and ignore unit
                print(f"❌ 錯誤: {self.name} 的單位 '{unit.name}' 位置 {unit.position} 無效 (必須為1-5)，該單位將被忽略")
        
        # Replace units list with only valid units
        self.units = valid_units
        
        # Show summary of valid units
        if valid_units:
            print(f"✅ {self.name} 成功載入 {len(valid_units)} 個單位: {[unit.name for unit in valid_units]}")
        else:
            print(f"⚠️  警告: {self.name} 沒有任何有效單位！")

class Battleground:
    def __init__(self, team_a_rows, team_b_rows):
        self.team_a = Team("Team A", team_a_rows)
        self.team_b = Team("Team B", team_b_rows)

def reset_support_counters(all_units):
    """Reset support attack and defense counters for all units at the beginning of each round"""
    for unit in all_units:
        if unit.current_hp > 0:
            # Reset to original values from the data
            unit.pilot.support_attack = safe_int(unit.pilot.original_support_attack)
            unit.pilot.support_defense = safe_int(unit.pilot.original_support_defense)

def reset_status_effects(all_units):
    """Reset status effects for all units at the beginning of each round"""
    for unit in all_units:
        if unit.current_hp > 0:
            # Reset attack reduction from 減攻 effects
            unit.pilot.attack_reduction_percent = 0.0
            # Reset defense reduction from 減防 effects
            if hasattr(unit.pilot, 'defense_reduction_percent'):
                unit.pilot.defense_reduction_percent = 0.0
            # Reset vulnerability effects from 易傷 effects
            if hasattr(unit.pilot, 'vulnerability_effects'):
                unit.pilot.vulnerability_effects = {}

# === 戰鬥主流程 ===

def use_pilot_abilities(attacker, all_units, action_log):
    """Handle pilot ability usage based on conditions"""
    abilities_used = []
    
    # Get all three abilities
    abilities = [attacker.pilot.ability1, attacker.pilot.ability2, attacker.pilot.ability3]
    abilities = [str(ability).strip() for ability in abilities if ability and str(ability).strip() and str(ability).strip() != 'nan']
    
    # Debug: Print pilot abilities
    raw_abilities = [attacker.pilot.ability1, attacker.pilot.ability2, attacker.pilot.ability3]
    action_log.append(f"[DEBUG] {attacker.name} 精神能力: {raw_abilities} -> 有效: {abilities}")
    action_log.append(f"[DEBUG] 當前士氣: {attacker.pilot.moral}, HP: {attacker.current_hp}/{attacker.hp}")
    
    # Calculate minimum distance to any unit
    all_other_units = [unit for unit in all_units if unit != attacker and unit.current_hp > 0]
    if all_other_units:
        min_distance = min(distance(attacker, unit) for unit in all_other_units)
        action_log.append(f"[DEBUG] 最近敵人距離: {min_distance}, 移動+射程+1: {attacker.move + attacker.longest_weapon_range + 1}")
    else:
        min_distance = float('inf')
        action_log.append(f"[DEBUG] 沒有其他存活單位")
    
    # Check for movement/range abilities (priority 1)
    if min_distance == attacker.move + attacker.longest_weapon_range + 1:
        action_log.append(f"[DEBUG] 觸發移動/射程檢查條件")
        for ability in abilities:
            if ability == "移動":
                attacker.move += 1
                action_log.append(f"{attacker.name} 發動精神「移動」，移動力增加1")
                abilities_used.append(ability)
                break
            elif ability == "射程":
                attacker.longest_weapon_range += 1
                action_log.append(f"{attacker.name} 發動精神「射程」，最遠武裝射程增加1")
                abilities_used.append(ability)
                break
    else:
        action_log.append(f"[DEBUG] 移動/射程條件不符")
    
    # Check for MP abilities (priority 2)
    if not abilities_used:
        action_log.append(f"[DEBUG] 檢查MP能力，當前士氣: {attacker.pilot.moral}")
        for ability in abilities:
            if ability.startswith("MP") and attacker.pilot.moral >= 2:
                try:
                    # Extract the number after "MP"
                    mp_increase = int(ability[2:])
                    old_moral = attacker.pilot.moral
                    attacker.pilot.moral = min(12, attacker.pilot.moral + mp_increase)
                    action_log.append(f"{attacker.name} 發動精神「{ability}」，士氣從 {old_moral} 增加到 {attacker.pilot.moral}")
                    abilities_used.append(ability)
                    break
                except (ValueError, IndexError):
                    action_log.append(f"[DEBUG] MP能力格式錯誤: {ability}")
                    continue
    
    # Check for healing ability (priority 3)
    if not abilities_used:
        hp_percentage = (attacker.current_hp / attacker.hp) * 100
        action_log.append(f"[DEBUG] 檢查回血能力，當前HP百分比: {hp_percentage:.1f}%")
        for ability in abilities:
            if ability == "回血" and attacker.current_hp < attacker.hp * 0.5:
                heal_amount = int(attacker.hp * 0.5)
                old_hp = attacker.current_hp
                attacker.heal(heal_amount)
                action_log.append(f"{attacker.name} 發動精神「回血」，HP從 {old_hp} 恢復到 {attacker.current_hp}")
                abilities_used.append(ability)
                break
    
    # Check if can attack any unit (for attack burst abilities)
    can_attack_someone = False
    for enemy in all_other_units:
        if distance(attacker, enemy) <= attacker.move + attacker.longest_weapon_range:
            can_attack_someone = True
            break
    action_log.append(f"[DEBUG] 能否攻擊敵人: {can_attack_someone}")
    
    # Check for attack burst abilities (priority 4)
    if not abilities_used and can_attack_someone:
        action_log.append(f"[DEBUG] 檢查攻擊爆裂能力")
        for ability in abilities:
            if ability.startswith("攻擊爆裂"):
                try:
                    # Extract the percentage after "攻擊爆裂", handle % symbol
                    percent_str = ability[4:].rstrip('%')  # Remove % if present
                    burst_percent = float(percent_str) / 100.0
                    attacker.pilot.temporaryDamageIncrease += burst_percent
                    action_log.append(f"{attacker.name} 發動精神「{ability}」，暫時增傷 +{burst_percent*100:.0f}%")
                    abilities_used.append(ability)
                    break
                except (ValueError, IndexError):
                    action_log.append(f"[DEBUG] 攻擊爆裂能力格式錯誤: {ability}")
                    continue
    
    # Check for defense abilities (priority 5 - only if no other ability used)
    if not abilities_used:
        action_log.append(f"[DEBUG] 檢查防禦能力")
        for ability in abilities:
            if ability.startswith("防禦"):
                try:
                    # Extract the percentage after "防禦", handle % symbol
                    percent_str = ability[2:].rstrip('%')  # Remove % if present
                    defense_percent = float(percent_str) / 100.0
                    attacker.pilot.temporaryDamageDecrease += defense_percent
                    action_log.append(f"{attacker.name} 發動精神「{ability}」，暫時減傷 +{defense_percent*100:.0f}%")
                    abilities_used.append(ability)
                    break
                except (ValueError, IndexError):
                    action_log.append(f"[DEBUG] 防禦能力格式錯誤: {ability}")
                    continue
    
    if not abilities_used:
        action_log.append(f"[DEBUG] {attacker.name} 沒有觸發任何精神能力")
    
    return abilities_used

def Action(attacker, allies, enemies):
    if attacker.current_hp <= 0:
        return False

    # Reset damage summary for this combat action
    reset_damage_summary()
    
    action_log = []  # Collect action descriptions
    log_action(action_log, f"{attacker.name} 開始行動 (HP: {attacker.current_hp}/{attacker.hp})")
    
    # Initialize variables for vigor tracking
    valid_support = []
    valid_counter = []
    
    # Reset temporary effects from previous actions
    attacker.pilot.temporaryDamageIncrease = 0.0
    attacker.pilot.temporaryDamageDecrease = 0.0
    
    # Use pilot abilities at the start of action
    all_units = allies + enemies
    abilities_used = use_pilot_abilities(attacker, all_units, action_log)
    
    # Stage 1: Seeking target
    stage_info = f"{attacker.name} 尋找目標中"
    battle_ended = printMap(all_units, "\n".join(action_log), active_unit=attacker, stage_info=stage_info)
    if battle_ended:
        return True  # Battle was ended by user

    target, can_attack = selectTarget(attacker, enemies, action_log, all_units)
    if not target:
        log_action(action_log, f"{attacker.name} 找不到任何目標")
        stage_info = f"{attacker.name} 無目標可攻擊"
        battle_ended = printMap(all_units, "\n".join(action_log), active_unit=attacker, stage_info=stage_info)
        return battle_ended

    log_action(action_log, f"{attacker.name} 選擇目標: {target.name}")

    # Stage 2: Moving towards target
    stage_info = f"{attacker.name} 向 {target.name} 移動中"
    use_max_weapon_result = move(attacker, target, can_attack, action_log, all_units)
    
    if isinstance(use_max_weapon_result, tuple):
        use_max_weapon, movement_path = use_max_weapon_result
    else:
        use_max_weapon = use_max_weapon_result
        movement_path = []

    # Show movement path
    battle_ended = printMap(all_units, "\n".join(action_log), active_unit=attacker, target_unit=target, 
                           stage_info=stage_info, movement_path=movement_path)
    if battle_ended:
        return True

    if not can_attack:
        log_action(action_log, f"{attacker.name} 移動接近 {target.name}，但無法攻擊")
        stage_info = f"{attacker.name} 移動完成，無法攻擊"
        battle_ended = printMap(all_units, "\n".join(action_log), active_unit=attacker, target_unit=target, stage_info=stage_info)
        return battle_ended

    # Stage 3: Combat begins
    stage_info = f"{attacker.name} 攻擊 {target.name}"

    # Stage 3: Combat begins
    stage_info = f"{attacker.name} 攻擊 {target.name}"
    
    # === 支援防禦判斷 ===
    potential_defenders = [
        unit for unit in enemies
        if unit.current_hp > 0 and unit != target
        and unit.pilot.support_defense > 0
        and distance(unit, target) <= unit.move
    ]
    
    if potential_defenders:
        # Debug: Show available support defense units and their remaining counts
        defense_info = [(u.name, u.pilot.support_defense) for u in potential_defenders]
        log_debug(action_log, f"可用支援防禦單位: {defense_info}")
    
    support_defender = None
    if potential_defenders:
        # Calculate damage that would be taken by each potential defender
        defenders_with_damage = []
        for unit in potential_defenders:
            dmg = damageCalculation(attacker, unit, use_max_weapon, "支援防禦", action_log=action_log)
            can_survive = dmg < unit.current_hp
            defenders_with_damage.append((unit, dmg, can_survive))
            log_debug(action_log, f"{unit.name} 支援防禦傷害預估: {dmg}, 可存活: {can_survive}, 當前HP: {unit.current_hp}")
        
        # Separate survivors and non-survivors
        survivors = [(unit, dmg) for unit, dmg, can_survive in defenders_with_damage if can_survive]
        non_survivors = [(unit, dmg) for unit, dmg, can_survive in defenders_with_damage if not can_survive]
        
        if survivors:
            # 1. Select the unit with least damage taken among all units that can survive
            support_defender = min(survivors, key=lambda x: x[1])[0]
            log_debug(action_log, f"選擇存活者中受傷最輕的: {support_defender.name}")
        elif non_survivors:
            # 2. If no unit can survive, select the unit with highest damage taken
            support_defender = max(non_survivors, key=lambda x: x[1])[0]
            log_debug(action_log, f"無存活者，選擇受傷最重的: {support_defender.name}")

    if support_defender:
        real_target = support_defender
        defense_type = "支援防禦"
        stage_info = f"{attacker.name} 攻擊 {target.name} (由 {support_defender.name} 支援防禦)"
        log_action(action_log, f"{support_defender.name} 為 {target.name} 進行支援防禦")
        log_debug(action_log, f"支援防禦次數: {support_defender.pilot.support_defense-1}")
        # Decrement support defense count
        support_defender.pilot.support_defense -= 1
    else:
        real_target = target
        # === 自我防禦判斷 ===
        can_counter = distance(target, attacker) <= target.longest_weapon_range
        dmg_if_defend = damageCalculation(attacker, target, use_max_weapon, "防禦", action_log=action_log)
        dmg_if_no_defend = damageCalculation(attacker, target, use_max_weapon, "否", action_log=action_log)
        
        # A unit should defend ONLY if:
        # 1. They cannot counter attack (out of range), OR
        # 2. They would die without defending AND defending would save them
        would_die_without_defend = dmg_if_no_defend >= target.current_hp
        would_survive_with_defend = dmg_if_defend < target.current_hp
        
        if not can_counter or (would_die_without_defend and would_survive_with_defend):
            defense_type = "防禦"
            stage_info = f"{attacker.name} 攻擊 {target.name} (防禦中)"
            if not can_counter:
                log_action(action_log, f"{target.name} 選擇防禦 - 無法反擊 (距離: {distance(target, attacker)}, 射程: {target.longest_weapon_range})")
            else:
                log_action(action_log, f"{target.name} 選擇防禦 - 防禦可避免死亡 (無防禦傷害: {dmg_if_no_defend}, 防禦傷害: {dmg_if_defend}, 當前HP: {target.current_hp})")
        else:
            defense_type = "否"
            if can_counter:
                log_action(action_log, f"{target.name} 選擇不防禦 - 可以反擊且不會死亡 (無防禦傷害: {dmg_if_no_defend}, 當前HP: {target.current_hp})")
            else:
                log_action(action_log, f"{target.name} 選擇不防禦 - 防禦無法避免死亡 (無防禦傷害: {dmg_if_no_defend}, 防禦傷害: {dmg_if_defend}, 當前HP: {target.current_hp})")

    # Show combat preparation
    battle_ended = printMap(all_units, "\n".join(action_log), active_unit=attacker, target_unit=real_target, stage_info=stage_info)
    if battle_ended:
        return True

    # === 支援攻擊選擇 (優化版) ===
    valid_support = optimize_support_attacks(attacker, allies, target, real_target, defense_type, action_log)

    # Stage 4: Damage resolution
    stage_info = f"傷害計算中 - {attacker.name} vs {real_target.name}"
    dead_units = []  # Track units that die during this phase
    
    # === 實際套用支援攻擊與主攻擊 ===
    target_killed_by_support = False
    for unit in valid_support:
        target_hp_before = real_target.current_hp
        dmg, debug_info = damageCalculation(unit, real_target, True, defense_type, return_debug_info=True, action_log=action_log)
        real_target.take_damage(dmg)
        add_damage_to_summary(unit.name, dmg, real_target.name)
        # Apply status effects only if HP was successfully reduced
        effects_applied = apply_status_effects_if_damage_dealt(unit, real_target, True, dmg, target_hp_before)
        
        log_action(action_log, f"{unit.name} 支援攻擊 {real_target.name} 造成 {dmg} 傷害")
        log_debug(action_log, f"基礎傷害: {debug_info['baseDamage']}, 武器: {debug_info['weapon_power']}, ATK: {debug_info['attackerUnitAtk']}, DEF: {debug_info['defenderUnitDef']}, charAtk: {debug_info['attackerCharacterAtk']}, charDef: {debug_info['defenderCharacterDef']}, totalDamageMultiplierPercent: {debug_info['totalDamageMultiplierPercent']}, 剩餘 {real_target.current_hp}/{real_target.hp}, 剩餘支援攻擊次數: {unit.pilot.support_attack-1}")
        if effects_applied:
            log_debug(action_log, "狀態效果已套用")
        
        # Decrement support attack count
        unit.pilot.support_attack -= 1
        if real_target.current_hp <= 0:
            log_action(action_log, f"{real_target.name} 被支援攻擊擊毀")
            dead_units.append(real_target)
            target_killed_by_support = True
            break

    # Main attacker always attacks, even if target is already dead
    target_hp_before = real_target.current_hp
    dmg, debug_info = damageCalculation(attacker, real_target, use_max_weapon, defense_type, return_debug_info=True, action_log=action_log)
    if not target_killed_by_support:
        real_target.take_damage(dmg)
        add_damage_to_summary(attacker.name, dmg, real_target.name)
        # Apply status effects only if HP was successfully reduced
        effects_applied = apply_status_effects_if_damage_dealt(attacker, real_target, use_max_weapon, dmg, target_hp_before)
        
        log_action(action_log, f"{attacker.name} 攻擊 {real_target.name} 造成 {dmg} 傷害")
        log_debug(action_log, f"基礎傷害: {debug_info['baseDamage']}, 武器: {debug_info['weapon_power']}, ATK: {debug_info['attackerUnitAtk']}, DEF: {debug_info['defenderUnitDef']}, charAtk: {debug_info['attackerCharacterAtk']}, charDef: {debug_info['defenderCharacterDef']}, totalDamageMultiplierPercent: {debug_info['totalDamageMultiplierPercent']}, 剩餘 {real_target.current_hp}/{real_target.hp}")
        if effects_applied:
            log_debug(action_log, "狀態效果已套用")
        
        if real_target.current_hp <= 0:
            log_action(action_log, f"{real_target.name} 被主攻擊擊毀")
            if real_target not in dead_units:
                dead_units.append(real_target)
    else:
        # Don't apply status effects if target is already dead
        log_debug(action_log, f"{attacker.name} 攻擊已死亡的 {real_target.name} 造成 {dmg} 傷害 (基礎傷害: {debug_info['baseDamage']}, 武器: {debug_info['weapon_power']})")

    # Show damage results with dead units highlighted
    attack_damage_summary = get_damage_summary()  # Attack phase damage
    if dead_units:
        if attack_damage_summary:
            stage_info = f"攻擊完成 - {', '.join([u.name for u in dead_units])} 被擊毀 ({attack_damage_summary})"
        else:
            stage_info = f"攻擊完成 - {', '.join([u.name for u in dead_units])} 被擊毀"
    else:
        if attack_damage_summary:
            stage_info = f"攻擊完成 - 無單位被擊毀 ({attack_damage_summary})"
        else:
            stage_info = f"攻擊完成 - 無單位被擊毀"
    
    initial_target_dead = target.current_hp <= 0
    battle_ended = printMap(all_units, "\n".join(action_log), active_unit=attacker, target_unit=real_target, 
                           stage_info=stage_info, dead_units=dead_units)
    if battle_ended:
        return True

    # === 反擊階段 (優化版) ===
    if not initial_target_dead:
        # Check if target can actually counter attack (within range AND not defending)
        can_counter = distance(target, attacker) <= target.longest_weapon_range
        target_is_defending = defense_type == "防禦"
        
        # Support counter attacks can happen even if target cannot counter or is defending
        stage_info = f"反擊階段 - {target.name} vs {attacker.name}"
        battle_ended = printMap(all_units, "\n".join(action_log), active_unit=target, target_unit=attacker, 
                               stage_info=stage_info, dead_units=dead_units)
        if battle_ended:
            return True
            
        counter_defense_type = "否"
        valid_counter = optimize_counter_attacks(target, enemies, attacker, counter_defense_type, action_log)
        
        # Log why target itself cannot counter (if applicable)
        if target_is_defending:
            log_action(action_log, f"{target.name} 無法反擊 - 選擇防禦")
        elif not can_counter:
            log_action(action_log, f"{target.name} 無法反擊 - 攻擊者超出射程範圍 (距離: {distance(target, attacker)}, 射程: {target.longest_weapon_range})")

        # Execute counter support attacks (can happen regardless of target's ability to counter)
        attacker_killed_by_counter_support = False
        if valid_counter:
            for unit in valid_counter:
                attacker_hp_before = attacker.current_hp
                dmg, debug_info = damageCalculation(unit, attacker, True, counter_defense_type, return_debug_info=True, action_log=action_log)
                attacker.take_damage(dmg)
                add_counter_damage_to_summary(unit.name, dmg, attacker.name)
                # Apply status effects only if HP was successfully reduced
                effects_applied = apply_status_effects_if_damage_dealt(unit, attacker, True, dmg, attacker_hp_before)
                
                log_action(action_log, f"{unit.name} 支援反擊 {attacker.name} 造成 {dmg} 傷害")
                log_debug(action_log, f"基礎傷害: {debug_info['baseDamage']}, 武器: {debug_info['weapon_power']}, ATK: {debug_info['attackerUnitAtk']}, DEF: {debug_info['defenderUnitDef']}, charAtk: {debug_info['attackerCharacterAtk']}, charDef: {debug_info['defenderCharacterDef']}, totalDamageMultiplierPercent: {debug_info['totalDamageMultiplierPercent']}, 剩餘 {attacker.current_hp}/{attacker.hp}, 剩餘支援攻擊次數: {unit.pilot.support_attack-1}")
                if effects_applied:
                    log_debug(action_log, "狀態效果已套用")
                
                # Decrement support attack count
                unit.pilot.support_attack -= 1
                if attacker.current_hp <= 0:
                    log_action(action_log, f"{attacker.name} 被支援反擊擊毀")
                    dead_units.append(attacker)
                    attacker_killed_by_counter_support = True
                    break

        # Main counter attack only happens when target can counter (within range AND not defending)
        if can_counter and not target_is_defending:
            attacker_hp_before = attacker.current_hp
            dmg, debug_info = damageCalculation(target, attacker, True, counter_defense_type, return_debug_info=True, action_log=action_log)
            
            if not attacker_killed_by_counter_support:
                # Attacker is still alive, apply damage normally
                attacker.take_damage(dmg)
                add_counter_damage_to_summary(target.name, dmg, attacker.name)
                # Apply status effects only if HP was successfully reduced
                effects_applied = apply_status_effects_if_damage_dealt(target, attacker, True, dmg, attacker_hp_before)
                
                log_action(action_log, f"{target.name} 反擊 {attacker.name} 造成 {dmg} 傷害")
                log_debug(action_log, f"基礎傷害: {debug_info['baseDamage']}, 武器: {debug_info['weapon_power']}, ATK: {debug_info['attackerUnitAtk']}, DEF: {debug_info['defenderUnitDef']}, charAtk: {debug_info['attackerCharacterAtk']}, charDef: {debug_info['defenderCharacterDef']}, totalDamageMultiplierPercent: {debug_info['totalDamageMultiplierPercent']}, 剩餘 {attacker.current_hp}/{attacker.hp}")
                if effects_applied:
                    log_debug(action_log, "狀態效果已套用")
                
                if attacker.current_hp <= 0:
                    log_action(action_log, f"{attacker.name} 被主反擊擊毀")
                    dead_units.append(attacker)
            else:
                # Attacker is already dead, but still count the damage and apply overkill
                attacker.take_damage(dmg)  # This will add to overkill damage
                add_counter_damage_to_summary(target.name, dmg, attacker.name)
                # Don't apply status effects to dead units
                log_action(action_log, f"{target.name} 反擊已死亡的 {attacker.name} 造成 {dmg} 傷害 (過度傷害)")
                log_debug(action_log, f"基礎傷害: {debug_info['baseDamage']}, 武器: {debug_info['weapon_power']}, ATK: {debug_info['attackerUnitAtk']}, DEF: {debug_info['defenderUnitDef']}, charAtk: {debug_info['attackerCharacterAtk']}, charDef: {debug_info['defenderCharacterDef']}, totalDamageMultiplierPercent: {debug_info['totalDamageMultiplierPercent']}, 過度傷害: {attacker.overkill_damage}")
        # If target cannot counter, skip main counter attack but support counter attacks already executed above
    else:
        # No counter attack if target is dead
        valid_counter = []

    # Show final results with all dead units
    counter_damage_summary = get_counter_damage_summary()  # Counter phase damage
    if attacker.current_hp <= 0:
        if counter_damage_summary:
            stage_info = f"戰鬥結束 - {attacker.name} 被擊毀 ({counter_damage_summary})"
        else:
            stage_info = f"戰鬥結束 - {attacker.name} 被擊毀"
    else:
        if counter_damage_summary:
            stage_info = f"戰鬥結束 ({counter_damage_summary})"
        else:
            stage_info = "戰鬥結束"
    
    battle_ended = printMap(all_units, "\n".join(action_log), active_unit=attacker, target_unit=real_target, 
                           stage_info=stage_info, dead_units=dead_units)
    if battle_ended:
        return True
    
    # Clean up dead units from the map for next action
    dead_unit_names = [unit.name for unit in dead_units]
    for unit in dead_units:
        # Remove from all_units list
        if unit in all_units:
            all_units.remove(unit)
        
        # Also remove from original team lists to prevent them from reappearing
        # Check team_a
        if hasattr(unit, 'team_name') and unit.team_name == "Team A":
            # Find the battleground reference - we need to access it from the global scope
            # For now, we'll mark the unit as removed by setting a flag
            unit._removed_from_battle = True
        elif hasattr(unit, 'team_name') and unit.team_name == "Team B":
            unit._removed_from_battle = True
        else:
            # Fallback: determine by position
            if unit.col <= 5:  # Team A
                unit._removed_from_battle = True
            else:  # Team B
                unit._removed_from_battle = True
    
    if dead_unit_names:
        log_action(action_log, f"清除被擊毀的單位: {', '.join(dead_unit_names)}")
    
    # Update display after cleanup
    battle_ended = printMap(all_units, "\n".join(action_log), active_unit=None, target_unit=None, 
                           stage_info="準備下一個行動")
    if battle_ended:
        return True

    # Update vigor for all participating units after combat (only if combat actually occurred)
    if can_attack:
        update_vigor_after_combat(attacker, real_target, target, valid_support, valid_counter, action_log, allies, enemies, defense_type)

    # Check if any enemy was killed (original target or support defender) to trigger extra action
    any_enemy_killed = initial_target_dead or (real_target.current_hp <= 0)
    if attacker.current_hp > 0 and any_enemy_killed and attacker.pilot.chanceStage > 0:
        attacker.pilot.chanceStage -= 1
        killed_unit_name = target.name if initial_target_dead else real_target.name
        # Reset movement for the extra action
        attacker.move = attacker.original_move
        action_log.append(f"{attacker.name} 擊破敵人 {killed_unit_name}，剩餘行動次數 {attacker.pilot.chanceStage}，移動力重置為 {attacker.move}")
        return Action(attacker, allies, enemies)
    
    return False  # Battle continues

def find_optimal_support_combination(main_attacker, potential_supporters, target, defense_type, action_log):
    """
    Find the optimal combination of main attacker + supporters to minimize total damage while guaranteeing a kill.
    Returns (selected_supporters, guaranteed_kill, main_attacker_damage)
    """
    from itertools import combinations
    
    # Calculate main attacker damage
    main_damage = damageCalculation(main_attacker, target, True, defense_type, action_log=action_log)
    target_hp = target.current_hp
    
    action_log.append(f"[DEBUG] 尋找最小傷害組合: 目標HP={target_hp}, 主攻者傷害={main_damage}")
    
    # If main attacker can kill alone, no support needed
    if main_damage >= target_hp:
        action_log.append(f"[DEBUG] 主攻者單獨可擊殺目標")
        return [], True, main_damage
    
    # Calculate damage for all potential supporters
    supporter_damages = []
    for unit in potential_supporters:
        dmg = damageCalculation(unit, target, True, defense_type, action_log=action_log)
        supporter_damages.append((unit, dmg))
        action_log.append(f"[DEBUG] {unit.name} 支援攻擊傷害: {dmg}")
    
    # Find the combination that minimizes total damage while guaranteeing kill
    best_combination = None
    min_total_damage = float('inf')
    
    # Try all possible combinations
    for combo_size in range(1, len(supporter_damages) + 1):
        for combo in combinations(supporter_damages, combo_size):
            total_support_damage = sum(dmg for _, dmg in combo)
            total_damage = main_damage + total_support_damage
            
            # Check if this combination can guarantee kill and has less total damage
            if total_damage >= target_hp and total_damage < min_total_damage:
                min_total_damage = total_damage
                best_combination = combo
                action_log.append(f"[DEBUG] 更佳組合: {[unit.name for unit, _ in combo]}, 總傷害={total_damage}")
    
    if best_combination:
        selected_supporters = [unit for unit, _ in best_combination]
        action_log.append(f"[DEBUG] 最佳最小傷害組合: {[u.name for u in selected_supporters]}, 總傷害={min_total_damage}, 浪費傷害={min_total_damage - target_hp}")
        return selected_supporters, True, main_damage
    
    # If no combination can guarantee kill, use all available supporters
    all_supporters = [unit for unit, _ in supporter_damages]
    total_damage = main_damage + sum(dmg for _, dmg in supporter_damages)
    action_log.append(f"[DEBUG] 無法保證擊殺，使用全部支援者，總傷害={total_damage}")
    return all_supporters, False, main_damage

def optimize_support_attacks(attacker, allies, initial_target, real_target, defense_type, action_log):
    """Optimized support attack selection logic - minimizes total damage while guaranteeing kill"""
    all_support = [
        unit for unit in allies
        if unit.current_hp > 0 and unit != attacker
        and unit.pilot.support_attack >  0
        and distance(unit, initial_target) <= unit.longest_weapon_range
    ]
    
    if not all_support:
        action_log.append(f"[DEBUG] 沒有可用的支援攻擊單位 (距離計算目標: {initial_target.name})")
        return []
    
    # Debug: Show available support units and their remaining counts
    support_info = [(u.name, u.pilot.support_attack) for u in all_support]
    action_log.append(f"[DEBUG] 可用支援攻擊單位 (距離計算目標: {initial_target.name}): {support_info}")
    
    # Find optimal combination
    selected_supporters, guaranteed_kill, main_damage = find_optimal_support_combination(
        attacker, all_support, real_target, defense_type, action_log
    )
    
    if guaranteed_kill:
        action_log.append(f"選擇最小傷害組合保證擊殺: {[u.name for u in selected_supporters]}")
    else:
        action_log.append(f"使用全部支援者但無法保證擊殺: {[u.name for u in selected_supporters]}")
    
    return selected_supporters

def optimize_counter_attacks(target, enemies, attacker, counter_defense_type, action_log):
    """Optimized counter attack selection logic - minimizes total damage while guaranteeing kill"""
    counter_support = [
        unit for unit in enemies
        if unit.current_hp > 0 and unit != target
        and unit.pilot.support_attack > 0
        and distance(unit, attacker) <= unit.longest_weapon_range
    ]
    
    if not counter_support:
        action_log.append(f"[DEBUG] 沒有可用的支援反擊單位")
        return []
    
    # Debug: Show available counter support units and their remaining counts
    counter_info = [(u.name, u.pilot.support_attack) for u in counter_support]
    action_log.append(f"[DEBUG] 可用支援反擊單位: {counter_info}")
    
    # Find optimal combination for counter attack
    selected_counter_supporters, guaranteed_kill, main_damage = find_optimal_support_combination(
        target, counter_support, attacker, counter_defense_type, action_log
    )
    
    if guaranteed_kill:
        action_log.append(f"反擊方選擇最小傷害組合保證擊殺: {[u.name for u in selected_counter_supporters]}")
    else:
        action_log.append(f"反擊方使用全部支援者但無法保證擊殺: {[u.name for u in selected_counter_supporters]}")
    
    return selected_counter_supporters

def update_vigor_after_combat(attacker, real_target, target, valid_support, valid_counter, action_log, allies, enemies, defense_type):
    """
    Update vigor for all participating units based on combat results.
    Vigor is in range of 0 to 12.
    All changes are calculated first, then clamped to valid range.
    """
    action_log.append(f"[DEBUG] === 士氣更新開始 ===")
    
    # Track combat results
    target_killed = real_target.current_hp <= 0
    attacker_killed = attacker.current_hp <= 0
    # Main counter attack only happens if target survives AND can reach attacker AND not defending
    main_counter_attack_occurred = not target_killed and distance(target, attacker) <= target.longest_weapon_range and defense_type != "防禦"
    # Support counter attacks can happen as long as target is not killed (regardless of main counter conditions)
    support_counter_attacks_occurred = not target_killed and len(valid_counter) > 0
    
    # Calculate vigor changes for each unit
    vigor_changes = {}
    
    def add_vigor_change(unit, amount, reason):
        if unit.name not in vigor_changes:
            vigor_changes[unit.name] = {'unit': unit, 'changes': [], 'total': 0}
        vigor_changes[unit.name]['changes'].append((amount, reason))
        vigor_changes[unit.name]['total'] += amount

    # 1. For unit that performs attack or counter attack: increase 1 vigor
    add_vigor_change(attacker, 1, "進行攻擊")
    
    if main_counter_attack_occurred:
        add_vigor_change(target, 1, "進行反擊")
    
   
    
    # 2. Unit being attacked: Reduce vigor by 1 per attack taken
    # Real target receives attacks from main attacker + support attackers
    attacks_on_target = 1 + len(valid_support)
    add_vigor_change(real_target, -attacks_on_target, f"受到 {attacks_on_target} 次攻擊")
    
    # Attacker receives counter attacks (if any counter attacks occurred)
    if support_counter_attacks_occurred or main_counter_attack_occurred:
        counter_attacks_on_attacker = len(valid_counter)
        if main_counter_attack_occurred:
            counter_attacks_on_attacker += 1  # Add main counter attack
        add_vigor_change(attacker, -counter_attacks_on_attacker, f"受到 {counter_attacks_on_attacker} 次反擊")
    
    # 3. For support attackers - based on combat outcomes
    if target_killed and not attacker_killed:
        # Case 1: Attacker killed the real target and attacker survives
        for unit in valid_support:
            add_vigor_change(unit, 2, "支援攻擊成功擊殺目標且主攻者存活")
        
    elif not target_killed and attacker_killed:
        # Case 2: Attacker failed to kill the real target and attacker died to counter attack
        for unit in valid_counter:
            add_vigor_change(unit, 2, "支援反擊成功擊殺敵方主攻者")
    
    elif not target_killed and attacker_killed:
        # Case 3: Attacker failed to kill the real target but attacker survives
        for unit in valid_support:
            add_vigor_change(unit, 1, "支援攻擊但未擊殺目標，主攻者存活")
        for unit in valid_counter:
            add_vigor_change(unit, 1, "支援反擊成功保護盟友")
    
    elif target_killed and attacker_killed:
        # Case 4: Attacker killed the real target but died to counter attack
        for unit in valid_support:
            add_vigor_change(unit, 1, "支援攻擊成功擊殺目標但主攻者陣亡")
        for unit in valid_counter:
            add_vigor_change(unit, 1, "支援反擊成功擊殺敵方主攻者")
    
    # 4. For attacker or counter attacker that killed the opponent: gain +4 vigor
    if target_killed:
        add_vigor_change(attacker, 4, "擊殺敵人")
    
    if attacker_killed and main_counter_attack_occurred:
        add_vigor_change(target, 4, "反擊擊殺敵人")
    
    # Apply all vigor changes with bounds checking (0-12)
    for unit_name, data in vigor_changes.items():
        unit = data['unit']
        total_change = data['total']
        old_vigor = unit.pilot.moral
        new_vigor = max(0, min(12, old_vigor + total_change))
        unit.pilot.moral = new_vigor
        
        # Log the change with details
        change_details = ", ".join([f"{reason}({amount:+d})" for amount, reason in data['changes']])
        if old_vigor + total_change != new_vigor:
            # Show if clamping occurred
            clamped_note = f" (原計算: {old_vigor + total_change}, 限制為 0-12)"
        else:
            clamped_note = ""
        action_log.append(f"{unit.name} 士氣變化: {old_vigor} -> {new_vigor}{clamped_note} ({change_details})")
    
    action_log.append(f"[DEBUG] === 士氣更新完成 ===")

def main():
    """Main function to run the battle simulator with restart capability"""
    while True:
        print("=== 戰術RPG戰鬥模擬器 ===")
        
        # Get Google Sheets URL from user
        print("請輸入您的Google試算表連結...")
        sheet_id, gid = get_google_sheets_url()
        
        if not sheet_id or not gid:
            print("未提供有效的Google試算表連結，使用測試模式...")
            battle_result = run_test_battle()
        else:
            battle_result = run_online_battle(sheet_id, gid)
        
        # After battle completion, ask user if they want to continue
        if not ask_continue_or_exit():
            break
    
    print("感謝使用戰術RPG戰鬥模擬器！")

def run_online_battle(sheet_id, gid):
    """Run battle with online Google Sheets data"""
    print(f"正在載入戰鬥資料...")
    print(f"工作表ID: {sheet_id}")
    print(f"頁面ID: {gid}")
    
    try:
        # Load data from Google Sheets using user-provided URL
        CSV_URL = f'https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}'
        
        df = pd.read_csv(CSV_URL, header=2)
        df.dropna(axis=1, how='all', inplace=True)
        
        print("資料載入成功！")
        print(f"載入了 {len(df)} 個單位的資料")
        
        # Validate data structure
        if len(df) < 14:
            raise ValueError(f"資料不足：需要至少14個單位，但只找到{len(df)}個")
        
        # Create teams from the data
        team_a_rows = [row for _, row in df.iloc[0:5].iterrows()]
        team_b_rows = [row for _, row in df.iloc[9:14].iterrows()]
        
        battleground = Battleground(team_a_rows, team_b_rows)
        
        print(f"\nTeam A: {[unit.name for unit in battleground.team_a.units]}")
        print(f"Team B: {[unit.name for unit in battleground.team_b.units]}")
        
        # Validate that both teams have at least one valid unit
        if len(battleground.team_a.units) == 0:
            print("❌ 錯誤: Team A 沒有任何有效單位，無法開始戰鬥！")
            print("請檢查Google試算表中Team A單位的位置設定（必須為1-5且不能重複）")
            return False
        
        if len(battleground.team_b.units) == 0:
            print("❌ 錯誤: Team B 沒有任何有效單位，無法開始戰鬥！")
            print("請檢查Google試算表中Team B單位的位置設定（必須為1-5且不能重複）")
            return False
        
        # Start the battle simulation
        print("\n=== 戰鬥開始 ===")
        return run_battle_simulation(battleground)
        
    except Exception as e:
        print(f"錯誤: 無法載入戰鬥資料")
        print(f"詳細錯誤: {e}")
        print("\n請檢查網路連線、工作表權限或使用測試模式...")
        
        # Ask user if they want to try test mode
        root = tk.Tk()
        root.withdraw()
        use_test = messagebox.askyesno(
            "載入失敗", 
            f"無法載入Google試算表資料:\n{str(e)}\n\n是否使用測試模式繼續？"
        )
        root.destroy()
        
        if use_test:
            return run_test_battle()
        else:
            print("程式結束")
            return False

def ask_continue_or_exit():
    """Ask user if they want to continue with another battle or exit"""
    root = tk.Tk()
    root.withdraw()
    
    continue_battle = messagebox.askyesno(
        "戰鬥完成",
        "戰鬥已結束！\n\n是否要開始新的戰鬥？\n\n點擊「是」返回主選單\n點擊「否」退出程式"
    )
    
    root.destroy()
    return continue_battle

def run_battle_simulation(battleground):
    """Run the main battle simulation loop"""
    all_units = battleground.team_a.units + battleground.team_b.units
    
    # Initialize all units
    for unit in all_units:
        unit.current_hp = unit.hp
    
    round_number = 1
    max_rounds = 20  # Prevent infinite loops
    
    while round_number <= max_rounds:
        print(f"\n{'='*50}")
        print(f"第 {round_number} 回合開始")
        print(f"{'='*50}")
        
        # Reset support counters and status effects at the start of each round
        reset_support_counters(all_units)
        reset_status_effects(all_units)
        
        # Get all living units and sort by action order - exclude removed units
        living_units = [unit for unit in all_units 
                       if unit.current_hp > 0 and not getattr(unit, '_removed_from_battle', False)]
        living_units.sort(key=lambda u: u.action_order)
        
        # Check win conditions - exclude units that have been removed from battle
        team_a_alive = [unit for unit in battleground.team_a.units 
                       if unit.current_hp > 0 and not getattr(unit, '_removed_from_battle', False)]
        team_b_alive = [unit for unit in battleground.team_b.units 
                       if unit.current_hp > 0 and not getattr(unit, '_removed_from_battle', False)]
        
        if not team_a_alive:
            print(f"\n🎉 Team B 獲勝！")
            break
        elif not team_b_alive:
            print(f"\n🎉 Team A 獲勝！")
            break
        
        # Execute actions for each unit in order
        for unit in living_units:
            if unit.current_hp <= 0:
                continue
                
            # Determine allies and enemies - exclude removed units
            if unit in battleground.team_a.units:
                allies = [u for u in battleground.team_a.units 
                         if u.current_hp > 0 and not getattr(u, '_removed_from_battle', False)]
                enemies = [u for u in battleground.team_b.units 
                          if u.current_hp > 0 and not getattr(u, '_removed_from_battle', False)]
            else:
                allies = [u for u in battleground.team_b.units 
                         if u.current_hp > 0 and not getattr(u, '_removed_from_battle', False)]
                enemies = [u for u in battleground.team_a.units 
                          if u.current_hp > 0 and not getattr(u, '_removed_from_battle', False)]
            
            # Execute the unit's action
            battle_ended = Action(unit, allies, enemies)
            
            if battle_ended is True:
                print("\n戰鬥被使用者終止")
                close_battle_window()
                return True
            
            # Check win conditions again after each action - exclude removed units
            team_a_alive = [unit for unit in battleground.team_a.units 
                           if unit.current_hp > 0 and not getattr(unit, '_removed_from_battle', False)]
            team_b_alive = [unit for unit in battleground.team_b.units 
                           if unit.current_hp > 0 and not getattr(unit, '_removed_from_battle', False)]
            
            if not team_a_alive or not team_b_alive:
                break
        
        round_number += 1
    
    if round_number > max_rounds:
        print(f"\n戰鬥達到最大回合數 ({max_rounds})，以平局結束")
    
    # Close the battle window but don't exit the program
    close_battle_window()
    return True

def run_test_battle():
    """Run a test battle with hardcoded data if online data loading fails"""
    print("=== 測試模式 ===")
    print("使用預設測試資料進行戰鬥...")
    
    # Create minimal test data
    test_team_a_data = [
        {
            '單位': 'TestA1', '位置': 1, 'ATK': 3000, 'DEF': 2500, 'MOB': 150, 'HP': 8000,
            'atk(base)': 300, 'def(base)': 250, 'mob(base)': 15, 'hp(base)': 800, '突破': 0,
            '最强武裝': 4500, '最强武裝屬性': '射擊', '最强武裝類型': '光束', '最强武裝射程': 3, '最强武裝特效': '',
            '最遠武裝': 4200, '最遠武裝屬性': '射擊', '最遠武裝類型': '光束', '最遠武裝射程': 5, '最遠武裝特效': '',
            '移動': 5, '抗性': '', '抗性數值': 0, '行動順序': 10,
            '防禦減傷(盾牌)': 0.8, '格鬥': 120, '射擊': 150, '覺醒': 100, '防禦': 130, '反應': 140,
            '額外行動次數': 0, '常駐增傷': 0.1, '特殊增傷': 0, '特殊減傷': 0,
            '支援防禦': 2, '支援防禦加成': 0.3, '支援攻擊': 2, '支援攻擊加成': 0.2,
            '初始MP': 6, '精神1': 'MP3', '精神2': '攻擊爆裂20%', '精神3': '移動'
        }
    ]
    
    test_team_b_data = [
        {
            '單位': 'TestB1', '位置': 1, 'ATK': 2800, 'DEF': 2800, 'MOB': 120, 'HP': 9000,
            'atk(base)': 280, 'def(base)': 280, 'mob(base)': 12, 'hp(base)': 900, '突破': 0,
            '最强武裝': 4200, '最强武裝屬性': '格鬥', '最强武裝類型': '物理', '最强武裝射程': 1, '最强武裝特效': '',
            '最遠武裝': 3800, '最遠武裝屬性': '射擊', '最遠武裝類型': '實彈', '最遠武裝射程': 4, '最遠武裝特效': '',
            '移動': 6, '抗性': '', '抗性數值': 0, '行動順序': 15,
            '防禦減傷(盾牌)': 0.9, '格鬥': 140, '射擊': 120, '覺醒': 90, '防禦': 150, '反應': 130,
            '額外行動次數': 0, '常駐增傷': 0.05, '特殊增傷': 0, '特殊減傷': 0,
            '支援防禦': 1, '支援防禦加成': 0.2, '支援攻擊': 1, '支援攻擊加成': 0.15,
            '初始MP': 4, '精神1': '防禦30%', '精神2': '回血', '精神3': 'MP2'
        }
    ]
    
    battleground = Battleground(test_team_a_data, test_team_b_data)
    return run_battle_simulation(battleground)

if __name__ == "__main__":
    main()