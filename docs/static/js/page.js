class DesktopController {
    constructor() {
        console.log('Using desktop controller.')

        document.querySelectorAll('section.content')
            .forEach(el => el.classList.add('content--hidden'))

        document.querySelectorAll('[data-link]')
            .forEach(el => {
                el.addEventListener('click', () => this.handleNavLink(el.dataset.link))
            })

        document.querySelector('[data-livedemo-start]')
            .addEventListener('click', () => this.hideNavigation())
        document.querySelector('.nav__header')
            .addEventListener('click', () => this.hideNavigation())
        document.querySelector('canvas#c')
            .addEventListener('click', () => this.hideNavigation())

        this.drawer_open = false

    }

    handleNavLink(target) {
        document.querySelector('.content__container').classList.add('content__container--ready')
        console.log('navigating to ' + target)
        document.querySelectorAll('section.content')
            .forEach(el => el.classList.add('content--hidden'))

        document.querySelector(`#${target}`).classList.remove('content--hidden')
        document.querySelector('canvas#c').classList.add('blurred')
        sim.set_blur( true )
        this.drawer_open = true
    }

    hideNavigation() {
        document.querySelector('.content__container').classList.remove('content__container--ready')
        document.querySelector('canvas#c').classList.remove('blurred')
        sim.set_blur( false )
        if (this.drawer_open) {
            sim.controls.autoRotate = true
        }
        this.drawer_open = false
    }
}

class MobileController {
    constructor() {
        console.log('Using mobile controller.')

        document.querySelectorAll('[data-link]')
            .forEach(el => {
                el.addEventListener('click', () => this.handleNavLink(el.href))
            })
    }

    handleNavLink(target) {
        console.log('navigating to ' + target)
    }
}

class ControlsController {
    constructor() {
        document.querySelectorAll('[data-room]')
            .forEach(el => {
                el.addEventListener('click', () => this.loadRoom(el.dataset.room))
            })
    }

    loadRoom(room) {
        console.log(`caught event: load ${room}`)
        api.load_room(room)
    }
}

const loadController = () => {
    if (window.innerWidth < 768) {
        window.controller = new MobileController()
    } else {
        window.controller = new DesktopController()
    }

    window.controls = new ControlsController()
}

window.addEventListener('load', loadController)
