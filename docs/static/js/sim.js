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
        this.scene.add(this.pathgroup)

        this.init_cubes()

    }

    init_cubes() {
        const cube_geo = new THREE.BoxGeometry()
        const cube_mat = new THREE.MeshStandardMaterial({
            color: 0x4BC6B9,
            roughness: 0.5,
            metalness: 0.2,
            specular: 0xFFFFFF })

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
                specular: color })
            const cube = new THREE.Mesh( cube_geo, cube_mat )
            cube.position.set(x, 0, z)
            cube.castShadow = true
            return cube
        }

        // TODO: clean up list if one is already loaded
        if (this.paths) {
            for (let path of paths) {
                if (path.obj) {
                    this.pathgroup.remove(path.obj)
                }
            }
        }

        this._max_path_length = 0

        this.paths = paths.map(path => {
            if (path.type === 'agent') {
                path.obj = makeCube(0,0,0x4BC6B9)
                this._max_path_length = Math.max(path.path.length, this._max_path_length) // hax
                path.obj.name = 'Agent'
                this.pathgroup.add(path.obj)
            } else if (path.type === 'obstacle') {
                path.obj = makeCube(path.loc[0],path.loc[1],0xe76F51)
                this.pathgroup.add(path.obj)
            }
            return path
        })
    }

    apply_paths(step) {
        for (let path of this.paths) {
            if (path.type !== 'agent' || path.pathFound === false) {continue}

            console.log(path)
            if (path.path.length <= step) {continue}

            let loc = path.path[step]
            console.log(path, loc, step)

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

    init_pipeline() {
        let bbox = this.el.getBoundingClientRect()

        // set up a camera
        this.camera = new THREE.PerspectiveCamera( 75, bbox.width / bbox.height, 0.1, 1000 )

        this.renderer = new THREE.WebGLRenderer({
            canvas: this.el,
            antialias: true
        })

        this.camera.lookAt(0, 0, 0)

        // controls config
        this.controls = new THREE.OrbitControls( this.camera, this.renderer.domElement )
        this.controls.enableDamping = false; // an animation loop is required when either damping or auto-rotation are enabled
        this.controls.dampingFactor = 0.01;
        this.controls.autoRotate = true
		this.controls.object.position.y += 4
        this.controls.target = this.cubes[2][2].position.clone()

        this.el.addEventListener('mouseup', () => this.controls.autoRotate = false)
        this.el.addEventListener('dblclick', () => this.controls.autoRotate = true)

        this.controls.screenSpacePanning = false;

        this.controls.minDistance = 1;
        this.controls.maxDistance = 500;

        this.controls.maxPolarAngle = Math.PI / 2;

        this.renderer.setSize(bbox.width, bbox.height);
    }

    render() {
        this.renderer.render( this.scene, this.camera );

        this.controls.update()

        this.animate_cubes()
        requestAnimationFrame( () => this.render() )
    }
}

class WebAPIController {
    constructor() {
        this._anim_timer = null
        this._anim_step  = 0
    }
    async load_room(room_name) {
        console.log(`loading '${room_name}' from ${API_URL}`)


        let path = await fetch(
            API_URL,
            {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body:   JSON.stringify({room: room_name})
            }
        )

        path = await path.json()

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
        
        sim.remove_cubes()
        sim.load_computed_paths(path)
        sim.apply_paths(0)
        sim.pathgroup.translateX(-8)
        sim.pathgroup.translateZ(-4.5)
        sim.pathgroup.scale.x = 0.5
        sim.pathgroup.scale.z = 0.5

        this._anim_step = 0
        this._anim_timer = setInterval(() => {
            sim.apply_paths(this._anim_step)
            this._anim_step = ((1 + this._anim_step) % sim._max_path_length)
        }, 500)

    }


}

window.addEventListener('load', () => {
    window.sim = new Simulator()
    window.sim.render()

    window.api = new WebAPIController()
    window.api.load_room(DEFAULT_ROOM)
})
