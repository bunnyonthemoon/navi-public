import { createRouter, createWebHistory } from 'vue-router'
import store from '@/store'
import LayoutMain from '@/layouts/main'
import PageMain from 'pages/main'

const routes = [
    {
        path: '',
        component: LayoutMain,
        children: [
            {
                path: '',
                name: 'main',
                component: PageMain
            },
            {
                path: '/complex/:id',
                name: 'complex',
                props: (route) => ({ id: route.params.id }),
                component: () => import('pages/complex'),
                meta: { title: 'Из комлекса строница' }
            },
            {
                path: '/selection/:id',
                name: 'selection',
                props: (route) => ({ selection_id: route.params.id }),
                component: () => import('pages/catalog')
            },
            {
                path: '/catalog',
                name: 'catalog',
                component: () => import('pages/catalog')
            },
            {
                path: '/favorites',
                name: 'favorites',
                component: () => import('pages/favorites')
            },
        ]
    },
    {
        path: '/:catchAll(.*)',
        name: '404',
        component: () => import('pages/404')
    },
]

const router = createRouter({
    history: createWebHistory('/'),
    routes,
    scrollBehavior(to, from, savedPosition) {
        if (to.path == from.path) return
        if (savedPosition) {
            return savedPosition
        } else {
            return { top: 0 }
        }
    },
})

export default router
