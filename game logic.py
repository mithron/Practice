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

## This is called from the car object
def carInit():

	## setup aliases for Blender API access ##
	cont = G.getCurrentController()
	G.scene = G.getCurrentScene()
	G.car  = cont.owner

	## setup general vehicle characteristics ##
	wheelAttachDirLocal = [0,0,-1]
	wheelAxleLocal = [-1,0,0]

	## setup vehicle physics ##
	vehicle = PC.createConstraint(G.car.getPhysicsId(),0,11)
	G.car["cid"] = vehicle.getConstraintId()
	vehicle = PC.getVehicleConstraint(G.car["cid"])

	## initialize temprary per-car variables ##
	G.car["dS"] = 0.0

	## attached wheel based on actuator name ##
	act0 = cont.actuators["wheel0"]
	wheel0 = act0.owner
	wheelAttachPosLocal = [wheelBaseWide ,wheelFrontOffset, AttachHeightLocal]
	vehicle.addWheel(wheel0,wheelAttachPosLocal,wheelAttachDirLocal,wheelAxleLocal,suspensionLength,wheelRadius,1)

	act1 = cont.actuators["wheel1"]
	wheel1 = act1.owner
	wheelAttachPosLocal = [-wheelBaseWide ,wheelFrontOffset, AttachHeightLocal]
	vehicle.addWheel(wheel1,wheelAttachPosLocal,wheelAttachDirLocal,wheelAxleLocal,suspensionLength,wheelRadius,1)

	act2 = cont.actuators["wheel2"]
	wheel2 = act2.owner
	wheelAttachPosLocal = [wheelBaseWide ,wheelBackOffset, AttachHeightLocal]
	vehicle.addWheel(wheel2,wheelAttachPosLocal,wheelAttachDirLocal,wheelAxleLocal,suspensionLength,wheelRadius,0)

	act3 = cont.actuators["wheel3"]
	wheel3 = act3.owner
	wheelAttachPosLocal = [-wheelBaseWide ,wheelBackOffset, AttachHeightLocal]
	vehicle.addWheel(wheel3,wheelAttachPosLocal,wheelAttachDirLocal,wheelAxleLocal,suspensionLength,wheelRadius,0)

	## set vehicle roll tendency ##
	vehicle.setRollInfluence(influence,0)
	vehicle.setRollInfluence(influence,1)
	vehicle.setRollInfluence(influence,2)
	vehicle.setRollInfluence(influence,3)

	## set vehicle suspension hardness ##
	vehicle.setSuspensionStiffness(stiffness,0)
	vehicle.setSuspensionStiffness(stiffness,1)
	vehicle.setSuspensionStiffness(stiffness,2)
	vehicle.setSuspensionStiffness(stiffness,3)

	## set vehicle suspension dampness ##
	vehicle.setSuspensionDamping(damping,0)
	vehicle.setSuspensionDamping(damping,1)
	vehicle.setSuspensionDamping(damping,2)
	vehicle.setSuspensionDamping(damping,3)

	## set vehicle suspension compression ratio ##
	vehicle.setSuspensionCompression(compression,0)
	vehicle.setSuspensionCompression(compression,1)
	vehicle.setSuspensionCompression(compression,2)
	vehicle.setSuspensionCompression(compression,3)

	## set vehicle tire friction ##
	vehicle.setTyreFriction(friction,0)
	vehicle.setTyreFriction(friction,1)
	vehicle.setTyreFriction(friction,2)
	vehicle.setTyreFriction(friction,3)


## called from main car object
def carHandler():
	vehicle = PC.getVehicleConstraint(G.car["cid"])

	## calculate speed by using the back wheel rotation speed ##
	S = vehicle.getWheelRotation(2)+vehicle.getWheelRotation(3)
	G.car["speed"] = (S - G.car["dS"])*10.0

	## apply engine force ##
	vehicle.applyEngineForce(G.car["force"],0)
	vehicle.applyEngineForce(G.car["force"],1)
	vehicle.applyEngineForce(G.car["force"],2)
	vehicle.applyEngineForce(G.car["force"],3)

	## calculate steering with varying sensitivity ##
	if math.fabs(G.car["speed"])<15.0: s = 5.0
	elif math.fabs(G.car["speed"])<28.0: s=4.5
	elif math.fabs(G.car["speed"])<40.0: s=4.0
	else: s=3.5

	## steer front wheels
	vehicle.setSteeringValue(G.car["steer"]*s,0)
	vehicle.setSteeringValue(G.car["steer"]*s,1)

	## slowly ease off gas and center steering ##
	G.car["steer"] *= 0.6
	G.car["force"] *= 0.9

	## align car to Z axis to prevent flipping ##
	
	G.car.alignAxisToVect([0.0,0.0,1.0], 2, Stability)
	
	## store old values ##
	G.car["dS"] = S



