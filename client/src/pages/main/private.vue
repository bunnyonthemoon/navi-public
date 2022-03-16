<template lang="pug">

.private
    .header
        .g-h2 Закрытые продажи
        .header-text Только для 
            .link  авторизованных
            |  пользователей
    i-slider
        .slide(v-for="complex in complexes" :key="complex.id")
            .complex
                .img(:style="{ backgroundImage: `url(${complex.image})` }")
                    .done {{ complex.done ? 'Сдан' : complex.deadline }}
                .info
                    .name {{ complex.name }}
                    .description {{ complex.description }}
                    .subway(v-if="complex.subway")
                        .color(:style="{ backgroundColor: complex.subway.color || '#7B9EB0' }")
                        | {{ complex.subway.name }}
                    .subway(v-else) {{ complex.location }}
                    .offer(@click="$store.commit('ui/popup', { name: 'offer', query: 'private|' + complex.id })") Получить предложение

</template>
<script>
import iSlider from 'components/slider'
export default {
    data: () => ({
    }),
    computed: {
        complexes() {
            return this.$store.state.catalog.private
        }
    },
    components: { iSlider }
}
</script>
<style lang="stylus" scoped>

.header
    margin 80px auto 0
    width $desktop-width
    display flex
    justify-content space-between
    align-items flex-end
    &-text
        // display flex
        .link
            display inline
            color $secondary
            cursor pointer
    +$tablet()
        width $tablet-width
        flex-direction column
        justify-content flex-start
        align-items flex-start
        &-text
            margin-top 10px
            color #899095
            .link
                text-decoration underline
                color $black
    +$phone()
        width 100%
        padding 0 16px

.slider
    // display flex
    // align-items flex-start
    margin-top 20px
    flex-shrink 0
    margin-bottom -20px
    
.slide
    &:first-child
        .complex
            margin-left 0
    &:last-child
        .complex
            margin-right 0

.complex
    flex-shrink 0
    background-color #fff
    border-radius 16px
    // border 1px solid $gray2
    width 384px
    margin 10px 24px 20px
    overflow hidden
    position relative
    transition all .2s
    box-shadow: 4px 4px 12px rgba(0, 0, 0, 0)
    &:first-child
        margin-left 0
    +$tablet()
        width 260px
        border-radius 10px
        margin-left 20px
        margin-right 20px
    .img
        height 240px
        background-size cover
        position relative
        +$tablet()
            height 140px
        .done
            position absolute
            background #fff
            top 15px
            left 10px
            border-radius 10px
            font-size 14px
            line-height 18px
            padding 3px 10px
    .info
        padding 10px 15px 15px
        position relative
        display flex
        flex-direction column
        +$tablet()
            padding 10px
        .name
            font-size 20px
            line-height 24px
            letter-spacing: 0.02em
            font-weight 500
            padding-right 40px
            transition all .2s
            +$tablet()
                font-size 16px
                line-height 20px
        .description
            font-size 14px
            line-height 18px
            margin-top 10px
            transition all .2s
            +$tablet()
                display none
        .subway
            transition all .2s
            margin-top 22px
            font-size 14px
            // line-height 18px
            line-height 1
            color $gray
            display flex
            align-items center
            +$tablet()
                margin-top 10px
            .color
                width 8px
                height 8px
                border-radius 100%
                margin-right 5px
                margin-top -2px
    .offer
        $btn('primary')
        white-space nowrap
        position absolute
        bottom 20px
        transform scale(0)
        align-self center
        transition all .2s
        &:hover
            transform scale(0)
        +$tablet()
            bottom 25px
    &:hover
        box-shadow: 4px 4px 12px rgba(0, 0, 0, 0.15)
        +$tablet()
            .name
                opacity 0
        .description, .subway
            opacity 0
        .offer
            transform scale(1)
            &:hover
                transform scale(1.05)
            &:active
                transform scale(0.95)

</style>
