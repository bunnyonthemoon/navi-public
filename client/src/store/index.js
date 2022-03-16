import { createStore } from 'vuex'

import content from './content'
import ui from './ui'
import user from './user'
import catalog from './catalog'

export default createStore({
    modules: {
        content,
        ui,
        user,
        catalog
    },
    actions: {
        async init({ dispatch, commit, state, getters }) {
            await dispatch('catalog/init')
            await dispatch('content/init')
            dispatch('ui/init')
        }
    },
})
