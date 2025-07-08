class Setting:

    def __init__(self, key_section: str, value_section: str):
        self.key_section = key_section
        self.value_section = value_section

    def get_key_section(self) -> str:
        return self.key_section

    def get_value_section(self) -> str:
        return self.value_section.strip()

class SettingConstSection:
    COOLDOWN_STREAM_READER="cooldown_stream_reader"
    SELECTED_LISTEN_COM_PORT="selected_listen_com_port"
    LOG_DIRECTORY_STORAGE="log_directory_storage"
    DATA_DIRECTORY_STORAGE="data_directory_storage"

class SettingController:

    def __init__(self, file='assets/config/settings.yml'):
        self.file = file
        reader = open(self.file, "r")

        self.setting_container = list[Setting]()

        for line in reader.readlines():
            if not line.__contains__(':'): continue

            key, value = line.replace('\n', '').strip().split(':', 1)

            self.setting_container.append(Setting(key, value))

    def get_parameter_by_key(self, key: str) -> Setting | None:
        setting_section = list(filter(lambda finder: finder.get_key_section() == key, self.setting_container))

        if len(setting_section) == 0 or len(setting_section) > 1:
            return None

        return setting_section[0]

    def get_parameter_line_by_key(self, key: str) -> str:
        parameter = self.get_parameter_by_key(key)
        return parameter.get_key_section() + ": " + parameter.get_value_section()

    def get_config_file_path(self) -> str:
        return self.file