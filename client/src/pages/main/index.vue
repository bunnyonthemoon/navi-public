<template lang="pug">

.main-page
    .welcome
        .welcome-title {{ text.main_title }}
        .welcome-text {{ text.main_subtitle }}
    i-filter
    //- l-ready
    l-selection(v-for="selection in selections" :key="selection.id" :selection="selection" :style="{ order: selection.order }")
    l-private(:style="{ order: order.private }")
    l-budget(:style="{ order: order.budget }")
    l-type(:style="{ order: order.type }")
    l-catalog(:style="{ order: order.catalog }")

</template>
<script>
import iFilter from 'components/filter'
import lReady from './ready'
import lPrivate from './private'
import lDistrict from './district'
import lBudget from './budget'
import lType from './type'
import lCatalog from './catalog'
import lSelection from './selection'

import { useMeta, useActiveMeta } from 'vue-meta'
export default {
    computed: {
        selections() {
            return this.$store.state.catalog.selections.filter(item => item.type == 'list')
        },
        order() {
            return this.$store.state.content.order
        },
        text() {
            return this.$store.state.content.text
        },
    },
    components: { iFilter, lReady, lPrivate, lDistrict, lBudget, lType, lCatalog, lSelection }
}
</script>
<style lang="stylus" scoped>

.main-page
    margin-bottom 100px
    display flex
    flex-direction column
    +$tablet()
        margin-bottom 60px

.welcome
    margin auto
    width 100%
    display flex
    flex-direction column
    align-items center
    // background-image url('~images/welcome.jpg')
    background-size cover
    background-position center
    background-repeat no-repeat
    padding 33px calc(50% - 370px)
    text-align center
    // color #fff
    order 0
    &-title
        font-size 48px
        line-height 50px
    &-text
        margin-top 15px
        font-size 20px
        color $gray
    +$tablet()
        padding 20px 30px
        &-title
            font-size 36px
            line-height 46px
            width 520px
        &-text
            margin-top 10px
            width 690px
            font-size 17px
    +$phone()
        &-title
            width 100%
            font-size 20px
            line-height 25px
        &-text
            width 100%
            display none

.filter
    // margin-top -15px
    order 0
    +$tablet()
        margin-top 0

</style>
