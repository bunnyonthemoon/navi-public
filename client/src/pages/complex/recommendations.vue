<template lang="pug">

.recommendations(v-if="complex.recommendations.length > 0")
    .g-h2 Вам может понравиться
    .list.desktop
        c-complex(v-for="recommendation in complex.recommendations"  :complex="recommendation" :horizontal="true" :bedrooms="true")
    .list.mobile
        c-complex(v-for="recommendation in complex.recommendations"  :complex="recommendation" :horizontal="true")
        //- c-complex(:complex="complexes[1]" :horizontal="true" :bedrooms="true")

</template>
<script>
import cComplex from 'components/complex.vue'
export default {
    props: {
        complex: Object
    },
    computed: {
    },
    components: { cComplex }
}
</script>
<style lang="stylus" scoped>

.recommendations
    margin-top 60px
    +$phone()
        padding 0 16px

.list
    margin-top 30px
    display flex
    justify-content space-between
    flex-wrap wrap
    &.mobile
        display none
    +$tablet()
        &.desktop
            display none
        &.mobile
            display flex

.complex.horizontal
    +$tablet()
        width 352px
        height 180px
        &:deep()
            .img
                width 160px
    +$phone()
        width 100%
        height 140px
        margin-bottom 20px
        border 1px solid $gray2
        &:last-child
            margin-bottom 0
        &:deep()
            .img
                width 110px!important
            .info
                padding 10px
//     width 580px
//     height 200px
    // &:deep()
    //     .img
    //         width 260px

</style>
