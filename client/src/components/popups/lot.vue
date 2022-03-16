<template lang="pug">

.lot(v-if="lot")
    .close(@click="$emit('close')")
        g-icon(name="ui/close")
    .desktop
        .head
            .name Квартира с {{ lot.rooms }} спальнями
            //- .options
            //-     g-share
        .main
            img.img(:src="lot.image")
            .about
                .about-item
                    .value {{ lot.area }} м²
                    .label Площадь
                .about-item
                    .value {{ maskPrice(lot.min_price) }} ₽
                    .label Стоимость
                .about-item
                    .value {{ maskPrice(lot.min_rate) }} ₽
                    .label Цена за метр
                .g-btn.phone +7 495 701-50-70
                .call Перезвонить
        .info
            .info-item(v-for="(item, index) in info" :key="index")
                .label {{ item.label }}
                .value {{ lot[item.key] }} {{ item.after }}
            .info-item
                .label Тип недвижимости
                .value
                    template(v-for="(type, index) in lot.property_type" :key="index") {{ type }}
                        template(v-if="index < lot.property_type.length - 1") , 
    
    .mobile
        .mobile-head
            .name(v-if="lot.rooms == 0") Студия
            .name(v-else) {{ lot.rooms }} комн. квартира
            .complex {{ lot.complex.name }}
        .mobile-img
            img(:src="lot.image")
        .mobile-stats
            .mobile-stats-item
                .mobile-stats-item-main от {{ (lot.min_price / 10**6) }} до {{ (lot.max_price / 10**6) }} млн ₽
                .mobile-stats-item-sub от {{ (lot.min_rate / 10**6).toFixed(2) }} до {{ (lot.max_rate / 10**6).toFixed(2) }} млн ₽/м²
            .mobile-stats-item
                .mobile-stats-item-main {{ lot.area }} м²
                .mobile-stats-item-sub Площадь

        .mobile-info
            .mobile-info-item
                .label Площадь
                .value {{ lot.area }}
            .mobile-info-item
                .label Кол-во спален
                .value {{ lot.rooms }}
            .mobile-info-item
                .label Тип недвижимости
                .value
                    template(v-for="(type, index) in lot.property_type" :key="index") {{ type }}
                        template(v-if="index < lot.property_type - 1") , 

</template>
<script>
import axios from 'axios'
export default {
    props: {
        query: String
    },
    async beforeCreate() {
        const { data } = await axios.get('/api/catalog/lot/' + this.query + '/')
        console.log(data)
        this.lot = data.lot
    },
    data: () => ({
        lot: null,
        info: [
            {
                label: 'Спален',
                key: 'rooms',
            },
            {
                label: 'Площадь',
                key: 'area',
                after: 'м²'
            },
        ]
    }),
    methods: {
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
    components: {}
}
</script>
<style lang="stylus" scoped>

.desktop
    display block
    +$phone()
        display none

.mobile
    display none
    +$phone()
        display flex
    flex-direction column
    &-head
        background-color #fff
        padding 20px 16px 10px
        .name
            font-size 20px
            line-height 24px
            font-weight 500
        .complex
            font-size 14px
            line-height 18px
            margin-top 5px
    &-img
        background-color #fff
        width 100%
        display flex
        img
            width 90%
            align-self center
            margin auto
    &-stats
        display flex
        justify-content space-between
        padding 20px 16px 10px
        &-item
            &:last-child
                text-align right
            &-main
                font-size 18px
                line-height 22px
            &-sub
                font-size 14px
                line-height 18px
                color $gray
                margin-top 5px
    &-info
        margin-top 40px
        padding 0 16px
        &-item
            padding 10px 0
            border-bottom 1px solid $gray2
            display flex
            justify-content space-between
            align-items flex-end
            font-size 14px
            line-height 18px
            .label
                color $gray
            .value
                text-align right

.lot
    width 1200px
    padding 80px 100px 85px
    +$phone()
        width 100%
        padding 0
        height calc(100% - 54px)
        transform none
        left 0
        bottom 0
        top auto
        background-color $bg
        .close
            top 20px
            right 16px
            font-size 24px

.head
    display flex
    justify-content space-between
    .name
        font-weight 500
        font-size 24px
        line-height 31px
        +$phone()
            font-size 20px
            line-height 24px
            font-weight 500
            padding-right 30px
    .options
        display flex
        .share
            margin-right 24px

.main
    display flex
    margin-top 45px
    +$phone()
        flex-direction column
    .img
        width 550px
        +$phone()
            width 90%
            margin auto
            background-color #fff
    .about
        margin-left 137px
        &-item
            margin-top 27px
            &:first-child
                margin-top 0
            .value
                font-size 24px
                line-height 31px
            .label
                margin-top 2px
                color #7A848B
                font-size 15px
                line-height 19px
        .phone
            border 1px solid #000
            width 242px
            margin-top 80px
            font-weight 500
            font-size 15px
            padding 12px 0 9px
        .call
            margin-top 20px
            text-decoration underline
            text-align center
            cursor pointer

.info
    margin-top 70px
    display flex
    flex-direction column
    flex-wrap wrap
    max-height 125px
    align-self flex-start
    &-item
        display flex
        justify-content space-between
        width 330px
        margin-top 15px
        margin-right 40px
        &:nth-child(4n+1)
            margin-top 0
        .label
            color #7A848B
        .value
            font-weight 500

</style>
