<template lang="pug">

v-flickity.slider(ref="flickity" :options="sliderOptions")
    .prev(@click="$refs.flickity.previous()")
    slot
    .next(@click="$refs.flickity.next()")

</template>
<script>
import vFlickity from 'vue-flickity'
export default {
    props: {
        count: Number,
        initialIndex: Number
    },
    mounted() {
        this.$refs.flickity.resize()
    },
    data: (context) => ({
        index: 1,
        sliderOptions: {
            cellAlign: 'left',
            prevNextButtons: false,
            pageDots: false,
            cellSelector: '.slide',
            contain: true,
        }
    }),
    methods: {
        select(index) {
            this.index = index
            if (index < 1)
                this.$refs.flickity.select(1)
            else if (index > this.count - 2)
                this.$refs.flickity.select(this.count - 2)
        }
    },
    components: { vFlickity }
}
</script>
<style lang="stylus" scoped>

.slider
    position relative

.next, .prev
    position absolute
    height 100%
    width 'calc(50% - %s / 2)' % $desktop-width
    z-index 2
    cursor pointer
    +$tablet()
        background none!important
        width 'calc(50% - %s / 2)' % $tablet-width
    +$phone()
        width 'calc(50% - %s / 2)' % $phone-width
.next
    right 0
.prev
    left 0
@css{
    .prev {
        --bg-empty: rgba(244, 245, 245, 0);
        --bg-half: rgba(244, 245, 245, 0.5);
        background: linear-gradient(to left, var(--bg-empty) 0%, var(--bg-half) 20%);
    }
    .next {
        --bg-empty: rgba(244, 245, 245, 0);
        --bg-half: rgba(244, 245, 245, 0.5);
        background: linear-gradient(to right, var(--bg-empty) 0%, var(--bg-half) 20%);
    }
}

.slider:deep() 
    .slide
        &:first-child
            padding-left 'calc(50% - %s /2)' % $desktop-width!important
        &:last-child
            padding-right 'calc(50% - %s /2)' % $desktop-width!important
        &.placeholder
            width 'calc(50% - %s /2)' % $desktop-width
    +$tablet()
        .slide
            &:first-child
                padding-left 'calc(50% - %s /2)' % $tablet-width!important
            &:last-child
                padding-right 'calc(50% - %s /2)' % $tablet-width!important
            &.placeholder
                width 'calc(50% - %s /2)' % $tablet-width
    +$phone()
        .slide
            &:first-child
                padding-left 'calc(50% - %s /2)' % $phone-width!important
                padding-left 16px!important
            &:last-child
                padding-right 'calc(50% - %s /2)' % $phone-width!important
                padding-right 16px!important
            &.placeholder
                width 'calc(50% - %s /2)' % $phone-width

</style>
