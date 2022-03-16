<template lang="pug">

.budget
    .header
        .g-h2 По бюджету
    i-slider
        .slide(v-for="(selection, index) in selections" :key="index")
            router-link.card(:to="{ name: 'selection', params: { id: selection.key } }" :style="{ backgroundImage: `url(${selection.image})` }")
                .name {{ selection.name }}
                .count {{ selection.count }} комплексов
                .arrow
                    g-icon(name="ui/arrow")

</template>
<script>
import iSlider from 'components/slider'
export default {
    computed: {
        selections() {
            return this.$store.state.catalog.selections.filter(item => item.type == 'price')
        }
    },
    components: { iSlider }
}
</script>
<style lang="stylus" scoped>

.header
    width $desktop-width
    margin 60px auto 20px
    +$tablet()
        width $tablet-width
        margin-bottom 10px
    +$tablet()
        width 100%
        padding 0 16px

.slider
    margin-bottom -20px

.slide
    &:first-child
        .card
            margin-left 0
    &:last-child
        .card
            margin-right 0

.card
    width 282px
    height 180px
    display block
    color #fff
    border-radius 16px
    overflow hidden
    padding-top 30px
    padding-left 20px
    background-size cover
    background-position center
    position relative
    box-shadow: 4px 4px 12px rgba(0, 0, 0, 0)
    transition all .2s
    margin 10px 12px 20px
    .name
        font-size 32px
        line-height 41px
    .arrow
        font-size 20px
        height 36px
        width 36px
        left 12px
        bottom 12px
        position absolute
        display flex
        align-items center
        justify-content center
        border-radius 100%
        transition all .25s
        overflow hidden
        .icon
            position relative
            z-index 2
        &::after
            content: ''
            position absolute
            z-index 1
            width 0
            height 100%
            left 0
            top 0
            transition all .2s
            background-color #fff
    &:hover
        box-shadow: 4px 4px 12px rgba(0, 0, 0, 0.3)
        .arrow
            color #000
            &::after
                width 100%
    &:active
        box-shadow: 4px 4px 12px rgba(0, 0, 0, 0.1)
    &.black
        color #fff
        border 0
        .arrow
            background-color #E5E5E5
            color #434343

</style>
