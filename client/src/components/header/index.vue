<template lang="pug">

.header.light
    router-link.logo(:to="{ name: 'main' }")
        img(:src="require('images/logo.svg')")
        .logo-text Navi
    .options
        //- .option.lightmode
        //-     g-icon(name="ui/sun")
        router-link.option.favorite(:to="{ name: 'favorites' }" :class="{ active: favorites > 0 }")
            g-icon(name="ui/favorite")
            .count(v-if="favorites > 0") {{ favorites }}
        .option.menu-btn(@click="menu = !menu")
            g-icon(v-if="menu" name="ui/close")
            g-icon(v-else name="ui/menu")
        //- .option.profile
        //-     g-icon(name="ui/profile")
    l-menu(:active="menu" @close="menu = false")


</template>
<script>
import lMenu from './menu'
export default {
    data: () => ({
        links: [
        ],
        menu: false
    }),
    computed: {
        favorites() {
            return this.$store.state.catalog.favorites.length
        }
    },
    components: { lMenu }
}
</script>
<style lang="stylus" scoped>

.header
    width 100%
    height 60px
    display flex
    align-items center
    justify-content space-between
    padding 0 "calc(50% - %s / 2)" % $desktop-width
    border-bottom 1px solid #E5E5E5
    position fixed
    z-index 20
    background-color $bg
    top 0
    left 0
    
    +$tablet()
        padding 0 "calc(50% - %s / 2)" % $tablet-width
    
    +$phone()
        padding 10px 15px
        height 55px

.logo
    display flex
    align-items center
    img
        width 40px
        height 40px
        +$phone()
            width 34px
            height 34px
    &-text
        font-size 20px
        line-height 24px
        letter-spacing: 0.04em
        font-weight 500
        margin-left 10px
        +$phone()
            font-size 16px

.options
    display flex
    align-items center
    font-size 24px
    .option
        margin-right 16px
        cursor pointer
        display flex
        &:last-child
            margin-right 0
        &.favorite
            +$phone()
                display none

.favorite
    position relative
    .count
        font-size 12px
        font-weight 500
        background $primary
        border-radius 100%
        width 17px
        height 17px
        line-height 17px
        color #fff
        text-align center
        position absolute
        top -6px
        right -8px
    +$phone()
        display none
        
.option.menu-btn
    font-size 40px
    display none
    +$phone()
        display flex

</style>
