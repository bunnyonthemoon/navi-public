<template lang="pug">

.about
    .description(v-html="complex.description")

    .title О проекте
    .list
        .column(v-for="(column, index) in columns" :key="index")
            .about-item(v-for="item in column" :key="item.key")
                .label {{ item.label }}
                .value(v-if="item.type == 'array'") 
                    template(v-for="(value, index) in complex[item.key]") {{ value }}
                        template(v-if="index < complex[item.key].length - 1") , 
                .value(v-else) {{ complex[item.key] }}

</template>
<script>
export default {
    props: {
        complex: Object
    },
    data: () => ({
        columns: [
            [
                {
                    label: 'Отделка',
                    key: 'trim'
                },
                {
                    label: 'Этажность',
                    key: 'floors'
                },
                {
                    label: 'Потолки',
                    key: 'ceilings'
                },
            ],
            [
                {
                    label: 'Тип недвижимости',
                    key: 'property_type',
                    type: 'array'
                },
                {
                    label: 'Территория',
                    key: 'territory'
                },
                {
                    label: 'Всего квартир',
                    key: 'lots_count_total'
                },
            ]
        ],
    })    
}
</script>
<style lang="stylus" scoped>

.about
    margin-top 60px
    +$phone()
        margin-top 40px

.description
    width 800px
    &:deep()
        h2
            font-weight 500
            font-size 28px
            line-height 34px
            margin-bottom 2em
            &:last-child
                padding-bottom 0
            +$tablet()
                $h2()
                margin-bottom 1.5em
        p
            color #434343
            font-size 18px
            line-height 22px
            padding-bottom 1em
            &:last-child
                padding-bottom 0
            +$tablet()
                font-size 16px
                line-height 20px
    +$tablet()
        width $tablet-width
    +$phone()
        width 100%
        padding 0 16px

.title
    $h2()
    margin-top 80px
    +$phone()
        padding 0 16px

.list
    margin-top 30px
    display flex
    +$phone()
        padding 0 16px
        position relative

.column
    margin-right 120px
    display flex
    flex-direction column
    +$phone()
        width 50%
        position relative
        margin-right 0
        padding-right 20px

.about-item
    display flex
    justify-content space-between
    width 250px
    margin-top 13px
    font-size 18px
    line-height 22px
    &:nth-child(4n+1)
        margin-top 0
    .label
        font-weight 500
        padding-right 10px
        +$phone()
            font-size 14px
            line-height 18px
            font-weight 400
            color $gray
            margin-top 2px
    .value
        text-align right
        +$phone()
            text-align left
    +$phone()
        flex-direction column-reverse
        width 100%


</style>
