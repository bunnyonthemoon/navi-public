import icon from './icon'
import share from './share'
import favorite from './favorite'

export default (App) => {
    App.component('g-icon', icon)
    App.component('g-share', share)
    App.component('g-favorite', favorite)
}
