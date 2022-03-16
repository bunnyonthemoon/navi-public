<template lang="pug">

.gallery
    v-flickity.main#complex-gallery-main(:options="mainOptions" ref="main")
        .img(v-for="(image, index) in complex.images" :key="index" :style="{ backgroundImage: `url(${image})` }")

    v-flickity.nav(:options="navOptions" ref="nav")
        .img(v-for="(image, index) in complex.images" :key="index" :style="{ backgroundImage: `url(${image})` }" @click="select(index)")

    v-flickity.mobile-slider(:options="mobile_options" ref="mobile")
        .img(v-for="(image, index) in complex.images" :key="index" :style="{ backgroundImage: `url(${image})` }")
    
    .mobile-head
        .class {{ complex.property_class }}
        .options
            g-share(:id="complex.key")
            g-favorite(:id="complex.id")

</template>
<script>
import vFlickity from 'vue-flickity'
export default {
    props: {
        complex: Object
    },
    mounted() {
        this.isMounted = true
    },
    data: (context) => ({
        isMounted: false,
        index: 0,
        mainOptions: {
            prevNextButtons: false,
            pageDots: false,
            wrapAround: true,
            on: {
                select: (index) => context.select(index)
            }
        },
        navOptions: {
            prevNextButtons: false,
            pageDots: false,
            contain: true,
            cellAlign: 'left',
            cellSelector: '.img',
            on: {
                select: (index) => context.select(index)
            }
        },
        mobile_options: {
            prevNextButtons: false,
            pageDots: true,
            wrapAround: true,
        },
    }),
    methods: {
        select(index) {
            if (!this.isMounted || this.index == index) return
            this.index = index
            this.$refs.main.select(index)
            this.$refs.nav.select(index)
        }
    },
    components: { vFlickity }
}
</script>
<style lang="stylus" scoped>

.gallery
    width 792px
    flex-shrink 0
    +$tablet()
        width 728px
    +$phone()
        width 100%
        position relative
    .main
        height 450px
        width 100%
        position relative
        +$tablet()
            height 420px
        +$phone()
            display none
        .img
            width 100%
            height 100%
            background-size cover
            background-position center
            margin 0 20px
            +$tablet()
                margin 0

    .nav
        width 100%
        height 80px
        position relative
        margin-top 10px
        +$phone()
            display none
        .img
            width 120px
            height 100%
            margin-right 5px
            background-size cover
            background-position center
            cursor pointer

.mobile-slider
    display none
    +$phone()
        display block
        height 240px
        width 100%
        .img
            height 100%
            width 100%
            background-size cover
            background-position center
        &:deep()
            .flickity-page-dots
                bottom 10px
                .dot
                    width 4px
                    height 4px
                    background-color #F4F4F4
                    margin 0 2px
                    opacity 1
                    transition all .25s
                    border-radius 2px
                    &.is-selected
                        background-color #5F8FAE
                        width 24px

.mobile-head
    display none
    +$phone()
        display flex
        position absolute
        top 16px
        left 16px
        right 16px
        justify-content space-between
        align-items center
        z-index 2
        .class
            padding 3px 10px
            border-radius 10px
            font-size 13px
            // line-height 1
            background-color #fff
            border 1px solid $gray
        .options
            color #fff
            display flex
            align-items center
            font-size 24px
            .g-favorite
                margin-left 16px

</style>
