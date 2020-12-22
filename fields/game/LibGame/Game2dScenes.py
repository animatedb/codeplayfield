import os
import enum
from operator import *
import pygame as pg
from typing import Dict, List, Union
import LibGame.Game2dBase as base2d
import LibGame.Game2dObject as obj


class Game2dScene:
    def __init__(self, sceneName:str) -> None:
        self.objects = []
        self.sceneName = sceneName

    def addObject(self, filePattern:Union[List, str]) -> obj.Object:
        newObj = obj.Object(filePattern)
        self.objects.append(newObj)
        return newObj

    def getObjects(self) -> List[obj.Object]:
        return self.objects

    def showSceneImages(self, show:bool=False) -> None:
        for obj in self.objects:
            obj.showImage(show)

    def enterScene(self) -> None:
        self.showSceneImages(True)

    def leaveScene(self) -> None:
        self.showSceneImages(False)

    def checkEvent(self, game, event) -> None:
        pass


class SceneDirector:
    def __init__(self, game) -> None:
        # Make a dict for easy name lookup
        self.scenes:Dict[str, Game2dScene] = {}
        self.scene = None

    def addScenes(self, scenes:List[Game2dScene]) -> None:
        for scene in scenes:
            self.scenes[scene.sceneName] = scene
            scene.showSceneImages(False)

    def getObjects(self) -> List[obj.Object]:
        objects = []
        for scene in self.scenes.values():
            objects.extend(scene.getObjects())
        return objects

    def showScene(self, sceneName:str) -> None:
        if self.scene:
            self.scene.leaveScene()
        self.scene = self.scenes[sceneName]
        self.scene.enterScene()

    def checkEvent(self, game, event):
        self.scene.checkEvent(game, event)
