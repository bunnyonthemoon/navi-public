<template lang="pug">

.filter
    .filter-item.rooms
        .label Площадь (м2):
        .rooms-list
            .room(v-for="room in rooms.values" :key="room.value" @click="setBedrooms(room.value)" :class="{ active: rooms.active.indexOf(room.value) != -1 }") {{ room.text }}
    .filter-item.area
        .label Площадь (м2):
        .slider
            .value от 
                span {{ area.values[0] }}
            .value до 
                span {{ area.values[1] }}
            v-slider.slider-line(v-model="area.values" :min="area.min" :max="area.max" :tooltips="false" @change="setPrice($event)" :lazy="false")
    .filter-item.price
        .label Цена (млн Р):
        .slider
            .value от 
                span {{ parseInt(price.values[0] / 10**6) }}
            .value до 
                span {{ parseInt(price.values[1] / 10**6) }}
            v-slider.slider-line(v-model="price.values" :min="price.min" :max="price.max" :tooltips="false" @change="setPrice($event)" :lazy="false")

</template>
<script>
import vSlider from '@vueform/slider'
export default {
    props: {
        complex: Object
    },
    data: (context) => ({
        price: {
            values: [context.complex.min_price, context.complex.max_price],
            min: context.complex.min_price,
            max: context.complex.max_price
        },
        area: {
            values: [context.complex.min_area, context.complex.max_area],
            min: context.complex.min_area,
            max: context.complex.max_area
        },
        rooms: {
            values: [
                {
                    text: 'Студия',
                    value: '0'
                },
                {
                    text: '1',
                    value: '1'
                },
                {
                    text: '2',
                    value: '2'
                },
                {
                    text: '3',
                    value: '3'
                },
                {
                    text: '4+',
                    value: '4+'
                },
            ],
            active: []
        }
    }),
    methods: {
        setBedrooms(value) {
            let index = this.rooms.active.indexOf(value)
            
            if (index == -1)
                this.rooms.active.push(value)
            else this.rooms.active.splice(index, 1)

            this.filter()
        },
        setPrice() {
            this.filter()
        },
        setArea() {
            this.filter()
        },
        filter() {
            let plans = this.complex.plans.filter(plan => {
                if (this.rooms.active.length > 0 && this.rooms.active.indexOf(String(plan.rooms)) == -1)
                    return false
                
                if (plan.max_price < this.price.values[0] || plan.min_price > this.price.values[1])
                    return false
                
                if (plan.area < this.area.values[0] || plan.area > this.area.values[1])
                    return false
                
                return true
            })

            this.$emit('filter', plans)
        }
    },
    components: { vSlider }
}
</script>
<style src="@vueform/slider/themes/default.css"></style>
<style lang="stylus" scoped>

.filter
    display flex
    margin-top 30px
    // &-item
    +$phone()
        flex-direction column

.label
    font-size 14px
    line-height 18px
    color $gray
    margin-bottom 10px

.rooms
    &-list
        display flex
    .room
        $btn('border')
        margin-right 10px
        border-color $gray2
        width 40px
        height 40px
        padding 0
        &.active
            $btn('secondary')
            padding 0
            width 40px
            height 40px
        &:first-child
            width auto
            padding 0 14px
        &:last-child
            margin-right 0

.area, .price
    width 300px
    +$phone()
        width 100%
        margin-top 30px

.area
    margin-left 48px
    margin-right 40px
    +$phone()
        margin-left 0
        margin-right 0

.slider
    width 100%
    height 40px
    padding 0 20px
    position relative
    display flex
    align-items center
    justify-content space-between
    background-color #F4F4F4
    .value
        color $gray
        span
            color $black
            font-weight 500
    &-line
        position absolute
        width 100%
        bottom 0
        left 0
        cursor pointer
        --slider-height 4px
        // --slider-bg $primary
        --slider-connect-bg $primary
        --slider-handle-bg $primary
        --slider-handle-shadow none
        --slider-handle-shadow-active none
    .vue-slider
        position absolute
        width 100%
        bottom 0
        left 0
        right 0
        transform translateY(50%)
        &:deep()
            .vue-slider-dot-handle
                background-color $primary
                box-shadow none

</style>
