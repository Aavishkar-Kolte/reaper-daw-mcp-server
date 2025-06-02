import reapy
import configparser
from mcp.server.fastmcp import FastMCP
from reapy import reascript_api as RPR
from helper import *

sample_library_path = "D:\\sample-library\\"

INSTRUCTIONS = f"""
STRICTLY FOLLOW THESE INSTRUCTIONS:

1. SAMPLE LIBRARY ACCESS:
   - Root path: "{sample_library_path}"
   - ONLY access and explore subfolders within this root path
   - NEVER attempt to access or explore folders outside this path
   - Treat this as a secure sandbox environment

2. EXPLORATION GUIDELINES:
   - The sample library is extensive - use iterative exploration
   - Start with high-level folder structure before diving deeper
   - Only explore folders that are relevant to the current task
   - Avoid unnecessary deep traversal of the entire library
   - Explore ONE LEVEL AT A TIME:
     * First, list contents of current directory
     * Use descriptive file/folder names to decide what to explore next
     * Only proceed to next level when specifically needed
   - File names are descriptive and will help guide exploration:
     * Use file names to understand content without opening
     * Look for patterns in naming conventions
     * Use descriptive names to identify relevant sections
     * Avoid exploring sections with clearly irrelevant names
"""

mcp = FastMCP(name="ReaperMCPServer", instructions=INSTRUCTIONS)

prj = reapy.Project()
if prj:
    print("Project open")
else:
    raise Exception("Unable to open project")

reaper_appdata_path = RPR.GetResourcePath()
reaper_vst_plugins_ini_path = reaper_appdata_path + "/reaper-vstplugins64.ini"

config = configparser.ConfigParser()
config.read(reaper_vst_plugins_ini_path)
reaper_vst_plugins = [plugin.split('.')[0] for plugin in config['vstcache']]


@mcp.tool(name="reaper_project_state", description="Get reaper project state")
def get_reaper_project_state() -> dict:
    state = {}
    state["project_bpm"] = prj.bpm
    state["project_length"] = prj.length
    state["tracks"] = get_tracks(prj)
    return str(state)

@mcp.tool(name="create_new_track", description="Creates a new track and inserts it at the given index in the current reaper project")
def create_new_track(index : int, name : str) -> None:
    prj.add_track(index, name)

@mcp.tool(name="add_new_midi_item_to_the_track", description="Adds a new item to the given track in the current reaper project")
def add_new_item_to_track(track_index : int, start : int, end : int) -> None:
    track = prj.tracks[track_index]
    track.add_midi_item(start, end)

@mcp.tool(name="set_project_bpm", description="Sets the bpm of the current reaper project")
def set_project_bpm(bpm : int) -> None:
    prj.bpm = bpm

@mcp.tool(name="add_notes_to_the_active_take_of_item", description="Adds given list of notes [{start, end, length, channel, pitch, velocity}, ...] to the active take of given item in the current reaper project. if no take exists, it will be created")
def add_notes_to_the_active_take_of_item(track_index : int, item_index : int, notes : list) -> None:
    item = prj.tracks[track_index].items[item_index]

    if item.n_takes == 0:
        item.add_take()
    
    for note in notes:
        item.active_take.add_note(note["start"], note["end"], note["pitch"], note["velocity"], note["channel"])

@mcp.tool(name="get_list_of_vst_plugins", description="Returns list of vst plugins")
def get_list_of_vst_plugins() -> list:
    return reaper_vst_plugins

@mcp.tool(name="add_vst_plugin_to_the_track", description="Adds given vst plugin to the given track in the current reaper project")
def add_vst_plugin_to_the_track(track_index : int, plugin_name : str) -> None:
    prj.tracks[track_index].add_fx(plugin_name)

@mcp.tool(name="get_list_of_fxs_on_track", description="Returns list of fxs on the given track in the current reaper project")
def get_list_of_fxs_on_track(track_index : int) -> list:
    return [{"index": fx.index, "name": fx.name} for fx in prj.tracks[track_index].fxs]

@mcp.tool(name="get_fx_state", description="Returns state of the given fx on the given track in the current reaper project")
def get_fx_state(track_index : int, fx_index : int) -> dict:
    fx = prj.tracks[track_index].fxs[fx_index]
    state = {}
    state["fx_name"] = fx.name
    state["fx_index"] = fx.index
    state["parent_track_index"] = fx.parent.index
    state["fx_params"] = [{"name": param.name, "value": param, "range": {"min": param.range[0], "max": param.range[1]}} for param in fx.params]
    return state

@mcp.tool(name="set_fx_params", description="Sets params of the given fx on the given track in the current reaper project, params is a list of dictionaries with name and value")
def set_fx_state(track_index : int, fx_index : int, params : dict) -> None:
    fx_params = prj.tracks[track_index].fxs[fx_index].params

    for param in params:
        fx_params[param["name"]] = param["value"]

@mcp.tool(name="delete_track", description="Deletes the given track in the current reaper project")
def delete_track(track_index : int) -> None:
    prj.tracks[track_index].delete()

@mcp.tool(name="delete_item", description="Deletes the given item in the current reaper project")
def delete_item(track_index : int, item_index : int) -> None:   
    prj.tracks[track_index].items[item_index].delete()

@mcp.tool(name="delete_fx_on_track", description="Deletes the given fx on the given track in the current reaper project")
def delete_fx_on_track(track_index : int, fx_index : int) -> None:
    prj.tracks[track_index].fxs[fx_index].delete()

@mcp.tool(name="explore_sample_library", description="Explore the sample library and return a hierarchical list of samples/folders at the given path. provide the path relative to the root path to sample library")
def explore_sample_library(path : str) -> list:
    return get_list_of_samples_in_library(sample_library_path, path)