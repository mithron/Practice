## This file contains all the gameplay python Logic for the Racing game.

## First, we import all the python modules
import PhysicsConstraints as PC
import GameLogic as G
import GameKeys as K
import Rasterizer as R
import math
 

## Car config ##
suspensionLength = 0.4
wheelRadius = 0.35
wheelBaseWide = 0.65
wheelFrontOffset = 0.75
wheelBackOffset = -1.75
influence = 0.05
stiffness = 20.0
damping = 1.0
compression = 4.0
friction = 8.0
AttachHeightLocal = 0.0
Stability = 0.07

