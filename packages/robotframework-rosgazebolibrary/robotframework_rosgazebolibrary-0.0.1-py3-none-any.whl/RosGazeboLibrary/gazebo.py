import subprocess

from roslibpy import Service, ServiceRequest


class GazeboClient:

    def __init__(self, *args, **kwargs):
        self.client = kwargs.get("ros_client")

    def get_model_state(self, model_name):
        service = Service(self.client,
                          'gazebo/get_model_state',
                          'gazebo_msgs/GetModelState'
                          )
        request = ServiceRequest({'model_name': model_name})

        return service.call(request)

    def get_model_properties(self, model_name):
        service = Service(self.client,
                          '/gazebo/get_model_properties',
                          'gazebo_msgs/GetModelProperties'
                          )
        request = ServiceRequest({'model_name': model_name})

        return service.call(request)

    def get_link_state(self, link_name):
        service = Service(self.client,
                          '/gazebo/get_link_state',
                          'gazebo_msgs/LinkState'
                          )
        request = ServiceRequest({'link_name': link_name})

        return service.call(request)

    def get_link_properties(self, link_name):
        service = Service(self.client,
                          '/gazebo/get_link_properties',
                          'gazebo_msgs/GetLinkProperties'
                          )
        request = ServiceRequest({'link_name': link_name})

        return service.call(request)

    def get_world_properties(self):
        service = Service(self.client,
                          '/gazebo/get_world_properties',
                          'gazebo_msgs/GetWorldProperties'
                          )
        request = ServiceRequest()

        return service.call(request)

    def get_physics_properties(self):
        service = Service(self.client,
                          '/gazebo/get_physics_properties',
                          'gazebo_msgs/GetPhysicsProperties'
                          )
        request = ServiceRequest()

        return service.call(request)

    def get_joint_properties(self, joint_name):
        service = Service(self.client,
                          '/gazebo/get_joint_properties',
                          'gazebo_msgs/GetJointProperties'
                          )
        request = ServiceRequest({'joint_name': joint_name})

        return service.call(request)

    def get_light_properties(self, light_name):
        service = Service(self.client,
                          '/gazebo/get_light_properties',
                          'gazebo_msgs/GetLightProperties'
                          )
        request = ServiceRequest({'light_name': light_name})

        return service.call(request)

    def unpause_physics(self):
        service = Service(self.client,
                          '/gazebo/unpause_physics',
                          'std_srvs/Empty'
                          )
        request = ServiceRequest()

        return service.call(request)

    def reset_simulation(self):
        return self.__call_service(
            '/gazebo/reset_simulation', 'std_srvs/Empty',
            None)

    def reset_world(self):
        service = Service(self.client, '/gazebo/reset_world', 'std_srvs/Empty')
        request = ServiceRequest()
        return service.call(request)

    @staticmethod
    def spawn_sdf_model(position: list, object_name: str, sdf_path: str):
        command = f"rosrun gazebo_ros spawn_model -file {sdf_path} -sdf -model {object_name}" \
                  f" -x {position[0]} -y {position[1]} -z {position[2]}"

        subprocess.run(command.split(), stdout=subprocess.DEVNULL)

    '''
    TODO: Move to separate usecase specific library
    '''

    def register_qr(self, qr_id: int, model_name: str, x, y, z, rx, ry, rz):
        service = Service(self.client,
                          '/subscriber/ObjReg',
                          'subscriber/srv/ObjReg'
                          )
        request = ServiceRequest({'objname': model_name, 'qrcodeid': qr_id, 'xOffsetofqr': x, 'yOffsetofqr': y,
                                  'zOffsetofqr': z, 'xRotationofqr': rx, 'yRotationofqr': ry, 'zRotationofqr': rz})

        return service.call(request)

    def get_cv_position(self, model_name):
        service = Service(self.client,
                          '/subscriber/QRAnalyzer',
                          'subscriber/srv/QRAnalyzer'
                          )
        request = ServiceRequest({'objname': model_name})

        return service.call(request)
