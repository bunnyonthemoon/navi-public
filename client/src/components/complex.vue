<template lang="pug">

router-link.complex(:to="{ name: 'complex', params: { id: complex.key } }" :class="{ horizontal, bedrooms }")
    .img(:style="{ backgroundImage: `url(${complex.image})` }")
        template(v-if="!horizontal")
            .type {{ complex.property_class }}
            .count {{ complex.lots_count }} {{ complex.lots_count >= 5 ? 'лотов' : 'лота' }}
            .status {{ complex.done ? 'Сдан' : complex.deadline }}
    .info
        template(v-if="horizontal && !bedrooms")
            .name {{ complex.name }}
            .address 
                .color(:style="{ backgroundColor: complex.subway.color || '#7B9EB0' }")
                | {{ complex.subway.name }}
            .done {{ complex.done ? 'Сдан' : complex.deadline }}
        template(v-if="horizontal && bedrooms")
            .name {{ complex.name }}
                .done {{ complex.done ? 'Сдан' : complex.deadline }}
            .address 
                .color(:style="{ backgroundColor: complex.subway.color || '#7B9EB0' }")
                | {{ complex.subway.name }}
        template(v-if="!horizontal")
            .name {{ complex.name }}
            //- .address {{ complex.address }}
            .address 
                .color(:style="{ backgroundColor: complex.subway.color || '#7B9EB0' }")
                | {{ complex.subway.name }}
        
        .about
            template(v-if="horizontal && bedrooms")
                .info-item(v-for="room in complex.rooms_info")
                    .g-text.small 
                        template(v-if="room.rooms == 0") Cтудия
                        template(v-else-if="room.rooms == 1") {{ room.rooms }} спальня
                        template(v-else) {{ room.rooms }} спальни
                        |  от {{ room.min_area }}
                        small  м²
                    .g-h4 от {{ parseInt(room.min_price / 10**6) }}
                        small  млн. ₽
            template(v-if="!horizontal && bedrooms")
                .info-item(v-for="room in complex.rooms_info")
                    .g-text.small.rooms
                        template(v-if="room.rooms == 0") Cтудия
                        template(v-else-if="room.rooms == 1") {{ room.rooms }} спальня
                        template(v-else-if="room.rooms < 5") {{ room.rooms }} спальни
                        template(v-else) {{ room.rooms }} спален
                    .g-text.area от {{ room.min_area }} 
                        small  м²
                    .g-h4.price
                        template(v-if="room.min_price != room.max_price") от {{ parseInt(room.min_price / 10**6) }}
                        small  млн. ₽

            template(v-if="horizontal && !bedrooms")
                .info-item
                    span.g-text.small.gray Площадь
                    span от {{ complex.min_area }}
                        small  м²
                .info-item
                    span.g-text.small.gray Стоимость
                    span от {{ parseInt(complex.min_price / 10**6) }}
                        small  млн

            template(v-if="!bedrooms && !horizontal")
                .g-h4.info-item.big
                    span от {{ complex.min_area }} до {{ complex.max_area }} 
                        small  м²
                    span от {{ parseInt(complex.min_price / 10**6) }}
                        small  млн. ₽
                .info-item.g-text.small.gray
                    //- span {{ complex.lots_count }} лотов
                    span Площадь
                    span от {{ parseInt(complex.min_rate / 1000) }} тыс/м²

</template>
<script>
export default {
    props: {
        complex: Object,
        horizontal: Boolean,
        bedrooms: Boolean
    },
}
</script>
<style lang="stylus" scoped>

.complex
    width 384px
    border-radius 10px
    // border 1px solid $gray2
    overflow hidden
    transition all .2s
    cursor pointer
    display block
    background-color #fff
    &:hover
        // border-color $primary
        box-shadow: 2px 4px 8px rgba(0, 0, 0, 0.15)
    &:active
        box-shadow: 1px 1px 1px rgba(0, 0, 0, 0.06)
    &.horizontal
        display flex
        height 180px
        .img
            height 100%
            width 160px
            flex-shrink 0
        .name
            font-size 18px
            line-height 24px
        .address
            $text-small()
            color $gray
        .done
            $text-small()
            color $gray
        .info
            padding 15px 15px 10px
            display flex
            flex-direction column
            width 100%
        .about
            margin-top auto
            width 100%
        &.bedrooms
            width 588px
            height 200px
            .img
                width 210px
            .name
                display flex
                justify-content space-between
                .done
                    margin-top 0
    &:not(.horizontal)
        &.bedrooms
            .rooms
                min-width 80px
            .price
                min-width 100px
                text-align right
    
    +$tablet()
        width 352px
    +$phone()
        width 100%

.img
    height 220px
    width 100%
    background-size cover
    background-position center
    position relative
    +$tablet()
        height 160px
    .count, .status
        color #fff
        position absolute
        bottom 10px
        font-size 16px
        line-height 22px
        font-weight 500
    .count
        left 10px
    .status
        right 10px
    .type
        background-color #fff
        padding 2px 12px
        border-radius 100px
        font-size 14px
        line-height 18px
        position absolute
        top 15px
        left 10px

.info
    padding 15px 10px 10px
    &-item
        display flex
        justify-content space-between
        align-items center
        margin-top 8px
        &:first-child
            margin-bottom 0
        &.gray
            color $gray
        &.small
            margin-top 2px
.about
    margin-top 20px

.gray
    color $gray

.name
    $h3()
.address
    $text-small()
    color $gray
    margin-top 2px
    .color
        width 8px
        height 8px
        margin-right 5px
        display inline-block
        border-radius 100%
.done
    color $gray
    margin-top 7px
    $text-small()

</style>
