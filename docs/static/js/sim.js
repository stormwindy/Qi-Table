const API_URL = 'https://qi-api.kage.dev/'
const DEFAULT_ROOM = 'room0'

class Simulator {
    constructor() {
        this.el = document.querySelector('#c')

        this.init_scene()
        this.init_pipeline()

        window.addEventListener('resize', this.resize_window.bind(this))
    }

    init_scene() {
        this.scene = new THREE.Scene()

        // add fog
        const fogColor = new THREE.Color( 0xFFFFFF )
        this.scene.background = fogColor
        this.scene.fog = new THREE.Fog(fogColor, 100, 200)

        // let there be light
        const ambientLight = new THREE.AmbientLight(0xFFFFFF, 0.6)
        this.scene.add(ambientLight)

        const directionalLight = new THREE.DirectionalLight(0xFFFFFF, 1);
        directionalLight.position.x = 0.5
        directionalLight.position.y = 0.8
        directionalLight.castShadow = true
        this.scene.add(directionalLight)

        // load the floor texture
        this.texture_loader = new THREE.TextureLoader()
        const floor_texture = this.texture_loader.load('static/textures/grid.png')
        floor_texture.wrapS = floor_texture.wrapT = THREE.RepeatMapping
        floor_texture.repeat.set(1024,1024) // must match plane size for 1-1 mapping
        floor_texture.encode = THREE.sRGBEncoding

        // make a material and instantiate the floor
        const floor_material = new THREE.MeshBasicMaterial({ map: floor_texture })
        //const floor_material = new THREE.MeshBasicMaterial({ color: 0xFF0FFF })
        const floor_mesh = new THREE.Mesh(
            new THREE.PlaneBufferGeometry(1024, 1024),
            floor_material
        )
        floor_mesh.receiveShadow = true
        floor_mesh.position.set(0.5, -0.5, 0.5)
        floor_mesh.rotation.x = -Math.PI / 2
        this.floor = floor_mesh
        this.scene.add(floor_mesh)


        // create the path group
        this.pathgroup = new THREE.Group()
        this.pathgroup.translateX(-8)
        this.pathgroup.translateZ(-4.5)
        this.scene.add(this.pathgroup)

        //this.init_cubes()

    }

    init_cubes() {
        const cube_geo = new THREE.BoxGeometry()
        const cube_mat = new THREE.MeshStandardMaterial({
            color: 0x4BC6B9,
            roughness: 0.5,
            metalness: 0.2,
        })

        const makeCube = (x,z) => {
            const cube = new THREE.Mesh( cube_geo, cube_mat )
            cube.position.set(x, 0, z)
            cube.castShadow = true
            return cube
        }

        this.cubes = []

        for (let i = 0; i < 5; i++) {
            this.cubes.push([])
            for (let j = 0; j < 5; j++) {
                let cube = makeCube(i, j)
                this.cubes[i].push(cube)
                this.scene.add(this.cubes[i][j])
            }
        }

        this._cube_anim = 0
    }

    animate_cubes() {
        const scale = v => v * (Math.PI/180)
        for (let i = 0; i < 5; i++) {
            for (let j = 0; j < 5; j++) {
                this.cubes[i][j].position.y = 1 + Math.sin(scale(16*(i + j) + this._cube_anim ))
            }
        }
        this._cube_anim += 1
    }

    remove_cubes() {
        for (let i = 0; i < 5; i++) {
            for (let j = 0; j < 5; j++) {
                this.scene.remove(this.cubes[i][j])
            }
        }
    }

    load_computed_paths(paths) {
        // helpers
        const cube_geo = new THREE.BoxGeometry()
        const makeCube = (x,z,color) => {
            const cube_mat = new THREE.MeshStandardMaterial({
                color,
                roughness: 0.5,
                metalness: 0.2,
            })
            const cube = new THREE.Mesh( cube_geo, cube_mat )
            cube.position.set(x, 0, z)
            cube.castShadow = true
            return cube
        }

        // clean up list if one is already loaded
        this.scene.remove(this.pathgroup)
        this.pathgroup = new THREE.Group()
        this.pathgroup.translateX(-8)
        this.pathgroup.translateZ(-4.5)
        this.scene.add(this.pathgroup)


        if (this.paths) {
            for (let path of paths) {
                if (path.obj) {
                    this.pathgroup.remove(path.obj)
                }
                if (path.goal) {
                    this.pathgroup.remove(path.goal)
                }
            }
        }

        this._max_path_length = 0

        this.paths = paths.map(path => {
            if (path.type === 'agent') {
                path.obj = makeCube(0,0,0x4BC6B9)
                this._max_path_length = Math.max(path.path.length, this._max_path_length) // hax
                this.pathgroup.add(path.obj)
            } else if (path.type === 'obstacle') {
                path.obj = makeCube(path.loc[0],path.loc[1],0xe76F51)
                this.pathgroup.add(path.obj)
            }
            return path
        })
    }

    draw_goals() {
        // create the materials
        const goal_geo = new THREE.CircleGeometry( 0.25, 32 )
        const goal_mat = new THREE.MeshStandardMaterial({
            color: 0x4AAD52,
            roughness: 0.5,
            metalness: 0.2
        })

        // find each agent's final path point
        for (let path of this.paths) {
            if (path.type !== 'agent' || path.pathFound === false) {continue}

            let loc = path.path[path.path.length - 1]

            path.goal = new THREE.Mesh(goal_geo, goal_mat)
            path.goal.position.x = loc[0]
            path.goal.position.y = -0.45
            path.goal.position.z = loc[1]
            path.goal.rotation.x = Math.PI / -2
            this.pathgroup.add( path.goal )
        }
    }

