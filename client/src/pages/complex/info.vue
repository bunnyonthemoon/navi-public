<template lang="pug">

.info
    .row.head
        .type {{ complex.property_class }}
        .options
            g-share(:id="complex.key")
            g-favorite(:id="complex.id")
    
    .name {{ complex.name }}
    .address.mobile {{ complex.location }}, 
        .grey  {{ complex.address }}

    .subways-and-stats

        .subways
            .subway(v-for="subway in complex.subways")
                .subway-name
                    .color(:style="{ backgroundColor: subway.color || '#7B9EB0' }")
                    | {{ subway.name }}
                .subway-duration {{ subway.duration }} минут пешком
        
        .row.stats
            .numbers 
                .big {{ parseInt(complex.min_price / 10**6) }} - {{ parseInt(complex.max_price / 10**6) }}
                    small  млн
                .small {{ (complex.min_rate / 10**6).toFixed(1) }} - {{ (complex.max_rate / 10**6).toFixed(1) }} млн ₽/м²
            .numbers
                .big {{ complex.min_area }} - {{ complex.max_area }}
                    small  м²
                .small Площадь
    
    .values-and-btns
        .values
            .values-item
                .label Застройщик
                .value {{ complex.developer.name }}
            .values-item
                .label Готовность
                .value {{ complex.done ? 'Сдан' : complex.deadline }}

        .btns
            a.presentation(v-if="complex.presentation" :href="complex.presentation" target="_blank") Скачать брошуру
            .order(:class="{ only: !complex.presentation }" @click="$store.commit('ui/popup', { name: 'offer', query: 'complex|' + complex.key })") Оставить заявку

</template>
<script>
export default {
    props: {
        complex: Object
    }
}
</script>
<style lang="stylus" scoped>

.info
    width 100%
    margin-left 24px
    display flex
    flex-direction column
    height 450px
    background-color #fff
    padding 15px
    border-radius 16px
    +$tablet()
        margin-left 0
        margin-top 40px
        display block
        height auto
    +$phone()
        width 100%
        margin-top 0
        border-radius 0
        padding 20px 16px


.row
    display flex
    justify-content space-between
    align-items center

.head
    +$phone()
        display none

.subways-and-stats
    +$tablet()
        display flex
        justify-content space-between
        align-items flex-end
        margin-top 10px
    +$phone()
        flex-direction column-reverse
        align-items flex-start

.values-and-btns
    margin-top auto
    +$tablet()
        display flex
        justify-content space-between
        margin-top 30px
    +$phone()
        flex-direction column

.type
    font-size 13px
    padding 3px 10px
    border 1px solid $gray
    border-radius 10px

.options
    display flex
    align-items center
    .g-favorite
        margin-left 16px

.name
    $h2()
    margin-top 20px
    +$tablet()
        font-size 28px
        line-height 34px
    +$phone()
        font-weight 400
        font-size 36px
        line-height 44px
        margin-top 0

.address
    display none
    +$phone()
        display block
        font-size 14px
        line-height 18px
        margin-top 10px
        .grey
            color $gray

.subways
    +$phone()
        margin-top 40px
.subway
    display flex
    font-size 14px
    line-height 18px
    margin-top 10px
    
    +$tablet()
        &:first-child
            margin-top 0
    &-name
        min-width 110px
        display flex
        align-items center
        .color
            width 8px
            height 8px
            border-radius 100%
            margin-right 5px
            flex-shrink 0
    &-duration
        color $gray
        margin-left 20px

.numbers
    margin-top 30px
    +$tablet()
        margin-top 0
        margin-right 50px
        &:last-child
            margin-right 0
    +$phone()
        margin-top 20px
    .big
        font-size 30px
        line-height 38px
        letter-spacing 1%
        small
            font-size 18px
            line-height 22px
            +$phone()
                font-size 16px
                line-height 20px
        +$phone()
            font-size 22px
            line-height 26px
    .small
        color $gray
        font-size 15px
        +$phone()
            font-size 14px

.values
    margin-top auto
    &-item
        margin-top 14px
        display flex
        justify-content space-between
        font-size 18px
        line-height 22px
        +$tablet()
            font-size 14px
            line-height 18px
            justify-content flex-start
            margin-top 8px
        &:first-child
            margin-top 0
        .label
            color $gray
            +$tablet()
                min-width 110px
                padding-right 15px

.btns
    display flex
    margin-top 25px
    justify-content space-between

.presentation
    $btn('border')
    border-width 2px
    +$phone()
        padding-right 5px
        padding-left 5px
        width 47%
.order
    $btn('secondary')
    border-width 2px
    // margin auto
    margin-left auto
    &.only
        margin-right auto
    +$tablet()
        margin-left 20px
    +$phone()
        margin-left auto
        padding-left 5px
        padding-right 5px
        width 47%
    // align-self center

</style>
