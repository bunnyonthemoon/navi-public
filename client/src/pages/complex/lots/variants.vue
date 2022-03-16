<template lang="pug">

.variants
    .list
        .variant(v-for="room in rooms" :key="room")
            .g-h3 {{ roomsTitle(room) }}
            .list
                .lot(v-for="plan in plans.filter(item => item.rooms == room)" :key="plan.id" @click="showLot(plan.id)")
                    img.img(:src="plan.image")
                    .info
                        .info-item
                            .value {{ plan.area }}
                                small  м²
                            .label Площадь
                        .info-item
                            .value от {{ parseInt(plan.min_price / 10**6) }}
                                small  млн ₽
                            .label Стоимость

    v-flickity.slider(:options="options" ref="slider")
        .slide(v-for="plan in plans" :key="plan.id" @click="$store.commit('ui/popup', { name: 'lot', query: plan.id })")
            .img(:style="{ backgroundImage: `url(${ plan.image })` }")
            .info
                .price от {{ (plan.min_price / 10**6).toFixed(0) }} до {{ (plan.max_price / 10**6).toFixed(0) }} млн ₽
                .area {{ plan.area }} м²

</template>
<script>
import vFlickity from 'vue-flickity'
export default {
    props: {
        complex: Object,
        plans: Array
    },
    data: () => ({
        rooms: [],
        options: {
            prevNextButtons: false,
            pageDots: true,
            wrapAround: true,
        },
    }),
    watch: {
        plans: {
            immediate: true,
            handler() {
                this.rooms = []
                this.plans.reduce((rooms, item) => {
                    if (rooms.indexOf(item.rooms) == -1)
                        rooms.push(item.rooms)

                    return rooms
                }, this.rooms)
            }
        }
    },
    methods: {
        showLot(id) {
            this.$store.commit('ui/popup', { name: 'lot', query: id })
        },
        roomsTitle(count) {
            if (count === 0)
                return 'Студия'
            if (count >= 5)
                return count + ' спален'
            return count + ' спальни'
        },
        maskPrice(value) {
            value = String(value)
            let str = ''
            for (let i = 1; i <= value.length; i++) {
                str += value[value.length - i]
                if (i % 3 == 0)
                    str += ' '
            }
            return str.split('').reverse().join('')
        },
    },
    components: { vFlickity }
}
</script>
<style lang="stylus" scoped>

.variants
    margin-top 40px

.variant
    margin-top 40px
    &:first-child
        margin-top 0

.list
    display flex
    flex-wrap wrap
    flex-direction column
    +$phone()
        display none

.lot
    width 281px
    cursor pointer
    margin-right 25px
    margin-top 20px
    padding 10px
    background-color #fff
    border 1px solid $gray2
    border-radius 12px
    position relative
    +$tablet()
        width 352px
        margin-right 24px
    &:nth-child(4n)
        margin-right 0
    .img
        width 100%
        margin-bottom 35px
    .info
        display flex
        justify-content space-between
        margin-top auto
        .value
            font-size 20px
            line-height 25px
            small
                font-size 16px
        .label
            $text-small()
            color $gray

.slider
    display none
    +$phone()
        display block
        width 100vw
        margin-left -16px
    &:deep()
        .flickity-page-dots
            bottom -8px
            .dot
                width 4px
                height 4px
                background-color $gray
                margin 0 2px
                opacity 1
                transition all .25s
                border-radius 2px
                &.is-selected
                    background-color $primary
                    width 24px

.slide
    width 100%
    .img
        background-color #fff
        height 300px
        width 100%
        background-size auto 90%
        background-position center
        background-repeat no-repeat
    .info
        display flex
        justify-content space-between
        padding 10px 16px


</style>
