#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from hrwros_factory_states.compute_grasp_state import ComputeGraspState
from hrwros_factory_states.detect_part_camera_state import DetectPartCameraState
from hrwros_factory_states.moveit_to_joints_dyn_state import MoveitToJointsDynState as hrwros_factory_states__MoveitToJointsDynState
from hrwros_factory_states.vacuum_gripper_control_state import VacuumGripperControlState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Sat Jun 18 2022
@author: ayman damoun
'''
class PickpartfromconveyorlearnSM(Behavior):
	'''
	Pick part from conveyor learn course
	'''


	def __init__(self):
		super(PickpartfromconveyorlearnSM, self).__init__()
		self.name = 'Pick part from conveyor learn'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		pick_group = 'robot1'
		home_config1 = [1.57, -1.57, 1.24, -1.57, -1.57,0]
		gripper1 = 'vacuum_gripper1_suction_cup'
		name1 = ['robot1_elbow_joint','robot1_shoulder_lift_joint','robot1_shoulder_pan_joint','robot1_wrist_1_joint','robot1_wrist_2_joint','robot1_wrist_3_joint']
		# x:923 y:553, x:38 y:568
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
		_state_machine.userdata.part_pose = []
		_state_machine.userdata.pick_configuration = home_config1
		_state_machine.userdata.joints_names = []
		_state_machine.userdata.home1 = home_config1

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:36 y:118
			OperatableStateMachine.add('detectobjpose',
										DetectPartCameraState(ref_frame='robot1_base', camera_topic='/hrwros/logical_camera_1', camera_frame='logical_camera_1_frame'),
										transitions={'continue': 'compute_the_grasping', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'pose': 'part_pose'})

			# x:559 y:370
			OperatableStateMachine.add('grasping',
										VacuumGripperControlState(enable='true', service_name='gripper1/control'),
										transitions={'continue': 'move_to_home', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off})

			# x:397 y:278
			OperatableStateMachine.add('move_the_robot',
										hrwros_factory_states__MoveitToJointsDynState(move_group=pick_group, offset=0.0, tool_link=gripper1, action_topic='/move_group'),
										transitions={'reached': 'grasping', 'planning_failed': 'failed', 'control_failed': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off},
										remapping={'joint_values': 'pick_configuration', 'joint_names': 'joints_names'})

			# x:754 y:453
			OperatableStateMachine.add('move_to_home',
										hrwros_factory_states__MoveitToJointsDynState(move_group=pick_group, offset=0.0, tool_link=gripper1, action_topic='/move_group'),
										transitions={'reached': 'finished', 'planning_failed': 'failed', 'control_failed': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off},
										remapping={'joint_values': 'home1', 'joint_names': 'joints_names'})

			# x:236 y:202
			OperatableStateMachine.add('compute_the_grasping',
										ComputeGraspState(group=pick_group, offset=0.0, joint_names=name1, tool_link=gripper1, rotation=3.1416),
										transitions={'continue': 'move_the_robot', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'pose': 'part_pose', 'joint_values': 'pick_configuration', 'joint_names': 'joints_names'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
