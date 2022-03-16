<template lang="pug">

.layout-main
    c-header
    router-view.page(v-slot="{ Component, route }")
        transition(name="fade" mode="out-in" @before-enter="loader = true" @before-leave="loader = false")
            component(:is="Component")
    c-footer
    c-popup

</template>
<script>
import cHeader from 'components/header'
import cFooter from 'components/footer'
import cPopup from 'components/popups'
export default {
    data: () => ({
        loader: false
    }),
	computed: {
		disableScroll() {
			return this.$store.state.ui.disableScroll
		},
		popup() {
			return this.$store.getters['ui/popup'].name
		},
        editor() {
            return this.$store.state.content.editor
        },
	},
	components: { cHeader, cFooter, cPopup }
}
</script>
<style lang="stylus" scoped>

.layout-main
    min-height 100vh
    display flex
    flex-direction column
    padding-top 60px
    +$phone()
        padding-top 55px


.page
    &.fade-enter-active, &.fade-leave-active
        transition: opacity .25s ease
    &.fade-enter-from, &.fade-leave-to
        opacity 0

</style>
