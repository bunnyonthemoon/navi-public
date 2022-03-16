<template lang="pug">

.selection(v-if="selection")
    h1.g-h1.title {{ selection.name }}
    .list
        i-complex(v-for="complex in selection.complexes" :key="complex.id" :complex="complex")

</template>
<script>
import iComplex from 'components/complex'
import axios from 'axios'
export default {
    props: {
        id: String
    },
    async beforeCreate() {
        const { data } = await axios.get('/api/catalog/selection/' + this.id + '/')
        console.log(data.selection)
        this.selection = data.selection
    },
    data: () => ({
        selection: null
    }),
    components: { iComplex }
}
</script>
<style lang="stylus" scoped>

.selection
    width $desktop-width
    margin 30px auto 100px

.title
    margin-bottom 40px

.list
    display flex
    flex-wrap wrap
    margin-top -40px
    .complex
        margin-top 40px
        margin-right 24px
        &:nth-child(3n+3)
            margin-right 0

</style>
