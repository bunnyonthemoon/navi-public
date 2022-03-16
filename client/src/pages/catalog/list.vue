<template lang="pug">

.sort
    .label Сортировать:
    
    .sort-item(v-for="(item, index) in sort" :key="index" @click="setSort(item.value)" :class="{ active: item.value.key == filter.sort.key, down: filter.sort.dir == 1, up: filter.sort.dir == -1 }") {{ item.text }}
        g-icon(name="ui/chevron")
.list
    i-complex(v-for="complex in complexes" :complex="complex" :bedrooms="true")
    .empty(v-if="complexes.length == 0") Результаты не найдены

</template>
<script>
import iComplex from 'components/complex'
export default {
    props: {
        complexes: Array
    },
    data: () => ({
        sort: [
            {
                text: 'Сначала новые',
                value: {
                    key: 'created',
                    dir: 1
                }
            },
            {
                text: 'Цене',
                value: {
                    key: 'price',
                    dir: 1
                }
            },
            {
                text: 'Цене за метр',
                value: {
                    key: 'rate',
                    dir: 1
                }
            }
        ]
    }),
    methods: {
        setSort(value) {
            if (this.filter.sort.key == value.key)
                this.filter.sort.dir = this.filter.sort.dir * -1
            else
                this.filter.sort = value
            this.$store.dispatch('catalog/filter')
        },
    },
    computed: {
        filter() {
            return this.$store.state.catalog.filter
        }
    },
    components: { iComplex }
}
</script>
<style lang="stylus" scoped>

.sort
    width $desktop-width
    margin 40px auto 0
    display flex
    +$tablet()
        width $tablet-width
        margin-top 25px
    +$phone()
        width 100%
        padding 0 16px
        justify-content space-between
    .label
        margin-right 20px
        font-weight 500
        +$phone()
            display none
    &-item
        margin-right 15px
        cursor pointer
        display flex
        align-items center
        transition all .15s
        +$phone()
            margin-right 0
            font-size 14px
            &:last-child
                margin-right 0
        .icon
            margin-left 3px
            opacity 0
            transition all .15s
        &.active
            color $primary
            .icon
                opacity 1
            &.up
                .icon
                    transform rotate(180deg)

.list
    width $desktop-width
    margin -10px auto 80px
    display flex
    flex-wrap wrap
    +$tablet()
        width $tablet-width
        // margin-top -20px
        margin-top -5px
        margin-bottom 50px
    +$phone()
        width 100%
        padding 0 16px
    .empty
        font-size 28px
        font-weight 500
        text-align center
        margin-top 60px
        align-self center
        width 100%

.complex
    margin-top 40px
    margin-right 24px
    &:nth-child(3n+3)
        margin-right 0
    +$tablet()
        margin-top 25px
        &:nth-child(3n+3)
            margin-right 24px
        &:nth-child(2n)
            margin-right 0
    +$phone()
        margin-right 0
        &:nth-child(3n+3)
            margin-right 0

</style>