## called from main car object
def keyHandler():
	cont = G.getCurrentController()
	keys = cont.sensors["key"].events
	for key in keys:
		## up arrow
		if   key[0] == K.UPARROWKEY:
			G.car["force"]  = -15.0
		## down arrow
		elif key[0] == K.DOWNARROWKEY:
			G.car["force"]  = 10.0
		## right arrow
		elif key[0] == K.RIGHTARROWKEY:
			G.car["steer"] -= 0.05
		## left arrow
		elif key[0] == K.LEFTARROWKEY:
			G.car["steer"] += 0.05
		## R
		elif key[0] == K.RKEY:
			if key[1] == 1:
				# re-orient car
				if G.car["jump"] > 2.0:
					G.car.position = (G.car.worldPosition[0], G.car.worldPosition[1], G.car.worldPosition[2]+3.0)
					G.car.alignAxisToVect([0.0,0.0,1.0], 2, 1.0)
					G.car.setLinearVelocity([0.0,0.0,0.0],1)
					G.car.setAngularVelocity([0.0,0.0,0.0],1)
					G.car["jump"] = 0
		## Spacebar
		elif key[0] == K.SPACEKEY:
			# hackish Brake
			if G.car["speed"] > 2.0:
				G.car["force"]  = 15.0
			if G.car["speed"] < -2.0:
				G.car["force"]  = -15.0





## called from Menu Camera
def initGUI():
	R.showMouse(1)
	G.UIScene = G.getCurrentScene()

## called from Menu scene text labels
def UIClickHandler():
	## setting up aliases
	cont = G.getCurrentController()
	hover = cont.sensors['hover']
	click = cont.sensors['click']
	own = cont.owner

	## trigger on mouseover
	if hover.positive:

		if own.name == "OBdrive" or own.name == "OBloc":
			## do fancy animation and lighting
			ray = G.UIScene.objects["OBray"]
			x = own.worldPosition[0]*0.2+ray.worldPosition[0]*0.8
			y = own.worldPosition[1]*0.2+ray.worldPosition[1]*0.8
			z = own.worldPosition[2]+2
			ray.worldPosition = [x,y,z]
			own.scaling = [1.2,1.2,1.2]
		else:
			## dim fancy animation and lighting
			ray = G.UIScene.objects["OBray"]
			x = own.worldPosition[0]*0.2+ray.worldPosition[0]*0.8
			y = own.worldPosition[1]*0.2+ray.worldPosition[1]*0.8
			z = own.worldPosition[2]+6
			ray.worldPosition = [x,y,z]
			own.scaling = [1,1,1]

		## set the global state for the menu
		G.menuState = own.name[2:]


		## trigger on mouseclick release
		if (click.triggered and not click.positive)  and own.name != "OBcar" :
			## animate
			wipe = G.UIScene.objects["OBwipe"]
			wipe["transition"] = True
			cam = G.UIScene.objects["OBCamera"]
			cam["transition"] = True

	else:
		own.scaling = [1,1,1]


## called from Menu Camera State Layer 2
def switchScene():
	G.loc = "1"

	if G.menuState == "car":
		G.UIScene.active_camera = G.UIScene.objects["OBCameraCar"]
	elif G.menuState == "loc":
		G.UIScene.active_camera = G.UIScene.objects["OBCameraLoc"]
	else:
		cont = G.getCurrentController()
		cont.actuators["load"].fileName = G.loc+".blend"
		cont.activate("load")

## called from Menu Scene Empty empty
def addCredit():
	## setup aliases
	cont = G.getCurrentController()
	add = cont.actuators["add"]
	own = cont.owner

	## add a sequence of objects, then repeat
	add.object = str(own["counter"])
	cont.activate(add)
	own["counter"] += 1
	if own["counter"] > 10:
		own["counter"] = 0

## called from Menu Scene Caption emtpy
def addCaption():
	## setup aliases
	cont = G.getCurrentController()
	add = cont.actuators["add"]
	own = cont.owner

	try:
		## if new caption differs from old ones
		if str(add.object) != ("OBcaption."+ G.menuState):

			## try to kill previous captions
			try:
				add.objectLastCreated.endObject()
			except:
				pass

			## add new caption
			add.object = "caption."+ G.menuState
			cont.activate(add)
	except:
		pass


## called from shadow lamp
def shadow():
	cont = G.getCurrentController()
	ownpos = [-5.0,0.0,8.0]
	pos = G.car.worldPosition
	cont.owner.worldPosition = [pos[0]+ownpos[0], pos[1]+ownpos[1], pos[2]+ownpos[2]]


#1 more commit line =D

# another line for cumshot to gitHub