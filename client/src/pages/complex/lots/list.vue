<template lang="pug">

.list-container
    .desktop-list
        .lot(v-for="plan in plans" :key="plan.id" @click="showLot(plan.id)")
            .column.img
                img.main-img(:src="plan.image")
                .tooltip
                    img(:src="plan.image")
            .column {{ roomsTitle(plan.rooms) }}

            .column
                .gray.desktop Площадь 
                span {{ plan.area }} м²
            .column 
                .type(v-for="(type, index) in plan.property_type" :key="index") {{ type }}
            b.column.desktop от {{ (plan.min_rate / 10**6).toFixed(1) }} до {{ (plan.max_rate / 10**6).toFixed(1) }} млн ₽/м²
            //- b.column.mobile {{ (plan.min_rate / 10**6).toFixed(1) }} - {{ (plan.max_rate / 10**6).toFixed(1) }} млн
                .gray ₽/м²
            b.column.price.desktop от {{ maskPrice(plan.min_price) }} до {{ maskPrice(plan.max_price) }} ₽
            b.column.price.mobile {{ (plan.min_price / 10**6) }} - {{ (plan.max_price / 10**6) }} млн ₽

    .mobile-list
        .count {{ plans.length }} планировок

        .room(v-for="room in complex.rooms_info")
            .room-head(@click="opened_rooms = (opened_rooms == room.rooms ? null : room.rooms)")
                .room-head-main {{ roomsTitle(room.rooms) }}
                    //- template(v-if="room.rooms == 0") Студии
                    //- template(v-else) {{ room.rooms }}-комнатные
                    |  от {{ room.min_area }} м²
                .room-head-sub {{ (room.min_price / 10**6) }} - {{ (room.max_price / 10**6) }} млн руб
                .room-head-arrow(:class="{ active: room.rooms == opened_rooms }")
                    g-icon(name="ui/chevron")
            .room-list(v-if="room.rooms == opened_rooms")
                .room-list-lot(v-for="plan in plans.filter(item => item.rooms == room.rooms)" :key="plan.id" @click="$store.commit('ui/popup', { name: 'lot', query: plan.id })")
                    //- .room-column.img(:style="{ backgroundImage: `url(${plan.image})` }")
                    .room-column.img
                        img(:src="plan.image")
                    .room-column {{ plan.area }} м²
                    .room-column {{ (plan.min_price / 10**6).toFixed(0) }} - {{ (plan.max_price / 10**6).toFixed(0) }} млн ₽


</template>
<script>
export default {
    props: {
        complex: Object,
        plans: Array
    },
    data: () => ({
        rooms: [],
        opened_rooms: null
    }),
    methods: {
        showLot(id) {
            this.$store.commit('ui/popup', { name: 'lot', query: id })
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
        roomsTitle(count) {
            if (count === 0)
                return 'Студия'
            if (count >= 5)
                return count + ' спален'
            return count + ' спальни'
        }
    },
}
</script>
<style lang="stylus" scoped>

.mobile-list
    display none
    +$phone()
        display flex
        flex-direction column
    
    .count
        margin 20px 0 10px
        color $gray
        font-size 14px
        line-height 18px
    .room
        border-top 1px solid $gray2
        &:last-child
            border-top 1px solid $gray2
        &-head
            padding 10px 0
            position relative
            cursor pointer
            &-sub
                font-size 14px
                line-height 18px
                color $gray
                margin-top 5px
            &-arrow
                position absolute
                font-size 24px
                right 8px
                top 50%
                margin-top -12px
                font-size 24px
                transition all .2s
                &.active
                    transform rotate(180deg)
        &-list
            &-lot
                display flex
                justify-content space-between
                align-items center
                cursor pointer
                padding 5px 0
        &-column
            width 100%
            text-align center
            &.img
                img
                    height 45px
            &:first-child
                text-align left
            &:last-child
                text-align right
                width 140%
            // &.img
            //     width 80px
            //     height 40px
            //     background-size contain
            //     background-repeat no-repeat
            //     background-position center left


.desktop-list
    margin-top 45px
    display flex
    flex-direction column
    +$tablet()
        .desktop
            display none
    +$phone()
        display none

    .lot
        cursor pointer
        background-color #fff
        padding 5px 11px 5px 5px
        display flex
        // justify-content space-between
        position relative
        height 76px
        margin-top 5px
        &:first-child
            margin-top 0
        &:hover
            z-index 2
        .column
            width 100%
            display flex
            align-items center
            margin-left auto
            justify-content center
            +$tablet()
                white-space nowrap
                padding-right 15px
                &:last-child
                    padding-right 0
            &:first-child
                margin-left 0
                justify-content flex-start
                width 60%
            &:last-child
                width 70%
                text-align right
                justify-content flex-end
            .gray
                margin .3em
                color $gray
            &.img
                align-self flex-start
                transition all .4s
                position relative
                height 100%
                .main-img
                    height 100%
                    position relative
                    display flex
                &:hover
                    .tooltip
                        padding 15px
                        img
                            width 300px
                .tooltip
                    border-radius 20px
                    box-shadow 0 4px 10px rgba(#000, .2)
                    position absolute
                    background-color #fff
                    left 100%
                    top 50%
                    transform translateY(-50%)
                    margin-left 15px
                    transition all .25s
                    img
                        transition all .25s
                        width 0
            &.desktop
                +$tablet()
                    display none
            &.mobile
                display none
                +$tablet()
                    display flex


    .more
        border-radius 8px
        background-color #fff
        border 2px solid $primary
        padding 8px 20px
        display inline-flex
        align-self center
        margin-top 30px

.type
    &::before
        content ', '
    &:first-child
        &::before
            content none

.price
    white-space nowrap

</style>
