<template lang="pug">

.selection
    .title
        .g-h2 {{ selection.name }}
        router-link.count(:to="{ name: 'selection', params: { id: selection.key } }") {{ selection.complexes.length }} {{ selection.complexes.length >= 5 ? 'объектов' : selection.complexes.length >= 2 ? 'объекта' : 'объект' }}
    .list
        c-complex(v-for="complex in selection.complexes" :key="complex.id" :complex="complex")

</template>
<script>
import cComplex from 'components/complex'
export default {
    props: {
        selection: Object
    },
    components: { cComplex }
}
</script>
<style lang="stylus" scoped>

.selection
    margin 60px auto 0
    width $desktop-width
    +$tablet()
        width $tablet-width
        margin-top 40px
    +$phone()
        width 100%
        padding 0 16px

.title
    margin-bottom 10px

.count
    color $primary
    text-decoration underline
    margin-top 10px
    font-size 20px
    font-weight 500
    line-height 26px
    display block
    +$tablet()
        font-size 16px
        line-height 20px
        font-weight 400

.complex
    margin 10px 0

.list
    display flex
    +$tablet()
        flex-wrap wrap
    .complex
        margin-right 24px
        &:last-child
            margin-right 0
        +$tablet()
            &:nth-child(2n)
                margin-right 0
        +$phone()
            width 100%
            margin-right 0

</style>