    apply_paths(step) {
        const lerp = (a,b,percent) => a + (percent * (b - a))
        for (let path of this.paths) {
            if (path.type !== 'agent' || path.pathFound === false) {continue}

            if (path.path.length <= step) {continue}

            // lerp between two positions
            const step_lower = Math.floor(step)
            const step_upper = Math.ceil( step)

            const step_fpart = step - Math.floor(step)

            let loc_l = path.path[step_lower]
            let loc_u = path.path[step_upper]

            // hacky, if we've run off the end of the list lerp to the same pos
            if (loc_u === undefined) { loc_u = loc_l }

            let loc = [
                lerp(loc_l[0], loc_u[0], step_fpart),
                lerp(loc_l[1], loc_u[1], step_fpart)
            ]

            path.obj.position.x = loc[0]
            path.obj.position.z = loc[1]
        }
    }

    resize_window() {
        this.el.style.height = window.innerHeight + 'px'
        this.el.style.width = window.innerWidth  + 'px'

        let bbox = this.el.getBoundingClientRect()

        this.camera.aspect = bbox.width / bbox.height
        this.camera.updateProjectionMatrix()
        this.renderer.setSize(bbox.width, bbox.height)
    }

    set_blur( blurred ) {
        this.blurred = blurred
    }

    init_pipeline() {
        let bbox = this.el.getBoundingClientRect()

        // set up a camera
        this.camera = new THREE.PerspectiveCamera( 75, bbox.width / bbox.height, 0.1, 1000 )

        this.renderer = new THREE.WebGLRenderer({
            canvas: this.el,
            antialias: true
        })

        this.camera.position.x = 5
        this.camera.lookAt(0, 0, 0)

        // controls config
        this.controls = new THREE.OrbitControls( this.camera, this.renderer.domElement )
        this.controls.enableDamping = false; // an animation loop is required when either damping or auto-rotation are enabled
        this.controls.dampingFactor = 0.01;
        this.controls.autoRotate = true
		this.controls.object.position.y += 4
        this.controls.target = new THREE.Vector3(0,0,0)

        this.el.addEventListener('mouseup', () => this.controls.autoRotate = false)
        this.el.addEventListener('dblclick', () => this.controls.autoRotate = true)

        this.controls.screenSpacePanning = false;

        this.controls.minDistance = 1;
        this.controls.maxDistance = 500;

        this.controls.maxPolarAngle = Math.PI / 2;

        this.renderer.setSize(bbox.width, bbox.height);

        // for blurred cases
        this.blur_renderer = new THREE.EffectComposer( this.renderer );
        this.blur_renderer.addPass( new THREE.RenderPass( this.scene, this.camera ) );
        const hblur = new THREE.ShaderPass( THREE.HorizontalBlurShader );
        this.blur_renderer.addPass( hblur );

        const vblur = new THREE.ShaderPass( THREE.VerticalBlurShader );
        // set this shader pass to render to screen so we can see the effects
        vblur.renderToScreen = true;
        this.blur_renderer.addPass( vblur );

        this.set_blur( false )
    }

    render() {
        if (this.blurred) {
            this.blur_renderer.render()
        } else {
            this.renderer.render( this.scene, this.camera );
        }

        this.controls.update()

        requestAnimationFrame( () => this.render() )
    }
}

class WebAPIController {
    constructor() {
        this._anim_timer = null
        this._anim_step  = 0
    }

    async get_live_room(room_name) {
        const path = await fetch(
            API_URL,
            {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body:   JSON.stringify({room: room_name})
            }
        )

        return await path.json()
    }

    async get_mocked_room(room_name) {
        const path = await fetch(`static/mock/${room_name}.json`)

        return await path.json()
    }

    async load_room(room_name) {
        console.log(`loading '${room_name}' from ${API_URL}`)


        let path = []
        if (room_name === 'room0') {
            path = await this.get_mocked_room(room_name)
        } else {
            try {
                path = await this.get_live_room(room_name)
            } catch (e) {
                console.warn('room load failed, falling back', e)
                path = await this.get_mocked_room(room_name)
            }
        }

        console.log(path)

        const scalePoint = l => [l[0]/60,l[1]/60]

        path = path.map(obj => {
            if (obj.type === 'agent' && obj.pathFound) {
                obj.path = obj.path.map(scalePoint)
            } else if (obj.type === 'obstacle') {
                obj.loc = scalePoint(obj.loc)
            }
            return obj
        })

        if (this._anim_timer !== null) {
            clearInterval(this._anim_timer)
        }

        //sim.remove_cubes()
        sim.load_computed_paths(path)
        sim.draw_goals()
        sim.apply_paths(0)
        sim.pathgroup.scale.x = 0.5
        sim.pathgroup.scale.y = 0.5
        sim.pathgroup.scale.z = 0.5

        // try to run the animation within 3 seconds (180 frames)
        const ANIM_STEP_SIZE = sim._max_path_length / (3 * 60)


        this._anim_step = 0
        this._anim_timer = setInterval(() => {
            sim.apply_paths(this._anim_step)
            this._anim_step = ((ANIM_STEP_SIZE + this._anim_step) % sim._max_path_length)
        }, 1000 / 60)

    }


}

window.addEventListener('load', () => {
    window.sim = new Simulator()
    window.sim.render()

    window.api = new WebAPIController()
    window.api.load_room(DEFAULT_ROOM)
})
