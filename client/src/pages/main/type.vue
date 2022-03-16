<template lang="pug">

.budget
    .header
        .g-h2 По типу
    .list
        router-link.type(v-for="selection in selections" :key="selection.id" :style="{ backgroundImage: `url(${selection.image})` }" :to="{ name: 'selection', params: { id: selection.key } }")
            .name {{ selection.name }}
            .description {{ selection.description }}
            .count {{ selection.count }} {{ selection.count >= 5 ? 'проектов' : selection.count >= 2 ? 'проекта' : 'проект' }}
            //- .arrow
            //-     g-icon(name="ui/arrow")
    //- .g-btn.more Показать ещё

</template>
<script>
import iSlider from 'components/slider'
export default {
    data: () => ({
        types: [
            {
                img: require('images/types/1.jpg'),
                name: 'Небоскреб',
                description: 'Sit amet, consectetur adipiscing elit ut aliquam'
            },
            {
                img: require('images/types/2.jpg'),
                name: 'Клубный дом',
                description: 'Sit amet, consectetur adipiscing elit ut aliquam'
            },
            {
                img: require('images/types/3.jpg'),
                name: 'Пентхаус',
                description: 'Sit amet, consectetur adipiscing elit ut aliquam'
            },
            {
                img: require('images/types/4.jpg'),
                name: 'Лофт',
                description: 'Sit amet, consectetur adipiscing elit ut aliquam'
            },
        ]
    }),
    computed: {
        selections() {
            return this.$store.state.catalog.selections.filter(item => item.type == 'type')
        }
    },
    components: { iSlider }
}
</script>
<style lang="stylus" scoped>

.budget
    width $desktop-width
    margin 60px auto 0
    display flex
    flex-direction column
    +$tablet()
        width $tablet-width
    +$phone()
        width 100%
        padding 0 16px

.header
    margin-bottom 30px

.list
    display flex
    flex-wrap wrap
    justify-content space-between

.type
    width 588px
    height 254px
    background-size cover
    background-position right bottom
    border-radius 26px
    overflow hidden
    padding 35px 18px 0
    color #fff
    position relative
    margin-top 22px
    transition all .2s
    box-shadow: 4px 4px 12px rgba(0, 0, 0, 0)
    &:nth-child(1), &:nth-child(2)
        margin-top 0
    &:hover
        box-shadow: 4px 4px 12px rgba(0, 0, 0, 0.3)
    &:active
        box-shadow: 4px 4px 12px rgba(0, 0, 0, 0.1)
    .name
        font-size 36px
        line-height 46px
        font-weight 700
    .description
        margin-top 11px
        width 225px
    .count
        position absolute
        bottom 15px
        font-size 22px
        line-height 26px
    +$tablet()
        width 350px
        height 220px
        .name
            font-size 30px
            line-height 38px
        // .description
        .count
            font-size 20px
            line-height 25px
    +$phone()
        width 100%
        height 180px
        padding 20px 15px 0
        &:nth-child(2)
            margin-top 22px

.more
    width auto
    display inline-block
    align-self center
    margin-top 20px
    border-radius 100px
    color #7A848B
    padding 9px 43px
    font-weight 500

</style>
