import axios from 'axios'
import router from '@/router'

export default {
    namespaced: true,
    state: () => ({
        editor: null,
        colors: {},
        contacts: {},
        meta: {},
        files: {},
        order: {},
        text: {}
    }),
    getters: {
    },
    mutations: {
    },
    actions: {
        async init({ commit, dispatch, state }) {
            let settings = window.preload_data.settings
            state.colors = {
                primary: settings.primary_color,
                secondary: settings.secondary_color
            }
            state.contacts = {
                instagram: settings.instagram,
                telegram: settings.telegram,
                phone: settings.phone,
                address: settings.address
            }
            state.meta = {
                description: settings.description
            }
            state.files = {
                catalog: settings.catalog,
                agreement: settings.agreement
            }
            state.order = {
                private: settings.private_order,
                budget: settings.budget_order,
                type: settings.type_order,
                catalog: settings.catalog_order,
            }
            state.text = {
                main_title: settings.main_title,
                main_subtitle: settings.main_subtitle,
                main_catalog_title: settings.main_catalog_title,
                main_catalog_text: settings.main_catalog_text,
            }
        },
        async save() {

        }
    }
}
