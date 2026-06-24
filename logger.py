import json
import time
from constants import SCREEN_WIDTH, SCREEN_HEIGHT

_start_time = time.time()
_last_log_time = time.time()

def log_state(player=None, updatable=None, drawable=None, asteroids=None, shots=None):
    """Log the current game state to game_state.jsonl once per second"""
    global _last_log_time
    
    current_time = time.time()
    elapsed_s = current_time - _start_time
    
    # Solo registrar si han pasado al menos 1 segundo desde el último log
    if current_time - _last_log_time >= 1.0:
        state = {
            "timestamp": time.strftime('%Y-%m-%dT%H:%M:%S'),
            "screen_size": [SCREEN_WIDTH, SCREEN_HEIGHT],
            "elapsed_s": elapsed_s,
            "type": "Player"
        }
        
        if player:
            state["pos"] = [player.position.x, player.position.y]
            state["rot"] = player.rotation
        
        if updatable is not None:
            # Incluir sprites con su tipo
            sprites = []
            for sprite in updatable:
                sprites.append({"type": sprite.__class__.__name__})
            state["updatable"] = {"count": len(updatable), "sprites": sprites}
        
        if drawable is not None:
            # Incluir sprites con su tipo
            sprites = []
            for sprite in drawable:
                sprites.append({"type": sprite.__class__.__name__})
            state["drawable"] = {"count": len(drawable), "sprites": sprites}
        
        if asteroids is not None:
            state["asteroids"] = {"count": len(asteroids)}
        
        if shots is not None:
            state["shots"] = {"count": len(shots)}
        
        # Escribir como JSONL (una línea por objeto, append mode)
        try:
            with open("game_state.jsonl", "a") as f:
                f.write(json.dumps(state) + "\n")
                f.flush()
        except Exception as e:
            print(f"Error writing to game_state.jsonl: {e}")
        
        _last_log_time = current_time

def log_event(event_type: str) -> None:
    """Log a game event to game_events.jsonl"""
    current_time = time.time()
    elapsed_s = current_time - _start_time
    
    event = {
        "timestamp": time.strftime('%Y-%m-%dT%H:%M:%S'),
        "elapsed_s": elapsed_s,
        "type": event_type
    }
    
    try:
        with open("game_events.jsonl", "a") as f:
            f.write(json.dumps(event) + "\n")
            f.flush()
    except Exception as e:
        print(f"Error writing to game_events.jsonl: {e}")
