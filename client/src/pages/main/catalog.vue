<template lang="pug">

.catalog
    .info
        .ps {{ text.main_catalog_title }}
        .title {{ text.main_catalog_text }}
        a.g-btn.load(:href="$store.state.content.files.catalog" target="_blank")
            span Получить каталог
            g-icon(name="ui/arrow")
    .adobe
        img(:src="require('images/brands/adobe.svg')")
    .img
        .text Каталог лучших комплексов Москвы
    a.g-btn.load.mobile(:href="$store.state.content.files.catalog" target="_blank")
        span Получить каталог
        g-icon(name="ui/arrow")

</template>
<script>
export default {
    computed: {
        text() {
            return this.$store.state.content.text
        }
    }
}
</script>
<style lang="stylus" scoped>

.catalog
    width $desktop-width
    height 400px
    background-color #fff
    border-radius 24px
    overflow hidden
    display flex
    margin 95px auto 0
    position relative
    +$tablet()
        width $tablet-width
        height 240px
        margin-top 40px
        border-radius 10px
    +$phone()
        width 100%
        padding 0 16px
        background transparent
        height auto
        flex-direction column
    .load.mobile
        display none
        +$phone()
            display flex
            $btn('primary')
            align-self center
            margin-top 20px
            border-radius 100px
            padding 6px 20px
            .icon
                font-size 24px
    .info
        width 50%
        padding 35px 31px
        color #434343
        display flex
        flex-direction column
        +$tablet()
            padding 20px
        +$phone()
            display none
        .ps
            font-weight 500
        .title
            font-size 32px
            line-height 41px
            margin-top 17px
            width 440px
            +$tablet()
                $h4()
                width 300px
        .load
            background-color $primary
            color #fff
            display inline-flex
            border-radius 100px
            // font-weight 500
            font-size 18px
            padding 7px 23px
            margin-top auto
            align-self flex-start
            span
                margin-right 7px
            +$tablet()
                font-size 16px
                padding 10px 20px
                line-height 20px
                span
                    margin-right 0
                .icon
                    font-size 24px
    .adobe
        position absolute
        z-index 3
        width 154px
        height 154px
        left 50%
        top 50%
        background-color #fff
        border-radius 100%
        transform translate(-50%, -50%)
        display flex
        align-items center
        justify-content center
        +$tablet()
            width 80px
            height 80px
            img
                width 40px
                height 40px
        +$phone()
            display none
    .img
        width 50%
        background-image url('~images/catalog-bg.jpg')
        background-size cover
        background-position center
        .text
            width 306px
            text-align left
            color #fff
            background-color rgba(#000, .5)
            font-size 24px
            line-height 31px
            font-weight 500
            position absolute
            top 50%
            transform translateY(-50%)
            display flex
            align-items center
            justify-content center
            padding-left 105px
            padding-right 67px
            padding-top 78px
            padding-bottom 69px
            +$tablet()
                width 200px
                $h4()
                font-weight 400
                padding 46px 11px 46px 59px
        +$phone()
            width 100%
            border-radius 12px
            position relative
            height 200px
            .text
                background-color transparent
                text-shadow: 0px 4px 4px rgba(0, 0, 0, 0.25)
                font-size 24px
                line-height 31px
                padding 0 15px
                transform none
                top 20px
                text-align center
                width 100%

</style>
