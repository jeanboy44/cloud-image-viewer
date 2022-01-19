class Settings(QObject):
    def __init__(self):
        super().__init__()
        try:
            with open("config.yml") as f:
                self.config = yaml.load(f, Loader=yaml.FullLoader)
        except:
            self.initialize()
            with open("config.yml") as f:
                self.config = yaml.load(f, Loader=yaml.FullLoader)

        self.config = edict(self.config)

    def initialize(self):
        config = edict({})
        config.name = "cloud-image_viewer"
        with open("config.yml", mode="w", encoding="utf8") as f:
            yaml.dump(self.edict2dict(config), f, sort_keys=True)

    def edict2dict(self, edict_obj):
        dict_obj = {}

        for key, vals in edict_obj.items():
            if isinstance(vals, edict):
                dict_obj[key] = self.edict2dict(vals)
            else:
                dict_obj[key] = vals

        return dict_obj

    def save(self):
        with open("config.yml", mode="w", encoding="utf8") as f:
            yaml.dump(self.edict2dict(config), f, sort_keys=True)
