<template lang="pug">

.complex(v-if="complex" :key="complex.id")
    .head
        .g-h1.name {{ complex.name }}
        .address {{ complex.location }}, 
            span.grey  {{ complex.address }}
    .main
        l-gallery(:complex="complex")
        l-info(:complex="complex")
    l-about(:complex="complex")
    l-lots(:complex="complex")
    l-location(:complex="complex" :around="around")
    l-recommendations(:complex="complex")

</template>
<script>
import lHead from './head'
import lGallery from './gallery'
import lInfo from './info'
import lAbout from './about'
import lLots from './lots'
import lLocation from './location'
import lRecommendations from './recommendations'
import axios from 'axios'
export default {
    async beforeRouteEnter(to, from, next) {
        const { data } = await axios.get('/api/catalog/complex/' + to.params.id + '/')
        to.meta.title = data.complex.name
        next(vm => {
            vm.complex = data.complex
            vm.around = data.around
        })
    },
    async beforeRouteUpdate(to, from) {
        if (to.params.id == from.params.id)
            return

        const { data } = await axios.get('/api/catalog/complex/' + to.params.id + '/')
        to.meta.title = data.complex.name
        this.complex = data.complex
        this.around = data.around
    },
    props: {
        id: String
    },
    data: () => ({
        complex: null,
        around: []
    }),
    components: { lHead, lGallery, lInfo, lAbout, lLocation, lRecommendations, lLots }
}
</script>
<style lang="stylus" scoped>

.complex
    width $desktop-width
    margin 30px auto 105px
    +$tablet()
        width $tablet-width
    +$phone()
        width 100%
        margin-top 0
        margin-bottom 40px

.head
    +$phone()
        display none
    .address
        .grey
            color $gray

.main
    display flex
    justify-content space-between
    margin-top 20px
    +$tablet()
        flex-wrap wrap
    +$phone()
        margin-top 0

</style>
