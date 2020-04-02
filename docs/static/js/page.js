class DesktopController {
    constructor() {
        console.log('Using desktop controller.')

        document.querySelectorAll('section.content')
            .forEach(el => el.classList.add('content--hidden'))

        document.querySelectorAll('[data-link]')
            .forEach(el => {
                el.addEventListener('click', () => this.handleNavLink(el.dataset.link))
            })
    }

    handleNavLink(target) {
        document.querySelector('.content__container').classList.add('content__container--ready')
        console.log('navigating to ' + target)
        document.querySelectorAll('section.content')
            .forEach(el => el.classList.add('content--hidden'))

        document.querySelector(`#${target}`).classList.remove('content--hidden')
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

const loadController = () => {
    if (window.innerWidth < 768) {
        window.controller = new MobileController()
    } else {
        window.controller = new DesktopController()
    }
}

window.addEventListener('load', loadController)
