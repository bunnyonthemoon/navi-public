<template lang="pug">

.catalog
    .selection-title(v-if="selection") {{ selection.name }}
        router-link.close(:to="{ name: 'catalog', query: { ...$route.query } }")
            g-icon(name="ui/close")

    c-filter(:is_catalog="true" @load="load")
    l-list(v-if="filter.view == 'list'" :complexes="$store.state.catalog.complexes")
    l-map(v-if="filter.view == 'map'" :complexes="$store.state.catalog.complexes")

</template>
<script>
import cFilter from 'components/filter'
import lList from './list'
import lMap from './map'
export default {
    async beforeRouteEnter(to, from, next) {
        await next(async (vm) => {
            await vm.setFilter()
        })
    },
    async beforeRouteUpdate(to, from) {
        if (to.name != from.name)
            await this.setFilter()
    },
    beforeUnmount() {
        this.$store.state.catalog.filter.view = 'list'
    },
    props: {
        selection_id: [String, Number]
    },
    data: () => ({
    }),
    methods: {
        async load() {
            await this.$store.dispatch('catalog/filter')
        },
        async setFilter() {
            let filter = this.$store.state.catalog.filter
        
            let routeOptions = this.$route.query
            console.log('route', routeOptions)
            
            if (routeOptions.bedrooms)
                filter.bedrooms = typeof routeOptions.bedrooms === 'string' ? [routeOptions.bedrooms] : routeOptions.bedrooms
            if (routeOptions.deadline)
                filter.deadline.choosen = typeof routeOptions.deadline === 'string' ? [routeOptions.deadline] : routeOptions.deadline
            if (routeOptions.class)
                filter.class.choosen = typeof routeOptions.class === 'string' ? [routeOptions.class] : routeOptions.class
            if (routeOptions.done)
                filter.done = JSON.parse(routeOptions.done)
            if (routeOptions.area)
                filter.area.values = [parseInt(routeOptions.area[0]), parseInt(routeOptions.area[1])]
            else
                filter.area.values = [filter.area.min, filter.area.max]
            if (routeOptions.price)
                filter.price.values = [parseInt(routeOptions.price[0]), parseInt(routeOptions.price[1])]
            else
                filter.price.values = [filter.price.min, filter.price.max]

            filter.sort.key = routeOptions.sort_key || filter.sort.key
            filter.sort.dir = routeOptions.sort_dir || filter.sort.dir

            filter.search = routeOptions.search || filter.search
            filter.view = routeOptions.view || filter.view
            filter.selection = this.selection_id

            filter.loaded = true

            await this.$store.dispatch('catalog/filter')
        }
    },
    computed: {
        filter() {
            return this.$store.state.catalog.filter
        },
        selection() {
            return this.selection_id ? this.$store.state.catalog.selections.find(item => item.key == this.selection_id) : null
        }
    },
    components: { cFilter, lList, lMap }
}
</script>
<style lang="stylus" scoped>

.selection-title
    width $desktop-width
    margin 10px auto 25px
    $h2()
    display flex
    align-items center
    .close
        font-size 20px
        cursor pointer
        margin-left 14px
        display flex
        align-items center
        justify-content center
        background-color $gray2
        // color #fff
        width 30px
        height 30px
        border-radius 100%
    +$phone()
        padding 0 16px
        margin-bottom 15px
        margin-top 15px
        .close
            width 24px
            height 24px
            font-size 18px
            margin-left 10px

.catalog
    padding-top 20px
    +$tablet()
        padding-top 0

</style>
