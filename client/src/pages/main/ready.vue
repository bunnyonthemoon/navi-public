<template lang="pug">

.ready
    .title
        .g-h2 Готовые дома ниже рынка
        router-link.count(:to="{ name: 'catalog' }") {{ complexes.length }} {{ complexes.length >= 5 ? 'объектов' : complexes.length >= 2 ? 'объекта' : 'объект' }}
    //- i-slider(:count="complexes.length")
    //-     .slide(v-for="complex in complexes" :key="complex.id")
    //-         i-complex(:complex="complex")
    .list
        i-complex(v-for="complex in complexes" :key="complex.id" :complex="complex")

</template>
<script>
import vFlickity from 'vue-flickity'
import iSlider from 'components/slider'
import iComplex from 'components/complex'
export default {
    data: (context) => ({
    }),
    computed: {
        complexes() {
            return this.$store.state.catalog.welcome_complexes
        }
    },
    components: { iComplex, vFlickity, iSlider }
}
</script>
<style lang="stylus" scoped>

.ready
    margin 60px auto 0
    width $desktop-width
    +$tablet()
        width $tablet-width
        margin-top 40px

.title
    margin-bottom 10px

.count
    color $primary
    text-decoration underline
    margin-top 10px
    font-size 20px
    font-weight 500
    line-height 26px
    display block
    +$tablet()
        font-size 16px
        line-height 20px
        font-weight 400

.slide
    margin-right 24px
    &:last-child
        margin-right 0

.complex
    margin 10px 0

.list
    display flex
    +$tablet()
        flex-wrap wrap
    .complex
        margin-right 24px
        &:last-child
            margin-right 0
        +$tablet()
            &:nth-child(2n)
                margin-right 0

</style>
