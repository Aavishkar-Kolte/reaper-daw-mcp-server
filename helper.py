import reapy

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
