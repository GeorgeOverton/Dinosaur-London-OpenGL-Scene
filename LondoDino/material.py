class Material:
    def __init__(self, name=None, Ka=[1.,1.,1.], Kd=[1.,1.,1.], Ks=[1.,1.,1.], Ns=10.0, texture=None, bump=None):
        # propeties of the meterial
        self.name = name
        self.Ka = Ka
        self.Kd = Kd
        self.Ks = Ks
        self.Ns = Ns
        self.texture = texture
        self.alpha = 1.0

class MaterialLibrary:
    def __init__(self):
        self.materials = []
        self.names = {}

    def add_material(self, material):
        # adds a new meterial
        self.names[material.name] = len(self.materials)
        self.materials.append(material)

