obs = obslua

output_folder = ""
source_name1 = ""
source_name2 = ""
interval = 50  -- milliseconds

function script_description()
    return "Reads player_1_life.txt and player_2_life.txt from a folder and updates two text sources every 50ms."
end

function script_properties()
    local props = obs.obs_properties_create()

    obs.obs_properties_add_path(props, "output_folder", "Output Folder",
        obs.OBS_PATH_DIRECTORY, nil, nil)

    obs.obs_properties_add_text(props, "source_name1", "Player 1 Life Text Source", obs.OBS_TEXT_DEFAULT)
    obs.obs_properties_add_text(props, "source_name2", "Player 2 Life Text Source", obs.OBS_TEXT_DEFAULT)

    return props
end

function script_update(settings)
    output_folder = obs.obs_data_get_string(settings, "output_folder")
    source_name1 = obs.obs_data_get_string(settings, "source_name1")
    source_name2 = obs.obs_data_get_string(settings, "source_name2")

    obs.timer_remove(update_sources)
    if output_folder ~= "" and source_name1 ~= "" and source_name2 ~= "" then
        obs.timer_add(update_sources, interval)
    end
end

local function read_file(path)
    local file = io.open(path, "r")
    if not file then return nil end
    local text = file:read("*l") or ""
    file:close()
    return text
end

function update_sources()
    local file1 = output_folder .. "/player_1_life.txt"
    local file2 = output_folder .. "/player_2_life.txt"

    local text1 = read_file(file1)
    local text2 = read_file(file2)

    if text1 then
        local src1 = obs.obs_get_source_by_name(source_name1)
        if src1 then
            local settings1 = obs.obs_data_create()
            obs.obs_data_set_string(settings1, "text", text1)
            obs.obs_source_update(src1, settings1)
            obs.obs_data_release(settings1)
            obs.obs_source_release(src1)
        end
    end

    if text2 then
        local src2 = obs.obs_get_source_by_name(source_name2)
        if src2 then
            local settings2 = obs.obs_data_create()
            obs.obs_data_set_string(settings2, "text", text2)
            obs.obs_source_update(src2, settings2)
            obs.obs_data_release(settings2)
            obs.obs_source_release(src2)
        end
    end
end

function script_unload()
    obs.timer_remove(update_sources)
end
