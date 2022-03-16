import axios from 'axios'
import router from '@/router'

export default {
    namespaced: true,
    state: () => ({
        complexes: [],
        selections: [],
        private: [],
        welcome_complexes: [],
        favorites: [],
        total: 0,

        filter: {
            bedrooms: [],
            deadline: {
                variants: [],
                choosen: []
            },
            price: {
                values: [0, 0],
                min: 0,
                max: 0
            },
            area: {
                values: [0, 0],
                min: 0,
                max: 0
            },
            sort: {
                key: 'created',
                dir: 1
            },
            view: 'list',
            found: 0,
            class: {
                variants: [],
                choosen: []
            },
            search: null,
            selection: null
        },
    }),
    getters: {
        serverOptions(state) {
            let options = {}

            if (state.filter.bedrooms.length > 0)
                options.bedrooms = state.filter.bedrooms
            else options.bedrooms = null

            if (state.filter.deadline.choosen.length > 0)
                options.deadline = state.filter.deadline.choosen
            else options.deadline = null
            
            if (state.filter.class.choosen.length > 0)
                options.class = state.filter.class.choosen
            else options.class = null

            if (state.filter.price.values[0] != state.filter.price.min || state.filter.price.values[1] != state.filter.price.max)
                options.price = state.filter.price.values
            else options.price = null

            if (state.filter.area.values[0] != state.filter.area.min || state.filter.area.values[1] != state.filter.area.max)
                options.area = state.filter.area.values
            else options.area = null

            options.search = state.filter.search
 
            options.sort_key = state.filter.sort.key
            options.sort_dir = state.filter.sort.dir

            options.view = state.filter.view

            options.selection = state.filter.selection

            return options
        }
    },
    mutations: {
    },
    actions: {
        async init({ commit, dispatch, state }) {
            state.welcome_complexes = window.preload_data.complexes
            state.private = window.preload_data.private
            state.selections = window.preload_data.selections

            let filter = window.preload_data.filter

            state.filter.price.min = filter.price.min
            state.filter.price.max = filter.price.max
            state.filter.price.values = [filter.price.min, filter.price.max]
            state.filter.area.min = filter.area.min
            state.filter.area.max = filter.area.max
            state.filter.area.values = [filter.area.min, filter.area.max]
            state.filter.class.variants = filter.property_classes
            state.filter.found = filter.total
            state.total = filter.total

            if (filter.deadlines.filter(item => item == null))
                state.filter.deadline.variants.push({
                    label: 'Сдан',
                    value: 'done'
                })
            state.filter.deadline.variants.push(...filter.deadlines.filter(item => item != null))
            
            state.favorites = JSON.parse(localStorage.getItem('favorites') || '[]')
        },
        
        async filter({ state, dispatch, getters }) {
            dispatch('updateRoute')
            const { data } = await axios.post('/api/catalog/filter/', { ...getters.serverOptions })
            state.complexes = data.complexes
            state.filter.found = data.found
            console.log(state.complexes)
        },
        async updateRoute({ state, getters }) {
            router.push({ query: { ...getters.serverOptions } })
        },

        async favorite({ state }, { id, action = 'add' }) {
            if (action == 'add' && state.favorites.indexOf(id) == -1)
                state.favorites.push(id)
            if (action == 'remove' && state.favorites.indexOf(id) != -1)
                state.favorites.splice(state.favorites.indexOf(id), 1)

            localStorage.setItem('favorites', JSON.stringify(state.favorites))
        }
    }
}
