import reapy
import os

def get_notes(list: reapy.NoteList) -> list:
    return [{"id": note.id, 
             "note_index": note.index,
             "start": note.start,
             "end": note.end,
             "channel": note.channel,
             "pitch": note.pitch, 
             "velocity": note.velocity} for note in list]

def get_takes(item: reapy.Item) -> list:
    return [{"id" : take.id,
             "take_index": i,
             "take_name": take.name,
             "number_of_notes": take.n_notes,
             "notes": get_notes(take.notes)
             } for i, take in item.takes]

def get_items(track: reapy.Track) -> list:
    return [{"id": item.id,
             "position": item.position, 
             "length": item.length, 
             "active_take_index": item.active_take.id,
             "number_of_takes": item.n_takes, 
             "takes": get_takes(item)} for item in track.items]

def get_tracks(reaper_prj: reapy.Project) -> list:
    
    return [{"id": track.id,
             "track_index": track.index, 
             "track_name": track.name, 
             "color": track.color,
             "number_of_items": track.n_items,
             "items": get_items(track)} for track in reaper_prj.tracks]

def get_list_of_samples_in_library(root_dir : str, path : str) -> list:
    full_path = os.path.join(root_dir, path)
    tree_str = ""
    
    try:
        items = os.listdir(full_path)
        dirs = []
        files = []
        for item in items:
            item_path = os.path.join(full_path, item)
            if os.path.isdir(item_path):
                dirs.append(item)
            else:
                files.append(item)
        tree_str += f"{path}/\n"

        for d in dirs:
            tree_str += f"    {d}/\n"

        for f in files:
            tree_str += f"    {f}\n"
            
    except Exception as e:
        tree_str = f"Error accessing directory: {e}"
        
    return tree_str
