<template lang="pug">

.district
    .header
        .g-h2 По районам
    i-slider(:count="lots.length")
        .slide(v-for="(lot, index) in lots" :key="index")
            router-link.lot(:to="{ name: 'selection', params: { id: 10 } }")
                .img(:style="{ backgroundImage: `url(${lot.img})` }")
                .info
                    .name {{ lot.name }}
                    .count {{ lot.count }} комплексов

</template>
<script>
import iSlider from 'components/slider'
export default {
    data: () => ({
        lots: [
            {
                img: require('images/placeholders/3.jpg'),
                name: 'Патриаршие пруды',
                count: 4
            },
            {
                img: require('images/placeholders/1.jpg'),
                name: 'Остоженка',
                count: 8
            },
            {
                img: require('images/placeholders/2.jpg'),
                name: 'Чистые пруды',
                count: 2
            },
            {
                img: require('images/placeholders/4.jpg'),
                name: 'Патриаршие пруды',
                count: 12
            },
        ]
    }),
    components: { iSlider }
}
</script>
<style lang="stylus" scoped>

.header
    width $desktop-width
    margin 60px auto 30px

.slide
    margin-right 24px
    &:last-child
        margin-right 0

.lot
    width 384px
    border-radius 10px
    border 1px solid $gray2
    overflow hidden
    transition all .2s
    cursor pointer
    display block
    &:hover
        border-color $primary
        box-shadow: 2px 4px 8px rgba(0, 0, 0, 0.15)
    &:active
        box-shadow: 1px 1px 1px rgba(0, 0, 0, 0.06)
    .img
        height 160px
        background-size cover
        background-position center
    .info
        padding 15px 10px 10px
        .name
            $h3()
        .count
            $text()
            color $gray
            margin-top 4px

</style>
