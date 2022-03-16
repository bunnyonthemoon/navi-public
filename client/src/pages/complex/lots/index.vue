<template lang="pug">

.lots
    .g-h2 Квартиры и аппартаменты
    .list-types
        .type(@click="listType = 'list'" :class="{ active: listType == 'list' }") Списком
        .type(@click="listType = 'variants'" :class="{ active: listType == 'variants' }") Варианты планировок

    l-filter(:complex="complex" @filter="plans = $event")

    l-list(v-if="listType == 'list'" :complex="complex" :plans="plans")
    l-variants(v-if="listType == 'variants'" :complex="complex" :plans="plans")

</template>
<script>
import lList from './list'
import lVariants from './variants'
import lFilter from './filter'
export default {
    props: {
        complex: Object
    },
    data: (context) => ({
        listType: 'list',
        plans: context.complex.plans
    }),
    components: { lList, lVariants, lFilter }
}
</script>
<style lang="stylus" scoped>

.lots
    margin-top 60px
    +$phone()
        padding 0 16px

.list-types
    margin-top 22px
    display flex
    .type
        $btn('border')
        margin-right 10px
        border-color $secondary
        +$phone()
            padding-left 13px
            padding-right 13px
        &.active
            $btn('primary')
            +$phone()
                padding-left 13px
                padding-right 13px
        //     color $black
        //     border-color $primary

</style>
