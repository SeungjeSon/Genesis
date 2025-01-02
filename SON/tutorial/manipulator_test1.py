import genesis as gs

def run_sim(scene, enable_vis):
    for i in range(500):
        scene.step()
    if enable_vis:
        scene.viewer.stop()

gs.init(backend=gs.metal) # mac gpu사용하기 위해 gs.metal
scene = gs.Scene(
    sim_options=gs.options.SimOptions(),
    viewer_options=gs.options.ViewerOptions(
        res = (1280, 960),      # default : None --> 4:3 창으로 자동 설정됨
        camera_pos=(3.5, 0.0, 2.5),
        camera_lookat=(0.0, 0.0, 0.5),
        camera_fov=40,
        max_FPS = 60,           # 지정 안하면 자동 FPS 설정됨
    ),
    show_viewer=True,
    rigid_options=gs.options.RigidOptions(
        dt=0.01,
        gravity=(0.0, 0.0, -10.0),
    ),
)

plane = scene.add_entity(gs.morphs.Plane())
franka = scene.add_entity(gs.morphs.MJCF(
    file='xml/franka_emika_panda/panda.xml',
    pos = (0, 0, 0),
    euler = (0, 0, 90), # we follow scipy's extrinsic x-y-z rotation convention, in degrees,
        # quat  = (1.0, 0.0, 0.0, 0.0), # we use w-x-y-z convention for quaternions,
    scale = 1.0,
    ),
)

scene.build()
gs.tools.run_in_another_thread(
    fn=run_sim,
    args=(scene, True)
)

scene.viewer.start()
