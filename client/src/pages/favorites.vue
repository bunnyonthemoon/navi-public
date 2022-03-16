<template lang="pug">

.favorites
    .title Избранное
    .list(v-if="complexes.length > 0")
        c-complex(v-for="complex in complexes" :key="complex.id" :complex="complex")
    .empty(v-else) Список избранного пуст

</template>
<script>
import axios from 'axios'
import cComplex from 'components/complex'
export default {
    async created() {
        await this.load()
    },
    data: () => ({
        complexes: []
    }),
    methods: {
        async load() {
            const { data } = await axios.post('/api/catalog/favorites/', {
                ids: this.$store.state.catalog.favorites
            })
            this.complexes = data.complexes
        }
    },
    components: { cComplex }
}
</script>
<style lang="stylus" scoped>

.favorites
    width $desktop-width
    margin 0 auto
    +$tablet()
        width $tablet-width
    +$phone()
        width 100%
        padding 0 16px

.title
    font-size 28px
    line-height 36px
    font-weight 500
    margin-top 40px

.list
    display flex
    flex-wrap wrap
    margin-bottom 80px
    .complex
        margin-top 40px
        margin-right 24px
        &:nth-child(3n+3)
            margin-right 0
    +$phone()
        flex-direction column
        .complex
            margin-right 0
            margin-top 25px

.empty
    font-size 30px
    line-height 1.2
    text-align center
    font-weight 500
    margin-top 100px
    +$phone()
        margin-top 60px
        font-size 27px

</style>
