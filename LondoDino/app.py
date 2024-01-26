import pygame

# import the scene class
from cubeMap import FlattenCubeMap
from scene import Scene

from lightSource import LightSource

from blender import load_obj_file

from BaseModel import DrawModelFromMesh

from shaders import *

from ShadowMapping import *

from sphereModel import Sphere

from skyBox import *

from environmentMapping import *

class LondonScene(Scene):
    def __init__(self):
        Scene.__init__(self)

        self.light = LightSource(self, position=[3., 15., -3.])

        self.shaders='phong'

        self.move = False

        # for shadow map rendering
        self.shadows = ShadowMap(light=self.light)
        self.show_shadow_map = ShowTexture(self, self.shadows)

        #loads the models
        platform = load_obj_file('models/platform.obj')
        #renders the mesh of a model
        self.platform = [DrawModelFromMesh(scene=self, M=np.matmul(translationMatrix([0, -4, 0]), scaleMatrix([0.75,0.75,0.75])), mesh=mesh, shader=ShadowMappingShader(shadow_map=self.shadows), name='platform') for mesh in platform]

        army_man1 = load_obj_file('models/army_man.obj')
        self.army_man1 = [DrawModelFromMesh(scene=self, M=np.matmul(translationMatrix([0, -4, 0]),rotationMatrixY(-0.523599*3)), mesh=mesh, shader=ShadowMappingShader(shadow_map=self.shadows), name='army_man1') for mesh in army_man1]
        self.army_man2 = [DrawModelFromMesh(scene=self, M=np.matmul(translationMatrix([0, -4, 0]),rotationMatrixY(-0.523599)), mesh=mesh, shader=ShadowMappingShader(shadow_map=self.shadows), name='army_man2') for mesh in army_man1]
        self.army_man3 = [DrawModelFromMesh(scene=self, M=np.matmul(translationMatrix([0, -4, 0]),rotationMatrixY(-0.523599*2)), mesh=mesh, shader=ShadowMappingShader(shadow_map=self.shadows), name='army_man3') for mesh in army_man1]

        barrier = load_obj_file('models/barrier_1.obj')
        self.barrier = [DrawModelFromMesh(scene=self, M=translationMatrix([0, -4, 0]), mesh=mesh, shader=ShadowMappingShader(shadow_map=self.shadows), name='barrier') for mesh in barrier]
        self.barrier2 = [DrawModelFromMesh(scene=self, M=np.matmul(translationMatrix([0, -4, 0]),rotationMatrixY(0.523599)), mesh=mesh, shader=ShadowMappingShader(shadow_map=self.shadows), name='barrier2') for mesh in barrier]
        self.barrier3 = [DrawModelFromMesh(scene=self, M=np.matmul(translationMatrix([0, -4, 0]),rotationMatrixY(0.523599*2)), mesh=mesh, shader=ShadowMappingShader(shadow_map=self.shadows), name='barrier3') for mesh in barrier]

        self.table1 = load_obj_file('models/dino_test.obj')
        self.table = [DrawModelFromMesh(scene=self, M=translationMatrix([0, -4, 0]), mesh=mesh, shader=ShadowMappingShader(shadow_map=self.shadows), name='table') for mesh in self.table1]

        # draw a skybox for the horizon
        self.skybox = SkyBox(scene=self)

        self.show_light = DrawModelFromMesh(scene=self, M=poseMatrix(position=self.light.position, scale=0.2), mesh=Sphere(material=Material(Ka=[10,10,10])), shader=PhongShader())

        self.environment = EnvironmentMappingTexture(width=400, height=400)

        self.sphere = DrawModelFromMesh(scene=self, M=poseMatrix(), mesh=Sphere(), shader=EnvironmentShader(map=self.environment))
        self.sphere = DrawModelFromMesh(scene=self, M=poseMatrix(), mesh=Sphere(), shader=FlatShader())

        #culling the back faces of the objects
        glEnable(GL_CULL_FACE)
        glCullFace(GL_BACK)


    def draw_shadow_map(self):
        #draw shadow
        # first we need to clear the scene, we also clear the depth buffer to handle occlusions
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # also all models from the table
        for model in self.table:
            model.draw()

        for model in self.barrier:
            model.draw()

        for model in self.barrier2:
            model.draw()

        for model in self.barrier3:
            model.draw()

        for model in self.army_man1:
            model.draw()

        for model in self.army_man2:
            model.draw()

        for model in self.army_man3:
            model.draw()

        for model in self.platform:
            model.draw()
            

    def draw_reflections(self):
        self.skybox.draw()

        for model in self.models:
            model.draw()

        # also all models from the table
        for model in self.table:
            model.draw()
        
        for model in self.barrier:
            model.draw()

        for model in self.barrier2:
            model.draw()

        for model in self.barrier3:
            model.draw()

        for model in self.army_man1:
            model.draw()

        for model in self.army_man2:
            model.draw()

        for model in self.army_man3:
            model.draw()

        for model in self.platform:
            model.draw()


    def draw(self, framebuffer=False):
        '''
        Draw all models in the scene
        :return: None
        '''

        # first we need to clear the scene, we also clear the depth buffer to handle occlusions
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # when using a framebuffer, we do not update the camera to allow for arbitrary viewpoint.
        if not framebuffer:
            self.camera.update()

        # first, we draw the skybox
        self.skybox.draw()

        # render the shadows
        self.shadows.render(self)

        # when rendering the framebuffer we ignore the reflective object
        if not framebuffer:

            self.environment.update(self)
            self.show_shadow_map.draw()

        # then we loop over all models in the list and draw them
        for model in self.models:
            model.draw()

        # also all models from the table
        for model in self.table:
            model.draw()

        for model in self.barrier:
            model.draw()

        for model in self.barrier2:
            model.draw()

        for model in self.barrier3:
            model.draw()
        
        for model in self.army_man1:
            model.draw()

        for model in self.army_man2:
            model.draw()

        for model in self.army_man3:
            model.draw()

        for model in self.platform:
            model.draw()

        self.show_light.draw()

        # once we are done drawing, we display the scene
        # Note that here we use double buffering to avoid artefacts:
        # we draw on a different buffer than the one we display,
        # and flip the two buffers once we are done drawing.
        if not framebuffer:
            pygame.display.flip()

    def keyboard(self, event):
        
        # starts an animation when you press space
        Scene.keyboard(self, event)
        if event.key == pygame.K_SPACE:
            print('--> starting animation')
            if self.move == True:
                self.move = False
            else:
                self.move = True



if __name__ == '__main__':
    # initialises the scene object
    # scene = Scene(shaders='gouraud')
    scene = LondonScene()

    # starts drawing the scene
    scene.run()
