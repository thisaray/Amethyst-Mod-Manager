"""
fallout_london.py
Fallout London game handler.
"""

from Games.Bethesda.fallout_4 import Fallout_4


class Fallout_London(Fallout_4):

    supports_script_extender_swap = False
    _PLUGINS_TXT_FILENAME = "Plugins.txt"
    # keep these out of vanilla_plugins, fo4 doesnt write those to Plugins.txt
    # and london wont load without them
    _london_plugins = [
        "LondonWorldSpace.esm",
        "LondonWorldSpace-DLCBlock.esp",
    ]

    @property
    def name(self) -> str:
        return "Fallout London"

    @property
    def game_id(self) -> str:
        return "Fallout_London"

    @property
    def steam_id(self) -> str:
        return ""

    @property
    def alt_steam_ids(self) -> list[str]:
        return []

    @property
    def additional_nexus_domains(self) -> list[str]:
        return ["fallout4london"]

    def _remove_plugins_txt_symlink(self, log_fn) -> None:
        from Utils.plugins import deploy_plugins_copy

        data_dir = self.get_vanilla_plugins_path()
        try:
            present = {
                entry.name.casefold(): entry.name
                for entry in data_dir.iterdir() if entry.is_file()
            } if data_dir is not None else {}
        except OSError:
            present = {}
        baseline = [
            present[name.casefold()] for name in self._london_plugins
            if name.casefold() in present
        ]
        if not baseline:
            super()._remove_plugins_txt_symlink(log_fn)
            return

        content = "".join(f"*{name}\n" for name in baseline)
        for target in self._plugins_txt_targets():
            deploy_plugins_copy(target.parent, target.name, content, log_fn)
        log_fn("  Restored the Fallout London base plugins list.")
