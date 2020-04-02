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
        this.scene.fog = new THREE.Fog(fogColor, 10, 20)

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

        

        // test mesh
        const cube_geo = new THREE.BoxGeometry()
        const cube_mat = new THREE.MeshLambertMaterial({ color: 0xFF0000, shininess: 20, specular: 0xFFFFFF })
        const cube = new THREE.Mesh( cube_geo, cube_mat )
        cube.position.z = -5
        cube.position.y = 0
        cube.position.x = -1
        cube.castShadow = true

        //this.scene.add(cube)
        this.cube = cube

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

        this.camera.lookAt(this.cube.position.x, this.cube.position.y, this.cube.position.z)
    
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

window.addEventListener('load', () => {
    window.sim = new Simulator()
    window.sim.render()
})
