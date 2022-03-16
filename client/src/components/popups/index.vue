<template lang="pug">

//- transition(name="show" :duration="{ enter: 800, leave: 600 }")
.popups(v-if="popup.name")
    .fade(@click="popup = null" @wheel.prevent="() => null" @scroll.prevent="() => null")
    component.popup(v-if="component" :is="component" :query="popup.query" @close="popup = null")

</template>
<script>
import { defineAsyncComponent } from 'vue'
export default {
    computed: {
        popup: {
            get() {
                return {
                    name: this.$route.query.popup,
                    query: this.$route.query.popupQuery,
                }
            },
            set(value) {
                this.$store.commit('ui/popup', { name: value })
            }
        },
        component() {
            let name = this.popup.name
            if (name)
                return defineAsyncComponent(() => import('./' + name))
            return null
        }
    },
}

</script>
<style lang="stylus" scoped>

.popups
    position fixed
    top 0
    left 0
    width 100%
    height 100%
    width 100vw
    height 100vh
    z-index 200
    &.show-enter, &.show-leave-to
        .fade
            opacity 0
        .popup
            top -100%
            top -100vh
            box-shadow 0 0 0 0 rgba(#000, 0)
    &.show-enter-active .popup
        animation showPopup .8s
    &.show-leave-active .popup
        animation hidePopup .6s

.fade
    position absolute
    width 100%
    height 100%
    top 0
    left 0
    z-index 1
    background-color rgba(#000, .5)
    cursor pointer
    opacity .5
    transition opacity .5s

.popup
    z-index 2
    position absolute
    left 50%
    left 50vw
    top 50%
    top 50vh
    transform translate(-50%, -50%)
    background-color #fff
    max-height calc(100vh - 20px)
    overflow-y auto
    overflow-x hidden
    display flex
    flex-direction column

@keyframes hidePopup
    0%
        margin-top 0
        top 50%
        top 50vh
    30%
        margin-top 35px
        top 50%
        top 50vh
    100%
        margin-top 0
        top -100%
        top -100vh

@keyframes showPopup
    0%
        margin-top 0
        top -100%
        top -100vh
    60%
        margin-top 45px
        top 50%
        top 50vh
    100%
        margin-top 0
        top 50%
        top 50vh

.popup:deep()
    .close
        position absolute
        z-index 10
        font-size 24px
        top 10px
        right 10px
        cursor pointer
        border 2px solid $dark
        border-radius 100%
        display flex
        align-items center
        justify-content center
        +$phone()
            font-size 18px
    .header
        display flex
        justify-content space-between
        align-items center
        margin-bottom 20px
        .close
            position relative
            top auto
            right auto
            flex-shrink 0
            margin-left 20px
    .title
        font-weight 700
        font-size 25px
        +$phone()
            font-size 18px

</style>
